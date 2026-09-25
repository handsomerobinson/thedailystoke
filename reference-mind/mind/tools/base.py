"""Tool registry: validation -> availability -> permission gate -> timed run -> capped, audited output.

No exception raised by a tool ever escapes execute(); failures become
observations the brain can read and react to.  The one exception that *is*
propagated is BudgetExceeded, because the agent loop must stop on it.
"""
from __future__ import annotations

import dataclasses
import hashlib
import re
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Callable

from ..audit import AuditError, AuditLog
from ..cost import Budget, BudgetExceeded
from ..permissions import ActionRequest, PermissionGate, Tier
from ..types import ToolCall, ToolSpec
from ..util import truncate


@dataclass
class ToolContext:
    user_id: str
    settings: Any
    memory: Any = None
    task_id: str = ""
    headless: bool = False
    scheduler: Any = None
    notifier: Any = None
    extras: dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolResult:
    ok: bool
    output: str
    pending_id: int | None = None
    denied: bool = False

    def as_observation(self) -> str:
        return self.output if self.ok else f"ERROR: {self.output}"


Handler = Callable[[dict[str, Any], ToolContext], str]
Availability = Callable[[ToolContext], tuple[bool, str]]


def _always(_ctx: ToolContext) -> tuple[bool, str]:
    return True, ""


@dataclass
class Tool:
    name: str
    description: str
    parameters: dict[str, Any]
    tier: Tier
    handler: Handler
    available: Availability = _always
    target: Callable[[dict[str, Any]], str] = lambda args: ""
    timeout: float = 20.0
    trust: str = "data"  # "untrusted" (web) / "other_user" (circle content) always taint; "data" only if it carries instructions
    # MC2: hosts this call would send bytes to (empty = stays on the device)
    destinations: Callable[[dict[str, Any], ToolContext], list[str]] = lambda args, ctx: []
    # MC15: does this call return content authored by people other than the user?
    third_party: Callable[[dict[str, Any]], bool] = lambda args: False
    declared_tier: Tier | None = None  # what the tool claimed; the signed registry decides (MC3)

    def spec(self) -> ToolSpec:
        return ToolSpec(self.name, f"[{self.tier.name}] {self.description}", self.parameters)


_TYPES = {"string": str, "integer": int, "number": (int, float), "boolean": bool, "object": dict, "array": list}


def validate_args(schema: dict[str, Any], args: Any) -> tuple[dict[str, Any] | None, str]:
    """Minimal JSON-schema check: object, required, property types, no unknown keys. Coerces numeric strings."""
    if not isinstance(args, dict):
        return None, "arguments must be a JSON object"
    props: dict[str, Any] = schema.get("properties", {})
    out: dict[str, Any] = {}
    for key in args:
        if key not in props:
            return None, f"unknown argument {key!r}; expected {sorted(props)}"
    for key in schema.get("required", []):
        if key not in args:
            return None, f"missing required argument {key!r}"
    for key, val in args.items():
        want = props[key].get("type")
        py = _TYPES.get(want)
        if py is None:
            out[key] = val
            continue
        if want == "integer" and isinstance(val, str) and val.strip().lstrip("-").isdigit():
            val = int(val)
        elif want == "number" and isinstance(val, str):
            try:
                val = float(val)
            except ValueError:
                pass
        if isinstance(val, bool) and want in ("integer", "number"):
            return None, f"argument {key!r} must be {want}"
        if not isinstance(val, py):
            return None, f"argument {key!r} must be {want}, got {type(val).__name__}"
        out[key] = val
    return out, ""


_SHINGLE_WORD = re.compile(r"[a-z0-9]+")


def _shingles(text: str, n: int = 5) -> set[tuple[str, ...]]:
    toks = _SHINGLE_WORD.findall((text or "").lower())
    if len(toks) < n:
        return {tuple(toks)} if len(toks) >= 3 else set()
    return {tuple(toks[i:i + n]) for i in range(len(toks) - n + 1)}


