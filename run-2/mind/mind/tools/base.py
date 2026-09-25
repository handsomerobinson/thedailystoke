"""The tool interface every hand plugs into.

Decision: a tool declares its own permission tier as a class attribute (not
decided per-call) — simpler mental model, and a rival can't "downgrade" a
dangerous tool's tier by constructing it differently.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from ..permissions import PermissionTier


@dataclass
class ToolResult:
    ok: bool
    output: str
    error: Optional[str] = None
    meta: Dict[str, Any] = field(default_factory=dict)
    truncated: bool = False


class Tool(ABC):
    name: str = "tool"
    tier: PermissionTier = PermissionTier.READ_ONLY
    description: str = ""

    @abstractmethod
    def run(self, **kwargs) -> ToolResult:
        raise NotImplementedError

    def describe_call(self, **kwargs) -> str:
        """Human-readable one-liner for approval prompts / audit log."""
        return f"{self.name}({kwargs})"
