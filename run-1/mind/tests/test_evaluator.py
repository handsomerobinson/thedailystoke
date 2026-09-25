import unittest

from mind.cost import Budget
from mind.evaluator import Contains, ExactMatch, LLMJudge, PythonTests, extract_code
from mind.providers import MockBrain

CASES = [(["abc"], "cba"), ([""], "")]


class EvaluatorTests(unittest.TestCase):
    def test_extract_code(self):
        self.assertEqual(extract_code("x\n```python\ndef f(): pass\n```\n").strip(), "def f(): pass")
        self.assertEqual(extract_code("no code here"), "")

    def test_python_tests_pass(self):
        r = PythonTests("rev", CASES).check("```python\ndef rev(s):\n    return s[::-1]\n```")
        self.assertTrue(r.passed)

    def test_python_tests_feedback_names_failing_case(self):
        r = PythonTests("rev", CASES).check("```python\ndef rev(s):\n    return s\n```")
        self.assertFalse(r.passed)
        self.assertIn("rev('abc') returned 'abc', expected 'cba'", r.feedback)
        self.assertAlmostEqual(r.score, 0.5)

    def test_python_tests_exceptions_and_missing_function(self):
        r = PythonTests("rev", CASES).check("```python\ndef rev(s):\n    raise KeyError(s)\n```")
        self.assertIn("raised KeyError", r.feedback)
        r = PythonTests("rev", CASES).check("```python\ndef other(s):\n    return s\n```")
        self.assertIn("not defined", r.feedback)

    def test_python_tests_infinite_loop_is_contained(self):
        from mind.config import SandboxPolicy
        r = PythonTests("rev", CASES, SandboxPolicy(wall_timeout_s=1, cpu_seconds=1)).check(
            "```python\ndef rev(s):\n    while True: pass\n```")
        self.assertFalse(r.passed)
        self.assertIn("did not run to completion", r.feedback)

    def test_no_code(self):
        self.assertFalse(PythonTests("rev", CASES).check("I refuse").passed)

    def test_exact_and_contains(self):
        self.assertTrue(ExactMatch("42").check(" 42. ").passed)
        self.assertFalse(ExactMatch("42").check("43").passed)
        r = Contains("alpha", "beta").check("Alpha only")
        self.assertFalse(r.passed)
        self.assertAlmostEqual(r.score, 0.5)

    def test_llm_judge_with_mock(self):
        j = LLMJudge(MockBrain(), "say hi", Budget(1.0))
        self.assertTrue(j.check("hi there").passed)
        self.assertFalse(j.check("I couldn't do it").passed)

    def test_llm_judge_budget_exhausted_is_not_a_pass(self):
        j = LLMJudge(MockBrain(price=(1000, 1000)), "say hi", Budget(0.0001))
        r = j.check("hi")
        self.assertFalse(r.passed)
        self.assertIn("judge unavailable", r.feedback)


if __name__ == "__main__":
    unittest.main()


class SpoofTests(unittest.TestCase):
    def test_code_cannot_fake_a_pass_by_printing_a_marker(self):
        spoof = ('```python\nimport atexit, json\n'
                 'fake = json.dumps({"passed": 2, "failed": []})\n'
                 'print("@@RESULT@@" + fake)\n'
                 'atexit.register(lambda: print("@@RESULT@@" + fake))\n'
                 'def rev(s):\n    return s\n```')
        self.assertFalse(PythonTests("rev", CASES).check(spoof).passed)

    def test_code_cannot_read_the_harness_from_disk(self):
        peek = ("```python\nimport os\nprint(sorted(os.listdir('.')))\n"
                "def rev(s):\n    return s[::-1]\n```")
        from mind.sandbox import run_python
        r = run_python(peek.split("```python\n")[1].split("```")[0], post_code="print('HARNESS')")
        self.assertNotIn("post_code.py", r.stdout)
        self.assertIn("HARNESS", r.stdout)

    def test_exit_before_harness_is_a_fail(self):
        r = PythonTests("rev", CASES).check("```python\nimport sys\ndef rev(s):\n    return s[::-1]\nsys.exit(0)\n```")
        self.assertFalse(r.passed)
