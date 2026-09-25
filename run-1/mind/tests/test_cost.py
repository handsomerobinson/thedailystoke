import unittest

from mind.cost import UNKNOWN_MODEL_PRICE, Budget, BudgetExceeded, cost_usd, price_for


class CostTests(unittest.TestCase):
    def test_cost_math(self):
        self.assertAlmostEqual(cost_usd(1_000_000, 1_000_000, (5, 25)), 30.0)

    def test_unknown_model_is_priced_high(self):
        self.assertEqual(price_for("some-new-model"), UNKNOWN_MODEL_PRICE)
        self.assertEqual(price_for("claude-opus-5"), (5.0, 25.0))

    def test_preflight_refuses_worst_case_overrun(self):
        b = Budget(limit_usd=0.01)
        b.preflight(100, 100, (5, 25))  # tiny, fine
        with self.assertRaises(BudgetExceeded):
            b.preflight(1000, 4000, (5, 25))  # 0.005 + 0.1 > 0.01

    def test_record_accumulates_and_calls_ledger(self):
        seen = []
        b = Budget(limit_usd=1, on_spend=seen.append)
        b.record(1000, 1000, (5, 25))
        self.assertAlmostEqual(b.spent_usd, 0.03)
        self.assertEqual(b.calls, 1)
        self.assertEqual(len(seen), 1)

    def test_ledger_failure_does_not_raise(self):
        def boom(_):
            raise RuntimeError("db down")
        Budget(limit_usd=1, on_spend=boom).record(1, 1, (1, 1))

    def test_preflight_after_spend(self):
        b = Budget(limit_usd=0.05)
        b.record(0, 1600, (0, 25))  # 0.04
        with self.assertRaises(BudgetExceeded):
            b.preflight(0, 1000, (0, 25))  # +0.025 > 0.05


if __name__ == "__main__":
    unittest.main()
