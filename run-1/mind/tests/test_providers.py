import json
import unittest

from mind.config import Config
from mind.prompts import FACTS_HEADER, LESSONS_HEADER, REFLECT_SYSTEM
from mind.providers import (AnthropicProvider, MockBrain, OpenAIProvider, ProviderError, ResilientProvider,
                            ToolSpec, make_provider)
from mind.providers.base import classify_http_error
from mind.util import FakeClock

TOOLS = [ToolSpec(n, n, {"type": "object", "properties": {}}) for n in
         ("calculator", "remember_fact", "write_note", "list_notes", "run_python", "web_search", "delete_note")]


class MockBrainTests(unittest.TestCase):
    def setUp(self):
        self.b = MockBrain()

    def test_calls_calculator_then_answers(self):
        r = self.b.complete("sys", [{"role": "user", "content": "calculate 2+3"}], TOOLS)
        self.assertEqual(r.tool_calls[0].name, "calculator")
        msgs = [{"role": "user", "content": "calculate 2+3"},
                {"role": "assistant", "content": "", "tool_calls": [r.tool_calls[0].to_dict()]},
                {"role": "tool", "tool_call_id": r.tool_calls[0].id, "content": "5"}]
        r2 = self.b.complete("sys", msgs, TOOLS)
        self.assertEqual(r2.tool_calls, [])
        self.assertIn("5", r2.text)

    def test_is_stateless(self):
        m = [{"role": "user", "content": "calculate 2+3"}]
        a = self.b.complete("sys", m, TOOLS)
        b = MockBrain().complete("sys", m, TOOLS)
        self.assertEqual(a.tool_calls[0].arguments, b.tool_calls[0].arguments)

    def test_answers_from_injected_facts(self):
        sys = f"x\n{FACTS_HEADER}\n- name: Ada\n"
        r = self.b.complete(sys, [{"role": "user", "content": "what is my name?"}], TOOLS)
        self.assertIn("Ada", r.text)

    def test_code_choice_depends_only_on_reflection_text(self):
        task = [{"role": "user", "content": "Write a python function is_palindrome(s)"}]
        first = self.b.complete("sys", task, TOOLS).text
        self.assertIn("approach: naive-reverse", first)
        sys = f"x\n{LESSONS_HEADER}\n- Avoid approach 'naive-reverse' next time\n"
        second = self.b.complete(sys, task, TOOLS).text
        self.assertIn("approach: normalize-alnum", second)

    def test_reflect_mode_uses_feedback(self):
        prompt = ("TASK:\nWrite a python function median(xs)\n\nATTEMPT (final):\n# approach: middle-index\n\n"
                  "TRAJECTORY:\n\nEVALUATOR FEEDBACK:\n1/2 tests passed.\nmedian([1, 2]) returned 2, expected 1.5\n\n"
                  "EARLIER REFLECTIONS ON THIS TASK:\n(none)")
        r = self.b.complete(REFLECT_SYSTEM, [{"role": "user", "content": prompt}], [])
        self.assertIn("Avoid approach 'middle-index'", r.text)
        self.assertIn("expected 1.5", r.text)

    def test_denied_tool_is_explained_not_retried(self):
        msgs = [{"role": "user", "content": "delete note x"},
                {"role": "assistant", "content": "", "tool_calls": [{"id": "c1", "name": "delete_note", "arguments": {}}]},
                {"role": "tool", "tool_call_id": "c1", "content": "permission denied", "is_error": True}]
        r = self.b.complete("sys", msgs, TOOLS)
        self.assertEqual(r.tool_calls, [])
        self.assertIn("couldn't", r.text)

    def test_unknown_request_is_honest(self):
        r = self.b.complete("sys", [{"role": "user", "content": "compose a symphony"}], TOOLS)
        self.assertIn("no skill", r.text)

    def test_missing_tool_is_reported(self):
        r = self.b.complete("sys", [{"role": "user", "content": "calculate 1+1"}], [])
        self.assertIn("not available", r.text)


