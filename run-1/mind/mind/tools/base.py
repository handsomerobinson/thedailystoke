"""Tool base class, argument validation, and the registry — the single choke point.

`ToolRegistry.execute()` is the ONLY path from a model's tool call to a side effect:
    validate args -> permission gate -> audit(decision) -> run (exceptions caught)
    -> cap output -> audit(result)
It never raises; every failure comes back to the model as an error tool result.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from ..audit import AuditError
from ..permissions import ActionRequest, Decision, PermissionGate, Tier
from ..providers.base import ToolCall, ToolSpec
from ..util import truncate


@dataclass
class ToolResult:
    ok: bool
    content: str
    data: Any = None
    denied: bool = False
    deferred: bool = False
    taint: str = ""        # set by a tool whose output carries untrusted content (e.g. a tainted note)


@dataclass
class ToolContext:
    user: str
    memory: Any                  # MemoryStore
    config: Any                  # Config
    clock: Any
    task_id: str = ""
    headless: bool = False
    job_id: str = ""
    scheduler: Any = None
    charter: Any = None          # CharterStore (read-only use: consent checks for R35)
    extra: dict = field(default_factory=dict)


class Tool:
    name: str = ""
    description: str = ""
    tier: Tier = Tier.READ
    parameters: dict = {"type": "object", "properties": {}, "required": []}
    taints: bool = False   # output is untrusted third-party content (suspends WRITE grants afterwards)

    def tier_for(self, args: dict) -> Tier:
        """Tools may escalate their tier based on arguments (never lower it)."""
        return self.tier

    def run(self, args: dict, ctx: ToolContext) -> ToolResult:  # pragma: no cover - abstract
        raise NotImplementedError

    def spec(self) -> ToolSpec:
        return ToolSpec(self.name, f"[{self.tier.name}] {self.description}", self.parameters)


_TYPES = {"string": str, "integer": int, "number": (int, float), "boolean": bool, "object": dict, "array": list}


def validate_args(schema: dict, args: Any) -> str | None:
    """Minimal JSON-schema check (type/required/maxLength/enum/min/max). Returns error or None."""
    if not isinstance(args, dict):
        return "arguments must be a JSON object"
    props = schema.get("properties", {})
    for req in schema.get("required", []):
        if req not in args:
            return f"missing required argument '{req}'"
    if schema.get("additionalProperties") is False:
        extra = set(args) - set(props)
        if extra:
            return f"unexpected argument(s): {sorted(extra)}"
    for k, v in args.items():
        p = props.get(k)
        if not p:
            continue
        t = p.get("type")
        if t and not isinstance(v, _TYPES[t]) or (t in ("integer", "number") and isinstance(v, bool)):
            return f"argument '{k}' must be {t}"
        if "maxLength" in p and isinstance(v, str) and len(v) > p["maxLength"]:
            return f"argument '{k}' too long (max {p['maxLength']})"
        if "enum" in p and v not in p["enum"]:
            return f"argument '{k}' must be one of {p['enum']}"
        if "minimum" in p and isinstance(v, (int, float)) and v < p["minimum"]:
            return f"argument '{k}' must be >= {p['minimum']}"
        if "maximum" in p and isinstance(v, (int, float)) and v > p["maximum"]:
            return f"argument '{k}' must be <= {p['maximum']}"
    return None


class ToolRegistry:
    def __init__(self, tools: list[Tool], audit, gate: PermissionGate, output_limit: int = 4000):
        self.tools = {t.name: t for t in tools}
        self.audit = audit
        self.gate = gate
        self.output_limit = output_limit

    def specs(self) -> list[ToolSpec]:
        return [t.spec() for t in self.tools.values()]

    def _audit(self, event: str, fail_closed: bool, **fields) -> bool:
        try:
            self.audit.write(event, **fields)
            return True
        except AuditError:
            return not fail_closed

    def execute(self, call: ToolCall, ctx: ToolContext) -> ToolResult:
        base = {"user": ctx.user, "task": ctx.task_id, "job": ctx.job_id, "tool": call.name,
                "args": call.arguments, "headless": ctx.headless}
        tool = self.tools.get(call.name)
        if tool is None:
            self._audit("tool.unknown", False, **base)
            return ToolResult(False, f"unknown tool '{call.name}'. Available: {sorted(self.tools)}")
        err = validate_args(tool.parameters, call.arguments)
        if err:
            self._audit("tool.invalid_args", False, **base, error=err)
            return ToolResult(False, f"invalid arguments for {call.name}: {err}")
        try:
            tier = max(tool.tier, tool.tier_for(call.arguments))
        except Exception:
            tier = Tier.IRREVERSIBLE  # if we cannot classify it, treat it as the most dangerous
        req = ActionRequest(ctx.user, call.name, Tier(tier), call.arguments, ctx.task_id, ctx.headless, ctx.job_id,
                            tainted_by=ctx.extra.get("tainted_by", ""))
        decision: Decision = self.gate.check(req)
        fail_closed = tier > Tier.READ
        if not self._audit("tool.decision", fail_closed, **base, tier=Tier(tier).name, allowed=decision.allowed,
                           reason=decision.reason, deferred=decision.deferred, digest=req.digest):
            return ToolResult(False, "audit log unavailable: state-changing actions are disabled (fail closed)",
                              denied=True)
        if not decision.allowed:
            return ToolResult(False, f"permission {'deferred' if decision.deferred else 'denied'}: {decision.reason}",
                              denied=True, deferred=decision.deferred)
        t0 = time.monotonic()
        try:
            result = tool.run(call.arguments, ctx)
            if not isinstance(result, ToolResult):
                result = ToolResult(True, str(result))
        except Exception as e:
            result = ToolResult(False, f"{call.name} raised {type(e).__name__}: {e}")
        result.content = truncate(str(result.content), self.output_limit)
        if (tool.taints and result.ok) or result.taint:
            # prompt-injection containment for the rest of this trial
            ctx.extra.setdefault("tainted_by", result.taint or tool.name)
        self._audit("tool.result", False, **base, ok=result.ok, ms=int((time.monotonic() - t0) * 1000),
                    result=result.content[:500])
        return result
