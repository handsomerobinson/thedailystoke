"""The act loop for ONE trial: prompt (with memory) -> LLM -> tool calls -> ... -> final answer.

Guarantees:
* never raises: every failure becomes a Trajectory with a status and a reason;
* bounded: max_steps, repeated-identical-call detector, per-task budget checked pre-flight;
* memory-aware: user facts, lessons/reflections and relevant episodes are injected into the
  system prompt under a fixed character budget (efficiency: we do not stuff the context).
"""
from __future__ import annotations

import datetime as _dt
import json
from dataclasses import dataclass, field

from .cost import Budget, BudgetExceeded
from .prompts import AGENT_SYSTEM, EPISODES_HEADER, FACTS_HEADER, LESSONS_HEADER, NOTICE_HEADER
from .providers.base import Provider, ProviderError
from .tools.base import ToolContext, ToolRegistry
from .util import canonical_json, estimate_tokens, new_id, truncate


@dataclass
class Step:
    kind: str                 # "llm" | "tool"
    detail: str
    ok: bool = True


@dataclass
class Trajectory:
    task: str
    answer: str = ""
    status: str = "running"   # answered | budget_exceeded | step_limit | loop_detected | provider_error | error
    reason: str = ""
    steps: list[Step] = field(default_factory=list)
    messages: list[dict] = field(default_factory=list)
    injected_ids: list[int] = field(default_factory=list)   # lessons/reflections retrieved from memory
    episode_ids: list[int] = field(default_factory=list)
    tool_calls: int = 0
    denied: int = 0

    @property
    def finished(self) -> bool:
        return self.status == "answered"

    def render(self, limit: int = 1500) -> str:
        return truncate("\n".join(f"[{s.kind}{'' if s.ok else ' FAILED'}] {s.detail}" for s in self.steps), limit)