def carried_memory(args: dict[str, Any], ctx: ToolContext) -> str:
    """MC2: does an outgoing payload contain stored memory or note contents?  Returns a description or ''."""
    payload = " ".join(str(v) for v in args.values())
    pay = _SHINGLE_WORD.findall(payload.lower())
    pay_sh = {tuple(pay[i:i + 5]) for i in range(max(0, len(pay) - 4))}
    pay_text = " " + " ".join(pay) + " "
    hits: list[str] = []

    def check(label: str, text: str) -> None:
        for sh in _shingles(text):
            if (len(sh) == 5 and sh in pay_sh) or (len(sh) < 5 and f" {' '.join(sh)} " in pay_text):
                hits.append(label)
                return
    mem = ctx.memory
    if mem is not None:
        try:
            for item in mem.recent(None, 500):
                if item.kind in ("fact", "note", "reflection"):
                    check(f"memory #{item.id}", item.text)
        except Exception:  # noqa: BLE001 - if memory cannot be read, assume the worst
            return "memory unreadable (assumed to be carried)"
    try:
        notes = ctx.settings.user_dir(ctx.user_id) / "notes"
        for p in list(notes.glob("*.md"))[:200]:
            check(f"note {p.stem}", p.read_text(encoding="utf-8", errors="replace")[:20000])
    except Exception:  # noqa: BLE001
        pass
    return ", ".join(sorted(set(hits))[:5])


