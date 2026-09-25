"""Retry, backoff, circuit breaking and fallback across a chain of brains.

No single provider is a single point of failure: transient errors are
retried with exponential backoff + jitter; a provider that keeps failing is
"opened" (skipped) for a cooldown; the next brain in the chain is tried.
When every brain fails, AllBrainsFailed is raised and the agent ends the task
cleanly with status "brain_unavailable" -- it never pretends.
"""
from __future__ import annotations

import random
import time
from dataclasses import dataclass, field
from typing import Callable

from ..types import BrainResponse, Message, ToolSpec
from .base import Brain, ProviderError


class AllBrainsFailed(Exception):
    pass


@dataclass
class _Breaker:
    failures: int = 0
    open_until: float = 0.0


class ResilientBrain(Brain):
    name = "resilient"

    def __init__(self, brains: list[Brain], retries: int = 2, base_delay: float = 0.5,
                 failure_threshold: int = 3, cooldown: float = 60.0,
                 sleep: Callable[[float], None] = time.sleep, clock: Callable[[], float] = time.monotonic):
        if not brains:
            raise ValueError("need at least one brain")
        self.brains = brains
        self.retries = retries
        self.base_delay = base_delay
        self.failure_threshold = failure_threshold
        self.cooldown = cooldown
        self.sleep = sleep
        self.clock = clock
        self.breakers = {id(b): _Breaker() for b in brains}
        self.events: list[str] = []

    @property
    def model(self) -> str:  # type: ignore[override]
        return self.brains[0].model

    def complete(self, system: str, messages: list[Message], tools: list[ToolSpec], max_tokens: int = 1024) -> BrainResponse:
        errors = []
        for brain in self.brains:
            br = self.breakers[id(brain)]
            if br.open_until > self.clock():
                errors.append(f"{brain.name}: circuit open")
                continue
            for attempt in range(self.retries + 1):
                try:
                    resp = brain.complete(system, messages, tools, max_tokens)
                    br.failures = 0
                    return resp
                except ProviderError as exc:
                    errors.append(f"{brain.name}: {exc}")
                    self.events.append(f"{brain.name} attempt {attempt + 1} failed: {exc}")
                    if not exc.transient:
                        break
                    if attempt < self.retries:
                        self.sleep(self.base_delay * (2 ** attempt) * (0.5 + random.random()))
                except Exception as exc:  # adapter bug: treat as non-transient failure of this brain
                    errors.append(f"{brain.name}: {type(exc).__name__}: {exc}")
                    break
            br.failures += 1
            if br.failures >= self.failure_threshold:
                br.open_until = self.clock() + self.cooldown
                self.events.append(f"{brain.name} circuit opened for {self.cooldown}s")
            if brain is not self.brains[-1]:
                self.events.append(f"falling back from {brain.name}")
        raise AllBrainsFailed("; ".join(errors[-6:]))
