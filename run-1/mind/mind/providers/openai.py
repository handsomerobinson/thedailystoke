"""OpenAI Chat Completions over plain HTTPS (stdlib urllib). Off by default.

Enable with MIND_PROVIDER=openai, OPENAI_API_KEY, and MIND_MODEL (required: this build does
not hard-code a current OpenAI model id or price; unknown models are priced conservatively
high by cost.py). Tested only through a fake transport.
"""
from __future__ import annotations

import json
import os

from .base import (LLMResponse, Provider, ProviderError, ToolCall, ToolSpec, Transport, Usage,
                   classify_http_error, urllib_transport)

API_URL = "https://api.openai.com/v1/chat/completions"


class OpenAIProvider(Provider):
    name = "openai"

    def __init__(self, api_key: str | None = None, model: str = "", transport: Transport | None = None,
                 timeout: float = 120.0, url: str = API_URL):
        self.api_key = api_key if api_key is not None else os.environ.get("OPENAI_API_KEY", "")
        if not self.api_key:
            raise ProviderError("OpenAIProvider requires OPENAI_API_KEY (provider is off by default)")
        if not model:
            raise ProviderError("OpenAIProvider requires an explicit model (set MIND_MODEL)")
        self.model = model
        self.transport = transport or urllib_transport
        self.timeout = timeout
        self.url = url

    @staticmethod
    def to_wire(system: str, messages: list[dict]) -> list[dict]:
        out = [{"role": "system", "content": system}] if system else []
        for m in messages:
            if m["role"] == "user":
                out.append({"role": "user", "content": m.get("content", "")})
            elif m["role"] == "assistant":
                msg = {"role": "assistant", "content": m.get("content") or None}
                if m.get("tool_calls"):
                    msg["tool_calls"] = [
                        {"id": tc["id"], "type": "function",
                         "function": {"name": tc["name"], "arguments": json.dumps(tc.get("arguments", {}))}}
                        for tc in m["tool_calls"]
                    ]
                out.append(msg)
            elif m["role"] == "tool":
                content = m.get("content", "")
                if m.get("is_error"):
                    content = "ERROR: " + content
                out.append({"role": "tool", "tool_call_id": m["tool_call_id"], "content": content})
        return out

    @staticmethod
    def tools_to_wire(tools: list[ToolSpec]) -> list[dict]:
        return [{"type": "function", "function": {"name": t.name, "description": t.description,
                                                  "parameters": t.parameters}} for t in tools]

    @staticmethod
    def from_wire(data: dict, model: str) -> LLMResponse:
        choices = data.get("choices") or []
        if not choices:
            raise ProviderError("OpenAI response had no choices", retryable=True)
        msg = choices[0].get("message") or {}
        calls = []
        for tc in msg.get("tool_calls") or []:
            fn = tc.get("function") or {}
            try:
                args = json.loads(fn.get("arguments") or "{}")
                if not isinstance(args, dict):
                    args = {"_raw": args}
            except json.JSONDecodeError:
                args = {"_invalid_json": fn.get("arguments", "")}
            calls.append(ToolCall(id=tc.get("id", ""), name=fn.get("name", ""), arguments=args))
        usage = data.get("usage") or {}
        return LLMResponse(
            text=(msg.get("content") or "").strip(),
            tool_calls=calls,
            usage=Usage(int(usage.get("prompt_tokens", 0) or 0), int(usage.get("completion_tokens", 0) or 0)),
            model=data.get("model", model),
            stop_reason=choices[0].get("finish_reason") or "stop",
            provider="openai",
        )

    def complete(self, system, messages, tools, max_tokens=1024) -> LLMResponse:
        body = {"model": self.model, "max_completion_tokens": max_tokens,
                "messages": self.to_wire(system, messages)}
        if tools:
            body["tools"] = self.tools_to_wire(tools)
        headers = {"content-type": "application/json", "authorization": f"Bearer {self.api_key}"}
        status, raw = self.transport(self.url, headers, json.dumps(body).encode("utf-8"), self.timeout)
        if status != 200:
            raise classify_http_error(status, raw)
        try:
            data = json.loads(raw.decode("utf-8"))
        except Exception as e:
            raise ProviderError(f"malformed JSON from OpenAI: {e}", retryable=True) from e
        return self.from_wire(data, self.model)