class FakeTransport:
    def __init__(self, responses):
        self.responses = list(responses)
        self.requests = []

    def __call__(self, url, headers, body, timeout):
        self.requests.append((url, headers, json.loads(body)))
        r = self.responses.pop(0)
        if isinstance(r, Exception):
            raise r
        status, data = r
        return status, json.dumps(data).encode()


HISTORY = [
    {"role": "user", "content": "hi"},
    {"role": "assistant", "content": "checking", "tool_calls": [
        {"id": "t1", "name": "calculator", "arguments": {"expression": "1+1"}},
        {"id": "t2", "name": "calculator", "arguments": {"expression": "2+2"}}]},
    {"role": "tool", "tool_call_id": "t1", "name": "calculator", "content": "2"},
    {"role": "tool", "tool_call_id": "t2", "name": "calculator", "content": "bad", "is_error": True},
]


class AnthropicTests(unittest.TestCase):
    def test_requires_key(self):
        with self.assertRaises(ProviderError):
            AnthropicProvider(api_key="")

    def test_wire_groups_parallel_tool_results_in_one_user_message(self):
        wire = AnthropicProvider.to_wire(HISTORY)
        self.assertEqual([m["role"] for m in wire], ["user", "assistant", "user"])
        self.assertEqual(len(wire[2]["content"]), 2)
        self.assertTrue(wire[2]["content"][1]["is_error"])
        self.assertEqual(wire[1]["content"][1]["type"], "tool_use")

    def test_raw_content_echoed_verbatim(self):
        raw = {"provider": "anthropic", "content": [{"type": "thinking", "thinking": "", "signature": "s"},
                                                    {"type": "text", "text": "x"}]}
        wire = AnthropicProvider.to_wire([{"role": "user", "content": "q"},
                                          {"role": "assistant", "content": "x", "raw": raw}])
        self.assertEqual(wire[1]["content"], raw["content"])

    def test_complete_parses_tool_use_and_usage(self):
        t = FakeTransport([(200, {"model": "claude-opus-5", "stop_reason": "tool_use",
                                  "content": [{"type": "text", "text": "let me"},
                                              {"type": "tool_use", "id": "tu1", "name": "calculator",
                                               "input": {"expression": "6*7"}}],
                                  "usage": {"input_tokens": 50, "output_tokens": 10}})])
        p = AnthropicProvider(api_key="k", transport=t)
        r = p.complete("sys", [{"role": "user", "content": "q"}], TOOLS[:1], 100)
        self.assertEqual(r.tool_calls[0].arguments, {"expression": "6*7"})
        self.assertEqual((r.usage.input_tokens, r.usage.output_tokens), (50, 10))
        url, headers, body = t.requests[0]
        self.assertEqual(headers["anthropic-version"], "2023-06-01")
        self.assertEqual(body["model"], "claude-opus-5")
        self.assertEqual(body["tools"][0]["input_schema"]["type"], "object")

    def test_http_errors_classified(self):
        t = FakeTransport([(529, {"error": "overloaded"}), (400, {"error": "bad"})])
        p = AnthropicProvider(api_key="k", transport=t)
        with self.assertRaises(ProviderError) as e:
            p.complete("s", [{"role": "user", "content": "q"}], [])
        self.assertTrue(e.exception.retryable)
        with self.assertRaises(ProviderError) as e:
            p.complete("s", [{"role": "user", "content": "q"}], [])
        self.assertFalse(e.exception.retryable)

    def test_refusal_has_text(self):
        t = FakeTransport([(200, {"content": [], "stop_reason": "refusal", "usage": {}})])
        r = AnthropicProvider(api_key="k", transport=t).complete("s", [{"role": "user", "content": "q"}], [])
        self.assertEqual(r.stop_reason, "refusal")
        self.assertTrue(r.text)


