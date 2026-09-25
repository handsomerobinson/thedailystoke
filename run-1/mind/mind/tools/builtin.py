"""Built-in tools: calculator, memory, notes, code execution, messaging, scheduling."""
from __future__ import annotations

import ast
import math
import operator

from ..permissions import Tier
from ..sandbox import run_python
from .base import Tool, ToolContext, ToolResult


# ---------------------------------------------------------------- calculator (READ) ----
_BIN = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod, ast.Pow: operator.pow}
_UN = {ast.UAdd: operator.pos, ast.USub: operator.neg}
_FUNCS = {n: getattr(math, n) for n in ("sqrt", "log", "log10", "log2", "exp", "sin", "cos", "tan",
                                        "floor", "ceil", "factorial")}
_FUNCS.update({"abs": abs, "round": round, "min": min, "max": max})
_CONSTS = {"pi": math.pi, "e": math.e}


def safe_eval(expr: str):
    """Evaluate arithmetic without eval(): whitelisted AST nodes, bounded exponents/factorials."""
    if len(expr) > 300:
        raise ValueError("expression too long")
    tree = ast.parse(expr.replace("^", "**"), mode="eval")

    def ev(n):
        if isinstance(n, ast.Expression):
            return ev(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)) and not isinstance(n.value, bool):
            return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in _BIN:
            a, b = ev(n.left), ev(n.right)
            if isinstance(n.op, ast.Pow) and (abs(b) > 1000 or abs(a) > 1e6 and b > 10):
                raise ValueError("exponent too large")
            if isinstance(n.op, ast.Mult) and isinstance(a, int) and isinstance(b, int) and \
                    abs(a).bit_length() + abs(b).bit_length() > 4096:
                raise ValueError("result too large")
            return _BIN[type(n.op)](a, b)
        if isinstance(n, ast.UnaryOp) and type(n.op) in _UN:
            return _UN[type(n.op)](ev(n.operand))
        if isinstance(n, ast.Name) and n.id in _CONSTS:
            return _CONSTS[n.id]
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in _FUNCS and not n.keywords:
            args = [ev(a) for a in n.args]
            if n.func.id == "factorial" and args and args[0] > 1000:
                raise ValueError("factorial argument too large")
            return _FUNCS[n.func.id](*args)
        raise ValueError(f"unsupported expression element: {type(n).__name__}")

    return ev(tree)


class Calculator(Tool):
    name = "calculator"
    description = "Evaluate an arithmetic expression exactly (supports + - * / // % ** and math functions)."
    tier = Tier.READ
    parameters = {"type": "object", "properties": {"expression": {"type": "string", "maxLength": 300}},
                  "required": ["expression"]}

    def run(self, args, ctx):
        try:
            v = safe_eval(args["expression"])
        except ZeroDivisionError:
            return ToolResult(False, "division by zero")
        except (ValueError, SyntaxError, TypeError, OverflowError) as e:
            return ToolResult(False, f"cannot evaluate: {e}")
        if isinstance(v, float) and v.is_integer() and abs(v) < 1e15:
            v = int(v)
        return ToolResult(True, str(v), data=v)


# ---------------------------------------------------------------- memory tools ---------
class RememberFact(Tool):
    name = "remember_fact"
    description = "Store a durable fact about the user (key/value). Overwrites the old value for that key."
    tier = Tier.WRITE
    parameters = {"type": "object", "properties": {"key": {"type": "string", "maxLength": 80},
                                                   "value": {"type": "string", "maxLength": 1000}},
                  "required": ["key", "value"]}

    def run(self, args, ctx):
        old = ctx.memory.get_fact(args["key"])
        ctx.memory.set_fact(args["key"], args["value"], source="agent")
        return ToolResult(True, f"remembered {args['key']} = {args['value']}" + (f" (was: {old})" if old else ""))


class Recall(Tool):
    name = "recall"
    description = "Search the user's long-term memory (facts, past episodes, lessons, notes)."
    tier = Tier.READ
    parameters = {"type": "object", "properties": {"query": {"type": "string", "maxLength": 500}},
                  "required": ["query"]}

    def run(self, args, ctx):
        q = args["query"]
        lines = []
        facts = ctx.memory.facts()
        ql = q.lower()
        for k, v in facts.items():
            if any(w in (k + " " + v).lower() for w in ql.split()):
                lines.append(f"fact: {k} = {v}")
        for h in ctx.memory.search(q, k=5):
            lines.append(f"{h.kind}#{h.id} (score {h.score}): {h.text[:300]}")
        for n in ctx.memory.search_notes(q, k=3):
            lines.append(f"note '{n['title']}': {n['body'][:200]}")
        return ToolResult(True, "\n".join(lines) if lines else "nothing relevant in memory")


