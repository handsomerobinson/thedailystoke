"""The single provider interface every brain (mock or real) implements.

Internal, provider-neutral message format (the agent only ever speaks this):
    {"role": "user", "content": str}
    {"role": "assistant", "content": str, "tool_calls": [{"id", "name", "arguments"}], "raw": <opaque>}
    {"role": "tool", "tool_call_id": str, "name": str, "content": str, "is_error": bool}
Each concrete provider converts to/from its vendor wire format.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "arguments": self.arguments}


@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0


@dataclass
class LLMResponse:
    text: str
    tool_calls: list[ToolCall] = field(default_factory=list)
    usage: Usage = field(default_factory=Usage)
    model: str = ""
    stop_reason: str = "end_turn"
    raw: Any = None          # provider-native assistant content, echoed back verbatim next turn
    provider: str = ""


@dataclass
class ToolSpec:
    name: str
    description: str
    parameters: dict  # JSON schema (object)


class ProviderError(Exception):
    def __init__(self, message: str, retryable: bool = False, status: int | None = None):
        super().__init__(message)
        self.retryable = retryable
        self.status = status


class Provider(ABC):
    name: str = "base"
    model: str = ""

    @abstractmethod
    def complete(self, system: str, messages: list[dict], tools: list[ToolSpec],
                 max_tokens: int = 1024) -> LLMResponse:
        ...

    def price(self) -> tuple[float, float]:
        from ..cost import price_for
        return price_for(self.model)

    def preflight_price(self) -> tuple[float, float]:
        """Price used for the worst-case pre-flight budget check."""
        return self.price()

    def billed_price(self) -> tuple[float, float]:
        """Price of the provider that actually answered the last call."""
        return self.price()

    def describe(self) -> str:
        return f"{self.name}:{self.model}"


# ---- HTTP transport (injectable so real providers are testable without keys) -------------

Transport = Callable[[str, dict, bytes, float], tuple[int, bytes]]


def urllib_transport(url: str, headers: dict, body: bytes, timeout: float) -> tuple[int, bytes]:
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310 (https only, fixed hosts)
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read() or b""
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise ProviderError(f"network error: {e}", retryable=True) from e


def classify_http_error(status: int, body: bytes) -> ProviderError:
    try:
        detail = json.loads(body.decode("utf-8", "replace"))
    except Exception:
        detail = body[:300].decode("utf-8", "replace")
    retryable = status in (408, 409, 425, 429, 500, 502, 503, 504, 529)
    return ProviderError(f"HTTP {status}: {str(detail)[:300]}", retryable=retryable, status=status)
