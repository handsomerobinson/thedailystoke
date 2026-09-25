"""Permission tiers, approvals and the gate every tool call passes through.

  READ          runs freely (no side effects outside the process)
  WRITE         changes user state: needs a human "yes", or a scoped grant (session/job)
  IRREVERSIBLE  cannot be undone: needs an explicit typed confirmation code every time;
                grants NEVER cover it

Headless runs (scheduled/event jobs) have no human present. A WRITE without a grant and
every IRREVERSIBLE action is *deferred*: recorded in the user's approvals queue and denied
for now. When a human approves it, the exact same action (same tool + same arguments,
matched by digest) may run once on a later run.
"""
from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Callable

from .util import canonical_json, sha256_hex


class Tier(enum.IntEnum):
    READ = 0
    WRITE = 1
    IRREVERSIBLE = 2


@dataclass
class ActionRequest:
    user: str
    tool: str
    tier: Tier
    args: dict
    task_id: str = ""
    headless: bool = False
    job_id: str = ""
    tainted_by: str = ""   # set when untrusted content (web) is already in this trial's context

    @property
    def digest(self) -> str:
        return sha256_hex(canonical_json({"u": self.user, "t": self.tool, "a": self.args}))[:16]

    @property
    def confirmation_code(self) -> str:
        return f"CONFIRM {self.tool} {self.digest[:6]}"

    def describe(self) -> str:
        return f"{self.tool}({canonical_json(self.args)[:300]}) [{self.tier.name}]"


@dataclass
class Decision:
    allowed: bool
    reason: str
    deferred: bool = False
    approval_id: int | None = None


class Approver:
    """Asks a human (or a policy standing in for one)."""

    def approve_write(self, req: ActionRequest) -> bool:
        return False

    def confirm_irreversible(self, req: ActionRequest) -> bool:
        return False


class DenyAll(Approver):
    pass


class ScriptedApprover(Approver):
    """Deterministic approver for demos/tests. `answers` maps tool name -> bool (or callable)."""

    def __init__(self, answers: dict | None = None, default: bool = False, confirm_irreversible: bool = False):
        self.answers = answers or {}
        self.default = default
        self._confirm = confirm_irreversible
        self.asked: list[str] = []

    def _answer(self, req):
        self.asked.append(req.describe())
        a = self.answers.get(req.tool, self.default)
        return a(req) if callable(a) else bool(a)

    def approve_write(self, req):
        return self._answer(req)

    def confirm_irreversible(self, req):
        self.asked.append("IRREVERSIBLE " + req.describe())
        a = self.answers.get(req.tool, self._confirm)
        return a(req) if callable(a) else bool(a)


class ConsoleApprover(Approver):
    """Interactive approver. IRREVERSIBLE actions require typing the exact confirmation code."""

    def __init__(self, input_fn: Callable[[str], str] = input, output_fn: Callable[[str], None] = print):
        self.input = input_fn
        self.output = output_fn

    def approve_write(self, req):
        self.output(f"\n[approval needed] {req.describe()}")
        try:
            return self.input("Allow? [y/N] ").strip().lower() in ("y", "yes")
        except EOFError:
            return False

    def confirm_irreversible(self, req):
        self.output(f"\n[IRREVERSIBLE ACTION] {req.describe()}\nThis cannot be undone. "
                    f"Type exactly:  {req.confirmation_code}")
        try:
            return self.input("> ").strip() == req.confirmation_code
        except EOFError:
            return False


@dataclass
class PermissionGate:
    approver: Approver
    memory: object = None              # MemoryStore (for the approvals queue); optional
    grants: set = field(default_factory=set)   # tool names pre-approved for WRITE in this scope
    headless: bool = False

    def check(self, req: ActionRequest) -> Decision:
        if req.tier == Tier.READ:
            return Decision(True, "read-only")

        # an earlier human approval of this exact action (one-shot)
        if self.memory is not None and self.memory.consume_approval(req.digest):
            return Decision(True, "previously approved by human (one-shot)")

        if req.tier == Tier.WRITE and req.tool in self.grants and not req.tainted_by:
            return Decision(True, f"granted for this {'job' if self.headless else 'session'}")
        taint_note = (f" (grant suspended: untrusted content from {req.tainted_by} is in context)"
                      if req.tainted_by and req.tool in self.grants else "")

        if self.headless:
            aid = None
            if self.memory is not None:
                aid = self.memory.add_approval(req.tool, req.args, req.digest,
                                               f"{req.tier.name} action requested by headless job",
                                               req.job_id)
            return Decision(False, f"deferred: {req.tier.name} action needs a human; queued as approval #{aid}"
                                   + taint_note, deferred=True, approval_id=aid)

        try:
            if req.tier == Tier.WRITE:
                ok = self.approver.approve_write(req)
                return Decision(ok, ("approved by user" if ok else "denied by user") + taint_note)
            ok = self.approver.confirm_irreversible(req)
            return Decision(ok, "explicitly confirmed by user" if ok else "irreversible action not confirmed")
        except Exception as e:  # a broken approver must fail closed
            return Decision(False, f"approver error, failing closed: {e}")
