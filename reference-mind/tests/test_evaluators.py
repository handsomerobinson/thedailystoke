import unittest

from mind.evaluators import (ContainsAll, JudgeEvaluator, NumericAnswer, PythonFunctionTests, RegexMatch,
                             evaluator_from_dict, numbers_in)
from mind.cost import Budget
from mind.providers import MockBrain


class EvaluatorTests(unittest.TestCase):
    def test_numeric(self):
        e = NumericAnswer(14)
        self.assertTrue(e("The note has 14 words").success)
        bad = e("It has 17 words")
        self.assertFalse(bad.success)
        self.assertIn("too high", bad.feedback)
        self.assertNotIn("14", bad.feedback)  # does not leak the key
        self.assertIn("expected 14", NumericAnswer(14, reveal=True)("17").feedback)
        self.assertFalse(e("no digits").success)
        self.assertEqual(numbers_in("1,200.5 and -3"), [1200.5, -3.0])

    def test_contains_and_regex(self):
        self.assertTrue(ContainsAll(["Paris"])("the capital is paris").success)
        self.assertIn("missing", ContainsAll(["a", "zz"])("a").feedback)
        self.assertTrue(RegexMatch(r"\d{3}")("code 123").success)

    def test_python_tests(self):
        e = PythonFunctionTests("add", [([1, 2], 3), ([0, 0], 0)])
        self.assertTrue(e("```python\ndef add(a, b):\n    return a + b\n```").success)
        bad = e("```python\ndef add(a, b):\n    return a - b\n```")
        self.assertFalse(bad.success)
        self.assertIn("returned -1, expected 3", bad.feedback)
        self.assertIn("did not run", e("```python\ndef add(:\n```").feedback)
        self.assertIn("raised", e("```python\ndef add(a, b):\n    raise ValueError\n```").feedback)

    def test_judge(self):
        j = JudgeEvaluator(MockBrain(), budget=Budget())
        self.assertTrue(j("42", "what is 6*7").success)
        self.assertFalse(j("[mock brain] I have no scripted skill", "x").success)

    def test_crash_is_failure(self):
        class Boom(NumericAnswer):
            def evaluate(self, a, t):
                raise RuntimeError("x")
        r = Boom(1)("1")
        self.assertFalse(r.success)
        self.assertIn("evaluator error", r.feedback)

    def test_roundtrip(self):
        for e in (NumericAnswer(3), ContainsAll(["a"]), RegexMatch("x"), PythonFunctionTests("f", [([1], 1)])):
            e2 = evaluator_from_dict(e.to_dict())
            self.assertEqual(type(e2), type(e))
        self.assertIsNone(evaluator_from_dict(None))
        with self.assertRaises(ValueError):
            evaluator_from_dict({"type": "vibes"})
