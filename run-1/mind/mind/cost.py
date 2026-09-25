"""Cost accounting and hard spending caps.

A `Budget` is attached to one task (all of its trials, tool loops and reflections).
Before every LLM call the agent asks `budget.preflight(...)` with a *worst-case* estimate
(estimated input tokens + the full max_tokens of output at list price). If that worst case
would exceed the remaining budget the call is refused before any money is spent.
After the call, the real usage reported by the provider is recorded.

Prices are USD per million tokens. The table is a cached snapshot (2026-06) and can be
overridden; unknown models are priced at a deliberately high default so a missing entry
makes caps trip *earlier*, never later.
"""
from __future__ import annotations

import threading
from dataclasses import dataclass, field

# (input $/MTok, output $/MTok)
PRICING: dict[str, tuple[float, float]] = {
    "claude-opus-5": (5.00, 25.00),
    "claude-opus-5-5": (4.00, 20.00),
    "claude-sonnet-5": (2.00, 10.00),
    "claude-haiku-4-5": (1.00, 5.00),
    "claude-fable-5-1": (10.00, 50.00),
    "mock-brain": (0.0, 0.0),
}
UNKNOWN_MODEL_PRICE = (15.00, 75.00)


def price_for(model: str, overrides: dict | None = None) -> tuple[float, float]:
    if overrides and model in overrides:
        return overrides[model]
    return PRICING.get(model, UNKNOWN_MODEL_PRICE)


def cost_usd(input_tokens: int, output_tokens: int, price: tuple[float, float]) -> float:
    return (input_tokens * price[0] + output_tokens * price[1]) / 1_000_000


class BudgetExceeded(Exception):
    """Raised when a call would (or did) exceed a spending cap."""


@dataclass
class Budget:
    limit_usd: float
    spent_usd: float = 0.0
    calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    label: str = "task"
    on_spend: object = None  # optional callback(usd) e.g. daily ledger
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    @property
    def remaining_usd(self) -> float:
        return max(0.0, self.limit_usd - self.spent_usd)

    def preflight(self, est_input_tokens: int, max_output_tokens: int, price: tuple[float, float]) -> float:
        worst = cost_usd(est_input_tokens, max_output_tokens, price)
        if self.spent_usd + worst > self.limit_usd + 1e-12:
            raise BudgetExceeded(
                f"{self.label} budget: worst-case next call ${worst:.4f} would exceed remaining "
                f"${self.remaining_usd:.4f} of ${self.limit_usd:.2f}"
            )
        return worst

    def record(self, input_tokens: int, output_tokens: int, price: tuple[float, float]) -> float:
        usd = cost_usd(input_tokens, output_tokens, price)
        with self._lock:
            self.spent_usd += usd
            self.calls += 1
            self.input_tokens += input_tokens
            self.output_tokens += output_tokens
        if callable(self.on_spend):
            try:
                self.on_spend(usd)
            except Exception:  # ledger failure must not crash the loop
                pass
        return usd

    def summary(self) -> dict:
        return {
            "limit_usd": round(self.limit_usd, 6),
            "spent_usd": round(self.spent_usd, 6),
            "calls": self.calls,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
        }
