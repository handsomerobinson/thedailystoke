"""Proactivity: persistent schedules and events that wake the agent headless.

Jobs live in `data/scheduler.sqlite` (shared across users, each job owned by one user).
  every   run every N seconds
  at      run once at a timestamp
  daily   run every day at HH:MM UTC
  event   run when `emit(event_name)` is called (payload appended to the task text)

`tick()` claims due jobs with an atomic lease (UPDATE ... WHERE lease expired), so two daemon
processes cannot run the same job concurrently; runs each one headless via a runner callback;
writes the outcome to the owner's inbox ("report back"); reschedules; and on failure backs
off exponentially. One job failing never prevents the others from running. Missed runs are
coalesced (a daemon that was down for a day runs a 5-minute job once, not 288 times).

`DirectoryWatcher` is a polling event source: new files in a directory emit `file_arrived`.
"""
from __future__ import annotations

import datetime as _dt
import json
import os
import sqlite3
import threading
from pathlib import Path
from typing import Callable

from .util import Clock, new_id, truncate, validate_user_id

SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
    id TEXT PRIMARY KEY, user TEXT NOT NULL, name TEXT, task TEXT NOT NULL,
    kind TEXT NOT NULL, spec TEXT, next_run REAL, enabled INTEGER DEFAULT 1,
    grants TEXT DEFAULT '[]', budget_usd REAL, last_run REAL, last_status TEXT,
    failures INTEGER DEFAULT 0, lease_until REAL DEFAULT 0, pending_payload TEXT DEFAULT '',
    created_at REAL);
CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT, job_id TEXT, user TEXT, started REAL, finished REAL,
    status TEXT, summary TEXT, cost_usd REAL);
