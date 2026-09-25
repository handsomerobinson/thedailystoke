import json

from mind.reporting import Outbox
from mind.scheduler import MAX_FAILURES, Scheduler
from tests.helpers import TempDirCase


class SchedulerTests(TempDirCase):
    def setUp(self):
        super().setUp()
        self.t = [1_700_000_000.0]
        self.rt = self.runtime()
        self.sch = Scheduler(self.rt, clock=lambda: self.t[0])

    def test_interval_runs_when_due_once_per_occurrence(self):
        jid = self.sch.add_job("alice", "calc", "what is 2+2", "interval", "3600")
        self.assertEqual(self.sch.tick(), [])
        self.t[0] += 3600
        recs = self.sch.tick()
        self.assertEqual([(r.job_id, r.status) for r in recs], [(jid, "answered")])
        self.assertEqual(self.sch.tick(), [])  # claimed; not re-run
        self.assertIn("2+2 = 4", recs[0].report)
        self.assertEqual(len(self.rt.outbox.list("alice")), 1)

    def test_concurrent_claim_single_run(self):
        self.sch.add_job("alice", "calc", "what is 1+1", "interval", "60", run_now=True)
        other = Scheduler(self.rt, clock=lambda: self.t[0])
        a, b = self.sch.tick(), other.tick()
        self.assertEqual(len(a) + len(b), 1)

    def test_daily_and_once(self):
        jid = self.sch.add_job("alice", "d", "what is 3+3", "daily", "07:30")
        job = next(j for j in self.sch.list_jobs("alice") if j["id"] == jid)
        self.assertGreater(job["next_run"], self.t[0])
        self.assertLessEqual(job["next_run"] - self.t[0], 86400)
        once = self.sch.add_job("alice", "o", "what is 4+4", "once", str(self.t[0] + 10))
        self.t[0] += 11
        self.assertEqual([r.job_id for r in self.sch.tick()], [once])
        self.assertEqual(next(j for j in self.sch.list_jobs() if j["id"] == once)["enabled"], 0)

    def test_validation(self):
        for args in (("interval", "abc"), ("daily", "25:00"), ("bogus", "1"), ("event", "../x")):
            with self.assertRaises(ValueError):
                self.sch.add_job("alice", "x", "t", *args)
        with self.assertRaises(ValueError):
            self.sch.add_job("alice", "x", "t", "interval", "60", grants=["format_disk"])
        with self.assertRaises(ValueError):
            self.sch.add_job("../bob", "x", "t", "interval", "60")

    def test_event_trigger_with_payload(self):
        self.sch.add_job("alice", "e", "what is {n}*2", "event", "number_arrived")
        self.sch.emit_event("alice", "number_arrived", {"n": 21})
        self.sch.emit_event("bob", "number_arrived", {"n": 5})  # bob has no such job
        recs = self.sch.tick()
        self.assertEqual(len(recs), 1)
        self.assertIn("42", recs[0].report)
        self.assertEqual(self.sch.tick(), [])  # events consumed

    def test_inbox_watcher(self):
        self.note("alice", "seed", "x")
        self.sch.add_job("alice", "inbox", "Count the words in note {note}", "event", "inbox_file", grants=["python_exec"])
        inbox = self.settings.user_dir("alice") / "inbox"
        inbox.mkdir()
        (inbox / "hello.txt").write_text("a b c")
        (inbox / "skip.bin").write_bytes(b"\0")
        recs = self.sch.tick()
        self.assertEqual(len(recs), 1)
        self.assertIn("inbox-hello", recs[0].report)
        self.assertFalse((inbox / "hello.txt").exists())
        self.assertTrue(list((inbox / "processed").iterdir()))

    def test_headless_grants_and_irreversible_queue(self):
        self.note("alice", "keep", "important")
        self.sch.add_job("alice", "no-grant", "Save a note called x: y", "interval", "60", run_now=True)
        self.sch.add_job("alice", "delete", "Delete the note keep", "interval", "60", run_now=True, grants=["note_delete"])
        recs = {r.name: r for r in self.sch.tick()}
        self.assertIn("denied", recs["no-grant"].report)
        self.assertIn("queued", recs["delete"].report)
        self.assertTrue(recs["delete"].pending)
        self.assertTrue((self.settings.user_dir("alice") / "notes" / "keep.md").exists())
        self.assertEqual(len(self.rt.pending.list("alice")), 1)

    def test_failure_backoff_and_auto_disable(self):
        jid = self.sch.add_job("alice", "bad", "compose an opera", "interval", "60", run_now=True,
                               evaluator={"type": "contains", "terms": ["aria"]})
        for i in range(MAX_FAILURES):
            recs = self.sch.tick()
            self.assertEqual(len(recs), 1, i)
            self.assertEqual(recs[0].status, "failed")
            job = next(j for j in self.sch.list_jobs() if j["id"] == jid)
            self.assertGreaterEqual(job["next_run"] - self.t[0], 60 * 2 ** (i + 1) if i < 5 else 0)
            self.t[0] = job["next_run"] or self.t[0]
        self.assertIn("DISABLED", recs[0].report)
        job = next(j for j in self.sch.list_jobs() if j["id"] == jid)
        self.assertEqual(job["enabled"], 0)
        self.assertTrue(self.sch.set_enabled("alice", jid, True))

    def test_one_bad_job_does_not_stop_others(self):
        self.sch.add_job("alice", "ok", "what is 1+1", "interval", "60", run_now=True)
        bad = self.sch.add_job("alice", "broken", "what is 2+2", "interval", "60", run_now=True)
        import sqlite3
        with sqlite3.connect(str(self.sch.path)) as db:
            db.execute("UPDATE jobs SET evaluator='{not json' WHERE id=?", (bad,))
        recs = {r.name: r.status for r in self.sch.tick()}
        self.assertEqual(recs, {"ok": "answered", "broken": "error"})

    def test_remove_is_per_user(self):
        jid = self.sch.add_job("alice", "x", "what is 1+1", "interval", "60")
        self.assertFalse(self.sch.remove_job("bob", jid))
        self.assertTrue(self.sch.remove_job("alice", jid))

    def test_daemon_survives_tick_errors(self):
        calls = []
        def bad_tick(now=None):
            calls.append(1)
            raise RuntimeError("db gone")
        self.sch.tick = bad_tick
        logs = []
        self.sch.daemon(interval=0, stop=lambda: len(calls) >= 3, log=logs.append, sleep=lambda s: None)
        self.assertEqual(len(calls), 3)
        self.assertTrue(any("continuing" in l for l in logs))

    def test_agent_can_schedule_but_without_grants(self):
        from mind.agent import Task  # noqa: F401
        from mind.permissions import PolicyApprover
        from mind.tools.base import ToolContext
        from mind.types import ToolCall
        reg = self.rt.registry(PolicyApprover({"schedule_job"}))
        ctx = ToolContext("alice", self.settings, scheduler=self.sch)
        r = reg.execute(ToolCall("schedule_job", {"task": "what is 1+1", "every_minutes": 30}), ctx)
        self.assertTrue(r.ok, r.output)
        self.assertEqual(json.loads(self.sch.list_jobs("alice")[0]["grants"]), [])
        self.assertFalse(reg.execute(ToolCall("schedule_job", {"task": "x", "every_minutes": 1}), ctx).ok)


class OutboxTests(TempDirCase):
    def test_outbox_and_webhook_failure_keeps_report(self):
        def fail(url, payload):
            raise ConnectionError("down")
        ob = Outbox(self.settings, webhook_url="http://hook", poster=fail)
        status = ob.send("alice", "Hello", "body")
        self.assertIn("webhook failed", status)
        self.assertEqual(len(ob.list("alice")), 1)
        sent = []
        ob2 = Outbox(self.settings, webhook_url="http://hook", poster=lambda u, p: sent.append(p))
        self.assertIn("delivered", ob2.send("alice", "Hi", "b"))
        self.assertEqual(sent[0]["title"], "Hi")
