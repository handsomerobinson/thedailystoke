"""Permission tiers and an approval gate for tool calls.

Decision: three tiers — READ_ONLY runs free, STATE_CHANGING requires an
approval callback to say yes, IRREVERSIBLE requires an explicit separate
confirmation phrase (not just a yes/no) so it cannot be approved by
accident. Every decision (granted or denied) is handed to the audit log by
the caller (agent.py), not by this module, so permissions stays a pure
policy component with no I/O side effects of its own.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional

IRREVERSIBLE_CONFIRM_PHRASE = "CONFIRM IRREVERSIBLE"


class PermissionTier(str, Enum):
    READ_ONLY = "read_only"
    STATE_CHANGING = "state_changing"
    IRREVERSIBLE = "irreversible"


# Decision: an approver is just Callable[[str, PermissionTier], bool] —
# in the demo it auto-approves state-changing and auto-denies irreversible
# (headless-safe default); a real UI/CLI can swap in a prompt-the-human
# callable without touching agent.py.
Approver = Callable[[str, PermissionTier], bool]


def auto_approver(state_changing_ok: bool = True, irreversible_ok: bool = False) -> Approver:
    def approve(action_desc: str, tier: PermissionTier) -> bool:
        if tier == PermissionTier.READ_ONLY:
            return True
        if tier == PermissionTier.STATE_CHANGING:
            return state_changing_ok
        if tier == PermissionTier.IRREVERSIBLE:
            return irreversible_ok
        return False

    return approve


def cli_approver() -> Approver:
    """Prompts on stdin. Not used by the automated demo/tests (they run
    headless) but available for interactive use."""

    def approve(action_desc: str, tier: PermissionTier) -> bool:
        if tier == PermissionTier.READ_ONLY:
            return True
        if tier == PermissionTier.IRREVERSIBLE:
            resp = input(
                f"[IRREVERSIBLE] {action_desc}\nType '{IRREVERSIBLE_CONFIRM_PHRASE}' to proceed: "
            )
            return resp.strip() == IRREVERSIBLE_CONFIRM_PHRASE
        resp = input(f"[approval needed] {action_desc} — allow? [y/N]: ")
        return resp.strip().lower() in ("y", "yes")

    return approve


@dataclass
class PermissionDecision:
    granted: bool
    tier: PermissionTier
    reason: str
