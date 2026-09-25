"""Retry with exponential backoff + ordered fallback + per-provider circuit breaker.

No single provider is a single point of failure: if the primary keeps failing, its breaker
opens for `cooldown_s` and calls go straight to the next provider in the chain. If every
provider is down the caller gets one ProviderError (the agent turns that into a graceful
"brain unavailable" result; it never silently switches to the mock).
"""
from __future__ import annotations

from dataclasses import dataclass

from ..util import Clock
from .base import LLMResponse, Provider, ProviderError


@dataclass
class _Breaker:
    failures: int = 0
    open_until: float = 0.0


class ResilientProvider(Provider):
    name = "resilient"

    def __init__(self, chain: list[Provider], retries: int = 2, backoff_s: float = 0.5,
                 breaker_threshold: int = 3, cooldown_s: float = 60.0, clock: Clock | None = None):
        if not chain:
            raise ValueError("ResilientProvider needs at least one provider")
        self.chain = chain
        self.retries = retries
        self.backoff_s = backoff_s
        self.breaker_threshold = breaker_threshold
        self.cooldown_s = cooldown_s
        self.clock = clock or Clock()
        self._breakers = {id(p): _Breaker() for p in chain}
        self.last_provider: Provider = chain[0]
        self.events: list[str] = []  # human-readable log of retries/fallbacks (for reports/tests)

    @property
    def model(self) -> str:  # type: ignore[override]
        return self.last_provider.model

    def price(self) -> tuple[float, float]:
        return self.last_provider.price()

    def preflight_price(self) -> tuple[float, float]:
        # worst case: the MOST expensive provider in the chain might be the one that answers
        prices = [p.price() for p in self.chain]
        return (max(p[0] for p in prices), max(p[1] for p in prices))

    def billed_price(self) -> tuple[float, float]:
        return self.last_provider.price()

    def describe(self) -> str:
        return " -> ".join(p.describe() for p in self.chain)

    def complete(self, system, messages, tools, max_tokens=1024) -> LLMResponse:
        errors = []
        for p in self.chain:
            br = self._breakers[id(p)]
            now = self.clock.now()
            if br.open_until > now:
                errors.append(f"{p.describe()}: circuit open")
                continue
            for attempt in range(self.retries + 1):
                try:
                    resp = p.complete(system, messages, tools, max_tokens)
                    br.failures = 0
                    self.last_provider = p
                    resp.provider = resp.provider or p.name
                    return resp
                except ProviderError as e:
                    errors.append(f"{p.describe()} attempt {attempt + 1}: {e}")
                    self.events.append(errors[-1])
                    if not e.retryable:
                        break
                    if attempt < self.retries:
                        self.clock.sleep(self.backoff_s * (2 ** attempt))
                except Exception as e:  # a buggy provider must not crash the loop
                    errors.append(f"{p.describe()} attempt {attempt + 1}: unexpected {type(e).__name__}: {e}")
                    self.events.append(errors[-1])
                    break
            br.failures += 1
            if br.failures >= self.breaker_threshold:
                br.open_until = self.clock.now() + self.cooldown_s
                self.events.append(f"circuit opened for {p.describe()} ({self.cooldown_s:.0f}s)")
            if len(self.chain) > 1:
                self.events.append(f"falling back from {p.describe()}")
        raise ProviderError("all providers failed: " + " | ".join(errors[-6:]), retryable=False)