class OpenAITests(unittest.TestCase):
    def test_requires_key_and_model(self):
        with self.assertRaises(ProviderError):
            OpenAIProvider(api_key="", model="m")
        with self.assertRaises(ProviderError):
            OpenAIProvider(api_key="k", model="")

    def test_wire_format(self):
        wire = OpenAIProvider.to_wire("sys", HISTORY)
        self.assertEqual(wire[0]["role"], "system")
        self.assertEqual(wire[2]["tool_calls"][0]["function"]["arguments"], json.dumps({"expression": "1+1"}))
        self.assertEqual([m["role"] for m in wire[3:]], ["tool", "tool"])
        self.assertTrue(wire[4]["content"].startswith("ERROR"))

    def test_invalid_json_arguments_are_contained(self):
        t = FakeTransport([(200, {"choices": [{"message": {"content": None, "tool_calls": [
            {"id": "c", "function": {"name": "calculator", "arguments": "{not json"}}]}, "finish_reason": "tool_calls"}],
            "usage": {"prompt_tokens": 3, "completion_tokens": 4}})])
        r = OpenAIProvider(api_key="k", model="m", transport=t).complete("s", [{"role": "user", "content": "q"}], [])
        self.assertIn("_invalid_json", r.tool_calls[0].arguments)
        self.assertEqual(r.usage.output_tokens, 4)


class Flaky(MockBrain):
    def __init__(self, fails, retryable=True, model="flaky"):
        super().__init__(model=model)
        self.fails = fails
        self.retryable = retryable
        self.n = 0

    def complete(self, *a, **k):
        self.n += 1
        if self.n <= self.fails:
            raise ProviderError("boom", retryable=self.retryable)
        return super().complete(*a, **k)


class Buggy(MockBrain):
    def complete(self, *a, **k):
        raise KeyError("bug")


MSG = [{"role": "user", "content": "what is my name?"}]


class ResilientTests(unittest.TestCase):
    def test_retries_then_succeeds_with_backoff(self):
        clock = FakeClock()
        p = ResilientProvider([Flaky(2)], retries=2, backoff_s=1, clock=clock)
        p.complete("s", MSG, [])
        self.assertEqual(clock.slept, [1, 2])

    def test_non_retryable_goes_straight_to_fallback(self):
        a, b = Flaky(99, retryable=False), MockBrain(model="b")
        p = ResilientProvider([a, b], retries=3, clock=FakeClock())
        p.complete("s", MSG, [])
        self.assertEqual(a.n, 1)
        self.assertIs(p.last_provider, b)

    def test_buggy_provider_does_not_crash(self):
        p = ResilientProvider([Buggy(), MockBrain(model="ok")], clock=FakeClock())
        self.assertEqual(p.complete("s", MSG, []).model, "ok")

    def test_all_down_raises_single_error(self):
        p = ResilientProvider([Flaky(99)], retries=1, clock=FakeClock())
        with self.assertRaises(ProviderError):
            p.complete("s", MSG, [])

    def test_circuit_breaker_skips_dead_provider(self):
        clock = FakeClock()
        dead, ok = Flaky(10**6), MockBrain(model="ok")
        p = ResilientProvider([dead, ok], retries=0, breaker_threshold=2, cooldown_s=100, clock=clock)
        for _ in range(3):
            p.complete("s", MSG, [])
        self.assertEqual(dead.n, 2)  # third call skipped the open breaker
        clock.advance(101)
        p.complete("s", MSG, [])
        self.assertEqual(dead.n, 3)  # half-open retry after cooldown

    def test_preflight_price_is_worst_in_chain(self):
        p = ResilientProvider([MockBrain(price=(1, 2)), MockBrain(price=(3, 1))], clock=FakeClock())
        self.assertEqual(p.preflight_price(), (3, 2))


class FactoryTests(unittest.TestCase):
    def test_default_is_mock(self):
        self.assertIn("mock", make_provider(Config()).describe())

    def test_real_provider_without_key_is_an_error_not_a_silent_mock(self):
        import os
        old = os.environ.pop("ANTHROPIC_API_KEY", None)
        try:
            with self.assertRaises(ProviderError):
                make_provider(Config(provider="anthropic"))
        finally:
            if old is not None:
                os.environ["ANTHROPIC_API_KEY"] = old

    def test_unknown_provider(self):
        with self.assertRaises(ProviderError):
            make_provider(Config(provider="nope"))


if __name__ == "__main__":
    unittest.main()
