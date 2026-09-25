import shutil
import tempfile
import unittest
from pathlib import Path

from mind.agent import Agent
from mind.audit import AuditLog
from mind.memory import MemoryStore
from mind.permissions import auto_approver
from mind.providers.mock import MockProvider
from mind.scheduler import Scheduler
from mind.tools import default_toolset


class SchedulerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.memory_store = MemoryStore(base_dir=self.tmp / "memory")
        self.audit = AuditLog(path=self.tmp / "audit.jsonl")
        self.agent = Agent(
            provider=MockProvider(),
            tools=default_toolset(),
            memory_store=self.memory_store,
            audit_log=self.audit,
            approver=auto_approver(),
        )

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_one_shot_task_runs_once_and_disables(self):
        reports = []
        sched = Scheduler(self.agent, store_path=self.tmp / "sched.json", reporter=lambda u, r: reports.append((u, r)))
        sched.schedule("alice", "please save a note about x", start_at=0)
        ran = sched.tick(now=1000)
        self.assertEqual(len(ran), 1)
        self.assertEqual(len(reports), 1)
        # second tick should not re-run a disabled one-shot task
        ran2 = sched.tick(now=2000)
        self.assertEqual(len(ran2), 0)

    def test_recurring_task_reschedules(self):
        sched = Scheduler(self.agent, store_path=self.tmp / "sched.json", reporter=lambda u, r: None)
        task = sched.schedule("alice", "please save a note about y", interval_seconds=100, start_at=0)
        sched.tick(now=1)
        self.assertAlmostEqual(sched.tasks[task.id].next_run, 101)
        self.assertTrue(sched.tasks[task.id].enabled)

    def test_not_yet_due_task_does_not_run(self):
        sched = Scheduler(self.agent, store_path=self.tmp / "sched.json", reporter=lambda u, r: None)
        sched.schedule("alice", "please save a note about z", start_at=5000)
        ran = sched.tick(now=1000)
        self.assertEqual(ran, [])

    def test_event_only_task_ignored_by_tick(self):
        sched = Scheduler(self.agent, store_path=self.tmp / "sched.json", reporter=lambda u, r: None)
        sched.schedule("alice", "please save a note about w", event_name="user_logged_in")
        ran = sched.tick(now=999999)
        self.assertEqual(ran, [])

    def test_fire_event_runs_matching_tasks_only(self):
        reports = []
        sched = Scheduler(self.agent, store_path=self.tmp / "sched.json", reporter=lambda u, r: reports.append((u, r)))
        sched.schedule("alice", "please save a note about login", event_name="user_logged_in")
        sched.schedule("alice", "please save a note about logout", event_name="user_logged_out")
        ran = sched.fire_event("user_logged_in")
        self.assertEqual(len(ran), 1)
        self.assertEqual(len(reports), 1)

    def test_persists_across_instances(self):
        sched1 = Scheduler(self.agent, store_path=self.tmp / "sched.json", reporter=lambda u, r: None)
        sched1.schedule("alice", "persisted task", interval_seconds=60, start_at=0)
        sched2 = Scheduler(self.agent, store_path=self.tmp / "sched.json", reporter=lambda u, r: None)
        self.assertEqual(len(sched2.tasks), 1)

    def test_cancel(self):
        sched = Scheduler(self.agent, store_path=self.tmp / "sched.json", reporter=lambda u, r: None)
        task = sched.schedule("alice", "cancel me", start_at=0)
        self.assertTrue(sched.cancel(task.id))
        self.assertFalse(sched.cancel(task.id))
        self.assertEqual(len(sched.tasks), 0)


if __name__ == "__main__":
    unittest.main()
