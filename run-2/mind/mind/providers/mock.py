"""A deterministic, zero-cost, zero-key stand-in brain.

Decision: the mock is rule-based, not random, so the demo and tests are
100% reproducible — it looks for keywords in the latest user message and
the running reflection notes to decide what to do, including deliberately
failing once on a specific trigger phrase so the reflection loop has
something real to learn from.
"""
from __future__ import annotations

import json
import re
from typing import List

from .base import LLMProvider, LLMResponse


class MockProvider(LLMProvider):
    name = "mock"

    def is_configured(self) -> bool:
        # Always "configured" — that's the point of the zero-key demo.
        return True

    def complete(self, system: str, messages: List[dict], max_tokens: int = 512) -> LLMResponse:
        last_user = ""
        for m in reversed(messages):
            if m.get("role") == "user":
                last_user = m.get("content", "")
                break

        text = self._respond(system, last_user, messages)
        return LLMResponse(text=text, cost_usd=0.0, input_tokens=len(last_user.split()), output_tokens=len(text.split()))

    def _respond(self, system: str, last_user: str, messages: List[dict]) -> str:
        lu = last_user.lower()

        # The agent asks the brain to pick a tool via this exact prompt shape
        # (see agent.py: _build_tool_prompt). Keep the mock's parsing in
        # lock-step with that format.
        if "AVAILABLE TOOLS" in last_user or "available tools" in lu:
            return self._pick_tool(last_user)

        if "reflect" in lu and "failed" in lu:
            return self._reflect(last_user)

        return f"ack: {last_user[:200]}"

    def _pick_tool(self, prompt: str) -> str:
        # Very small heuristic "planner": look at the task text embedded in
        # the prompt and choose a tool + args deterministically.
        m = re.search(r"TASK:\s*(.*)", prompt)
        task = m.group(1).strip() if m else prompt
        tlow = task.lower()

        if "divide" in tlow and "zero" in tlow:
            if "LESSONS FROM PAST ATTEMPTS" in prompt:
                # Learned from the reflection: guard the denominator instead
                # of naively dividing.
                safe_code = (
                    "denominator = 0\n"
                    "if denominator == 0:\n"
                    "    print('skipped: cannot divide by zero')\n"
                    "else:\n"
                    "    print(10 / denominator)"
                )
                return f"TOOL: code_exec\nARGS: {json.dumps({'code': safe_code})}"
            # First attempt: the mock brain naively proposes a divide-by-zero
            # so the reflection loop has a genuine failure to learn from.
            return f"TOOL: code_exec\nARGS: {json.dumps({'code': 'print(10/0)'})}"

        if "search" in tlow or "look up" in tlow or "find out" in tlow:
            args = json.dumps({"query": task})
            return f"TOOL: web_search\nARGS: {args}"
        if "note" in tlow or "remember" in tlow or "save" in tlow:
            args = json.dumps({"action": "write", "title": "task-note", "body": task})
            return f"TOOL: notes\nARGS: {args}"
        if "calculate" in tlow or "compute" in tlow or "sum" in tlow or any(c.isdigit() for c in tlow):
            numbers = re.findall(r"\d+", task)
            code = f"print(sum({numbers}))"
            args = json.dumps({"code": code})
            return f"TOOL: code_exec\nARGS: {args}"
        return "TOOL: none\nARGS: {}"

    def _reflect(self, prompt: str) -> str:
        if "zerodivisionerror" in prompt.lower():
            return (
                "Reflection: I divided by zero without checking the divisor first. "
                "Next time, guard the denominator and skip the operation (or ask "
                "for a valid divisor) instead of executing it blindly."
            )
        return "Reflection: the previous attempt failed; I should validate inputs before acting."
