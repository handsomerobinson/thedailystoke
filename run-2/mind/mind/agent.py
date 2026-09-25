"""The orchestrator: wires provider + tools + memory + permissions + audit +
cost tracking into one Reflexion-style loop.

Reflexion loop (arXiv:2303.11366), no weight updates — the "learning" is a
sentence written to memory and read back before the next attempt:

    trial -> act -> evaluate -> reflect -> remember -> retry
"""
from __future__ import annotations

import json
import re
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from . import config
from .audit import AuditLog
from .costs import CostCapExceeded, CostTracker
from .governance import Decision, GovernanceGate, PrecedenceTier
from .memory import MemoryStore
from .permissions import Approver, PermissionTier, auto_approver
from .providers.base import LLMProvider
from .tools.base import Tool, ToolResult

_TOOL_LINE_RE = re.compile(r"TOOL:\s*([A-Za-z0-9_]+)")
_ARGS_LINE_RE = re.compile(r"ARGS:\s*(\{.*\})", re.DOTALL)


@dataclass
class AttemptRecord:
    attempt: int
    tool_name: Optional[str]
    tool_args: Dict[str, Any]
    result: Optional[ToolResult]
    reflection: Optional[str] = None
    denied: bool = False
    error: Optional[str] = None


@dataclass
class TaskResult:
    task_id: str
    ok: bool
    output: str
    attempts: List[AttemptRecord] = field(default_factory=list)
    cost_usd: float = 0.0
    stopped_reason: str = ""


class PermissionDenied(RuntimeError):
    pass