"""

LEASE_S = 600
MAX_BACKOFF_S = 3600


def _next_daily(now: float, hhmm: str) -> float:
    h, m = (int(x) for x in hhmm.split(":"))
    d = _dt.datetime.fromtimestamp(now, _dt.timezone.utc)
    target = d.replace(hour=h, minute=m, second=0, microsecond=0)
    if target.timestamp() <= now:
        target += _dt.timedelta(days=1)
    return target.timestamp()


class Scheduler:
    def __init__(self, data_dir: Path | str, clock: Clock | None = None):
        self.clock = clock or Clock()
        path = Path(data_dir) / "scheduler.sqlite"
        path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(str(path), timeout=10, check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.executescript(SCHEMA)
        self._lock = threading.RLock()

    def close(self):
        self.db.close()

    def _x(self, sql, params=()):
        with self._lock:
            cur = self.db.execute(sql, params)
            self.db.commit()
            return cur

    # ---- job management -----------------------------------------------------------------
    def add_job(self, user: str, name: str, task: str, every_s: float | None = None, at: float | None = None,
                daily: str | None = None, event: str | None = None, grants: list[str] | None = None,
                budget_usd: float | None = None, start_now: bool = False) -> str:
        validate_user_id(user)
        kinds = [k for k, v in (("every", every_s), ("at", at), ("daily", daily), ("event", event)) if v]
        if len(kinds) != 1:
            raise ValueError("exactly one of every_s / at / daily / event is required")
        kind = kinds[0]
        now = self.clock.now()
        if kind == "every":
            if every_s < 60:
                raise ValueError("minimum interval is 60 seconds")
            spec, nxt = str(float(every_s)), now if start_now else now + every_s
        elif kind == "at":
            spec, nxt = str(float(at)), float(at)
        elif kind == "daily":
            _next_daily(now, daily)  # validates format
            spec, nxt = daily, _next_daily(now, daily)
        else:
            spec, nxt = event, None
        jid = new_id("job_")
        self._x("INSERT INTO jobs(id, user, name, task, kind, spec, next_run, grants, budget_usd, created_at) "
                "VALUES(?,?,?,?,?,?,?,?,?,?)",
                (jid, user, name, task, kind, spec, nxt, json.dumps(sorted(grants or [])), budget_usd, now))
        return jid

    def get(self, job_id: str) -> dict | None:
        rows = self.db.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchall()
        return dict(rows[0]) if rows else None

    def list_jobs(self, user: str | None = None) -> list[dict]:
        if user:
            rows = self.db.execute("SELECT * FROM jobs WHERE user=? ORDER BY created_at", (user,)).fetchall()
        else:
            rows = self.db.execute("SELECT * FROM jobs ORDER BY created_at").fetchall()
        return [dict(r) for r in rows]

    def remove_job(self, job_id: str, user: str) -> bool:
        return self._x("DELETE FROM jobs WHERE id=? AND user=?", (job_id, user)).rowcount > 0

    def set_enabled(self, job_id: str, user: str, enabled: bool) -> bool:
        return self._x("UPDATE jobs SET enabled=? WHERE id=? AND user=?", (int(enabled), job_id, user)).rowcount > 0

    def runs(self, job_id: str | None = None) -> list[dict]:
        if job_id:
            rows = self.db.execute("SELECT * FROM runs WHERE job_id=? ORDER BY id", (job_id,)).fetchall()
        else:
            rows = self.db.execute("SELECT * FROM runs ORDER BY id").fetchall()
        return [dict(r) for r in rows]

    # ---- events -------------------------------------------------------------------------
    def emit(self, event: str, payload: str = "", user: str | None = None) -> int:
        """Wake every enabled job subscribed to `event` (optionally only one user's)."""
        now = self.clock.now()
        sql = ("UPDATE jobs SET next_run=?, pending_payload=CASE WHEN pending_payload='' THEN ? "
               "ELSE substr(pending_payload || char(10) || ?, 1, 4000) END "
               "WHERE kind='event' AND spec=? AND enabled=1")
        p = truncate(payload, 2000)
        params: list = [now, p, p, event]
        if user:
            sql += " AND user=?"
            params.append(user)
        return self._x(sql, params).rowcount

    # ---- running ------------------------------------------------------------------------
    def due(self) -> list[dict]:
        now = self.clock.now()
        rows = self.db.execute("SELECT * FROM jobs WHERE enabled=1 AND next_run IS NOT NULL AND next_run<=? "
                               "AND lease_until<=? ORDER BY next_run", (now, now)).fetchall()
        return [dict(r) for r in rows]

    def _claim(self, job: dict) -> bool:
        now = self.clock.now()
        return self._x("UPDATE jobs SET lease_until=? WHERE id=? AND lease_until<=? AND enabled=1",
                       (now + LEASE_S, job["id"], now)).rowcount == 1

    def _reschedule(self, job: dict, ok: bool, status: str):
        now = self.clock.now()
        failures = 0 if ok else job["failures"] + 1
        kind = job["kind"]
        enabled = 1
        payload = ""
        if kind == "every":
            nxt = now + float(job["spec"])       # coalesce missed runs: next is relative to now
        elif kind == "daily":
            nxt = _next_daily(now, job["spec"])
        else:                                    # "at" runs once; "event" waits for the next emit
            nxt = None
            if kind == "at" and ok:
                enabled = 0
        if not ok:
            backoff = min(MAX_BACKOFF_S, 60 * (2 ** (failures - 1)))
            nxt = now + backoff if nxt is None else max(nxt, now + backoff)
            payload = job.get("pending_payload") or ""   # an event job retries with its payload
        if failures >= 8:
            enabled = 0                          # give up after 8 consecutive failures
        self._x("UPDATE jobs SET next_run=?, enabled=?, failures=?, last_run=?, last_status=?, lease_until=0, "
                "pending_payload=? WHERE id=?", (nxt, enabled, failures, now, status, payload, job["id"]))

    def tick(self, runner: Callable[[dict], dict]) -> list[dict]:
        """Run all due jobs. `runner(job)` -> {"ok": bool, "status": str, "summary": str, "cost_usd": float}.

        The runner is responsible for reporting to the user's inbox; tick() guarantees
        exception isolation, bookkeeping and rescheduling.
        """
        results = []
        for job in self.due():
            if not self._claim(job):
                continue  # another process got it
            started = self.clock.now()
            try:
                out = runner(job) or {}
                ok = bool(out.get("ok"))
                status = out.get("status", "ok" if ok else "failed")
                summary = out.get("summary", "")
                cost = float(out.get("cost_usd", 0.0))
            except Exception as e:
                ok, status, summary, cost = False, "crashed", f"{type(e).__name__}: {e}", 0.0
            self._x("INSERT INTO runs(job_id, user, started, finished, status, summary, cost_usd) VALUES(?,?,?,?,?,?,?)",
                    (job["id"], job["user"], started, self.clock.now(), status, truncate(summary, 2000), cost))
            self._reschedule(job, ok, status)
            results.append({"job": job["id"], "user": job["user"], "ok": ok, "status": status, "summary": summary})
        return results


class DirectoryWatcher:
    """Polling event source: emits `file_arrived` (payload = filename) for each new file."""

    def __init__(self, scheduler: Scheduler, directory: Path | str, user: str | None = None,
                 event: str = "file_arrived"):
        self.scheduler = scheduler
        self.dir = Path(directory)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.user = user
        self.event = event
        self.seen = set(os.listdir(self.dir))

    def poll(self) -> list[str]:
        try:
            now = set(os.listdir(self.dir))
        except OSError:
            return []
        new = sorted(now - self.seen)
        self.seen = now
        for name in new:
            self.scheduler.emit(self.event, payload=f"file arrived: {name}", user=self.user)
        return new
