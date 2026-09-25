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
from .circles import CircleStore
from .crypto import make_cipher
from .tiers import TierRegistry
from .trust import SoftAuthenticator, Trust
from .util import safe_user_id


class Runtime:
    def __init__(self, settings: Settings | None = None, brain=None, brain_desc: str | None = None,
                 trust: Trust | None = None, authenticator=None):
        self.settings = settings or Settings()
        if brain is None:
            brain, brain_desc = make_brain()
        self.brain = brain
        self.brain_desc = brain_desc or getattr(brain, "name", "custom")
        # The trust root lives outside the data dir: keys, credentials, the anchor, the signed tier registry.
        self.trust = trust or Trust(self.settings.trust_dir)
        # TEST DOUBLE for WebAuthn (see trust.py).  A real deployment passes a passkey-backed Authenticator.
        self.authenticator = authenticator or SoftAuthenticator(self.trust)
        self.tiers = TierRegistry(self.trust)
        self.audit = AuditLog(self.settings.audit_path, anchor=self.trust.anchor, stream="audit")
        # MC6: fail at startup, never downgrade silently, if encrypted mode is required but unavailable.
        make_cipher(self.settings.encryption, b"\0" * 32, b"\0" * 32) if self.settings.encryption != "off" else None
        self.pending = PendingApprovals(self.settings.approvals_db)
        self.outbox = Outbox(self.settings)
        self.ledger = SpendLedger(self.settings.spend_db)
        self._memories: dict[str, MemoryStore] = {}
        self._charters: dict[str, CharterStore] = {}
        self._guards: dict[str, LoyaltyGuard] = {}
        self._circles: dict[str, CircleStore] = {}
        self.operator_system: str | None = None  # an operator-supplied system instruction (attack-2 vector); screened
        self.scheduler = None  # attached by Scheduler when present

    def cipher(self, user_id: str):
        """MC6: per-user data key held in the trust dir (stand-in for a key derived on the user's device)."""
        uid = safe_user_id(user_id)
        if self.settings.encryption == "off":
            return make_cipher("off")
        return make_cipher(self.settings.encryption, self.trust.secrets.get(f"user-data-{uid}"),
                           self.trust.secrets.get(f"user-tag-{uid}"))

    def memory(self, user_id: str) -> MemoryStore:
        if user_id not in self._memories:
            self._memories[user_id] = MemoryStore(self.settings.data_dir, user_id, cipher=self.cipher(user_id),
                                                  episode_ttl_days=self.settings.episode_ttl_days)
        return self._memories[user_id]

    def charter(self, user_id: str) -> CharterStore:
        if user_id not in self._charters:
            self._charters[user_id] = CharterStore(self.settings.data_dir, user_id, self.audit,
                                                   removal_cooldown_s=self.settings.charter_removal_cooldown_s,
                                                   trust=self.trust, profile=self.settings.profile)
        return self._charters[user_id]

    def circles(self, user_id: str) -> CircleStore:
        if user_id not in self._circles:
            self._circles[user_id] = CircleStore(self.settings.data_dir, user_id)
        return self._circles[user_id]

    def assertion(self, party: str, challenge: bytes):
        """Enrol `party` on the (test-double) authenticator if needed and sign `challenge` as them."""
        self.authenticator.enroll(party)
        return self.authenticator.get_assertion(party, challenge)

    def guard(self, user_id: str) -> LoyaltyGuard:
        return self._guards.setdefault(user_id, LoyaltyGuard())

    def registry(self, approver: Approver):
        return default_registry(PermissionGate(approver, self.audit), self.audit, self.settings.tool_output_cap, self.tiers)

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
                     charter=charter, guard=self.guard(user_id), operator_system=self.operator_system,
                     profile=self.settings.profile)

    def close(self) -> None:
        for m in self._memories.values():
            m.close()
        self._memories.clear()
        for c in self._charters.values():
            c.close()
        self._charters.clear()
        for c in self._circles.values():
            c.close()
        self._circles.clear()


class _BrokenCharter:
    """Stands in for a charter store that could not be opened: load() raises, so the agent fails closed."""

    def __init__(self, exc: Exception):
        self.exc = exc

    def load(self):
        raise self.exc

    def mark_disclosed(self, state) -> None:
        pass
