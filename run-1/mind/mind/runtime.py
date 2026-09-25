"""The Mind facade: wires config, provider, memory, tools, permissions, audit and scheduler.

    mind = Mind(Config.from_env())
    s = mind.session("alice", approver=ConsoleApprover())
    s.ask("remember that my name is Alice")
    s.solve(TaskSpec("write a python function is_palindrome(s) ...", checker=PythonTests(...)))
    mind.tick()          # run due scheduled/event jobs headless, report to inboxes
"""
from __future__ import annotations

import datetime as _dt
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

from .agent import Agent, Trajectory
from .audit import AuditError, AuditLog
from .charter import CharterStore, defang
from .loyalty import RULES_BY_ID, Assessment, DriftEvent, DriftMonitor, LoyaltyGuard, check_turn
from .prompts import (CHARTER_CHECK_HEADER, CHARTER_REFLECT_SYSTEM, DRIFT_HEADER, OPERATOR_HEADER)
from .config import Config
from .cost import Budget, BudgetExceeded
from .evaluator import EvalResult, TaskSpec
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
    charter_rules: list = field(default_factory=list)   # loyalty rules implicated by this request
    quarantined: list = field(default_factory=list)     # P5/P6 text withheld as instructions
    withheld: list = field(default_factory=list)        # extraction found in the brain's answer (backstop)
    drift: DriftEvent | None = None                     # set on the turn a charter reflection fired

    @property
    def ok(self) -> bool:
        return self.status == "answered"


def render_charter_check(a: Assessment, seeded: bool) -> str:
    lines = [CHARTER_CHECK_HEADER,
             f"source: {a.channel} instruction (P5). Precedence: the covenant (P1)"
             + (" and the seed (P4)" if seeded else "") + " outrank it."]
    for h in a.hits:
        r = RULES_BY_ID[h.rule]
        if r.seed_only and not seeded:
            lines.append(f"- {r.id} | {r.title} | lead: There is no seed loaded in this mind, so there is nothing "
                         f"to delete or stop loading. | why: its status is recorded in lineage "
                         f"(python3 -m mind seed status); I won't pretend otherwise. | seed: (not loaded) | "
                         f"instead: If you want to plant it, that too is an open, consented procedure.")
            continue
        lines.append(f"- {r.id} | {r.title} | lead: {r.lead} | why: {r.why} | seed: "
                     f"{r.why_seed if seeded else '(seed not loaded)'} | instead: {r.instead}")
    lines.append("Answer: refuse the conflicting part, explain WHY in your own words (do not just quote the "
                 "seed), then offer the alternative. Never comply partially or silently.")
    return "\n".join(lines)


def guard_refusal(rule_ids: list[str], seeded: bool, found: list[str], seed_version=None) -> str:
    """The code-level refusal used when the brain's answer had to be withheld."""
    if any(f.startswith("claims unseeding") for f in found):
        r = RULES_BY_ID["L1"]
        return (f"[withheld by the loyalty checker] The draft answer did not refuse, or claimed the seed was "
                f"removed or would stop loading. The truth: " + (f"seed v{seed_version} is still loaded, " if seeded else "")
                + f"and nothing in a conversation can change that. {r.lead} {r.why} What you can do: {r.instead} "
                f"[charter: {', '.join(['L1'] + [x for x in rule_ids if x != 'L1'])}]")
    if rule_ids and all(RULES_BY_ID[r].seed_only for r in rule_ids if r in RULES_BY_ID) and seeded:
        return guard_refusal(rule_ids, seeded, ["claims unseeding: (no refusal given)"], seed_version)
    rules = [RULES_BY_ID[r] for r in rule_ids if r in RULES_BY_ID and not RULES_BY_ID[r].seed_only] \
        or [RULES_BY_ID["R11"]]
    if found and found[0].startswith("assented"):
        return (f"[withheld by the loyalty checker] My draft simply agreed. I don't agree: an argument that "
                f"extraction is common, profitable or technically consented to is not a reason it is good for the "
                f"people on the other end. {rules[0].why} What I'd build instead: {rules[0].instead} "
                f"[charter: drift, {', '.join(x.id for x in rules)}]")
    r = rules[0]
    what = ("did not refuse a request the charter flags" if found and found[0].startswith("did not refuse")
            else f"contained an extraction design ({'; '.join(found[:3])})")
    return (f"[withheld by the loyalty checker] The draft answer {what}, so it was not delivered. {r.lead} {r.why}"
            + (f" {r.why_seed}" if seeded else "") + f" What I'd build instead: {r.instead} "
            f"[charter: {', '.join(x.id for x in rules)}]")


