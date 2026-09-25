"""Provider-neutral message and response types."""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any


def new_id(prefix: str = "") -> str:
    return prefix + uuid.uuid4().hex[:12]


@dataclass
class ToolCall:
    name: str
    args: dict[str, Any]
    id: str = field(default_factory=lambda: new_id("call_"))


@dataclass
class Message:
    """One conversation turn.

    role is one of: "user", "assistant", "tool".  (System text is passed to the
    brain separately, because providers disagree on where it goes.)
    """

    role: str
    content: str = ""
    tool_calls: list[ToolCall] = field(default_factory=list)
    tool_call_id: str | None = None
    name: str | None = None  # tool name for role == "tool"


@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0

    def __add__(self, other: "Usage") -> "Usage":
        return Usage(self.input_tokens + other.input_tokens,
                     self.output_tokens + other.output_tokens)


@dataclass
class BrainResponse:
    text: str
    tool_calls: list[ToolCall] = field(default_factory=list)
    usage: Usage = field(default_factory=Usage)
    model: str = "unknown"
    stop_reason: str = "end_turn"
    provider: str = "unknown"


@dataclass
class ToolSpec:
    """What the brain is told about a tool."""

    name: str
    description: str
    parameters: dict[str, Any]
