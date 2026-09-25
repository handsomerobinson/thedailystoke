"""Per-task cost accounting and hard caps.

A Budget is created per task and shared by every brain call (acting,
reflecting, judging) and every tool call in that task, across all trials.
It is checked *before* each brain call using a worst-case estimate, so a
single call cannot overshoot the cap by more than the estimate error.

Prices are USD per million tokens.  They are configuration, not truth: the
defaults below are placeholders you must verify against your provider's
price sheet (override with MIND_PRICE_IN / MIND_PRICE_OUT).  The mock brain
is charged a *simulated* price so that caps are exercised in the demo.
"""
from __future__ import annotations

import datetime as _dt
import os
import sqlite3
import threading
import time
from pathlib import Path
from dataclasses import dataclass, field

from .types import Usage

# (input $/Mtok, output $/Mtok).  Placeholder values -- verify before relying on them.
DEFAULT_PRICES: dict[str, tuple[float, float]] = {
    "mock": (3.0, 15.0),         # simulated, so budgets bite in the demo
    "default": (3.0, 15.0),      # used for any unknown real model (conservative-ish)
}


def price_for(model: str) -> tuple[float, float]:
    env_in, env_out = os.environ.get("MIND_PRICE_IN"), os.environ.get("MIND_PRICE_OUT")
    if env_in and env_out:
        try:
            return float(env_in), float(env_out)
        except ValueError:
            pass
    for key, price in DEFAULT_PRICES.items():
        if key != "default" and model.startswith(key):
            return price
    return DEFAULT_PRICES["default"]


def cost_of(usage: Usage, model: str) -> float:
    pin, pout = price_for(model)
    return usage.input_tokens * pin / 1e6 + usage.output_tokens * pout / 1e6


class BudgetExceeded(Exception):
    """Raised when a task would exceed one of its caps."""

    def __init__(self, which: str, detail: str):
        super().__init__(f"budget exceeded ({which}): {detail}")
        self.which = which
        self.detail = detail


class SpendLedger:
    """Per-user, per-day spend across ALL tasks and jobs (SQLite, shared by processes).

    Per-task caps stop one runaway loop; the daily cap stops a runaway
    *schedule* (e.g. a job firing every minute) from adding up.
    """

    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        with sqlite3.connect(str(self.path), timeout=10) as db:
            db.execute("CREATE TABLE IF NOT EXISTS spend (user TEXT NOT NULL, day TEXT NOT NULL, "
                       "usd REAL NOT NULL DEFAULT 0, PRIMARY KEY(user, day))")

    @staticmethod
    def today() -> str:
        return _dt.date.today().isoformat()

    def add(self, user: str, usd: float) -> None:
        with self._lock, sqlite3.connect(str(self.path), timeout=10) as db:
            db.execute("INSERT INTO spend(user, day, usd) VALUES (?,?,?) "
                       "ON CONFLICT(user, day) DO UPDATE SET usd = usd + excluded.usd", (user, self.today(), usd))

    def spent_today(self, user: str) -> float:
        with sqlite3.connect(str(self.path), timeout=10) as db:
            row = db.execute("SELECT usd FROM spend WHERE user=? AND day=?", (user, self.today())).fetchone()
        return float(row[0]) if row else 0.0


@dataclass
class Budget:
    max_usd: float = 0.25
    max_tokens: int = 60000
    max_tool_calls: int = 30
    max_seconds: float = 300.0
    spent_usd: float = 0.0
    tokens: int = 0
    tool_calls: int = 0
    brain_calls: int = 0
    started: float = field(default_factory=time.monotonic)
    clock: object = field(default=time.monotonic, repr=False)
    ledger: SpendLedger | None = field(default=None, repr=False)
    user: str = ""
    daily_cap_usd: float | None = None

    # -- checks ------------------------------------------------------------
    def _check_time(self) -> None:
        elapsed = self.clock() - self.started  # type: ignore[operator]
        if elapsed > self.max_seconds:
            raise BudgetExceeded("time", f"{elapsed:.1f}s > {self.max_seconds}s")

    def check_brain_call(self, prompt_tokens: int, max_output_tokens: int, model: str) -> None:
        """Refuse a brain call whose worst case would break the caps."""
        self._check_time()
        worst = cost_of(Usage(prompt_tokens, max_output_tokens), model)
        if self.spent_usd + worst > self.max_usd:
            raise BudgetExceeded(
                "usd", f"spent ${self.spent_usd:.4f} + worst-case next call ${worst:.4f} > cap ${self.max_usd:.4f}")
        if self.ledger is not None and self.daily_cap_usd is not None:
            today = self.ledger.spent_today(self.user)
            if today + worst > self.daily_cap_usd:
                raise BudgetExceeded(
                    "daily", f"user {self.user!r} spent ${today:.4f} today; next call could exceed the daily cap ${self.daily_cap_usd:.2f}")
        if self.tokens + prompt_tokens + max_output_tokens > self.max_tokens:
            raise BudgetExceeded(
                "tokens", f"{self.tokens} + {prompt_tokens + max_output_tokens} > cap {self.max_tokens}")

    def check_tool_call(self) -> None:
        self._check_time()
        if self.tool_calls + 1 > self.max_tool_calls:
            raise BudgetExceeded("tool_calls", f"cap {self.max_tool_calls} reached")

    # -- charges -----------------------------------------------------------
    def charge_brain(self, usage: Usage, model: str) -> float:
        cost = cost_of(usage, model)
        self.spent_usd += cost
        self.tokens += usage.input_tokens + usage.output_tokens
        self.brain_calls += 1
        if self.ledger is not None:
            try:
                self.ledger.add(self.user, cost)
            except sqlite3.Error:
                pass  # the per-task cap still holds; ledger is an extra layer
        return cost

    def charge_tool(self) -> None:
        self.tool_calls += 1

    @property
    def remaining_usd(self) -> float:
        return max(0.0, self.max_usd - self.spent_usd)

    def summary(self) -> dict:
        return {
            "spent_usd": round(self.spent_usd, 6), "max_usd": self.max_usd,
            "tokens": self.tokens, "max_tokens": self.max_tokens,
            "brain_calls": self.brain_calls, "tool_calls": self.tool_calls,
        }
