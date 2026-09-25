"""Provider factory. The ONE place that decides which brain is rented."""
from __future__ import annotations

from ..util import Clock
from .anthropic import AnthropicProvider
from .base import LLMResponse, Provider, ProviderError, ToolCall, ToolSpec, Usage
from .mock import MockBrain
from .openai import OpenAIProvider
from .resilient import ResilientProvider

__all__ = ["Provider", "ProviderError", "LLMResponse", "ToolCall", "ToolSpec", "Usage", "MockBrain",
           "AnthropicProvider", "OpenAIProvider", "ResilientProvider", "make_provider", "make_single"]


def make_single(spec: str, config, model: str | None = None) -> Provider:
    """`spec` is "name" or "name:model" (e.g. "openai:some-model" for a fallback)."""
    spec = (spec or "mock").strip()
    name, _, spec_model = spec.partition(":")
    name = name.lower()
    model = spec_model or (config.model if model is None else model)
    if name == "mock":
        return MockBrain(price=(config.mock_price_in_per_mtok, config.mock_price_out_per_mtok))
    if name == "anthropic":
        return AnthropicProvider(model=model)
    if name == "openai":
        return OpenAIProvider(model=model)
    raise ProviderError(f"unknown provider {name!r} (expected mock|anthropic|openai)")


def make_provider(config, clock: Clock | None = None) -> ResilientProvider:
    """Build primary + fallbacks, wrapped in retry/circuit-breaker.

    A misconfigured real provider raises ProviderError here — we never silently substitute
    the mock for a brain the user asked for.
    """
    chain = [make_single(config.provider, config)]
    for fb in config.fallback_providers:
        chain.append(make_single(fb, config, model=""))
    return ResilientProvider(chain, clock=clock)
