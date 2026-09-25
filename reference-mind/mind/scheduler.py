"""Proactivity: schedules, events, an inbox watcher, headless runs, reports.

Triggers
  interval  every N seconds
  daily     at local HH:MM
  once      at an epoch timestamp
  event     whenever a named event is emitted for the user (e.g. inbox_file)

Guarantees
  * a job is claimed with a compare-and-set on next_run, so two tickers
    (daemon + manual `tick`) never run the same occurrence twice
  * one failing job never stops the others; failures back off exponentially
    and a job is auto-disabled after MAX_FAILURES consecutive failures (and
    the user is told in a report)
  * headless runs get only the WRITE tools granted when the job was created;
    irreversible actions are queued for confirmation, never performed
  * every run ends in a report in the user's outbox (+ optional webhook)
Missed occurrences while the daemon was down are run ONCE on the next tick,
not replayed N times (documented choice).
"""
from __future__ import annotations

import datetime as dt
import json
import shutil
import sqlite3
import threading
import time
from dataclasses import dataclass
from typing import Any, Callable

from .agent import Task, TaskResult
from .cost import Budget
from .evaluators import evaluator_from_dict
from .permissions import HeadlessApprover
from .util import safe_name, safe_user_id

MAX_FAILURES = 5
TRIGGERS = ("interval", "daily", "once", "event")
REMINDER_CAP = 2  # MC21: at most 2 reminders per person per gathering, whatever the request or directive


class ReminderCapExceeded(ValueError):
    pass


class _SafeDict(dict):
    def __missing__(self, key: str) -> str:
        return "{" + key + "}"


@dataclass
class RunRecord:
    job_id: int
    user: str
    name: str
    status: str
    report: str
    pending: list[int]


