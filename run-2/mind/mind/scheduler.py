"""Proactivity: schedule tasks to run headless (no user present) and report
back through a pluggable reporter.

Decision: no background threads/daemons/cron dependency — a Scheduler
holds a list of ScheduledTask records (persisted as JSON) and exposes
`tick(now)`, which the caller (demo, cron job, or a real event loop)
invokes; this keeps the whole thing deterministic and trivially testable
without sleeping in tests.

Decision: "events" are modeled the same way as "schedules" — an event is
just a schedule whose `due(now)` check is replaced by an explicit
`fire_event(event_name)` call from whoever noticed the event. Same
task/report/audit path either way.
"""
from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional

from . import config
from .agent import Agent, TaskResult

Reporter = Callable[[str, TaskResult], None]


def print_reporter(user_id: str, result: TaskResult) -> None:
    status = "OK" if result.ok else f"FAILED ({result.stopped_reason})"
    print(f"[scheduler->report] user={user_id} task={result.task_id} status={status} output={result.output[:200]!r}")


@dataclass
class ScheduledTask:
    id: str
    user_id: str
    description: str
    interval_seconds: Optional[float] = None  # None => one-shot / event-only
    next_run: float = field(default_factory=time.time)
    last_run: Optional[float] = None
    enabled: bool = True
    event_name: Optional[str] = None  # if set, only fires via fire_event

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "description": self.description,
            "interval_seconds": self.interval_seconds,
            "next_run": self.next_run,
            "last_run": self.last_run,
            "enabled": self.enabled,
            "event_name": self.event_name,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ScheduledTask":
        return cls(**d)


class Scheduler:
    def __init__(
        self,
        agent: Agent,
        store_path: Optional[Path] = None,
        reporter: Reporter = print_reporter,
    ):
        self.agent = agent
        self.store_path = store_path or config.SCHEDULE_STORE_PATH
        self.reporter = reporter
        self.tasks: Dict[str, ScheduledTask] = {}
        self._load()

    # -- persistence ------------------------------------------------------
    def _load(self) -> None:
        if self.store_path.exists():
            raw = json.loads(self.store_path.read_text(encoding="utf-8"))
            self.tasks = {t["id"]: ScheduledTask.from_dict(t) for t in raw}

    def _save(self) -> None:
        self.store_path.parent.mkdir(parents=True, exist_ok=True)
        self.store_path.write_text(
            json.dumps([t.to_dict() for t in self.tasks.values()], indent=2), encoding="utf-8"
        )

    # -- scheduling ---------------------------------------------------------
    def schedule(
        self,
        user_id: str,
        description: str,
        interval_seconds: Optional[float] = None,
        start_at: Optional[float] = None,
        event_name: Optional[str] = None,
    ) -> ScheduledTask:
        task = ScheduledTask(
            id=uuid.uuid4().hex[:10],
            user_id=user_id,
            description=description,
            interval_seconds=interval_seconds,
            next_run=start_at if start_at is not None else time.time(),
            event_name=event_name,
        )
        self.tasks[task.id] = task
        self._save()
        return task

    def cancel(self, task_id: str) -> bool:
        if task_id in self.tasks:
            del self.tasks[task_id]
            self._save()
            return True
        return False

    # -- execution ---------------------------------------------------------
    def tick(self, now: Optional[float] = None) -> List[TaskResult]:
        """Run every due, enabled, non-event-only task. Headless: no user
        interaction happens here (the agent's approver must be able to
        decide alone, e.g. an auto_approver)."""
        now = now if now is not None else time.time()
        results = []
        for task in list(self.tasks.values()):
            if not task.enabled or task.event_name is not None:
                continue
            if task.next_run > now:
                continue
            results.append(self._run_and_report(task, now))
        self._save()
        return results

    def fire_event(self, event_name: str, now: Optional[float] = None) -> List[TaskResult]:
        now = now if now is not None else time.time()
        results = []
        for task in list(self.tasks.values()):
            if not task.enabled or task.event_name != event_name:
                continue
            results.append(self._run_and_report(task, now))
        self._save()
        return results

    def _run_and_report(self, task: ScheduledTask, now: float) -> TaskResult:
        result = self.agent.run_task(task.user_id, task.description, task_id=task.id + f"-{int(now)}")
        task.last_run = now
        if task.interval_seconds:
            task.next_run = now + task.interval_seconds
        else:
            task.enabled = False  # one-shot tasks disable themselves after firing
        self.reporter(task.user_id, result)
        return result
