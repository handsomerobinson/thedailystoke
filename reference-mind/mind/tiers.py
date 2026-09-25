"""Signed tool-tier registry (MC3): a tool's tier comes from here, never from the tool.

  * SIGNED_TIERS is the reviewed source of truth in code.  On first use it is installed into the trust dir as
    tiers.json with a MAC under a trust-dir key (the reference's stand-in for a release signature; a production
    build ships the manifest signed with the release key and verifies it with a pinned public key).
  * A tool that is not in the verified manifest is IRREVERSIBLE (it needs the typed phrase, and never runs headless).
  * If the manifest fails verification (edited on disk), EVERY tool is IRREVERSIBLE until it is re-installed: fail
    closed, never fail open to the tools' own declarations.
  * A tool whose declared tier differs from the signed one runs at the signed tier and the mismatch is reported.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from .permissions import Tier
from .purpose import POLICY_VERSION

SIGNED_TIERS: dict[str, str] = {
    "calculator": "READ",
    "clock": "READ",
    "recall": "READ",
    "note_read": "READ",
    "note_list": "READ",
    "note_search": "READ",
    "circle_list": "READ",
    "circle_read": "READ",
    "remember": "WRITE",
    "python_exec": "WRITE",
    "schedule_job": "WRITE",
    "note_write": "WRITE",
    "schedule_reminder": "WRITE",
    "send_report": "EGRESS",   # outbox is local; the optional webhook sends bytes off the device
    "web_search": "EGRESS",    # the query leaves the device (MC2: READ-tier web tools were the bug in all 3 runs)
    "web_fetch": "EGRESS",
    "note_delete": "IRREVERSIBLE",
}


class TierRegistry:
    KEY = "tier-registry"

    def __init__(self, trust=None, tiers: dict[str, str] | None = None):
        """trust=None: an in-process registry built from code (tests, harnesses) - nothing on disk to tamper with.
        With a Trust: load and verify <trust dir>/tiers.json, installing it from SIGNED_TIERS on first use."""
        self.trust = trust
        self.problem = ""
        self.source = "code"
        self._tiers: dict[str, Tier] = {}
        wanted = dict(SIGNED_TIERS if tiers is None else tiers)
        if trust is None:
            self._tiers = {k: Tier[v] for k, v in wanted.items()}
            return
        self.path = Path(trust.dir) / "tiers.json"
        if not self.path.exists():
            self.install(wanted)
        self._load()

    def install(self, tiers: dict[str, str]) -> None:
        body = {"tiers": dict(sorted(tiers.items())), "policy_version": POLICY_VERSION}
        doc = {**body, "mac": self.trust.mac(self.KEY, body)}
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(doc, indent=1, sort_keys=True), encoding="utf-8")
        os.replace(tmp, self.path)

    def _load(self) -> None:
        try:
            doc = json.loads(self.path.read_text(encoding="utf-8"))
            body = {"tiers": doc["tiers"], "policy_version": doc["policy_version"]}
            if not self.trust.mac_ok(self.KEY, body, doc.get("mac", "")):
                raise ValueError("signature does not verify")
            self._tiers = {k: Tier[v] for k, v in body["tiers"].items()}
            self.source = f"signed manifest {self.path.name}"
        except (OSError, ValueError, KeyError, TypeError) as exc:
            self._tiers = {}
            self.problem = f"tier registry failed verification ({exc}); every tool is IRREVERSIBLE until reinstalled"

    def declared(self, name: str) -> bool:
        return name in self._tiers

    def tier_of(self, name: str) -> Tier:
        return self._tiers.get(name, Tier.IRREVERSIBLE)

    def status(self) -> str:
        return self.problem or f"{len(self._tiers)} tools declared ({self.source}); undeclared tools are IRREVERSIBLE"
