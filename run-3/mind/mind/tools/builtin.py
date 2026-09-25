"""Built-in tools and the default registry."""
from __future__ import annotations

import ast
import datetime as _dt
import operator
from typing import Any

from ..audit import AuditLog
from ..permissions import PermissionGate, Tier
from .base import Tool, ToolContext, ToolRegistry
from .notes import note_tools
from .sandbox import run_python
from .web import web_tools

# -- calculator -------------------------------------------------------------
_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod, ast.Pow: operator.pow,
        ast.USub: operator.neg, ast.UAdd: operator.pos}


def safe_eval(expr: str) -> float | int:
    if len(expr) > 200:
        raise ValueError("expression too long")

    def ev(node: ast.AST):
        if isinstance(node, ast.Expression):
            return ev(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
            left, right = ev(node.left), ev(node.right)
            if isinstance(node.op, ast.Pow) and (abs(right) > 100 or abs(left) > 1e6):
                raise ValueError("exponent too large")
            return _OPS[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
            return _OPS[type(node.op)](ev(node.operand))
        raise ValueError(f"unsupported expression element: {type(node).__name__}")

    return ev(ast.parse(expr.replace("^", "**"), mode="eval"))


def calculator(args: dict[str, Any], ctx: ToolContext) -> str:
    val = safe_eval(args["expression"])
    if isinstance(val, float) and val.is_integer():
        val = int(val)
    return str(val)


def clock(args: dict[str, Any], ctx: ToolContext) -> str:
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")


# -- memory -----------------------------------------------------------------
def _need_memory(ctx: ToolContext) -> tuple[bool, str]:
    return (True, "") if ctx.memory is not None else (False, "memory store not attached")


def remember(args: dict[str, Any], ctx: ToolContext) -> str:
    mid = ctx.memory.add("fact", args["fact"], meta={"source": "remember-tool"}, importance=0.7)
    return f"remembered (memory #{mid})"


def recall(args: dict[str, Any], ctx: ToolContext) -> str:
    k = int(args.get("k", 5))
    facts = ctx.memory.search(args["query"], k=k, kinds=["fact"])
    if len(facts) < k:  # lexical search misses paraphrases; always surface recent facts too
        seen = {f.id for f in facts}
        facts += [f for f in ctx.memory.recent("fact", k) if f.id not in seen][: k - len(facts)]
    other = ctx.memory.search(args["query"], k=3, kinds=["note", "episode"], min_score=0.3)
    lines = [f"- [fact] {f.text}" for f in facts] + [f"- [{h.kind}] {h.text}" for h in other]
    return "\n".join(lines) if lines else "(nothing relevant remembered)"


# -- code -------------------------------------------------------------------
def python_exec(args: dict[str, Any], ctx: ToolContext) -> str:
    timeout = min(float(args.get("timeout", 10)), 30.0)
    res = run_python(args["code"], timeout=timeout, deny_paths=[str(ctx.settings.data_dir)])
    return res.render()


# -- reporting & scheduling -------------------------------------------------
def send_report(args: dict[str, Any], ctx: ToolContext) -> str:
    if ctx.notifier is None:
        from ..reporting import Outbox
        ctx.notifier = Outbox(ctx.settings)
    return ctx.notifier.send(ctx.user_id, args["title"], args["body"])


def _need_scheduler(ctx: ToolContext) -> tuple[bool, str]:
    return (True, "") if ctx.scheduler is not None else (False, "scheduler not attached in this session")


def schedule_job(args: dict[str, Any], ctx: ToolContext) -> str:
    every = int(args["every_minutes"])
    if every < 5:
        raise ValueError("minimum interval is 5 minutes")
    # Jobs created by the agent itself never get write grants: a human must add them.
    jid = ctx.scheduler.add_job(ctx.user_id, args.get("name") or args["task"][:40], args["task"],
                                "interval", str(every * 60), grants=[])
    return f"scheduled job #{jid} every {every} min (no write permissions; edit with `mind schedule` to grant)"


def default_registry(gate: PermissionGate, audit: AuditLog, output_cap: int = 4000) -> ToolRegistry:
    reg = ToolRegistry(gate, audit, output_cap)
    obj = lambda props, req: {"type": "object", "properties": props, "required": req}  # noqa: E731
    reg.register(Tool("calculator", "Evaluate an arithmetic expression exactly.",
                      obj({"expression": {"type": "string"}}, ["expression"]), Tier.READ, calculator, timeout=2))
    reg.register(Tool("clock", "Current local date and time.", obj({}, []), Tier.READ, clock, timeout=2))
    reg.register(Tool("remember", "Store a durable fact about the user.",
                      obj({"fact": {"type": "string"}}, ["fact"]), Tier.WRITE, remember, available=_need_memory,
                      target=lambda a: a.get("fact", "")[:40]))
    reg.register(Tool("recall", "Search long-term memory about the user and past tasks.",
                      obj({"query": {"type": "string"}, "k": {"type": "integer"}}, ["query"]), Tier.READ, recall,
                      available=_need_memory))
    reg.register(Tool("python_exec", "Run Python 3 code in a sandbox (no network, temp dir, 10s). Print results.",
                      obj({"code": {"type": "string"}, "timeout": {"type": "number"}}, ["code"]),
                      Tier.WRITE, python_exec, timeout=35))
    reg.register(Tool("send_report", "Send the user a report (outbox, optional webhook).",
                      obj({"title": {"type": "string"}, "body": {"type": "string"}}, ["title", "body"]),
                      Tier.WRITE, send_report, target=lambda a: a.get("title", "")[:40]))
    reg.register(Tool("schedule_job", "Schedule a recurring headless task for this user.",
                      obj({"task": {"type": "string"}, "every_minutes": {"type": "integer"}, "name": {"type": "string"}},
                          ["task", "every_minutes"]), Tier.WRITE, schedule_job, available=_need_scheduler))
    for t in note_tools() + web_tools():
        reg.register(t)
    return reg
