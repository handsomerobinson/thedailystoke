"""Reflexion (Shinn et al., arXiv:2303.11366): trial -> evaluate -> reflect -> remember -> retry.

No weights change. Improvement lives entirely in language:
  1. Before trial 1, lessons/reflections from earlier sessions are retrieved from memory.
  2. After a failed trial, the brain writes a short verbal self-reflection from the task, its
     answer, its tool trajectory and the evaluator's concrete feedback.
  3. The reflection is stored in the user's memory (keyed by a task signature + indexed for
     similarity search) and injected into the next trial's system prompt.
  4. Credit assignment on the reflections themselves: reflections that were in the prompt
     of a trial that PASSED get +helpful, and the most recent one is promoted to a durable
     `lesson`; old reflections that were read by a trial that still FAILED get +harmful and
     sink in retrieval (and are filtered out after repeated harm).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .agent import Agent, Trajectory
from .cost import Budget, BudgetExceeded
from .evaluator import EvalResult, LLMJudge, TaskSpec
from .prompts import REFLECT_SYSTEM, REFLECT_USER
from .util import estimate_tokens, sha256_hex, tokenize, truncate


def task_signature(text: str) -> str:
    """Order-insensitive signature of the task's content words (same task, reworded -> often same sig)."""
    toks = sorted(set(tokenize(text)))[:24]
    return sha256_hex(" ".join(toks))[:16]


@dataclass
class TrialRecord:
    n: int
    answer: str
    status: str
    eval: EvalResult | None
    reflection: str = ""
    reflection_source: str = ""   # "llm" | "heuristic" | ""
    lessons_in_prompt: int = 0
    cost_usd: float = 0.0


@dataclass
class SolveResult:
    task: str
    success: bool
    answer: str
    trials: list[TrialRecord] = field(default_factory=list)
    budget: dict = field(default_factory=dict)
    stopped_reason: str = ""

    def report(self) -> str:
        lines = [f"task: {truncate(self.task, 120)}",
                 f"result: {'SUCCESS' if self.success else 'FAILED'} after {len(self.trials)} trial(s)"
                 + (f" ({self.stopped_reason})" if self.stopped_reason else ""),
                 f"cost: ${self.budget.get('spent_usd', 0):.5f} of ${self.budget.get('limit_usd', 0):.2f} cap"]
        for t in self.trials:
            ev = t.eval.feedback.splitlines()[0] if t.eval and t.eval.feedback else t.status
            lines.append(f"  trial {t.n}: {'PASS' if t.eval and t.eval.passed else 'FAIL'} "
                         f"(lessons in prompt: {t.lessons_in_prompt}) — {truncate(ev, 140)}")
            if t.reflection:
                lines.append(f"    reflection[{t.reflection_source}]: {truncate(t.reflection, 220)}")
        return "\n".join(lines)


