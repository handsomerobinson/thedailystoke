"""The single provider interface every brain implements."""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from abc import ABC, abstractmethod
from typing import Callable

from ..types import BrainResponse, Message, ToolSpec


class ProviderError(Exception):
    def __init__(self, message: str, transient: bool = False, status: int | None = None):
        super().__init__(message)
        self.transient = transient
        self.status = status


class Brain(ABC):
    """Rented intelligence.  Implementations must be stateless per call."""

    name: str = "brain"
    model: str = "unknown"

    @abstractmethod
    def complete(self, system: str, messages: list[Message], tools: list[ToolSpec],
                 max_tokens: int = 1024) -> BrainResponse:
        """Return the next assistant turn: text and/or tool calls, with token usage."""


# (url, headers, body) -> (status, body)
Transport = Callable[[str, dict, bytes, float], tuple[int, bytes]]


def urllib_transport(url: str, headers: dict, body: bytes, timeout: float) -> tuple[int, bytes]:
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310 - fixed https endpoints
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise ProviderError(f"network error: {exc}", transient=True) from exc


def post_json(transport: Transport, url: str, headers: dict, payload: dict, timeout: float) -> dict:
    status, raw = transport(url, {"Content-Type": "application/json", **headers}, json.dumps(payload).encode(), timeout)
    if status >= 400:
        transient = status in (408, 409, 425, 429) or status >= 500
        raise ProviderError(f"HTTP {status}: {raw[:300].decode('utf-8', 'replace')}", transient=transient, status=status)
    try:
        return json.loads(raw)
    except ValueError as exc:
        raise ProviderError(f"invalid JSON from provider: {raw[:200]!r}", transient=True) from exc
