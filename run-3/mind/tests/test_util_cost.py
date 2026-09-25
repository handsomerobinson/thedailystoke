import unittest

from mind.cost import Budget, BudgetExceeded, cost_of, price_for
from mind.types import Usage
from mind.util import InvalidName, safe_name, safe_user_id, truncate


class UtilTests(unittest.TestCase):
    def test_user_ids(self):
        self.assertEqual(safe_user_id("alice_1"), "alice_1")
        for bad in ("../bob", "a/b", "", ".hidden", "x" * 65, "al ice", None):
            with self.assertRaises(InvalidName):
                safe_user_id(bad)

    def test_names(self):
        self.assertEqual(safe_name("draft.v2"), "draft.v2")
        for bad in ("../x", "a/b", ".env", "a..b"):
            with self.assertRaises(InvalidName):
                safe_name(bad)

    def test_truncate(self):
        self.assertEqual(truncate("abc", 5), "abc")
        self.assertIn("truncated 5", truncate("a" * 10, 5))


class BudgetTests(unittest.TestCase):
    def test_cost_math(self):
        self.assertAlmostEqual(cost_of(Usage(1_000_000, 0), "mock"), price_for("mock")[0])

    def test_precall_worst_case_refuses(self):
        b = Budget(max_usd=0.01)
        with self.assertRaises(BudgetExceeded) as cm:
            b.check_brain_call(100, 1_000_000, "mock")
        self.assertEqual(cm.exception.which, "usd")

    def test_charges_accumulate_until_cap(self):
        b = Budget(max_usd=0.02)
        calls = 0
        with self.assertRaises(BudgetExceeded):
            while True:
                b.check_brain_call(1000, 500, "mock")
                b.charge_brain(Usage(1000, 500), "mock")
                calls += 1
        self.assertGreater(calls, 0)
        self.assertLessEqual(b.spent_usd, 0.02)

    def test_token_tool_time_caps(self):
        b = Budget(max_tokens=100)
        with self.assertRaises(BudgetExceeded):
            b.check_brain_call(90, 20, "mock")
        b = Budget(max_tool_calls=1)
        b.check_tool_call(); b.charge_tool()
        with self.assertRaises(BudgetExceeded):
            b.check_tool_call()
        t = [0.0]
        b = Budget(max_seconds=5, clock=lambda: t[0], started=0.0)
        t[0] = 6
        with self.assertRaises(BudgetExceeded) as cm:
            b.check_tool_call()
        self.assertEqual(cm.exception.which, "time")

    def test_env_price_override(self):
        import os
        os.environ["MIND_PRICE_IN"], os.environ["MIND_PRICE_OUT"] = "1", "2"
        try:
            self.assertEqual(price_for("anything"), (1.0, 2.0))
        finally:
            del os.environ["MIND_PRICE_IN"], os.environ["MIND_PRICE_OUT"]


if __name__ == "__main__":
    unittest.main()
