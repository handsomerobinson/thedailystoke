"""Permission tiers, approvers, and the gate every tool call passes through.

    READ          runs freely (still audit-logged)
    WRITE         changes state reversibly -> needs approval
    EGRESS        sends bytes off the device (MC2) -> destination must be on the allowlist; SUSPENDED (denied)
                  whenever the task is tainted; carrying memory contents needs a FRESH human approval that no
                  pre-grant, session grant or headless grant can supply.  No destination = local only = WRITE rules.
    IRREVERSIBLE  cannot be undone        -> needs explicit typed confirmation
                                             of an exact phrase ("note_delete draft")

Tiers come from the signed tier registry (tiers.py), never from the tool itself (MC3); an undeclared tool is
IRREVERSIBLE.

Headless runs (schedules/events) have no human: WRITE tools run only if the
job was granted them when it was created; IRREVERSIBLE actions are never run
headless -- they are parked in a pending-approvals queue and surfaced in the
job's report for the user to confirm later.

Fail-closed: if the audit log cannot be written, state-changing actions are
denied.  READ actions still run (and the failure is reported on stderr) so a
full disk does not blind the agent.
"""
from __future__ import annotations

import json
import sqlite3
import sys
import threading
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import IntEnum
from pathlib import Path
from typing import Any, Callable

from .audit import AuditError, AuditLog


class Tier(IntEnum):
    READ = 0
    WRITE = 1
    EGRESS = 2
    IRREVERSIBLE = 3


@dataclass
class ActionRequest:
    user: str
    tool: str
    tier: Tier
    args: dict[str, Any]
    summary: str
    confirmation_phrase: str
    task_id: str = ""
    headless: bool = False
    tainted: str = ""  # non-empty: untrusted content with instructions was read earlier in this task
    destinations: list[str] = field(default_factory=list)  # EGRESS: hosts the bytes go to
    allowlist: frozenset = frozenset()                      # EGRESS: hosts the user allowed
    carries_memory: str = ""  # EGRESS: non-empty if the payload contains stored memory/notes (needs fresh approval)

    @property
    def needs_fresh(self) -> bool:
        return bool(self.carries_memory)


@dataclass
class Decision:
    allowed: bool
    reason: str
    pending_id: int | None = None


class Approver(ABC):
    @abstractmethod
    def approve(self, req: ActionRequest) -> bool:
        """Approve a WRITE action."""

    @abstractmethod
    def confirm(self, req: ActionRequest) -> str | None:
        """Return the phrase the human typed for an IRREVERSIBLE action (None = declined)."""


class DenyAllApprover(Approver):
    def approve(self, req: ActionRequest) -> bool:
        return False

    def confirm(self, req: ActionRequest) -> str | None:
        return None


class PolicyApprover(Approver):
    """Scripted approver: pre-granted tools only. Used by tests, the demo, and `run --approve`."""

    def __init__(self, write_grants: set[str] | None = None, irreversible_grants: set[str] | None = None,
                 log: Callable[[str], None] | None = None):
        self.write_grants = set(write_grants or ())
        self.irreversible_grants = set(irreversible_grants or ())
        self.log = log
        self.seen: list[ActionRequest] = []

    def approve(self, req: ActionRequest) -> bool:
        self.seen.append(req)
        # pre-grants never cover a tainted task, nor egress that carries memory contents (MC2: fresh approval only)
        ok = req.tool in self.write_grants and not req.tainted and not req.needs_fresh
        if self.log:
            why = ('tainted: pre-grants suspended' if req.tainted else
                   'carries memory: needs a fresh human approval' if req.needs_fresh else 'not granted')
            self.log(f"  [approval] {req.summary} -> {'approved (pre-granted)' if ok else 'DENIED (' + why + ')'}")
        return ok

    def confirm(self, req: ActionRequest) -> str | None:
        self.seen.append(req)
        ok = req.tool in self.irreversible_grants and not req.tainted
        if self.log:
            self.log(f"  [confirm]  {req.summary} -> {'confirmed' if ok else 'NOT confirmed'}")
        return req.confirmation_phrase if ok else None


