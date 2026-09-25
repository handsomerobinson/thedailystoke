"""A real LLM provider using stdlib urllib only (no SDK dependency).

Decision: this hits the Anthropic Messages API directly over urllib so the
project has zero third-party runtime dependencies; it is entirely optional
and only activates when ANTHROPIC_API_KEY is set.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import List

from .base import LLMProvider, LLMResponse

API_URL = "https://api.anthropic.com/v1/messages"
DEFAULT_MODEL = "claude-3-5-haiku-20241022"

# Decision: rough published per-token pricing used only to produce a cost
# estimate for the cost-cap machinery; not billing-accurate.
_PRICE_PER_1K_INPUT = 0.0008
_PRICE_PER_1K_OUTPUT = 0.004


class AnthropicProvider(LLMProvider):
    name = "anthropic"

    def __init__(self, api_key: str | None = None, model: str = DEFAULT_MODEL, timeout: float = 20.0):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        self.model = model
        self.timeout = timeout

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def complete(self, system: str, messages: List[dict], max_tokens: int = 512) -> LLMResponse:
        if not self.is_configured():
            raise RuntimeError(
                "AnthropicProvider is not configured: set ANTHROPIC_API_KEY "
                "or use MockProvider for the zero-key path."
            )

        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "system": system,
            "messages": [{"role": m["role"], "content": m["content"]} for m in messages],
        }
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            API_URL,
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Anthropic API error {e.code}: {detail}") from e
        except urllib.error.URLError as e:
            raise RuntimeError(f"Anthropic API unreachable: {e}") from e

        text_parts = [b.get("text", "") for b in raw.get("content", []) if b.get("type") == "text"]
        text = "".join(text_parts)
        usage = raw.get("usage", {})
        in_tok = usage.get("input_tokens", 0)
        out_tok = usage.get("output_tokens", 0)
        cost = (in_tok / 1000.0) * _PRICE_PER_1K_INPUT + (out_tok / 1000.0) * _PRICE_PER_1K_OUTPUT
        return LLMResponse(text=text, cost_usd=cost, input_tokens=in_tok, output_tokens=out_tok, raw=raw)
