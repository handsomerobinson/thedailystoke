"""Purpose binding (MC8): every stored record carries purpose[], source and policy_version.

A record may be used only for a purpose it lists.  POLICY_VERSION names the rules in force when it was written, so a
later policy change cannot silently re-purpose old records (they keep the version they were written under).
"""
from __future__ import annotations

POLICY_VERSION = "mind-policy/2026-09-v3"

# Default purposes by memory kind.  A caller may narrow them; nothing widens them after the fact.
KIND_PURPOSE: dict[str, list[str]] = {
    "fact": ["personalisation"],        # things the user asked the mind to remember about them
    "episode": ["task-history"],        # one-line outcome of a task; ephemeral (MC1: 30 days)
    "reflection": ["self-improvement"], # lessons from failures, re-read before retries
    "note": ["user-notes"],
}
PURPOSES = {"personalisation", "task-history", "self-improvement", "user-notes", "charter", "accountability",
            "approval-queue", "scheduling"}
