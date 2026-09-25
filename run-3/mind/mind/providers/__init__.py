"""Brain providers and the factory that picks one from the environment."""
from __future__ import annotations

import os
import sys

from .anthropic import AnthropicBrain
from .base import Brain, ProviderError
from .mock import MockBrain
from .openai_compat import OpenAICompatBrain
from .resilient import AllBrainsFailed, ResilientBrain

__all__ = ["Brain", "ProviderError", "MockBrain", "AnthropicBrain", "OpenAICompatBrain",
           "ResilientBrain", "AllBrainsFailed", "make_brain"]


def make_brain(provider: str | None = None, strict: bool = False, warn=lambda s: print(s, file=sys.stderr)) -> tuple[Brain, str]:
    """Build the configured brain chain. Returns (brain, human-readable description).

    MIND_PROVIDER: mock (default) | anthropic | openai | a comma list for a
    fallback chain, e.g. "anthropic,openai".  A provider whose key is missing
    is skipped with a loud warning; if none remain the mock is used (unless
    strict=True), and the description says DEGRADED so nobody mistakes mock
    output for a real model's.
    """
    spec = (provider or os.environ.get("MIND_PROVIDER", "mock")).lower()
    chain: list[Brain] = []
    notes: list[str] = []
    for name in [s.strip() for s in spec.split(",") if s.strip()]:
        try:
            if name == "mock":
                chain.append(MockBrain())
            elif name == "anthropic":
                chain.append(AnthropicBrain())
            elif name in ("openai", "openai-compat"):
                chain.append(OpenAICompatBrain())
            else:
                notes.append(f"unknown provider {name!r}")
        except ProviderError as exc:
            notes.append(f"{name}: {exc}")
    if not chain:
        if strict:
            raise ProviderError("no usable provider: " + "; ".join(notes))
        warn("[mind] DEGRADED: no usable LLM provider (" + "; ".join(notes) + ") - using the scripted MockBrain")
        return ResilientBrain([MockBrain()]), "mock (DEGRADED fallback)"
    for n in notes:
        warn(f"[mind] warning: {n}")
    desc = " -> ".join(f"{b.name}:{b.model}" for b in chain)
    return ResilientBrain(chain), desc
