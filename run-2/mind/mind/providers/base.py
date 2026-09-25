"""The one provider interface every LLM brain plugs into.

Decision: providers are synchronous and stateless (system + messages in,
LLMResponse out) so the agent loop never needs to know which brain it is
talking to — mock, Anthropic, or anything else implementing this ABC.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class LLMResponse:
    text: str
    # Decision: providers self-report a cost estimate in USD (0.0 for the
    # mock) so the cost-cap machinery works identically regardless of brain.
    cost_usd: float = 0.0
    input_tokens: int = 0
    output_tokens: int = 0
    raw: Optional[dict] = field(default=None, repr=False)


class LLMProvider(ABC):
    """Minimal chat-completion interface. One system prompt, a list of
    (role, content) messages, and a max token hint — that's the whole
    surface every brain must support."""

    name: str = "base"

    @abstractmethod
    def complete(
        self,
        system: str,
        messages: List[dict],
        max_tokens: int = 512,
    ) -> LLMResponse:
        """messages: list of {"role": "user"|"assistant", "content": str}."""
        raise NotImplementedError

    def is_configured(self) -> bool:
        """Whether this provider has what it needs (e.g. an API key) to run
        for real. The agent uses this for graceful degradation."""
        return True
