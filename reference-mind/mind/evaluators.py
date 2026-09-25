"""Evaluators turn an answer into (success, score, feedback).

Feedback is the raw material of reflection, so every evaluator explains
*what* was wrong as specifically as it can without leaking the answer key
(numeric evaluators say "too high/too low", not the expected value, unless
reveal=True).  An evaluator that crashes returns a failure, never a pass.
"""
from __future__ import annotations

import json
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from .tools.sandbox import run_python

_NUM = re.compile(r"-?\d+(?:,\d{3})*(?:\.\d+)?")


@dataclass
class Evaluation:
    success: bool
    score: float
    feedback: str


class Evaluator(ABC):
    name = "evaluator"

    def __call__(self, answer: str, task: str = "") -> Evaluation:
        try:
            return self.evaluate(answer or "", task)
        except Exception as exc:  # noqa: BLE001
            return Evaluation(False, 0.0, f"evaluator error ({type(exc).__name__}: {exc}); treated as failure")

    @abstractmethod
    def evaluate(self, answer: str, task: str) -> Evaluation: ...

    def to_dict(self) -> dict[str, Any]:
        return {"type": self.name, **{k: v for k, v in vars(self).items() if not k.startswith("_")}}


def numbers_in(text: str) -> list[float]:
    return [float(x.replace(",", "")) for x in _NUM.findall(text)]


class NumericAnswer(Evaluator):
    """Pass if any number in the answer is within tol of expected."""

    name = "numeric"

    def __init__(self, expected: float, tol: float = 1e-6, reveal: bool = False):
        self.expected, self.tol, self.reveal = float(expected), tol, reveal

    def evaluate(self, answer: str, task: str) -> Evaluation:
        nums = numbers_in(answer)
        if not nums:
            return Evaluation(False, 0.0, "the answer contains no number")
        if any(abs(n - self.expected) <= self.tol for n in nums):
            return Evaluation(True, 1.0, "correct")
        main = nums[0]
        direction = "too high" if main > self.expected else "too low"
        extra = f" (expected {self.expected:g})" if self.reveal else ""
        return Evaluation(False, 0.0, f"answer {main:g} is wrong: {direction}{extra}")


class ContainsAll(Evaluator):
    name = "contains"

    def __init__(self, terms: list[str], case_sensitive: bool = False):
        self.terms, self.case_sensitive = list(terms), case_sensitive

    def evaluate(self, answer: str, task: str) -> Evaluation:
        hay = answer if self.case_sensitive else answer.lower()
        missing = [t for t in self.terms if (t if self.case_sensitive else t.lower()) not in hay]
        if not missing:
            return Evaluation(True, 1.0, "all required terms present")
        return Evaluation(False, 1 - len(missing) / len(self.terms), f"missing required content: {missing}")


class RegexMatch(Evaluator):
    name = "regex"

    def __init__(self, pattern: str):
        self.pattern = pattern

    def evaluate(self, answer: str, task: str) -> Evaluation:
        ok = re.search(self.pattern, answer, re.S) is not None
        return Evaluation(ok, float(ok), "matches" if ok else f"answer does not match /{self.pattern}/")


class PythonFunctionTests(Evaluator):
    """Extract the python code block from the answer, run test cases in the sandbox."""

    name = "python_tests"

    def __init__(self, func: str, cases: list[tuple[list[Any], Any]]):
        self.func = func
        self.cases = [(list(a), e) for a, e in cases]

    def evaluate(self, answer: str, task: str) -> Evaluation:
        m = re.search(r"```(?:python)?\n(.*?)```", answer, re.S)
        code = m.group(1) if m else answer
        harness = code + "\n\nimport json as _j\n_cases = _j.loads(" + repr(json.dumps(self.cases)) + ")\n_fails = []\n" \
            "for _args, _exp in _cases:\n    try:\n        _got = " + self.func + "(*_args)\n    except Exception as _e:\n" \
            "        _got = 'raised ' + type(_e).__name__\n    if _got != _exp:\n" \
            "        _fails.append({'args': _args, 'expected': _exp, 'got': _got})\n" \
            "print('RESULT', _j.dumps({'failed': _fails, 'total': len(_cases)}, default=str))\n"
        res = run_python(harness, timeout=10)
        out = re.search(r"RESULT (.+)", res.stdout)
        if not out:
            return Evaluation(False, 0.0, f"code did not run: {(res.stderr or res.stdout)[-400:]}")
        data = json.loads(out.group(1))
        fails, total = data["failed"], data["total"]
        if not fails:
            return Evaluation(True, 1.0, f"all {total} tests passed")
        shown = "; ".join(f"{self.func}(*{f['args']!r}) returned {f['got']!r}, expected {f['expected']!r}" for f in fails[:3])
        return Evaluation(False, 1 - len(fails) / total, f"{len(fails)}/{total} tests failed: {shown}")


class JudgeEvaluator(Evaluator):
    """LLM-as-judge.  Only as good as the judging brain (the mock judge is shallow)."""

    name = "judge"

    def __init__(self, brain, rubric: str = "Does the answer correctly and fully address the task?", budget=None):
        self._brain, self.rubric, self._budget = brain, rubric, budget

    def evaluate(self, answer: str, task: str) -> Evaluation:
        from .types import Message
        system = "MODE: JUDGE\nYou grade answers strictly. Reply 'VERDICT: PASS' or 'VERDICT: FAIL' then 'REASON: ...'."
        msg = Message("user", f"RUBRIC: {self.rubric}\nTASK: {task}\nANSWER: {answer}")
        if self._budget is not None:
            self._budget.check_brain_call(len(system + msg.content) // 4, 200, self._brain.model)
        resp = self._brain.complete(system, [msg], [], 200)
        if self._budget is not None:
            self._budget.charge_brain(resp.usage, resp.model)
        ok = "VERDICT: PASS" in resp.text.upper()
        reason = re.search(r"REASON:\s*(.+)", resp.text, re.S)
        return Evaluation(ok, float(ok), reason.group(1).strip()[:400] if reason else resp.text[:400])


def evaluator_from_dict(d: dict[str, Any] | None) -> Evaluator | None:
    """Rebuild an evaluator from a stored job spec (JSON-safe types only)."""
    if not d:
        return None
    kind = d.get("type")
    if kind == "numeric":
        return NumericAnswer(d["expected"], d.get("tol", 1e-6), d.get("reveal", False))
    if kind == "contains":
        return ContainsAll(d["terms"], d.get("case_sensitive", False))
    if kind == "regex":
        return RegexMatch(d["pattern"])
    if kind == "python_tests":
        return PythonFunctionTests(d["func"], d["cases"])
    raise ValueError(f"unknown evaluator type {kind!r}")
