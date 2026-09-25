"""Anthropic Messages API over plain HTTPS (stdlib urllib). Off by default.

Enable with MIND_PROVIDER=anthropic and ANTHROPIC_API_KEY set. Model defaults to
claude-opus-5 (override with MIND_MODEL). Unit tests drive this through a fake transport;
it has NOT been exercised against the live API from this build environment (no key).
"""
from __future__ import annotations

import json
import math
import os

from .base import (LLMResponse, Provider, ProviderError, ToolCall, ToolSpec, Transport, Usage,
                   classify_http_error, urllib_transport)

API_URL = "https://api.anthropic.com/v1/messages"
API_VERSION = "2023-06-01"
DEFAULT_MODEL = "claude-opus-5"


class AnthropicProvider(Provider):
    name = "anthropic"

    def __init__(self, api_key: str | None = None, model: str = "", transport: Transport | None = None,
                 timeout: float = 120.0, url: str = API_URL, prompt_cache: bool = True):
        self.api_key = api_key if api_key is not None else os.environ.get("ANTHROPIC_API_KEY", "")
        if not self.api_key:
            raise ProviderError("AnthropicProvider requires ANTHROPIC_API_KEY (provider is off by default)")
        self.model = model or DEFAULT_MODEL
        self.transport = transport or urllib_transport
        self.timeout = timeout
        self.url = url
        self.prompt_cache = prompt_cache

    # -- conversion ----------------------------------------------------------------------
    @staticmethod
    def to_wire(messages: list[dict]) -> list[dict]:
        out: list[dict] = []
        pending_results: list[dict] = []

        def flush():
            if pending_results:
                out.append({"role": "user", "content": list(pending_results)})
                pending_results.clear()

        for m in messages:
            role = m["role"]
            if role == "tool":
                pending_results.append({
                    "type": "tool_result",
                    "tool_use_id": m["tool_call_id"],
                    "content": m.get("content", ""),
                    "is_error": bool(m.get("is_error", False)),
                })
                continue
            flush()
            if role == "user":
                out.append({"role": "user", "content": m.get("content", "")})
            elif role == "assistant":
                raw = m.get("raw")
                if isinstance(raw, dict) and raw.get("provider") == "anthropic":
                    # echo verbatim (keeps thinking blocks valid for the same model)
                    out.append({"role": "assistant", "content": raw["content"]})
                    continue
                blocks = []
                if m.get("content"):
                    blocks.append({"type": "text", "text": m["content"]})
                for tc in m.get("tool_calls", []) or []:
                    blocks.append({"type": "tool_use", "id": tc["id"], "name": tc["name"],
                                   "input": tc.get("arguments", {})})
                out.append({"role": "assistant", "content": blocks or [{"type": "text", "text": "(no content)"}]})
        flush()
        return out

    @staticmethod
    def tools_to_wire(tools: list[ToolSpec]) -> list[dict]:
        return [{"name": t.name, "description": t.description, "input_schema": t.parameters} for t in tools]

    @staticmethod
    def from_wire(data: dict, model: str) -> LLMResponse:
        text_parts, calls = [], []
        for block in data.get("content", []) or []:
            btype = block.get("type")
            if btype == "text":
                text_parts.append(block.get("text", ""))
            elif btype == "tool_use":
                args = block.get("input") or {}
                if not isinstance(args, dict):
                    args = {"_raw": args}
                calls.append(ToolCall(id=block.get("id", ""), name=block.get("name", ""), arguments=args))
        usage = data.get("usage") or {}
        return LLMResponse(
            text="".join(text_parts).strip(),
            tool_calls=calls,
            # billed-equivalent input tokens: 5-minute cache writes cost 1.25x input, cache reads 0.1x
            usage=Usage(math.ceil(int(usage.get("input_tokens", 0) or 0)
                                  + 1.25 * int(usage.get("cache_creation_input_tokens", 0) or 0)
                                  + 0.10 * int(usage.get("cache_read_input_tokens", 0) or 0)),
                        int(usage.get("output_tokens", 0) or 0)),
            model=data.get("model", model),
            stop_reason=data.get("stop_reason") or "end_turn",
            raw={"provider": "anthropic", "content": data.get("content", [])},
            provider="anthropic",
        )

    # -- call ----------------------------------------------------------------------------
    def complete(self, system, messages, tools, max_tokens=1024) -> LLMResponse:
        body = {
            "model": self.model,
            "max_tokens": max_tokens,
            "system": system,
            "messages": self.to_wire(messages),
        }
        if tools:
            body["tools"] = self.tools_to_wire(tools)
        if self.prompt_cache:
            # top-level automatic prompt caching: the tool loop re-sends the same prefix every step
            body["cache_control"] = {"type": "ephemeral"}
        headers = {
            "content-type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": API_VERSION,
        }
        status, raw = self.transport(self.url, headers, json.dumps(body).encode("utf-8"), self.timeout)
        if status != 200:
            raise classify_http_error(status, raw)
        try:
            data = json.loads(raw.decode("utf-8"))
        except Exception as e:
            raise ProviderError(f"malformed JSON from Anthropic: {e}", retryable=True) from e
        resp = self.from_wire(data, self.model)
        if resp.stop_reason == "refusal":
            resp.text = resp.text or "(the model declined this request)"
        return resp
