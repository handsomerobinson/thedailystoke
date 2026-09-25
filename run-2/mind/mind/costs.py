"""Per-task cost tracking and hard caps so a runaway reflection loop cannot
spend unbounded money.

Decision: the cap is enforced *before* spending, not after — CostTracker
raises the moment a proposed spend would exceed the cap, rather than
letting it through and complaining afterward.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from . import config


class CostCapExceeded(RuntimeError):
    pass


@dataclass
class CostTracker:
    cap_usd: float = config.DEFAULT_TASK_COST_CAP_USD
    spent_usd: float = 0.0
    _log: list = field(default_factory=list)

    def remaining(self) -> float:
        return max(0.0, self.cap_usd - self.spent_usd)

    def would_exceed(self, amount_usd: float) -> bool:
        return (self.spent_usd + amount_usd) > self.cap_usd + 1e-9

    def charge(self, amount_usd: float, reason: str = "") -> None:
        if amount_usd < 0:
            raise ValueError("cost must be non-negative")
        if self.would_exceed(amount_usd):
            raise CostCapExceeded(
                f"charging ${amount_usd:.4f} for {reason!r} would exceed the "
                f"${self.cap_usd:.2f} task cap (already spent ${self.spent_usd:.4f})"
            )
        self.spent_usd += amount_usd
        self._log.append((reason, amount_usd))

    def history(self):
        return list(self._log)
