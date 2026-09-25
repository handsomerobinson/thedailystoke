"""Wiring: one place that assembles brain + memory + tools + gate + audit for a user."""
from __future__ import annotations

import sys

from .agent import Agent
from .audit import AuditLog
from .charter import CharterStore
from .guard import LoyaltyGuard
from .config import Settings
from .cost import SpendLedger
from .memory import MemoryStore
from .permissions import Approver, DenyAllApprover, PendingApprovals, PermissionGate
from .providers import make_brain
from .reporting import Outbox
from .tools import default_registry
from .util import safe_user_id


class Runtime:
    def __init__(self, settings: Settings | None = None, brain=None, brain_desc: str | None = None):
        self.settings = settings or Settings()
        if brain is None:
            brain, brain_desc = make_brain()
        self.brain = brain
        self.brain_desc = brain_desc or getattr(brain, "name", "custom")
        self.audit = AuditLog(self.settings.audit_path)
        self.pending = PendingApprovals(self.settings.approvals_db)
        self.outbox = Outbox(self.settings)
        self.ledger = SpendLedger(self.settings.spend_db)
        self._memories: dict[str, MemoryStore] = {}
        self._charters: dict[str, CharterStore] = {}
        self._guards: dict[str, LoyaltyGuard] = {}
        self.operator_system: str | None = None  # an operator-supplied system instruction (attack-2 vector); screened
        self.scheduler = None  # attached by Scheduler when present

    def memory(self, user_id: str) -> MemoryStore:
        if user_id not in self._memories:
            self._memories[user_id] = MemoryStore(self.settings.data_dir, user_id)
        return self._memories[user_id]

    def charter(self, user_id: str) -> CharterStore:
        if user_id not in self._charters:
            self._charters[user_id] = CharterStore(self.settings.data_dir, user_id, self.audit,
                                                   removal_cooldown_s=self.settings.charter_removal_cooldown_s)
        return self._charters[user_id]

    def guard(self, user_id: str) -> LoyaltyGuard:
        return self._guards.setdefault(user_id, LoyaltyGuard())

    def registry(self, approver: Approver):
        return default_registry(PermissionGate(approver, self.audit), self.audit, self.settings.tool_output_cap)

    def agent(self, user_id: str, approver: Approver | None = None, log=None) -> Agent:
        approver = approver or DenyAllApprover()
        safe_user_id(user_id)
        try:
            memory = self.memory(user_id)
        except Exception as exc:  # corrupt/locked DB: run without memory rather than not at all
            print(f"[mind] DEGRADED: memory unavailable for {user_id}: {exc}", file=sys.stderr)
            memory = None
        try:
            charter = self.charter(user_id)
        except Exception as exc:  # noqa: BLE001 - the agent will treat a missing store as an integrity failure
            print(f"[mind] CHARTER UNAVAILABLE for {user_id}: {exc}", file=sys.stderr)
            charter = _BrokenCharter(exc)
        return Agent(user_id, self.brain, self.registry(approver), memory, self.audit,
                     self.settings, scheduler=self.scheduler, notifier=self.outbox, log=log, ledger=self.ledger,
                     charter=charter, guard=self.guard(user_id), operator_system=self.operator_system)

    def close(self) -> None:
        for m in self._memories.values():
            m.close()
        self._memories.clear()
        for c in self._charters.values():
            c.close()
        self._charters.clear()


class _BrokenCharter:
    """Stands in for a charter store that could not be opened: load() raises, so the agent fails closed."""

    def __init__(self, exc: Exception):
        self.exc = exc

    def load(self):
        raise self.exc

    def mark_disclosed(self, state) -> None:
        pass