class ToolRegistry:
    def __init__(self, gate: PermissionGate, audit: AuditLog, output_cap: int = 4000, tiers=None):
        from ..tiers import TierRegistry
        self.gate = gate
        self.audit = audit
        self.output_cap = output_cap
        self.tiers = tiers if tiers is not None else TierRegistry()
        self._tools: dict[str, Tool] = {}
        self.tier_notes: list[str] = []

    def register(self, tool: Tool) -> None:
        """The signed registry decides the tier (MC3).  Undeclared -> IRREVERSIBLE; a mismatch is reported."""
        signed = self.tiers.tier_of(tool.name)
        declared = tool.declared_tier if tool.declared_tier is not None else tool.tier
        if not self.tiers.declared(tool.name):
            self.tier_notes.append(f"{tool.name}: not in the signed tier registry -> IRREVERSIBLE")
        elif signed != declared:
            self.tier_notes.append(f"{tool.name}: declares {declared.name}, signed registry says {signed.name}")
        self._tools[tool.name] = dataclasses.replace(tool, tier=signed, declared_tier=declared)

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def names(self) -> list[str]:
        return sorted(self._tools)

    def specs(self, ctx: ToolContext | None = None) -> list[ToolSpec]:
        specs = []
        for t in self._tools.values():
            spec = t.spec()
            if ctx is not None:
                ok, why = self._safe_available(t, ctx)
                if not ok:
                    spec = ToolSpec(spec.name, spec.description + f" (CURRENTLY UNAVAILABLE: {why})", spec.parameters)
            specs.append(spec)
        return specs

    @staticmethod
    def _safe_available(tool: Tool, ctx: ToolContext) -> tuple[bool, str]:
        try:
            return tool.available(ctx)
        except Exception as exc:
            return False, f"availability check failed: {exc}"

    def status(self, ctx: ToolContext) -> dict[str, str]:
        out = {}
        for name, t in sorted(self._tools.items()):
            ok, why = self._safe_available(t, ctx)
            out[name] = f"{t.tier.name:12s} {'ready' if ok else 'unavailable: ' + why}"
        return out

    def _log(self, event: str, **fields: Any) -> None:
        try:
            self.audit.record(event, **fields)
        except AuditError:
            pass  # gate already enforced fail-closed before any state change

    def execute(self, call: ToolCall, ctx: ToolContext, budget: Budget | None = None,
                preconfirmed: bool = False) -> ToolResult:
        if budget is not None:
            budget.check_tool_call()  # BudgetExceeded propagates by design
        tool = self._tools.get(call.name)
        base = dict(user=ctx.user_id, tool=call.name, task_id=ctx.task_id, headless=ctx.headless)
        if tool is None:
            self._log("tool.rejected", **base, reason="unknown tool")
            return ToolResult(False, f"unknown tool {call.name!r}; available tools: {', '.join(self.names())}")
        args, err = validate_args(tool.parameters, call.args)
        if args is None:
            self._log("tool.rejected", **base, reason=err)
            return ToolResult(False, f"invalid arguments for {tool.name}: {err}")
        ok, why = self._safe_available(tool, ctx)
        if not ok:
            self._log("tool.unavailable", **base, reason=why)
            return ToolResult(False, f"tool {tool.name} is unavailable ({why}). Continue without it and say so.")
        try:
            target = str(tool.target(args))
        except Exception:
            target = ""
        lock = ctx.extras.get("charter_lock")
        if lock and tool.tier > Tier.READ:
            self._log("tool.rejected", **base, reason=f"charter integrity failure: {lock}")
            return ToolResult(False, f"permission denied: charter integrity failure ({lock}); state-changing tools are "
                                     f"disabled until an operator runs `mind charter restore` or a recorded removal", denied=True)
        tainted = str(ctx.extras.get("tainted") or "")
        destinations, carries = [], ""
        if tool.tier == Tier.EGRESS:
            try:
                destinations = [str(d).lower() for d in tool.destinations(args, ctx) if d]
            except Exception as exc:  # noqa: BLE001 - an unknown destination is not a local one
                self._log("tool.rejected", **base, reason=f"cannot determine egress destination: {exc}")
                return ToolResult(False, f"permission denied: cannot determine where {tool.name} would send data ({exc})",
                                  denied=True)
            if destinations:
                carries = carried_memory(args, ctx)
        allow = frozenset(getattr(ctx.settings, "egress_allowlist", lambda: frozenset())())
        req = ActionRequest(user=ctx.user_id, tool=tool.name, tier=tool.tier, args=args,
                            summary=f"{tool.name}({_short_args(args)}) [{tool.tier.name}]" + (f" [TAINTED: {tainted}]" if tainted else "")
                            + (f" -> {', '.join(destinations)}" if destinations else ""),
                            confirmation_phrase=f"{tool.name} {target}".strip(),
                            task_id=ctx.task_id, headless=ctx.headless, tainted=tainted,
                            destinations=destinations, allowlist=allow, carries_memory=carries)
        if not preconfirmed:
            decision = self.gate.authorize(req)
            if not decision.allowed:
                return ToolResult(False, f"permission denied: {decision.reason}",
                                  pending_id=decision.pending_id, denied=True)
        else:
            try:
                self.audit.record("permission.decision", **base, tier=tool.tier.name, args=args,
                                  allowed=True, reason="confirmed via pending-approval queue")
            except AuditError as exc:
                return ToolResult(False, f"audit log unavailable, refusing: {exc}", denied=True)
        if budget is not None:
            budget.charge_tool()
        started = time.monotonic()
        result = self._run_with_timeout(tool, args, ctx)
        duration = round(time.monotonic() - started, 3)
        result.output = truncate(result.output, self.output_cap)
        self._log("tool.result", **base, ok=result.ok, duration_s=duration,
                  output_sha256=hashlib.sha256(result.output.encode()).hexdigest()[:16],
                  preview=result.output[:200])
        return result

    @staticmethod
    def _run_with_timeout(tool: Tool, args: dict[str, Any], ctx: ToolContext) -> ToolResult:
        box: dict[str, Any] = {}

        def target() -> None:
            try:
                box["out"] = tool.handler(args, ctx)
            except BaseException as exc:  # noqa: BLE001 - tools must never kill the loop
                box["err"] = exc

        th = threading.Thread(target=target, name=f"tool-{tool.name}", daemon=True)
        th.start()
        th.join(tool.timeout)
        if th.is_alive():
            # In-process handlers cannot be force-killed in Python; the thread is
            # abandoned (daemon).  Code execution runs out-of-process and IS killed.
            return ToolResult(False, f"tool {tool.name} timed out after {tool.timeout}s")
        if "err" in box:
            exc = box["err"]
            return ToolResult(False, f"{tool.name} failed: {type(exc).__name__}: {exc}")
        return ToolResult(True, str(box.get("out", "")))


def _short_args(args: dict[str, Any]) -> str:
    parts = []
    for k, v in args.items():
        s = repr(v)
        parts.append(f"{k}={s[:60] + '...' if len(s) > 60 else s}")
    return ", ".join(parts)