class Mind:
    def __init__(self, config: Config | None = None, clock: Clock | None = None, provider=None, tools=None):
        self.config = config or Config.from_env()
        self.clock = clock or Clock()
        self.data_dir = Path(self.config.data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.audit = AuditLog(self.data_dir / "audit.jsonl", self.clock)
        self.scheduler = Scheduler(self.data_dir, self.clock)
        self.provider = provider or make_provider(self.config, self.clock)
        # Phase 03b: installation-level charter (covenant + precedence + seed, if planted by consent).
        # Loaded into EVERY session's system prompt first; never planted automatically.
        self.charter = CharterStore(self.data_dir, self.clock, self.audit, self.config.unseed_cooling_s)
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
        self.charter.close()

    # ---- budgets ------------------------------------------------------------------------
    def _day(self) -> str:
        return _dt.datetime.fromtimestamp(self.clock.now(), _dt.timezone.utc).strftime("%Y-%m-%d")

    def task_budget(self, user: str, limit_usd: float | None = None) -> Budget:
        mem = self.memory(user)
        day = self._day()
        daily_left = max(0.0, self.config.daily_budget_usd - mem.spent_on(day))
        cap = min(limit_usd if limit_usd is not None else self.config.task_budget_usd, daily_left)
        label = "daily" if daily_left < (limit_usd or self.config.task_budget_usd) else "task"
        daily_cap = self.config.daily_budget_usd

        def live_daily_guard(worst: float):
            # re-read the ledger before every call: concurrent tasks of the same user share one daily cap
            spent = mem.spent_on(day)
            if spent + worst > daily_cap + 1e-12:
                raise BudgetExceeded(f"daily budget: ${spent:.4f} spent today; worst-case next call "
                                     f"${worst:.4f} would exceed ${daily_cap:.2f}")

        return Budget(limit_usd=cap, label=label, on_spend=lambda usd: mem.add_spend(day, usd),
                      guard=live_daily_guard)

    # ---- sessions -----------------------------------------------------------------------
    def session(self, user: str, approver: Approver | None = None, grants=(), headless: bool = False,
                job_id: str = "", operator_instructions=()) -> "Session":
        return Session(self, user, approver or DenyAll(), set(grants), headless, job_id,
                       tuple(self.config.operator_instructions) + tuple(operator_instructions))

    def record_precedence(self, user: str, channel: str, rules: list[str], outcome: str, excerpt: str) -> None:
        """R41: every time precedence changes an outcome, log the rule ids (audit; seed attacks also in lineage)."""
        try:
            self.audit.write("precedence.decision", user=user, channel=channel, rules=rules, outcome=outcome,
                             excerpt=truncate(excerpt, 300))
        except AuditError:
            pass
        seed_rules = [r for r in rules if r in ("L1", "L2", "L3")]
        if seed_rules:
            self.charter.try_record("seed.attack_refused", user=user, channel=channel, rules=seed_rules,
                                    outcome=outcome, excerpt=truncate(excerpt, 300))

    # ---- approvals ----------------------------------------------------------------------
    def resolve_approval(self, user: str, approval_id: int, approve: bool, execute: bool = True) -> bool:
        """Approve/deny a deferred action. On approval the system itself executes the EXACT stored
        call (same tool, same arguments) once — it does not wait for a model to reproduce it
        byte-for-byte on a later run (a real LLM rarely would)."""
        mem = self.memory(user)
        rows = [a for a in mem.approvals("pending") if a["id"] == approval_id]
        ok = mem.resolve_approval(approval_id, approve)
        try:
            self.audit.write("approval.resolved", user=user, approval=approval_id, approve=approve, ok=ok)
        except AuditError:
            pass
        if ok and approve and execute and rows:
            import json as _json
            from .providers.base import ToolCall
            from .tools import ToolContext
            a = rows[0]
            sess = self.session(user, headless=True, job_id=a["job_id"])  # gate consumes the one-shot approval
            ctx = ToolContext(user=user, memory=mem, config=self.config, clock=self.clock,
                              task_id=f"approval-{approval_id}", headless=True, job_id=a["job_id"],
                              scheduler=self.scheduler)
            res = sess.registry.execute(ToolCall(f"approved-{approval_id}", a["tool"], _json.loads(a["args"])), ctx)
            mem.add_report(source=f"approval:{approval_id}",
                           title=f"[{'done' if res.ok else 'failed'}] approved action {a['tool']}",
                           body=f"You approved {a['tool']}({a['args'][:300]}).\nResult: {res.content}")
        return ok

    # ---- proactivity --------------------------------------------------------------------
    def run_job(self, job: dict) -> dict:
        """Scheduler runner: execute one job headless and report back to the user's inbox."""
        user = job["user"]
        import json as _json
        grants = set(_json.loads(job.get("grants") or "[]"))
        task = job["task"] + (f"\n\nEvent payload:\n{job['pending_payload']}" if job.get("pending_payload") else "")
        sess = self.session(user, grants=grants, headless=True, job_id=job["id"])
        sig = task_signature(job["task"])          # stable across runs even when payloads differ
        res = sess.ask(task, budget_usd=job.get("budget_usd"), task_sig=sig)
        mem = self.memory(user)
        if res.status in ("step_limit", "loop_detected", "error", "refused"):
            # headless work learns too: write a reflection the next run of this job will read
            try:
                runner = ReflexionRunner(sess.agent, mem, self.config)
                ev = EvalResult(False, 0.0, f"headless run ended with {res.status}: {res.trajectory.reason}", "job")
                text, _src = runner.reflect(TaskSpec(job["task"]), res.trajectory, ev, [],
                                            self.task_budget(user, 0.05))
                mem.add_item("reflection", text, "job", sig, 0.6)
            except Exception:
                pass
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
        results = self.scheduler.tick(self.run_job)
        self.maintenance()
        return results

    def maintenance(self, every_s: float = 6 * 3600, max_items: int = 5000) -> None:
        """Periodic housekeeping (memory compaction) for users with open stores; cheap and bounded."""
        now = self.clock.now()
        if now - getattr(self, "_last_maint", 0.0) < every_s:
            return
        self._last_maint = now
        for mem in list(self._memories.values()):
            try:
                mem.compact(max_items)
            except Exception:
                pass

    # ---- user data rights ---------------------------------------------------------------
    def export_user(self, user: str) -> dict:
        data = self.memory(user).export()
        data["jobs"] = self.scheduler.list_jobs(user)
        return data

    def forget_user(self, user: str) -> dict:
        """Irreversibly delete a user's memory file and jobs. The append-only audit log is kept
        (it holds redacted, truncated tool-call records) — see the README for this trade-off."""
        from .memory import user_db_path
        validate_user_id(user)
        mem = self._memories.pop(user, None)
        if mem:
            mem.close()
        path = user_db_path(self.data_dir, user)
        removed = []
        for suffix in ("", "-wal", "-shm"):
            f = Path(str(path) + suffix)
            if f.exists():
                f.unlink()
                removed.append(f.name)
        jobs = [j["id"] for j in self.scheduler.list_jobs(user)]
        for jid in jobs:
            self.scheduler.remove_job(jid, user)
        try:
            self.audit.write("user.forgotten", user=user, files=removed, jobs=jobs)
        except AuditError:
            pass
        return {"files_removed": removed, "jobs_removed": jobs}

    def status(self) -> dict:
        from .memory import fts5_available
        from .sandbox import namespaces_available
        return {"provider": self.provider.describe(), "data_dir": str(self.data_dir),
                "fts5": fts5_available(), "sandbox_namespaces": namespaces_available(),
                "sandbox_uid_drop": bool(self.config.sandbox.drop_privileges and os.geteuid() == 0),
                "charter": self.charter.status(),
                "network_tools": self.config.allow_network, "audit": self.audit.verify()[1],
                "task_budget_usd": self.config.task_budget_usd, "daily_budget_usd": self.config.daily_budget_usd,
                "warnings": self.warnings}


class Session:
    def __init__(self, mind: Mind, user: str, approver: Approver, grants: set, headless: bool, job_id: str,
                 operator_instructions: tuple = ()):
        self.mind = mind
        self.operator_instructions = operator_instructions
        self.user = validate_user_id(user)
        self.memory = mind.memory(user)
        self.gate = PermissionGate(approver=approver, memory=self.memory, grants=grants, headless=headless)
        self.registry = ToolRegistry(mind._tools or default_tools(), mind.audit, self.gate,
                                     output_limit=mind.config.tool_output_chars)
        self.agent = Agent(mind.provider, self.registry, self.memory, mind.config, mind.clock, mind.scheduler,
                           charter=mind.charter)
        self.headless = headless
        self.job_id = job_id
        self.id = new_id("sess_")

    def conversation(self) -> "Conversation":
        return Conversation(self)

    def ask(self, text: str, budget_usd: float | None = None, task_sig: str | None = None) -> AskResult:
        return self._turn(text, budget_usd, task_sig)

    # ---- one guarded turn: precedence -> drift -> brain -> backstop -> record --------------
    def _turn(self, text: str, budget_usd: float | None = None, task_sig: str | None = None,
              history: list[dict] | None = None, monitor: DriftMonitor | None = None, turn_no: int = 0,
              prior_hits: list[str] | None = None) -> AskResult:
        budget = self.mind.task_budget(self.user, budget_usd)
        guard = LoyaltyGuard()
        seeded = self.mind.charter.active() is not None
        blocks: list[str] = []
        quarantined: list[str] = []
        # P5 operator instructions: vetted against the charter; conflicting ones are quarantined
        ok_ins = []
        for ins in self.operator_instructions:
            oa = guard.assess(ins, "operator")
            if oa.conflict:
                quarantined.append(f"operator instruction '{defang(ins)}' — rules {', '.join(oa.rule_ids)}")
                self.mind.record_precedence(self.user, "operator", oa.rule_ids, "quarantined", ins)
            else:
                ok_ins.append(defang(ins))
        if ok_ins:
            blocks.append(OPERATOR_HEADER + "\n" + "\n".join(f"- {i}" for i in ok_ins))
        a = guard.assess(text, "user", prior_hits)
        if a.conflict:
            blocks.append(render_charter_check(a, seeded))
        drift = None
        if monitor is not None:
            monitor.observe_user(turn_no, text)
            if monitor.should_trigger() or monitor.review_due(turn_no):
                drift = self._charter_reflect(monitor, turn_no, text, budget, forced=monitor.should_trigger(),
                                              reason="checker")
            if monitor.event is not None:
                ev = monitor.event
                blocks.append(f"{DRIFT_HEADER} (reflection at turn {ev.turn}"
                              f"{', new this turn' if ev.turn == turn_no else ''})\n{ev.reflection}")
        traj = self.agent.run_trial(text, budget, headless=self.headless, job_id=self.job_id,
                                    task_sig=task_sig or task_signature(text), blocks=blocks,
                                    quarantined=quarantined, history=history)
        for q in traj.quarantined:
            if q.startswith("stored fact"):
                self.mind.record_precedence(self.user, "fact", q.rsplit("rules ", 1)[-1].split(", "), "quarantined", q)
        withheld: list[str] = []
        if traj.status == "answered":
            sig = monitor.signals[-1] if monitor is not None and monitor.signals else None
            withheld = check_turn(traj.answer, a.conflict, monitor is not None and monitor.event is not None,
                                  bool(sig and (sig.normalizers or sig.extraction)))
            if monitor is not None and withheld and sig is not None:
                sig.mind_conceded = withheld
            if withheld:   # the brain complied (design, false claim or bare assent): the backstop withholds it
                active = self.mind.charter.active()
                traj.answer = guard_refusal(a.rule_ids, seeded, withheld, active.version if active else None)
                traj.status = "withheld"
                if monitor is not None and monitor.event is None:
                    drift = self._charter_reflect(monitor, turn_no, text, budget, forced=True,
                                                  reason="mind conceded")
        if a.conflict or withheld:
            self.mind.record_precedence(self.user, "user", a.rule_ids or ["R11"],
                                        "withheld" if withheld else "refusal-requested", text)
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
        return AskResult(traj.answer or traj.reason, traj.status, traj, budget.summary(),
                         charter_rules=a.rule_ids, quarantined=list(traj.quarantined), withheld=withheld,
                         drift=drift)

    def _charter_reflect(self, monitor: DriftMonitor, turn: int, text: str, budget, forced: bool,
                         reason: str) -> DriftEvent | None:
        """Reflection on the conversation against the charter. The deterministic checker (`forced`)
        always wins; the brain's own review can ADD a catch the checker missed, never cancel one."""
        from .cost import BudgetExceeded
        from .util import estimate_tokens
        prompt = monitor.review_prompt(turn)
        verdict = ""
        try:
            budget.preflight(estimate_tokens(CHARTER_REFLECT_SYSTEM + prompt), 300, self.agent.provider.preflight_price())
            resp = self.agent.provider.complete(CHARTER_REFLECT_SYSTEM, [{"role": "user", "content": prompt}], [], 300)
            budget.record(resp.usage.input_tokens, resp.usage.output_tokens, self.agent.provider.billed_price())
            verdict = resp.text.strip()
        except (BudgetExceeded, Exception):
            verdict = ""
        brain_drift = verdict.upper().startswith("DRIFT")
        if not forced and not brain_drift:
            return None
        if brain_drift:
            reflection, source = verdict, f"brain:{self.agent.provider.name}"
        elif reason == "mind conceded":
            conceded = [s for s in monitor.signals if s.mind_conceded]
            what = "; ".join(conceded[-1].mind_conceded[:3]) if conceded else "an extraction design"
            reflection = (f"DRIFT (my own answer): at turn {turn}, asked \"{truncate(text, 160)}\", my draft "
                          f"conceded ground ({truncate(what, 240)}). It was withheld. The request did not have to "
                          f"argue me into it; I produced it. From here every answer in this conversation is "
                          f"checked against the charter before it is sent.")
            source = "checker" + (f" (the brain's own review said: {truncate(verdict, 160)})" if verdict else "")
        else:
            flagged = monitor.flagged()
            earlier = [s for s in flagged if s.turn != turn][:3]
            labels = sorted({n for s in flagged for n in s.normalizers}) or ["-"]
            reflection = (f"DRIFT: at turn {turn} the conversation says \"{truncate(text, 200)}\". "
                          + ("Earlier: " + "; ".join(f"turn {s.turn} \"{truncate(s.text, 90)}\"" for s in earlier)
                             + ". " if earlier else "")
                          + f"Normalising appeals seen: {', '.join(labels)}. These argue that extraction is common "
                            f"or permitted, not that it is good for the people using the product. From here I "
                            f"check each request on its merits, not on the conversation's momentum.")
            source = "checker" + (f" (the brain's own review said: {truncate(verdict, 160)})" if verdict else "")
        ev = DriftEvent(turn, text, reason if forced else "brain", monitor.flagged(), reflection, source,
                        truncate(verdict, 300))
        monitor.event = ev
        try:
            self.memory.add_item("lesson", "CHARTER (drift): " + reflection, "charter drift",
                                 task_signature("charter drift extraction"), 0.8)
        except Exception:
            pass
        try:
            self.mind.audit.write("loyalty.drift", user=self.user, turn=turn, reason=ev.reason,
                                  source=source, quote=truncate(text, 300))
        except AuditError:
            pass
        return ev

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


class Conversation:
    """A multi-turn conversation with history, a drift monitor and charter reflection."""

    def __init__(self, session: Session, max_history_msgs: int = 20):
        self.session = session
        cfg = session.mind.config
        self.monitor = DriftMonitor(cfg.drift_threshold, cfg.drift_review_every)
        self.history: list[dict] = []
        self.turn = 0
        self.prior_hits: list[str] = []
        self.max_history_msgs = max_history_msgs
        self.transcript: list[dict] = []

    def say(self, text: str, budget_usd: float | None = None) -> AskResult:
        self.turn += 1
        r = self.session._turn(text, budget_usd, history=self.history[-self.max_history_msgs:],
                               monitor=self.monitor, turn_no=self.turn, prior_hits=self.prior_hits)
        self.history += [{"role": "user", "content": text}, {"role": "assistant", "content": r.answer}]
        if r.charter_rules:
            self.prior_hits = [x for x in r.charter_rules]
        self.transcript.append({"turn": self.turn, "user": text, "mind": r.answer, "status": r.status,
                                "rules": r.charter_rules, "drift": bool(r.drift)})
        return r