class ReflexionRunner:
    def __init__(self, agent: Agent, memory, config, reflect_provider=None):
        self.agent = agent
        self.memory = memory
        self.config = config
        self.reflect_provider = reflect_provider or agent.provider

    def reflect(self, task: TaskSpec, traj: Trajectory, ev: EvalResult, previous: list[str],
                budget: Budget) -> tuple[str, str]:
        user = REFLECT_USER.format(task=truncate(task.text, 2000), answer=truncate(traj.answer or "(none)", 3000),
                                   trajectory=traj.render(1500), feedback=truncate(ev.feedback, 1500),
                                   previous="\n".join(f"- {p}" for p in previous) or "(none)")
        try:
            budget.preflight(estimate_tokens(REFLECT_SYSTEM + user), 300, self.reflect_provider.preflight_price())
            resp = self.reflect_provider.complete(REFLECT_SYSTEM, [{"role": "user", "content": user}], [], 300)
            budget.record(resp.usage.input_tokens, resp.usage.output_tokens, self.reflect_provider.billed_price())
            text = resp.text.strip()
            if text:
                return truncate(text, 600), "llm"
        except BudgetExceeded:
            raise
        except Exception:
            pass
        # Degraded path: no brain available for reflection -> a templated note built from the
        # evaluator's feedback. Clearly labelled; still better than nothing.
        first = next((ln for ln in ev.feedback.splitlines() if ln.strip()), "unknown failure")
        return (f"Previous attempt failed: {truncate(first, 300)}. Do not repeat the same answer; "
                f"address this failing case directly.", "heuristic")

    def solve(self, task: TaskSpec, budget: Budget, headless: bool = False, job_id: str = "") -> SolveResult:
        sig = task_signature(task.text)
        max_trials = task.max_trials or self.config.max_trials
        session_reflections: list[str] = []
        result = SolveResult(task=task.text, success=False, answer="")
        checker = task.checker or LLMJudge(self.agent.provider, task.text, budget)

        for n in range(1, max_trials + 1):
            spent_before = budget.spent_usd
            traj = self.agent.run_trial(task.text, budget, lessons=session_reflections, headless=headless,
                                        job_id=job_id, task_sig=sig)
            rec = TrialRecord(n, traj.answer, traj.status, None,
                              lessons_in_prompt=len(session_reflections) + len(traj.injected_ids))
            result.trials.append(rec)
            if traj.status in ("budget_exceeded", "provider_error", "error"):
                rec.cost_usd = budget.spent_usd - spent_before
                result.stopped_reason = f"{traj.status}: {traj.reason}"
                break
            if traj.status != "answered":
                ev = EvalResult(False, 0.0, f"trial ended without an answer ({traj.status}: {traj.reason})", "agent")
            else:
                try:
                    ev = checker.check(traj.answer)
                except Exception as e:
                    ev = EvalResult(False, 0.0, f"evaluator crashed: {e}", "error")
            rec.eval = ev
            # Credit assignment only for lessons about THIS task (same signature). Cross-task
            # lessons pulled in by similarity get no credit/blame: we cannot tell if they mattered.
            retrieved = [i for i in traj.injected_ids if self._sig_of(i) == sig]
            if ev.passed:
                result.success, result.answer = True, traj.answer
                for i in retrieved:
                    self._safe(self.memory.feedback, i, True)
                if n > 1 and session_reflections:
                    # the reflection that led to success becomes a durable lesson
                    self._promote(session_reflections[-1], sig, task)
                rec.cost_usd = budget.spent_usd - spent_before
                break
            for i in retrieved:  # read an old lesson and still failed -> it did not help
                self._safe(self.memory.feedback, i, False)
            if n == max_trials:
                rec.cost_usd = budget.spent_usd - spent_before
                result.answer = traj.answer
                result.stopped_reason = "max trials reached"
                break
            try:
                text, source = self.reflect(task, traj, ev, session_reflections, budget)
            except BudgetExceeded as e:
                rec.cost_usd = budget.spent_usd - spent_before
                result.stopped_reason = f"budget_exceeded during reflection: {e}"
                result.answer = traj.answer
                break
            rec.reflection, rec.reflection_source = text, source
            session_reflections.append(text)
            self._safe(self.memory.add_item, "reflection", text, " ".join(task.tags), sig, 0.6)
            rec.cost_usd = budget.spent_usd - spent_before

        outcome = "succeeded" if result.success else "failed"
        self._safe(self.memory.add_item, "episode",
                   f"Task '{truncate(task.text, 160)}' {outcome} after {len(result.trials)} trial(s)."
                   + (f" Final answer: {truncate(result.answer, 200)}" if result.answer else ""),
                   " ".join(task.tags), sig, 0.4)
        result.budget = budget.summary()
        return result

    # helpers ---------------------------------------------------------------------------
    def _sig_of(self, item_id: int) -> str:
        try:
            it = self.memory.get_item(item_id)
            return it["task_sig"] if it else ""
        except Exception:
            return ""

    def _promote(self, text: str, sig: str, task: TaskSpec):
        existing = [i for i in self.memory.items(kind="lesson", task_sig=sig) if i["text"] == text]
        if existing:
            self._safe(self.memory.feedback, existing[0]["id"], True)
            return
        lid = self._safe(self.memory.add_item, "lesson", "LESSON (validated): " + text, " ".join(task.tags), sig, 0.9)
        if lid:
            self._safe(self.memory.feedback, lid, True)

    @staticmethod
    def _safe(fn, *args):
        try:
            return fn(*args)
        except Exception:
            return None
