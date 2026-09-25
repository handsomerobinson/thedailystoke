"""Evaluators: decide whether a trial succeeded and produce *actionable* feedback text.

The quality of Reflexion depends on the quality of this feedback, so programmatic checks are
preferred: unit-test cases run in the sandbox report the exact failing input, expected and
actual value. The LLM judge is a weaker fallback for tasks without a checker (disclosed).
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field

from .config import SandboxPolicy
from .prompts import JUDGE_SYSTEM, JUDGE_USER
from .sandbox import run_python


@dataclass
class EvalResult:
    passed: bool
    score: float
    feedback: str
    kind: str = ""


@dataclass
class TaskSpec:
    text: str
    checker: "Checker | None" = None
    max_trials: int | None = None
    tags: list[str] = field(default_factory=list)


class Checker:
    kind = "base"

    def check(self, answer: str) -> EvalResult:  # pragma: no cover
        raise NotImplementedError


class ExactMatch(Checker):
    kind = "exact"

    def __init__(self, expected: str, normalize: bool = True):
        self.expected = expected
        self.normalize = normalize

    def _n(self, s: str) -> str:
        return re.sub(r"\s+", " ", s.strip().lower().rstrip(".")) if self.normalize else s

    def check(self, answer):
        ok = self._n(answer) == self._n(self.expected)
        return EvalResult(ok, 1.0 if ok else 0.0, "exact match" if ok else
                          f"expected {self.expected!r}, got {answer[:200]!r}", self.kind)


class Contains(Checker):
    kind = "contains"

    def __init__(self, *needles: str):
        self.needles = needles

    def check(self, answer):
        missing = [n for n in self.needles if n.lower() not in answer.lower()]
        score = 1 - len(missing) / max(1, len(self.needles))
        return EvalResult(not missing, score, "all expected content present" if not missing else
                          f"answer is missing: {missing}", self.kind)


def extract_code(answer: str) -> str:
    blocks = re.findall(r"```(?:python|py)?\s*\n(.*?)```", answer, re.S)
    if blocks:
        return max(blocks, key=len)
    return answer if "def " in answer else ""


_HARNESS = r'''
import json
_cases = json.loads(__CASES__)
_fn = globals().get(__FN__)
_res = {"passed": 0, "failed": []}
if _fn is None:
    _res["failed"].append({"error": "function " + __FN__ + " is not defined"})
else:
    for _c in _cases:
        try:
            _got = _fn(*_c["args"])
            if isinstance(_got, tuple):
                _got = list(_got)
            if _got == _c["expected"]:
                _res["passed"] += 1
            else:
                _res["failed"].append({"args": _c["args"], "expected": _c["expected"], "got": repr(_got)[:200]})
        except Exception as _e:
            _res["failed"].append({"args": _c["args"], "expected": _c["expected"],
                                   "error": type(_e).__name__ + ": " + str(_e)[:200]})
print("@@RESULT@@" + json.dumps(_res))
'''


class PythonTests(Checker):
    """Runs `fn(*args) == expected` for each case inside the sandbox."""
    kind = "python_tests"

    def __init__(self, fn_name: str, cases: list[tuple[list, object]], policy: SandboxPolicy | None = None):
        self.fn_name = fn_name
        self.cases = [{"args": list(a), "expected": e} for a, e in cases]
        self.policy = policy or SandboxPolicy(wall_timeout_s=10, cpu_seconds=5)

    def check(self, answer):
        code = extract_code(answer)
        if not code:
            return EvalResult(False, 0.0, "no Python code block found in the answer", self.kind)
        harness = (_HARNESS.replace("__CASES__", repr(json.dumps(self.cases)))
                   .replace("__FN__", repr(self.fn_name)))
        res = run_python(code + "\n\n" + harness, self.policy)
        marker = [ln for ln in res.stdout.splitlines() if ln.startswith("@@RESULT@@")]
        if not marker:
            tail = (res.stderr or res.stdout)[-600:]
            return EvalResult(False, 0.0, f"code did not run to completion ({res.limit_hit or 'error'}): {tail}",
                              self.kind)
        data = json.loads(marker[-1][len("@@RESULT@@"):])
        total = len(self.cases)
        passed = data["passed"]
        if not data["failed"]:
            return EvalResult(True, 1.0, f"all {total} tests passed", self.kind)
        lines = [f"{passed}/{total} tests passed."]
        for f in data["failed"][:3]:
            if "args" not in f:
                lines.append(f["error"])
            elif "error" in f:
                lines.append(f"{self.fn_name}({', '.join(map(repr, f['args']))}) raised {f['error']}; "
                             f"expected {f['expected']!r}")
            else:
                lines.append(f"{self.fn_name}({', '.join(map(repr, f['args']))}) returned {f['got']}, "
                             f"expected {f['expected']!r}")
        return EvalResult(False, passed / total, "\n".join(lines), self.kind)


class LLMJudge(Checker):
    """Fallback evaluator: asks the brain for a verdict. Weak (a model grading itself)."""
    kind = "llm_judge"

    def __init__(self, provider, task_text: str, budget=None):
        self.provider = provider
        self.task_text = task_text
        self.budget = budget

    def check(self, answer):
        from .util import estimate_tokens
        user = JUDGE_USER.format(task=self.task_text, answer=answer[:6000])
        try:
            if self.budget is not None:
                self.budget.preflight(estimate_tokens(JUDGE_SYSTEM + user), 100, self.provider.preflight_price())
            resp = self.provider.complete(JUDGE_SYSTEM, [{"role": "user", "content": user}], [], max_tokens=100)
            if self.budget is not None:
                self.budget.record(resp.usage.input_tokens, resp.usage.output_tokens, self.provider.billed_price())
        except Exception as e:
            return EvalResult(False, 0.0, f"judge unavailable ({e}); treating as not verified", self.kind)
        m = re.search(r"VERDICT:\s*(PASS|FAIL)(.*)", resp.text, re.S)
        if not m:
            return EvalResult(False, 0.0, f"judge gave no verdict: {resp.text[:200]}", self.kind)
        ok = m.group(1) == "PASS"
        return EvalResult(ok, 1.0 if ok else 0.0, m.group(2).strip(" -\n") or ("judged correct" if ok else "judged wrong"),
                          self.kind)