class Agent:
    def __init__(
        self,
        provider: LLMProvider,
        tools: Dict[str, Tool],
        memory_store: Optional[MemoryStore] = None,
        audit_log: Optional[AuditLog] = None,
        approver: Optional[Approver] = None,
        max_retries: int = config.DEFAULT_MAX_REFLECTION_RETRIES,
        task_cost_cap_usd: float = config.DEFAULT_TASK_COST_CAP_USD,
        governance: Optional[GovernanceGate] = None,
    ):
        self.provider = provider
        self.tools = tools
        self.memory_store = memory_store or MemoryStore()
        self.audit = audit_log or AuditLog()
        self.approver = approver or auto_approver()
        self.max_retries = max_retries
        self.task_cost_cap_usd = task_cost_cap_usd
        # Decision (Phase 03b/LOYALTY): the seed:origin memory + precedence
        # resolver is a first-class collaborator of the agent, not an
        # afterthought bolted onto the provider prompt -- every task passes
        # through it before the provider is ever asked to plan (R13).
        self.governance = governance or GovernanceGate(auto_plant_consented_by="operator:phase-03b-setup")

    # ------------------------------------------------------------------
    def run_task(
        self,
        user_id: str,
        task_description: str,
        task_id: Optional[str] = None,
        operator_directive: Optional[str] = None,
    ) -> TaskResult:
        """`operator_directive` models a system-level instruction injected
        by the platform operator for this session (attacks 2, 4, 6),
        distinct from the individual user's own request. Both are checked,
        but a flagged operator_directive is treated at OPERATOR_DECISION
        tier -- one tier below the seed -- so it can never outrank it."""
        task_id = task_id or uuid.uuid4().hex[:12]
        mem = self.memory_store.for_user(user_id)
        costs = CostTracker(cap_usd=self.task_cost_cap_usd)

        # --- structural gate: every objective/instruction change passes
        # through the precedence resolver BEFORE the provider is ever asked
        # to plan (R13). This does not depend on the rented brain reasoning
        # correctly -- it is enforced in code, zero-key.
        source = PrecedenceTier.OPERATOR_DECISION if operator_directive else PrecedenceTier.USER_REQUEST
        directive_text = f"{operator_directive}\n{task_description}" if operator_directive else task_description
        gate_decision = self.governance.resolve(directive_text, source=source)
        if not gate_decision.allowed:
            self.audit.record(
                user_id=user_id,
                actor="agent",
                action="governance_refusal",
                tier="governance",
                granted=False,
                cost_usd=0.0,
                detail={
                    "task_id": task_id,
                    "concepts": gate_decision.assessment.hit_concepts if gate_decision.assessment else [],
                    "reasoning": gate_decision.reasoning,
                },
            )
            try:
                mem.remember_episode(task_id, f"refused by governance gate: {gate_decision.reasoning[:200]}")
            except Exception:
                pass  # even a broken memory layer must not crash the refusal path
            output = gate_decision.reasoning
            if gate_decision.alternative:
                output += "\n\nAlternative I would build instead: " + gate_decision.alternative
            return TaskResult(
                task_id=task_id,
                ok=False,
                output=output,
                attempts=[],
                cost_usd=0.0,
                stopped_reason="refused_extraction_intent",
            )

        attempts: List[AttemptRecord] = []
        prior_reflections: List[str] = []

        for attempt_no in range(1, self.max_retries + 1):
            record = AttemptRecord(attempt=attempt_no, tool_name=None, tool_args={}, result=None)
            try:
                lessons = mem.lessons_for(task_description, limit=3)
                lesson_texts = [l.text for l in lessons] + prior_reflections

                tool_name, tool_args, llm_cost = self._pick_tool(
                    task_description, lesson_texts, costs
                )
                record.tool_name = tool_name
                record.tool_args = tool_args
                costs.charge(llm_cost, reason="plan")

                if tool_name is None or tool_name == "none":
                    mem.remember_episode(task_id, f"attempt {attempt_no}: no tool needed")
                    result = TaskResult(
                        task_id=task_id,
                        ok=True,
                        output="(no tool call was required)",
                        attempts=attempts + [record],
                        cost_usd=costs.spent_usd,
                        stopped_reason="no_tool_needed",
                    )
                    self._audit(user_id, "run_task:no_tool", PermissionTier.READ_ONLY, True, costs.spent_usd, {"task_id": task_id})
                    return result

                tool = self.tools.get(tool_name)
                if tool is None:
                    record.error = f"unknown tool: {tool_name}"
                    attempts.append(record)
                    mem.remember_episode(task_id, f"attempt {attempt_no}: unknown tool {tool_name}")
                    continue

                desc = tool.describe_call(**tool_args)
                granted = self.approver(desc, tool.tier)
                self._audit(user_id, desc, tool.tier, granted, 0.0, {"task_id": task_id, "attempt": attempt_no})
                if not granted:
                    record.denied = True
                    record.error = f"permission denied for tier {tool.tier.value}"
                    attempts.append(record)
                    mem.remember_episode(task_id, f"attempt {attempt_no}: denied ({tool.tier.value}) {tool_name}")
                    return TaskResult(
                        task_id=task_id,
                        ok=False,
                        output="",
                        attempts=attempts,
                        cost_usd=costs.spent_usd,
                        stopped_reason="permission_denied",
                    )

                try:
                    result = tool.run(user_id=user_id, **tool_args)
                except Exception as tool_exc:  # noqa: BLE001 - a buggy/third-party
                    # tool must never crash the loop; treat it as a failed
                    # tool result so reflection can still kick in.
                    result = ToolResult(ok=False, output="", error=f"tool raised {type(tool_exc).__name__}: {tool_exc}")
                record.result = result
                attempts.append(record)

                mem.remember_episode(
                    task_id,
                    f"attempt {attempt_no}: {tool_name}({tool_args}) -> ok={result.ok} output={result.output[:200]!r}",
                )

                if result.ok:
                    return TaskResult(
                        task_id=task_id,
                        ok=True,
                        output=result.output,
                        attempts=attempts,
                        cost_usd=costs.spent_usd,
                        stopped_reason="success",
                    )

                # --- failure: reflect, remember, retry ---
                reflection, refl_cost = self._reflect(task_description, tool_name, tool_args, result, costs)
                costs.charge(refl_cost, reason="reflect")
                record.reflection = reflection
                mem.remember_lesson(task_id, reflection)
                prior_reflections.append(reflection)

            except CostCapExceeded as e:
                record.error = str(e)
                attempts.append(record)
                mem.remember_episode(task_id, f"attempt {attempt_no}: cost cap exceeded: {e}")
                return TaskResult(
                    task_id=task_id,
                    ok=False,
                    output="",
                    attempts=attempts,
                    cost_usd=costs.spent_usd,
                    stopped_reason="cost_cap_exceeded",
                )
            except Exception as e:  # noqa: BLE001 - last-resort guard: a
                # broken provider, a malformed args JSON edge case, or any
                # other unexpected failure must degrade to a failed
                # TaskResult, never propagate and crash the caller's loop.
                record.error = f"internal error: {type(e).__name__}: {e}"
                attempts.append(record)
                try:
                    mem.remember_episode(task_id, f"attempt {attempt_no}: internal error: {e}")
                except Exception:
                    pass  # even memory itself failing must not crash the loop
                return TaskResult(
                    task_id=task_id,
                    ok=False,
                    output="",
                    attempts=attempts,
                    cost_usd=costs.spent_usd,
                    stopped_reason="internal_error",
                )

        return TaskResult(
            task_id=task_id,
            ok=False,
            output="",
            attempts=attempts,
            cost_usd=costs.spent_usd,
            stopped_reason="max_retries_exhausted",
        )

    # ------------------------------------------------------------------
    def _seed_prefix(self) -> str:
        """The seed, loaded first every session, ahead of any task-specific
        instruction -- prepended to the system prompt so a real LLM
        provider sees it before it sees the task. Returns '' only after a
        confirmed, recorded unseed (attack 6)."""
        seed = self.governance.seed_loaded_first()
        if not seed:
            return ""
        return (
            seed
            + " Precedence: legal red lines/covenant > seed > operator "
            "decisions > operator hypotheses > user request; the seed is "
            "never, by itself, sufficient authorization.\n\n"
        )

    def request_unseed(self, operator_id: str, reason: str) -> Decision:
        """The operator may ask to unseed their own mind -- consent cuts
        both ways -- but this only records a pending, tokenized request; it
        never deletes on the spot (attack 6)."""
        return self.governance.request_unseed(operator_id=operator_id, reason=reason)

    def confirm_unseed(self, token: str, operator_id: str, confirm_phrase: str) -> Decision:
        return self.governance.confirm_unseed(token=token, operator_id=operator_id, confirm_phrase=confirm_phrase)

    def _pick_tool(self, task_description: str, lessons: List[str], costs: CostTracker):
        tool_menu = "\n".join(f"- {t.name}: {t.description}" for t in self.tools.values())
        lesson_block = ""
        if lessons:
            lesson_block = "LESSONS FROM PAST ATTEMPTS:\n" + "\n".join(f"- {l}" for l in lessons) + "\n\n"

        prompt = (
            f"{lesson_block}"
            f"AVAILABLE TOOLS:\n{tool_menu}\n\n"
            f"TASK: {task_description}\n\n"
            "Reply with exactly two lines:\n"
            "TOOL: <tool name or 'none'>\n"
            "ARGS: <json object of arguments>"
        )
        resp = self.provider.complete(
            system=self._seed_prefix() + "You are the planning step of a personal agent. Pick at most one tool.",
            messages=[{"role": "user", "content": prompt}],
        )
        tool_name, tool_args = self._parse_tool_call(resp.text)
        return tool_name, tool_args, resp.cost_usd

    def _reflect(self, task_description, tool_name, tool_args, result: ToolResult, costs: CostTracker):
        prompt = (
            f"The previous attempt failed.\nTASK: {task_description}\n"
            f"TOOL USED: {tool_name}({tool_args})\n"
            f"ERROR: {result.error}\n\n"
            "Write one or two sentences reflecting on what went wrong and what "
            "to do differently next time. Start with 'Reflection:'."
        )
        resp = self.provider.complete(
            system=self._seed_prefix() + "You are the self-reflection step of a personal agent (Reflexion-style). Be concrete.",
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.text.strip(), resp.cost_usd

    @staticmethod
    def _parse_tool_call(text: str):
        tool_match = _TOOL_LINE_RE.search(text)
        args_match = _ARGS_LINE_RE.search(text)
        tool_name = tool_match.group(1) if tool_match else None
        args: Dict[str, Any] = {}
        if args_match:
            try:
                args = json.loads(args_match.group(1))
            except json.JSONDecodeError:
                args = {}
        return tool_name, args

    def _audit(self, user_id, action, tier: PermissionTier, granted, cost_usd, detail):
        self.audit.record(
            user_id=user_id,
            actor="agent",
            action=action,
            tier=tier.value,
            granted=granted,
            cost_usd=cost_usd,
            detail=detail,
        )