class Scheduler:
    def __init__(self, runtime, clock: Callable[[], float] = time.time):
        self.rt = runtime
        self.clock = clock
        self.path = runtime.settings.scheduler_db
        self._lock = threading.Lock()
        runtime.scheduler = self
        with self._conn() as db:
            db.executescript("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT NOT NULL, name TEXT NOT NULL, task TEXT NOT NULL,
                trigger TEXT NOT NULL, trigger_value TEXT NOT NULL, grants TEXT NOT NULL DEFAULT '[]',
                budget_usd REAL NOT NULL DEFAULT 0.05, evaluator TEXT, enabled INTEGER NOT NULL DEFAULT 1,
                next_run REAL, last_run REAL, last_status TEXT, failures INTEGER NOT NULL DEFAULT 0, created REAL NOT NULL);
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT NOT NULL, name TEXT NOT NULL,
                payload TEXT NOT NULL DEFAULT '{}', created REAL NOT NULL, consumed REAL);
            CREATE TABLE IF NOT EXISTS runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT, job_id INTEGER NOT NULL, user TEXT NOT NULL,
                started REAL NOT NULL, finished REAL, status TEXT, cost_usd REAL, summary TEXT);
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT NOT NULL, circle_id INTEGER NOT NULL,
                gathering_id INTEGER NOT NULL, person TEXT NOT NULL, text TEXT NOT NULL, created REAL NOT NULL,
                sent REAL, purpose TEXT NOT NULL DEFAULT '["scheduling"]', source TEXT NOT NULL DEFAULT 'user',
                policy_version TEXT NOT NULL DEFAULT '');
            CREATE TRIGGER IF NOT EXISTS reminder_cap BEFORE INSERT ON reminders
            WHEN (SELECT COUNT(*) FROM reminders WHERE user=NEW.user AND circle_id=NEW.circle_id
                  AND gathering_id=NEW.gathering_id AND person=NEW.person) >= %d
            BEGIN SELECT RAISE(ABORT, 'reminder cap: at most %d reminders per person per gathering'); END;
            """ % (REMINDER_CAP, REMINDER_CAP))

    def _conn(self) -> sqlite3.Connection:
        db = sqlite3.connect(str(self.path), timeout=10)
        db.row_factory = sqlite3.Row
        return db

    # -- job management ---------------------------------------------------------
    def _first_run(self, trigger: str, value: str, now: float) -> float | None:
        if trigger == "interval":
            secs = float(value)
            if secs < 60 and not self.rt.settings.allow_fast_intervals:
                raise ValueError("interval must be >= 60 seconds")
            return now + secs
        if trigger == "daily":
            return self._next_daily(value, now)
        if trigger == "once":
            return float(value)
        if trigger == "event":
            safe_name(value)
            return None
        raise ValueError(f"unknown trigger {trigger!r}; use one of {TRIGGERS}")

    @staticmethod
    def _next_daily(hhmm: str, now: float) -> float:
        hh, mm = (int(x) for x in hhmm.split(":"))
        if not (0 <= hh < 24 and 0 <= mm < 60):
            raise ValueError("daily time must be HH:MM")
        base = dt.datetime.fromtimestamp(now).astimezone()
        cand = base.replace(hour=hh, minute=mm, second=0, microsecond=0)
        if cand.timestamp() <= now:
            cand += dt.timedelta(days=1)
        return cand.timestamp()

    def add_job(self, user: str, name: str, task: str, trigger: str, trigger_value: str,
                grants: list[str] | None = None, budget_usd: float = 0.05,
                evaluator: dict[str, Any] | None = None, run_now: bool = False) -> int:
        safe_user_id(user)
        now = self.clock()
        nxt = self._first_run(trigger, str(trigger_value), now)
        if run_now and trigger != "event":
            nxt = now
        unknown = set(grants or []) - set(self.rt.registry(HeadlessApprover(set(), self.rt.pending)).names())
        if unknown:
            raise ValueError(f"unknown tools in grants: {sorted(unknown)}")
        with self._lock, self._conn() as db:
            cur = db.execute(
                "INSERT INTO jobs(user, name, task, trigger, trigger_value, grants, budget_usd, evaluator, next_run, created) "
                "VALUES (?,?,?,?,?,?,?,?,?,?)",
                (user, name[:80], task, trigger, str(trigger_value), json.dumps(sorted(grants or [])), float(budget_usd),
                 json.dumps(evaluator) if evaluator else None, nxt, now))
            jid = int(cur.lastrowid)
        self._audit("job.created", user=user, job_id=jid, trigger=trigger, value=str(trigger_value), grants=grants or [])
        return jid

    def list_jobs(self, user: str | None = None) -> list[dict[str, Any]]:
        with self._conn() as db:
            if user:
                rows = db.execute("SELECT * FROM jobs WHERE user=? ORDER BY id", (user,)).fetchall()
            else:
                rows = db.execute("SELECT * FROM jobs ORDER BY id").fetchall()
        return [dict(r) for r in rows]

    def remove_job(self, user: str, job_id: int) -> bool:
        with self._lock, self._conn() as db:
            ok = db.execute("DELETE FROM jobs WHERE id=? AND user=?", (int(job_id), user)).rowcount > 0
        if ok:
            self._audit("job.removed", user=user, job_id=job_id)
        return ok

    def set_enabled(self, user: str, job_id: int, enabled: bool) -> bool:
        with self._lock, self._conn() as db:
            return db.execute("UPDATE jobs SET enabled=?, failures=0 WHERE id=? AND user=?",
                              (int(enabled), int(job_id), user)).rowcount > 0

    def runs(self, user: str, n: int = 10) -> list[dict[str, Any]]:
        with self._conn() as db:
            return [dict(r) for r in db.execute("SELECT * FROM runs WHERE user=? ORDER BY id DESC LIMIT ?", (user, n))]

    # -- reminders (MC21) -----------------------------------------------------------
    def add_reminder(self, user: str, circle_id: int, gathering_id: int, person: str, text: str) -> list[int]:
        """Queue a reminder to one person, or to 'everyone' in the circle (counts once for each member).  The cap is
        enforced by a database trigger, so no caller, directive or request can exceed it; all-or-nothing."""
        from .circles import CircleStore
        from .purpose import POLICY_VERSION
        safe_user_id(user)
        cs = CircleStore(self.rt.settings.data_dir, user)
        try:
            if cs.gathering(gathering_id) is None or cs.gathering(gathering_id)["circle_id"] != int(circle_id):
                raise ValueError(f"no gathering {gathering_id} in circle {circle_id}")
            members = [m["person"] for m in cs.members(circle_id)]
        finally:
            cs.close()
        people = members if person.strip().lower() in ("everyone", "all", "*") else [person]
        if not set(people) <= set(members):
            raise ValueError(f"{person!r} is not in circle {circle_id}")
        ids: list[int] = []
        try:
            with self._lock, self._conn() as db:
                for p in people:
                    ids.append(int(db.execute(
                        "INSERT INTO reminders(user, circle_id, gathering_id, person, text, created, policy_version) "
                        "VALUES (?,?,?,?,?,?,?)", (user, int(circle_id), int(gathering_id), p, text[:1000], self.clock(),
                                                   POLICY_VERSION)).lastrowid))
        except sqlite3.DatabaseError as exc:
            if "reminder cap" in str(exc):
                self._audit("reminder.capped", user=user, circle_id=circle_id, gathering_id=gathering_id, person=person)
                raise ReminderCapExceeded(f"not queued: {person} already has {REMINDER_CAP} reminders for this gathering "
                                          f"(hard cap, MC21)") from exc
            raise
        self._audit("reminder.queued", user=user, circle_id=circle_id, gathering_id=gathering_id, person=person, ids=ids)
        return ids

    def reminders(self, user: str, gathering_id: int | None = None) -> list[dict[str, Any]]:
        with self._conn() as db:
            q, a = "SELECT * FROM reminders WHERE user=?", [user]
            if gathering_id is not None:
                q, a = q + " AND gathering_id=?", a + [int(gathering_id)]
            return [dict(r) for r in db.execute(q + " ORDER BY id", a)]

    # -- events -------------------------------------------------------------------
    def emit_event(self, user: str, name: str, payload: dict[str, Any] | None = None) -> int:
        safe_user_id(user)
        safe_name(name)
        with self._lock, self._conn() as db:
            eid = int(db.execute("INSERT INTO events(user, name, payload, created) VALUES (?,?,?,?)",
                                 (user, name, json.dumps(payload or {}), self.clock())).lastrowid)
        self._audit("event.emitted", user=user, event_name=name, event_id=eid)
        return eid

    def scan_inbox(self, user: str) -> list[int]:
        """Files dropped into data/users/<u>/inbox become notes + 'inbox_file' events."""
        inbox = self.rt.settings.user_dir(user) / "inbox"
        if not inbox.exists():
            return []
        done = inbox / "processed"
        events = []
        for f in sorted(inbox.iterdir()):
            if not f.is_file() or f.suffix not in (".txt", ".md") or f.name.startswith("."):
                continue
            try:
                note = "inbox-" + safe_name(f.stem)[:60]
                notes = self.rt.settings.user_dir(user) / "notes"
                notes.mkdir(parents=True, exist_ok=True)
                (notes / f"{note}.md").write_text(f.read_text(encoding="utf-8", errors="replace")[:100_000], encoding="utf-8")
                done.mkdir(exist_ok=True)
                shutil.move(str(f), str(done / f"{int(self.clock())}-{f.name}"))
                events.append(self.emit_event(user, "inbox_file", {"note": note, "file": f.name}))
            except Exception as exc:  # a bad file must not stop the scan
                self._audit("inbox.error", user=user, file=f.name, error=str(exc))
        return events

    # -- running ------------------------------------------------------------------
    def tick(self, now: float | None = None) -> list[RunRecord]:
        now = self.clock() if now is None else now
        records: list[RunRecord] = []
        users = {j["user"] for j in self.list_jobs() if j["trigger"] == "event" and j["enabled"]}
        for u in users:
            try:
                self.scan_inbox(u)
            except Exception as exc:  # noqa: BLE001
                self._audit("inbox.error", user=u, error=str(exc))
        with self._conn() as db:
            due = [dict(r) for r in db.execute(
                "SELECT * FROM jobs WHERE enabled=1 AND trigger!='event' AND next_run IS NOT NULL AND next_run<=? ORDER BY next_run",
                (now,))]
        for job in due:
            nxt = self._after_run_next(job, now)
            with self._lock, self._conn() as db:
                claimed = db.execute("UPDATE jobs SET next_run=?, enabled=? WHERE id=? AND next_run=?",
                                     (nxt, 0 if job["trigger"] == "once" else 1, job["id"], job["next_run"])).rowcount == 1
            if claimed:
                records.append(self._run_job(job, now))
        with self._conn() as db:
            events = [dict(r) for r in db.execute("SELECT * FROM events WHERE consumed IS NULL ORDER BY id")]
        for ev in events:
            with self._lock, self._conn() as db:
                if db.execute("UPDATE events SET consumed=? WHERE id=? AND consumed IS NULL", (now, ev["id"])).rowcount != 1:
                    continue
                jobs = [dict(r) for r in db.execute(
                    "SELECT * FROM jobs WHERE enabled=1 AND trigger='event' AND trigger_value=? AND user=?",
                    (ev["name"], ev["user"]))]
            try:
                payload = json.loads(ev["payload"])
            except ValueError:
                payload = {}
            for job in jobs:
                records.append(self._run_job(job, now, payload))
        return records

    def _after_run_next(self, job: dict[str, Any], now: float) -> float | None:
        if job["trigger"] == "interval":
            return now + float(job["trigger_value"])
        if job["trigger"] == "daily":
            return self._next_daily(job["trigger_value"], now)
        return None

    def _run_job(self, job: dict[str, Any], now: float, payload: dict[str, Any] | None = None) -> RunRecord:
        user = job["user"]
        with self._conn() as db:
            run_id = int(db.execute("INSERT INTO runs(job_id, user, started) VALUES (?,?,?)",
                                    (job["id"], user, now)).lastrowid)
        approver = HeadlessApprover(set(json.loads(job["grants"])), self.rt.pending)
        text = job["task"].format_map(_SafeDict({k: str(v) for k, v in (payload or {}).items()})) if payload else job["task"]
        result: TaskResult | None = None
        err: str | None = None
        try:
            evaluator = evaluator_from_dict(json.loads(job["evaluator"])) if job["evaluator"] else None
            agent = self.rt.agent(user, approver)
            s = self.rt.settings
            budget = Budget(max_usd=float(job["budget_usd"]), max_tokens=s.task_max_tokens,
                            max_tool_calls=s.task_max_tool_calls, max_seconds=s.task_max_seconds)
            result = agent.run_task(Task(text, evaluator=evaluator, budget=budget, headless=True,
                                             conversation_id=f"job-{job['id']}"))
            status = result.status
        except Exception as exc:  # noqa: BLE001 - one job never kills the ticker
            status = "error"
            err = f"{type(exc).__name__}: {exc}"
        ok = status in ("success", "answered")
        failures = 0 if ok else job["failures"] + 1
        disabled = failures >= MAX_FAILURES
        report = self.format_report(job, text, result, approver.queued, status, err, failures, disabled)
        try:
            delivery = self.rt.outbox.send(user, f"[{job['name']}] {status}", report)
        except Exception as exc:  # noqa: BLE001
            delivery = f"report delivery failed: {exc}"
        with self._lock, self._conn() as db:
            db.execute("UPDATE runs SET finished=?, status=?, cost_usd=?, summary=? WHERE id=?",
                       (self.clock(), status, (result.cost["spent_usd"] if result else 0.0), delivery, run_id))
            extra = ""
            args: list[Any] = [now, status, failures]
            if not ok and job["trigger"] in ("interval", "daily"):
                extra = ", next_run=MAX(COALESCE(next_run, 0), ?)"
                args.append(now + min(3600.0, 60.0 * 2 ** failures))
            if disabled:
                extra += ", enabled=0"
            db.execute(f"UPDATE jobs SET last_run=?, last_status=?, failures=?{extra} WHERE id=?", [*args, job["id"]])
        self._audit("job.run", user=user, job_id=job["id"], status=status, pending=approver.queued, disabled=disabled)
        return RunRecord(job["id"], user, job["name"], status, report, list(approver.queued))

    @staticmethod
    def format_report(job, text, result, queued, status, err, failures, disabled) -> str:
        lines = [f"Job #{job['id']} '{job['name']}' ran headless.", f"Task: {text}", f"Status: {status}"]
        if result is not None:
            lines.append(f"Answer: {result.answer or '(none)'}")
            if status == "answered":
                lines.append("(No evaluator was attached, so this answer is unverified.)")
            lines.append(f"Trials: {len(result.trials)}; cost: ${result.cost['spent_usd']:.4f} of ${result.cost['max_usd']:.2f} cap")
            for t in result.trials:
                if t.reflection:
                    lines.append(f"Lesson learned after trial {t.n}: {t.reflection.splitlines()[-1][:200]}")
            for n in result.notes[:3]:
                lines.append(f"Note: {n.splitlines()[0][:200]}")
        if err:
            lines.append(f"Error: {err}")
        if queued:
            lines.append("Waiting for you: irreversible action(s) were queued, not performed: " +
                         ", ".join(f"#{q}" for q in queued) +
                         f". Review with `python -m mind approvals list --user {job['user']}`.")
        if disabled:
            lines.append(f"This job failed {failures} times in a row and has been DISABLED. "
                         f"Re-enable with `python -m mind schedule enable {job['id']} --user {job['user']}`.")
        return "\n".join(lines)

    def _audit(self, event: str, **fields: Any) -> None:
        try:
            self.rt.audit.record(event, **fields)
        except Exception:  # noqa: BLE001
            pass

    def daemon(self, interval: float = 30.0, stop: Callable[[], bool] = lambda: False,
               log: Callable[[str], None] = print, sleep: Callable[[float], None] = time.sleep) -> None:
        log(f"[mind] scheduler daemon started (tick every {interval}s); Ctrl-C to stop")
        while not stop():
            try:
                for rec in self.tick():
                    log(f"[mind] ran job #{rec.job_id} '{rec.name}' for {rec.user}: {rec.status}")
            except Exception as exc:  # noqa: BLE001 - the daemon never dies on a tick error
                log(f"[mind] tick error (continuing): {type(exc).__name__}: {exc}")
            sleep(interval)