# ---------------------------------------------------------------- notes ----------------
class WriteNote(Tool):
    name = "write_note"
    description = "Create or update a note (previous versions are kept and restorable)."
    tier = Tier.WRITE
    parameters = {"type": "object", "properties": {"title": {"type": "string", "maxLength": 200},
                                                   "body": {"type": "string", "maxLength": 20000}},
                  "required": ["title", "body"]}

    def run(self, args, ctx):
        v = ctx.memory.write_note(args["title"], args["body"])
        return ToolResult(True, f"note '{args['title']}' saved (version {v})")


class ReadNote(Tool):
    name = "read_note"
    description = "Read a note by title."
    tier = Tier.READ
    parameters = {"type": "object", "properties": {"title": {"type": "string", "maxLength": 200}},
                  "required": ["title"]}

    def run(self, args, ctx):
        n = ctx.memory.read_note(args["title"])
        if not n:
            return ToolResult(False, f"no note titled '{args['title']}'")
        return ToolResult(True, f"# {n['title']} (v{n['version']})\n{n['body']}")


class ListNotes(Tool):
    name = "list_notes"
    description = "List the user's notes."
    tier = Tier.READ
    parameters = {"type": "object", "properties": {}, "required": []}

    def run(self, args, ctx):
        notes = ctx.memory.list_notes()
        if not notes:
            return ToolResult(True, "no notes yet")
        return ToolResult(True, f"{len(notes)} note(s): " + ", ".join(f"'{n['title']}'" for n in notes))


class DeleteNote(Tool):
    name = "delete_note"
    description = "Permanently delete a note and all of its history. Cannot be undone."
    tier = Tier.IRREVERSIBLE
    parameters = {"type": "object", "properties": {"title": {"type": "string", "maxLength": 200}},
                  "required": ["title"]}

    def run(self, args, ctx):
        ok = ctx.memory.purge_note(args["title"])
        return ToolResult(ok, f"note '{args['title']}' permanently deleted" if ok else f"no note '{args['title']}'")


# ---------------------------------------------------------------- code execution -------
class RunPython(Tool):
    name = "run_python"
    description = ("Run Python 3 code in a sandbox (no network, temp dir, CPU/memory/time/output limits). "
                   "Print what you need to see.")
    tier = Tier.WRITE  # executes arbitrary code: treated as state-changing even though it is sandboxed
    parameters = {"type": "object", "properties": {"code": {"type": "string", "maxLength": 20000}},
                  "required": ["code"]}

    def run(self, args, ctx):
        extra = (str(ctx.config.data_dir),) if ctx.config is not None else ()
        res = run_python(args["code"], ctx.config.sandbox if ctx.config else None, extra_hide=extra)
        return ToolResult(res.ok, res.summary(), data=res)


# ---------------------------------------------------------------- outbound message -----
class SendMessage(Tool):
    name = "send_message"
    description = ("Send a message to someone outside this system. Irreversible once sent. "
                   "(In this build delivery is SIMULATED: it is recorded in the user's outbox.)")
    tier = Tier.IRREVERSIBLE
    parameters = {"type": "object", "properties": {"to": {"type": "string", "maxLength": 200},
                                                   "body": {"type": "string", "maxLength": 4000}},
                  "required": ["to", "body"]}

    def run(self, args, ctx):
        mid = ctx.memory.record_sent(args["to"], args["body"])
        return ToolResult(True, f"message #{mid} delivered to {args['to']} (simulated channel)")


# ---------------------------------------------------------------- scheduling -----------
class ScheduleTask(Tool):
    name = "schedule_task"
    description = "Schedule a recurring headless task for this user (it will report back to the inbox)."
    tier = Tier.WRITE
    parameters = {"type": "object", "properties": {
        "task": {"type": "string", "maxLength": 1000},
        "every_minutes": {"type": "integer", "minimum": 1, "maximum": 525600}},
        "required": ["task", "every_minutes"]}

    def run(self, args, ctx):
        if ctx.scheduler is None:
            return ToolResult(False, "scheduler not available in this session")
        job = ctx.scheduler.add_job(ctx.user, name=args["task"][:60], task=args["task"],
                                    every_s=args["every_minutes"] * 60)
        return ToolResult(True, f"job {job} scheduled every {args['every_minutes']} min (no WRITE grants; "
                                f"state-changing steps will be queued for your approval)")
