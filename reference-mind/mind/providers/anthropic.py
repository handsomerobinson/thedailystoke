"""Anthropic Messages API adapter (stdlib HTTP).  Model id comes from config."""
from __future__ import annotations

import json
import os

from ..types import BrainResponse, Message, ToolCall, ToolSpec, Usage
from .base import Brain, ProviderError, Transport, post_json, urllib_transport


class AnthropicBrain(Brain):
    name = "anthropic"
    URL = "https://api.anthropic.com/v1/messages"

    def __init__(self, api_key: str | None = None, model: str | None = None,
                 transport: Transport = urllib_transport, timeout: float = 60.0):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        if not self.api_key:
            raise ProviderError("ANTHROPIC_API_KEY is not set")
        # Model ids change; set MIND_MODEL to one your account can use.
        self.model = model or os.environ.get("MIND_MODEL", "claude-sonnet-4-5")
        self.transport = transport
        self.timeout = timeout

    @staticmethod
    def to_wire(messages: list[Message]) -> list[dict]:
        wire: list[dict] = []
        for m in messages:
            if m.role == "tool":
                block = {"type": "tool_result", "tool_use_id": m.tool_call_id, "content": m.content}
                if wire and wire[-1]["role"] == "user" and isinstance(wire[-1]["content"], list):
                    wire[-1]["content"].append(block)  # parallel tool results share one user turn
                else:
                    wire.append({"role": "user", "content": [block]})
            elif m.role == "assistant":
                content: list[dict] = []
                if m.content:
                    content.append({"type": "text", "text": m.content})
                for c in m.tool_calls:
                    content.append({"type": "tool_use", "id": c.id, "name": c.name, "input": c.args})
                wire.append({"role": "assistant", "content": content or [{"type": "text", "text": "(no content)"}]})
            else:
                wire.append({"role": "user", "content": m.content})
        return wire

    def complete(self, system: str, messages: list[Message], tools: list[ToolSpec], max_tokens: int = 1024) -> BrainResponse:
        payload = {"model": self.model, "max_tokens": max_tokens, "system": system, "messages": self.to_wire(messages)}
        if tools:
            payload["tools"] = [{"name": t.name, "description": t.description, "input_schema": t.parameters} for t in tools]
        data = post_json(self.transport, self.URL,
                         {"x-api-key": self.api_key, "anthropic-version": "2023-06-01"}, payload, self.timeout)
        text, calls = [], []
        for block in data.get("content", []):
            if block.get("type") == "text":
                text.append(block.get("text", ""))
            elif block.get("type") == "tool_use":
                calls.append(ToolCall(name=block["name"], args=block.get("input") or {}, id=block["id"]))
        u = data.get("usage", {})
        return BrainResponse("".join(text), calls, Usage(int(u.get("input_tokens", 0)), int(u.get("output_tokens", 0))),
                             model=data.get("model", self.model), stop_reason=data.get("stop_reason", ""), provider=self.name)