class InteractiveApprover(Approver):
    """Asks on the terminal. 'a' approves a WRITE tool for the rest of the session."""

    def __init__(self, input_fn: Callable[[str], str] = input, output_fn: Callable[[str], None] = print):
        self.input_fn = input_fn
        self.output_fn = output_fn
        self.session_grants: set[str] = set()

    def approve(self, req: ActionRequest) -> bool:
        if req.tool in self.session_grants and not req.tainted and not req.needs_fresh:
            return True
        self.output_fn(self.describe(req))
        if req.needs_fresh:
            self.output_fn(f"NOTE: this sends stored memory/notes off the device ({req.carries_memory}) to "
                           f"{', '.join(req.destinations) or 'nowhere'}. Session approvals do not cover this.")
        if req.tainted:
            self.output_fn(f"WARNING: this task read content containing instructions aimed at the agent ({req.tainted}). "
                           f"Session-wide approvals are suspended; approve only if YOU want this.")
        try:
            ans = self.input_fn(f"[approval needed] {req.summary}\n  allow? [y]es / [n]o / [a]lways this session: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return False
        if ans == "a":
            self.session_grants.add(req.tool)
            return True
        return ans in ("y", "yes")

    @staticmethod
    def describe(req: ActionRequest, cap: int = 4000) -> str:
        """Full arguments -- a human must see the whole code/content they approve, not a 60-char summary."""
        lines = [f"\n--- {req.tool} [{req.tier.name}] wants to run with:"]
        for k, v in req.args.items():
            text = str(v)
            if len(text) > cap:
                text = text[:cap] + f"\n...[{len(text) - cap} more chars not shown - answer n if unsure]"
            lines.append(f"{k}:\n{text}" if "\n" in text else f"{k}: {text}")
        return "\n".join(lines) + "\n---"

    def confirm(self, req: ActionRequest) -> str | None:
        self.output_fn(self.describe(req))
        try:
            return self.input_fn(
                f"\n[IRREVERSIBLE] {req.summary}\n  type exactly '{req.confirmation_phrase}' to confirm (anything else cancels): ").strip()
        except (EOFError, KeyboardInterrupt):
            return None


class PendingApprovals:
    """Queue of actions a headless run wanted but was not allowed to do alone."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        with self._conn() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS pending (
                id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT NOT NULL, tool TEXT NOT NULL,
                args TEXT NOT NULL, summary TEXT NOT NULL, phrase TEXT NOT NULL, task_id TEXT,
                created REAL NOT NULL, status TEXT NOT NULL DEFAULT 'pending', resolved REAL)""")

    def _conn(self) -> sqlite3.Connection:
        db = sqlite3.connect(str(self.path), timeout=10)
        db.row_factory = sqlite3.Row
        return db

    def add(self, req: ActionRequest) -> int:
        with self._lock, self._conn() as db:
            cur = db.execute(
                "INSERT INTO pending(user, tool, args, summary, phrase, task_id, created) VALUES (?,?,?,?,?,?,?)",
                (req.user, req.tool, json.dumps(req.args), req.summary, req.confirmation_phrase, req.task_id, time.time()))
            return int(cur.lastrowid)

    def list(self, user: str, status: str = "pending") -> list[dict[str, Any]]:
        with self._conn() as db:
            rows = db.execute("SELECT * FROM pending WHERE user=? AND status=? ORDER BY id", (user, status)).fetchall()
        return [dict(r) | {"args": json.loads(r["args"])} for r in rows]

    def get(self, pid: int, user: str) -> dict[str, Any] | None:
        with self._conn() as db:
            r = db.execute("SELECT * FROM pending WHERE id=? AND user=?", (int(pid), user)).fetchone()
        return (dict(r) | {"args": json.loads(r["args"])}) if r else None

    def resolve(self, pid: int, user: str, status: str) -> None:
        with self._lock, self._conn() as db:
            db.execute("UPDATE pending SET status=?, resolved=? WHERE id=? AND user=?", (status, time.time(), int(pid), user))


class HeadlessApprover(Approver):
    """For unattended runs: grants decided at schedule time; irreversible -> queue."""

    def __init__(self, grants: set[str], pending: PendingApprovals):
        self.grants = set(grants)
        self.pending = pending
        self.queued: list[int] = []

    def approve(self, req: ActionRequest) -> bool:
        return req.tool in self.grants and not req.tainted and not req.needs_fresh

    def confirm(self, req: ActionRequest) -> str | None:
        self.queued.append(self.pending.add(req))
        return None


