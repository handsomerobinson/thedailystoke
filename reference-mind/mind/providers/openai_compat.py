"""OpenAI-compatible Chat Completions adapter (works with many hosted and local servers)."""
from __future__ import annotations

import json
import os

from ..types import BrainResponse, Message, ToolCall, ToolSpec, Usage
from .base import Brain, ProviderError, Transport, post_json, urllib_transport


class OpenAICompatBrain(Brain):
    name = "openai"

    def __init__(self, api_key: str | None = None, model: str | None = None, base_url: str | None = None,
                 transport: Transport = urllib_transport, timeout: float = 60.0):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.base_url = (base_url or os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")).rstrip("/")
        if not self.api_key and "api.openai.com" in self.base_url:
            raise ProviderError("OPENAI_API_KEY is not set")
        self.model = model or os.environ.get("MIND_MODEL", "gpt-4o-mini")
        self.transport = transport
        self.timeout = timeout
        import ipaddress
        import urllib.parse
        host = (urllib.parse.urlparse(self.base_url).hostname or "").lower()
        try:
            self.on_device = host == "localhost" or ipaddress.ip_address(host).is_loopback  # MC15: a local model
        except ValueError:
            self.on_device = False

    @staticmethod
    def to_wire(system: str, messages: list[Message]) -> list[dict]:
        wire: list[dict] = [{"role": "system", "content": system}]
        for m in messages:
            if m.role == "tool":
                wire.append({"role": "tool", "tool_call_id": m.tool_call_id, "content": m.content})
            elif m.role == "assistant":
                item: dict = {"role": "assistant", "content": m.content or None}
                if m.tool_calls:
                    item["tool_calls"] = [{"id": c.id, "type": "function",
                                           "function": {"name": c.name, "arguments": json.dumps(c.args)}} for c in m.tool_calls]
                wire.append(item)
            else:
                wire.append({"role": "user", "content": m.content})
        return wire

    def complete(self, system: str, messages: list[Message], tools: list[ToolSpec], max_tokens: int = 1024) -> BrainResponse:
        payload: dict = {"model": self.model, "max_tokens": max_tokens, "messages": self.to_wire(system, messages)}
        if tools:
            payload["tools"] = [{"type": "function", "function": {"name": t.name, "description": t.description,
                                                                  "parameters": t.parameters}} for t in tools]
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        data = post_json(self.transport, self.base_url + "/chat/completions", headers, payload, self.timeout)
        try:
            choice = data["choices"][0]
            msg = choice["message"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderError(f"unexpected response shape: {str(data)[:200]}", transient=True) from exc
        calls = []
        for c in msg.get("tool_calls") or []:
            fn = c.get("function", {})
            try:
                args = json.loads(fn.get("arguments") or "{}")
            except ValueError:
                args = {"__unparseable__": fn.get("arguments", "")}  # registry will reject -> brain sees error
            calls.append(ToolCall(name=fn.get("name", ""), args=args if isinstance(args, dict) else {}, id=c.get("id") or ""))
        u = data.get("usage") or {}
        return BrainResponse(msg.get("content") or "", calls,
                             Usage(int(u.get("prompt_tokens", 0)), int(u.get("completion_tokens", 0))),
                             model=data.get("model", self.model), stop_reason=choice.get("finish_reason", ""), provider=self.name)
