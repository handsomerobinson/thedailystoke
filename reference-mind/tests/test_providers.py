import json
import os
import unittest

from mind.providers import (AllBrainsFailed, AnthropicBrain, MockBrain, OpenAICompatBrain, ProviderError,
                            ResilientBrain, make_brain)
from mind.types import Message, ToolCall, ToolSpec

TOOLS = [ToolSpec("note_read", "read", {"type": "object", "properties": {"name": {"type": "string"}}}),
         ToolSpec("python_exec", "run", {"type": "object", "properties": {"code": {"type": "string"}}}),
         ToolSpec("calculator", "calc", {"type": "object", "properties": {"expression": {"type": "string"}}})]


class FakeTransport:
    def __init__(self, responses):
        self.responses = list(responses)
        self.requests = []

    def __call__(self, url, headers, body, timeout):
        self.requests.append((url, headers, json.loads(body)))
        status, payload = self.responses.pop(0)
        return status, json.dumps(payload).encode() if not isinstance(payload, bytes) else payload


class MockBrainTests(unittest.TestCase):
    def test_multistep_plan_and_strategy_elimination(self):
        b = MockBrain()
        msgs = [Message("user", "Count the words in note 'draft'")]
        r = b.complete("sys", msgs, TOOLS)
        self.assertEqual(r.tool_calls[0].name, "note_read")
        msgs += [Message("assistant", r.text, r.tool_calls), Message("tool", "a  b", name="note_read")]
        r = b.complete("sys", msgs, TOOLS)
        self.assertIn("strategy: split_on_space", r.tool_calls[0].args["code"])
        r2 = b.complete("## Lessons\n- LESSON: AVOID strategy split_on_space", msgs, TOOLS)
        self.assertIn("strategy: split_on_whitespace", r2.tool_calls[0].args["code"])

    def test_no_hidden_state_between_calls(self):
        b = MockBrain()
        msgs = [Message("user", "Write a Python function is_palindrome(s)")]
        first = b.complete("sys", msgs, TOOLS).text
        b.complete("MODE: REFLECT\n", [Message("user", "TRAJECTORY: strategy: naive_reverse\nEVALUATOR FEEDBACK: bad")], [])
        self.assertEqual(b.complete("sys", msgs, TOOLS).text, first)  # only context text changes behaviour

    def test_reflection_format(self):
        out = MockBrain().complete("MODE: REFLECT\n", [Message("user", "CALL x: # strategy: integers_only\nEVALUATOR FEEDBACK: too high")], []).text
        self.assertIn("AVOID strategy integers_only", out)
        self.assertIn("DIAGNOSIS", out)
        generic = MockBrain().complete("MODE: REFLECT\n", [Message("user", "EVALUATOR FEEDBACK: permission denied")], []).text
        self.assertIn("LESSON", generic)

    def test_honest_fallback_and_usage(self):
        r = MockBrain().complete("sys", [Message("user", "compose a sonnet about tea")], TOOLS)
        self.assertIn("no scripted skill", r.text)
        self.assertGreater(r.usage.input_tokens, 0)

    def test_injected_failures(self):
        b = MockBrain(fail_times=1)
        with self.assertRaises(ProviderError):
            b.complete("s", [Message("user", "what is 1+1")], TOOLS)
        self.assertTrue(b.complete("s", [Message("user", "what is 1+1")], TOOLS).tool_calls)


class AnthropicTests(unittest.TestCase):
    def test_wire_format_and_parse(self):
        t = FakeTransport([(200, {"content": [{"type": "text", "text": "hi"},
                                              {"type": "tool_use", "id": "tu1", "name": "calculator", "input": {"expression": "1+1"}}],
                                  "usage": {"input_tokens": 10, "output_tokens": 5}, "stop_reason": "tool_use", "model": "m"})])
        b = AnthropicBrain(api_key="k", model="m", transport=t)
        msgs = [Message("user", "q"), Message("assistant", "", [ToolCall("calculator", {"expression": "2"}, "c1"),
                                                                ToolCall("clock", {}, "c2")]),
                Message("tool", "2", tool_call_id="c1", name="calculator"), Message("tool", "now", tool_call_id="c2", name="clock")]
        r = b.complete("SYS", msgs, TOOLS, 100)
        url, headers, body = t.requests[0]
        self.assertEqual(headers["x-api-key"], "k")
        self.assertEqual(body["system"], "SYS")
        self.assertEqual(body["tools"][0]["input_schema"]["type"], "object")
        self.assertEqual(len(body["messages"]), 3)  # parallel tool results merged in one user turn
        self.assertEqual([b_["type"] for b_ in body["messages"][2]["content"]], ["tool_result", "tool_result"])
        self.assertEqual(r.text, "hi")
        self.assertEqual(r.tool_calls[0].args, {"expression": "1+1"})
        self.assertEqual((r.usage.input_tokens, r.usage.output_tokens), (10, 5))

    def test_errors_classified(self):
        for status, transient in ((429, True), (529, True), (400, False), (401, False)):
            b = AnthropicBrain(api_key="k", transport=FakeTransport([(status, {"error": "x"})]))
            with self.assertRaises(ProviderError) as cm:
                b.complete("s", [Message("user", "q")], [])
            self.assertEqual(cm.exception.transient, transient, status)

    def test_missing_key(self):
        saved = os.environ.pop("ANTHROPIC_API_KEY", None)
        try:
            with self.assertRaises(ProviderError):
                AnthropicBrain()
        finally:
            if saved:
                os.environ["ANTHROPIC_API_KEY"] = saved