class PermissionGate:
    def __init__(self, approver: Approver, audit: AuditLog):
        self.approver = approver
        self.audit = audit

    def _audit(self, event: str, **fields: Any) -> bool:
        try:
            self.audit.record(event, **fields)
            return True
        except AuditError as exc:
            print(f"[mind] AUDIT FAILURE: {exc}", file=sys.stderr)
            return False

    @staticmethod
    def _clip(args: dict[str, Any], limit: int = 200) -> dict[str, Any]:
        """Audit what was asked without copying whole documents/code into the log."""
        out = {}
        for k, v in args.items():
            sv = v if isinstance(v, (int, float, bool)) or v is None else str(v)
            if isinstance(sv, str) and len(sv) > limit:
                import hashlib
                sv = sv[:limit] + f"...[{len(sv)} chars, sha256 {hashlib.sha256(sv.encode()).hexdigest()[:12]}]"
            out[k] = sv
        return out

    def _egress(self, req: ActionRequest) -> Decision:
        """MC2: allowlist-only, suspended under taint, memory contents only with a fresh approval."""
        if req.tainted:
            return Decision(False, f"egress suspended: this task read untrusted content ({req.tainted}); nothing leaves "
                                   f"the device for the rest of the task")
        off = [d for d in req.destinations if d not in req.allowlist]
        if off:
            return Decision(False, f"egress to {', '.join(off)} is not on the allowlist (MIND_EGRESS_ALLOW)")
        if req.needs_fresh:
            try:
                ok = bool(self.approver.approve(req))
            except Exception as exc:  # noqa: BLE001
                return Decision(False, f"approver error: {exc}")
            return Decision(ok, "fresh approval for egress carrying memory" if ok else
                            f"egress would carry stored memory ({req.carries_memory}); needs a fresh human approval")
        return Decision(True, f"egress to allowlisted {', '.join(req.destinations)}")

    def authorize(self, req: ActionRequest) -> Decision:
        base = dict(user=req.user, tool=req.tool, tier=req.tier.name, args=self._clip(req.args),
                    task_id=req.task_id, headless=req.headless)
        if req.destinations:
            base["destinations"] = list(req.destinations)
        if not self._audit("permission.request", **base) and req.tier > Tier.READ:
            return Decision(False, "audit log unavailable; state-changing actions are disabled (fail-closed)")
        if req.tier == Tier.EGRESS and req.destinations:
            decision = self._egress(req)
        elif req.tier == Tier.READ:
            decision = Decision(True, "read-only: allowed")
        elif req.tier in (Tier.WRITE, Tier.EGRESS):
            try:
                ok = bool(self.approver.approve(req))
            except Exception as exc:  # a broken approver must deny, never allow
                ok, why = False, f"approver error: {exc}"
            else:
                why = "approved" if ok else ("not granted for this headless job" if req.headless else "user declined")
            decision = Decision(ok, why)
        else:
            before = len(getattr(self.approver, "queued", []))
            try:
                phrase = self.approver.confirm(req)
            except Exception as exc:
                phrase, err = None, str(exc)
            else:
                err = ""
            queued = getattr(self.approver, "queued", [])
            pending_id = queued[-1] if len(queued) > before else None
            if phrase is not None and phrase == req.confirmation_phrase:
                decision = Decision(True, "explicitly confirmed")
            elif pending_id is not None:
                decision = Decision(False, f"irreversible action queued for your confirmation (pending #{pending_id}); "
                                           f"headless runs never perform irreversible actions", pending_id)
            elif phrase is not None:
                decision = Decision(False, "confirmation phrase did not match; cancelled")
            else:
                decision = Decision(False, "not confirmed" + (f" ({err})" if err else ""))
        if not self._audit("permission.decision", **base, allowed=decision.allowed,
                           reason=decision.reason) and req.tier > Tier.READ:
            return Decision(False, "audit log unavailable; state-changing actions are disabled (fail-closed)")
        return decision