class Agent:
    def __init__(self, provider: Provider, registry: ToolRegistry, memory, config, clock, scheduler=None):
        self.provider = provider
        self.registry = registry
        self.memory = memory
        self.config = config
        self.clock = clock
        self.scheduler = scheduler

    # ---- context ------------------------------------------------------------------------
    def build_system(self, task: str, extra_lessons: list[str], headless: bool,
                     task_sig: str = "", notices: list[str] | None = None) -> tuple[str, list[int], list[int]]:
        """Returns (system prompt, ids of injected lessons/reflections, ids of injected episodes)."""
        now = _dt.datetime.fromtimestamp(self.clock.now(), _dt.timezone.utc).strftime("%Y-%m-%d %H:%M")
        parts = [AGENT_SYSTEM.format(user=self.memory.user_id, now=now,
                                     mode="headless (no human present)" if headless else "interactive")]
        budget = self.config.memory_context_chars
        used_ids: list[int] = []
        episode_ids: list[int] = []

        facts = self.memory.facts(limit=20)
        if facts:
            block = FACTS_HEADER + "\n" + "\n".join(f"- {k}: {v}" for k, v in facts.items())
            block = truncate(block, budget // 3)
            parts.append(block)
            budget -= len(block)

        lessons = list(dict.fromkeys(extra_lessons))  # this-session reflections first, deduped
        try:
            for h in self.memory.search(task, kinds=["lesson", "reflection"], k=5, task_sig=task_sig or None):
                if h.text not in lessons:
                    lessons.append(h.text)
                    used_ids.append(h.id)
        except Exception:
            pass
        if lessons:
            block = LESSONS_HEADER + "\n" + "\n".join(f"- {t}" for t in lessons)
            block = truncate(block, max(300, budget // 2))
            parts.append(block)
            budget -= len(block)

        try:
            eps = self.memory.search(task, kinds=["episode"], k=3)
        except Exception:
            eps = []
        if eps and budget > 200:
            block = EPISODES_HEADER + "\n" + "\n".join(f"- {truncate(e.text, 300)}" for e in eps)
            parts.append(truncate(block, budget))
            episode_ids.extend(e.id for e in eps)
        if notices:
            parts.append(NOTICE_HEADER + "\n" + "\n".join(f"- {n}" for n in notices))
        return "\n\n".join(parts), used_ids, episode_ids

    # ---- the loop -----------------------------------------------------------------------
    def run_trial(self, task: str, budget: Budget, lessons: list[str] | None = None, headless: bool = False,
                  job_id: str = "", task_id: str = "", task_sig: str = "", notices: list[str] | None = None) -> Trajectory:
        traj = Trajectory(task=task)
        task_id = task_id or new_id("task_")
        try:
            system, used, eps = self.build_system(task, lessons or [], headless, task_sig, notices)
        except Exception as e:  # memory trouble must not kill the trial
            system, used, eps = AGENT_SYSTEM.format(user=self.memory.user_id, now="?", mode="degraded"), [], []
            traj.steps.append(Step("memory", f"context build failed, continuing without memory: {e}", False))
        traj.injected_ids = used
        traj.episode_ids = eps
        try:
            self.memory.mark_used(used + eps)
        except Exception:
            pass
        messages: list[dict] = [{"role": "user", "content": task}]
        traj.messages = messages
        ctx = ToolContext(user=self.memory.user_id, memory=self.memory, config=self.config, clock=self.clock,
                          task_id=task_id, headless=headless, job_id=job_id, scheduler=self.scheduler)
        specs = self.registry.specs()
        tools_chars = len(json.dumps([s.__dict__ for s in specs]))
        seen_calls: dict[str, int] = {}
        try:
            for step in range(self.config.max_steps):
                prompt_chars = len(system) + tools_chars + sum(len(str(m.get("content", ""))) +
                                                               len(json.dumps(m.get("tool_calls", []))) for m in messages)
                budget.preflight(estimate_tokens("x" * prompt_chars), self.config.max_output_tokens,
                                 self.provider.preflight_price())
                resp = self.provider.complete(system, messages, specs, max_tokens=self.config.max_output_tokens)
                cost = budget.record(resp.usage.input_tokens, resp.usage.output_tokens, self.provider.billed_price())
                traj.steps.append(Step("llm", f"{resp.provider or self.provider.name} {resp.stop_reason} "
                                              f"in={resp.usage.input_tokens} out={resp.usage.output_tokens} "
                                              f"${cost:.5f}"))
                messages.append({"role": "assistant", "content": resp.text,
                                 "tool_calls": [tc.to_dict() for tc in resp.tool_calls], "raw": resp.raw})
                if not resp.tool_calls:
                    traj.answer = resp.text
                    traj.status = "answered" if resp.stop_reason != "refusal" else "refused"
                    return traj
                for tc in resp.tool_calls:
                    key = tc.name + canonical_json(tc.arguments)
                    seen_calls[key] = seen_calls.get(key, 0) + 1
                    if seen_calls[key] >= 3:
                        traj.status, traj.reason = "loop_detected", f"identical call {tc.name} repeated 3x"
                        traj.steps.append(Step("tool", traj.reason, False))
                        return traj
                    result = self.registry.execute(tc, ctx)
                    traj.tool_calls += 1
                    traj.denied += int(result.denied)
                    traj.steps.append(Step("tool", f"{tc.name}({truncate(canonical_json(tc.arguments), 160)}) -> "
                                                   f"{truncate(result.content, 200)}", result.ok))
                    content = result.content
                    if seen_calls[key] == 2:
                        content += "\n[notice: you already made this exact call; do something different]"
                    messages.append({"role": "tool", "tool_call_id": tc.id, "name": tc.name,
                                     "content": truncate(content, self.config.tool_output_chars),
                                     "is_error": not result.ok})
            traj.status, traj.reason = "step_limit", f"no final answer after {self.config.max_steps} steps"
        except BudgetExceeded as e:
            traj.status, traj.reason = "budget_exceeded", str(e)
        except ProviderError as e:
            traj.status, traj.reason = "provider_error", f"brain unavailable: {e}"
        except Exception as e:  # last line of defence: the loop never crashes the caller
            traj.status, traj.reason = "error", f"{type(e).__name__}: {e}"
        traj.steps.append(Step("stop", f"{traj.status}: {traj.reason}", False))
        return traj