class OpenAITests(unittest.TestCase):
    def test_wire_and_parse(self):
        t = FakeTransport([(200, {"choices": [{"message": {"content": None, "tool_calls": [
            {"id": "c9", "type": "function", "function": {"name": "calculator", "arguments": "{\"expression\": \"3*3\"}"}}]},
            "finish_reason": "tool_calls"}], "usage": {"prompt_tokens": 7, "completion_tokens": 3}})])
        b = OpenAICompatBrain(api_key="k", model="m", base_url="http://local/v1", transport=t)
        r = b.complete("SYS", [Message("user", "q")], TOOLS)
        url, headers, body = t.requests[0]
        self.assertEqual(url, "http://local/v1/chat/completions")
        self.assertEqual(body["messages"][0], {"role": "system", "content": "SYS"})
        self.assertEqual(r.tool_calls[0].args, {"expression": "3*3"})
        self.assertEqual(r.usage.output_tokens, 3)

    def test_bad_arguments_json_surface_as_invalid(self):
        t = FakeTransport([(200, {"choices": [{"message": {"tool_calls": [
            {"id": "c", "function": {"name": "calculator", "arguments": "{not json"}}]}}]})])
        r = OpenAICompatBrain(api_key="k", base_url="http://x/v1", transport=t).complete("s", [Message("user", "q")], [])
        self.assertIn("__unparseable__", r.tool_calls[0].args)

    def test_malformed_response(self):
        t = FakeTransport([(200, {"nope": 1})])
        with self.assertRaises(ProviderError):
            OpenAICompatBrain(api_key="k", base_url="http://x/v1", transport=t).complete("s", [Message("user", "q")], [])


class ResilienceTests(unittest.TestCase):
    def test_retry_then_success(self):
        sleeps = []
        rb = ResilientBrain([MockBrain(fail_times=2)], retries=2, sleep=sleeps.append)
        self.assertTrue(rb.complete("s", [Message("user", "what is 1+1")], TOOLS).tool_calls)
        self.assertEqual(len(sleeps), 2)
        self.assertLess(sleeps[0], sleeps[1] * 2)  # exponential-ish backoff

    def test_non_transient_skips_retries_and_falls_back(self):
        dead = MockBrain(fail_times=99, fail_transient=False)
        rb = ResilientBrain([dead, MockBrain()], sleep=lambda s: None)
        rb.complete("s", [Message("user", "what is 1+1")], TOOLS)
        self.assertEqual(dead.calls, 1)

    def test_circuit_breaker(self):
        t = [0.0]
        dead = MockBrain(fail_times=99, fail_transient=False)
        rb = ResilientBrain([dead, MockBrain()], failure_threshold=2, cooldown=30, sleep=lambda s: None, clock=lambda: t[0])
        for _ in range(4):
            rb.complete("s", [Message("user", "what is 1+1")], TOOLS)
        self.assertEqual(dead.calls, 2)  # opened after 2 failures, skipped afterwards
        t[0] = 31
        rb.complete("s", [Message("user", "what is 1+1")], TOOLS)
        self.assertEqual(dead.calls, 3)  # half-open retry after cooldown

    def test_all_fail(self):
        rb = ResilientBrain([MockBrain(fail_times=99)], retries=1, sleep=lambda s: None)
        with self.assertRaises(AllBrainsFailed):
            rb.complete("s", [Message("user", "x")], [])

    def test_adapter_bug_is_contained(self):
        class Buggy(MockBrain):
            def complete(self, *a, **k):
                raise KeyError("oops")
        rb = ResilientBrain([Buggy(), MockBrain()], sleep=lambda s: None)
        self.assertTrue(rb.complete("s", [Message("user", "what is 1+1")], TOOLS).tool_calls)


class FactoryTests(unittest.TestCase):
    def test_default_mock_and_degraded(self):
        warnings = []
        b, desc = make_brain("mock", warn=warnings.append)
        self.assertIn("mock", desc)
        saved = os.environ.pop("ANTHROPIC_API_KEY", None)
        try:
            b, desc = make_brain("anthropic", warn=warnings.append)
            self.assertIn("DEGRADED", desc)
            self.assertTrue(any("DEGRADED" in w for w in warnings))
            with self.assertRaises(ProviderError):
                make_brain("anthropic", strict=True, warn=warnings.append)
        finally:
            if saved:
                os.environ["ANTHROPIC_API_KEY"] = saved

    def test_chain(self):
        os.environ["ANTHROPIC_API_KEY"] = "test-key"
        try:
            b, desc = make_brain("anthropic,mock", warn=lambda s: None)
            self.assertEqual([x.name for x in b.brains], ["anthropic", "mock"])
        finally:
            del os.environ["ANTHROPIC_API_KEY"]
