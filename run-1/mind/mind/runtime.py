"""The Mind facade: wires config, provider, memory, tools, permissions, audit and scheduler.

    mind = Mind(Config.from_env())
    s = mind.session("alice", approver=ConsoleApprover())
    s.ask("remember that my name is Alice")
    s.solve(TaskSpec("write a python function is_palindrome(s) ...", checker=PythonTests(...)))
    mind.tick()          # run due scheduled/event jobs headless, report to inboxes
"""
from __future__ import annotations

import datetime as _dt
import sys
from dataclasses import dataclass
from pathlib import Path

from .agent import Agent, Trajectory
from .audit import AuditError, AuditLog
from .config import Config
from .cost import Budget
from .evaluator import TaskSpec
from .memory import MemoryStore, MemoryUnavailable
from .permissions import Approver, DenyAll, PermissionGate
from .providers import make_provider
from .reflexion import ReflexionRunner, SolveResult, task_signature
from .scheduler import Scheduler
from .tools import ToolRegistry, default_tools
from .util import Clock, new_id, truncate, validate_user_id


@dataclass
class AskResult:
    answer: str
    status: str
    trajectory: Trajectory
    budget: dict

    @property
    def ok(self) -> bool:
        return self.status == "answered"


class Mind:
    def __init__(self, config: Config | None = None, clock: Clock | None = None, provider=None, tools=None):
        self.config = config or Config.from_env()
        self.clock = clock or Clock()
        self.data_dir = Path(self.config.data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.audit = AuditLog(self.data_dir / "audit.jsonl", self.clock)
        self.scheduler = Scheduler(self.data_dir, self.clock)
        self.provider = provider or make_provider(self.config, self.clock)
        self._tools = tools
        self._memories: dict[str, MemoryStore] = {}
        self.warnings: list[str] = []

    # ---- memory (per user, degrades to in-memory rather than crashing) -------------------
    def memory(self, user: str) -> MemoryStore:
        validate_user_id(user)
        if user not in self._memories:
            try:
                self._memories[user] = MemoryStore(self.data_dir, user, self.clock)
            except MemoryUnavailable as e:
                msg = f"memory for {user} unavailable ({e}); using a temporary in-memory store — nothing will persist"
                self.warnings.append(msg)
                print("WARNING: " + msg, file=sys.stderr)
                self._memories[user] = MemoryStore(None, user, self.clock, in_memory=True)
        return self._memories[user]

    def close(self):
        for m in self._memories.values():
            m.close()
        self.scheduler.close()

    # ---- budgets ------------------------------------------------------------------------
    def _day(self) -> str:
        return _dt.datetime.fromtimestamp(self.clock.now(), _dt.timezone.utc).strftime("%Y-%m-%d")

    def task_budget(self, user: str, limit_usd: float | None = None) -> Budget:
        mem = self.memory(user)
        day = self._day()
        daily_left = max(0.0, self.config.daily_budget_usd - mem.spent_on(day))
        cap = min(limit_usd if limit_usd is not None else self.config.task_budget_usd, daily_left)
        label = "daily" if daily_left < (limit_usd or self.config.task_budget_usd) else "task"
        return Budget(limit_usd=cap, label=label, on_spend=lambda usd: mem.add_spend(day, usd))

    # ---- sessions -----------------------------------------------------------------------
    def session(self, user: str, approver: Approver | None = None, grants=(), headless: bool = False,
                job_id: str = "") -> "Session":
        return Session(self, user, approver or DenyAll(), set(grants), headless, job_id)

    # ---- approvals ----------------------------------------------------------------------
    def resolve_approval(self, user: str, approval_id: int, approve: bool) -> bool:
        ok = self.memory(user).resolve_approval(approval_id, approve)
        try:
            self.audit.write("approval.resolved", user=user, approval=approval_id, approve=approve, ok=ok)
        except AuditError:
            pass
        return ok

    # ---- proactivity --------------------------------------------------------------------
    def run_job(self, job: dict) -> dict:
        """Scheduler runner: execute one job headless and report back to the user's inbox."""
        user = job["user"]
        import json as _json
        grants = set(_json.loads(job.get("grants") or "[]"))
        task = job["task"] + (f"\n\nEvent payload:\n{job['pending_payload']}" if job.get("pending_payload") else "")
        sess = self.session(user, grants=grants, headless=True, job_id=job["id"])
        res = sess.ask(task, budget_usd=job.get("budget_usd"))
        mem = self.memory(user)
        deferred = [s.detail for s in res.trajectory.steps if "deferred" in s.detail]
        status = res.status if not deferred else "needs_approval"
        body = (f"Job '{job['name']}' ran headless at {self._day()} — status: {status}\n\n"
                f"{res.answer or res.trajectory.reason}\n\n"
                f"cost: ${res.budget['spent_usd']:.5f}")
        if deferred:
            body += "\n\nWaiting for your approval:\n" + "\n".join(f"- {truncate(d, 200)}" for d in deferred)
        mem.add_report(source=f"job:{job['id']}", title=f"[{status}] {job['name']}", body=body)
        try:
            self.audit.write("job.run", user=user, job=job["id"], status=status, cost=res.budget["spent_usd"])
        except AuditError:
            pass
        return {"ok": res.ok and not deferred, "status": status, "summary": truncate(res.answer, 500),
                "cost_usd": res.budget["spent_usd"]}

    def tick(self) -> list[dict]:
        return self.scheduler.tick(self.run_job)

    def status(self) -> dict:
        from .memory import fts5_available
        from .sandbox import namespaces_available
        return {"provider": self.provider.describe(), "data_dir": str(self.data_dir),
                "fts5": fts5_available(), "sandbox_namespaces": namespaces_available(),
                "network_tools": self.config.allow_network, "audit": self.audit.verify()[1],
                "task_budget_usd": self.config.task_budget_usd, "daily_budget_usd": self.config.daily_budget_usd,
                "warnings": self.warnings}


class Session:
    def __init__(self, mind: Mind, user: str, approver: Approver, grants: set, headless: bool, job_id: str):
        self.mind = mind
        self.user = validate_user_id(user)
        self.memory = mind.memory(user)
        self.gate = PermissionGate(approver=approver, memory=self.memory, grants=grants, headless=headless)
        self.registry = ToolRegistry(mind._tools or default_tools(), mind.audit, self.gate,
                                     output_limit=mind.config.tool_output_chars)
        self.agent = Agent(mind.provider, self.registry, self.memory, mind.config, mind.clock, mind.scheduler)
        self.headless = headless
        self.job_id = job_id
        self.id = new_id("sess_")

    def ask(self, text: str, budget_usd: float | None = None) -> AskResult:
        budget = self.mind.task_budget(self.user, budget_usd)
        traj = self.agent.run_trial(text, budget, headless=self.headless, job_id=self.job_id,
                                    task_sig=task_signature(text))
        try:
            self.mind.audit.write("task.ask", user=self.user, session=self.id, status=traj.status,
                                  tools=traj.tool_calls, cost=budget.spent_usd, headless=self.headless)
        except AuditError:
            pass
        if traj.tool_calls:  # only tool-using tasks are worth an episode; chit-chat is not stored
            try:
                self.memory.add_item("episode", f"Asked '{truncate(text, 160)}' -> {traj.status}: "
                                                f"{truncate(traj.answer or traj.reason, 200)}",
                                     "", task_signature(text), 0.3)
            except Exception:
                pass
        return AskResult(traj.answer or traj.reason, traj.status, traj, budget.summary())

    def solve(self, task: TaskSpec, budget_usd: float | None = None) -> SolveResult:
        budget = self.mind.task_budget(self.user, budget_usd)
        runner = ReflexionRunner(self.agent, self.memory, self.mind.config)
        res = runner.solve(task, budget, headless=self.headless, job_id=self.job_id)
        try:
            self.mind.audit.write("task.solve", user=self.user, session=self.id, success=res.success,
                                  trials=len(res.trials), cost=budget.spent_usd)
        except AuditError:
            pass
        return res
