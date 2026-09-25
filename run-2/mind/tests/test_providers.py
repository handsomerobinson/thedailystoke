import unittest

from mind.providers.anthropic_provider import AnthropicProvider
from mind.providers.mock import MockProvider


class MockProviderTest(unittest.TestCase):
    def test_is_always_configured(self):
        self.assertTrue(MockProvider().is_configured())

    def test_deterministic_tool_pick_for_search(self):
        provider = MockProvider()
        prompt = "AVAILABLE TOOLS:\n- web_search: x\n\nTASK: please search for cats\n\nReply with ARGS: <json>"
        resp1 = provider.complete("sys", [{"role": "user", "content": prompt}])
        resp2 = provider.complete("sys", [{"role": "user", "content": prompt}])
        self.assertEqual(resp1.text, resp2.text)
        self.assertIn("web_search", resp1.text)

    def test_zero_cost(self):
        provider = MockProvider()
        resp = provider.complete("sys", [{"role": "user", "content": "hello"}])
        self.assertEqual(resp.cost_usd, 0.0)


class AnthropicProviderTest(unittest.TestCase):
    def test_not_configured_without_key(self):
        provider = AnthropicProvider(api_key="")
        self.assertFalse(provider.is_configured())
        with self.assertRaises(RuntimeError):
            provider.complete("sys", [{"role": "user", "content": "hi"}])

    def test_configured_with_key(self):
        provider = AnthropicProvider(api_key="sk-test-fake")
        self.assertTrue(provider.is_configured())


if __name__ == "__main__":
    unittest.main()
