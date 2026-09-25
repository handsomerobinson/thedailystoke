from mind.scheduler import DirectoryWatcher, Scheduler, _next_daily
from tests.helpers import TempDirCase


def ok_runner(job):
    return {"ok": True, "status": "answered", "summary": "done"}


class SchedulerTests(TempDirCase):
    def setUp(self):
        super().setUp()
        self.s = Scheduler(self.tmp, self.clock)

    def test_every_job_runs_when_due_and_reschedules(self):
        j = self.s.add_job("alice", "n", "t", every_s=3600)
        self.assertEqual(self.s.tick(ok_runner), [])
        self.clock.advance(3600)
        self.assertEqual(len(self.s.tick(ok_runner)), 1)
        self.assertEqual(self.s.tick(ok_runner), [])
        self.assertAlmostEqual(self.s.get(j)["next_run"], self.clock.now() + 3600)

    def test_missed_runs_are_coalesced(self):
        self.s.add_job("alice", "n", "t", every_s=300)
        self.clock.advance(86400)
        self.assertEqual(len(self.s.tick(ok_runner)), 1)
        self.assertEqual(self.s.tick(ok_runner), [])

    def test_min_interval_and_validation(self):
        with self.assertRaises(ValueError):
            self.s.add_job("alice", "n", "t", every_s=5)
        with self.assertRaises(ValueError):
            self.s.add_job("alice", "n", "t")
        with self.assertRaises(ValueError):
            self.s.add_job("../x", "n", "t", every_s=60)

    def test_at_job_runs_once(self):
        j = self.s.add_job("alice", "n", "t", at=self.clock.now() + 10)
        self.clock.advance(10)
        self.assertEqual(len(self.s.tick(ok_runner)), 1)
        self.clock.advance(10**6)
        self.assertEqual(self.s.tick(ok_runner), [])
        self.assertEqual(self.s.get(j)["enabled"], 0)

    def test_daily(self):
        nxt = _next_daily(self.clock.now(), "09:30")
        self.assertGreater(nxt, self.clock.now())
        self.assertLessEqual(nxt - self.clock.now(), 86400)

    def test_event_job_wakes_on_emit_with_payloads(self):
        seen = []
        self.s.add_job("alice", "n", "handle", event="file_arrived")
        self.assertEqual(self.s.tick(ok_runner), [])
        self.s.emit("file_arrived", "file arrived: a.txt")
        self.s.emit("file_arrived", "file arrived: b.txt")
        self.s.tick(lambda j: seen.append(j["pending_payload"]) or {"ok": True})
        self.assertIn("a.txt", seen[0])
        self.assertIn("b.txt", seen[0])
        self.assertEqual(self.s.tick(ok_runner), [])

    def test_emit_scoped_to_user(self):
        self.s.add_job("alice", "n", "t", event="e")
        self.s.add_job("bob", "n", "t", event="e")
        self.assertEqual(self.s.emit("e", user="bob"), 1)

    def test_failure_backoff_and_isolation(self):
        bad = self.s.add_job("alice", "bad", "t", every_s=60, start_now=True)
        good = self.s.add_job("alice", "good", "t", every_s=60, start_now=True)

        def runner(job):
            if job["id"] == bad:
                raise RuntimeError("boom")
            return {"ok": True}
        res = {r["job"]: r for r in self.s.tick(runner)}
        self.assertEqual(res[bad]["status"], "crashed")
        self.assertTrue(res[good]["ok"])
        self.assertEqual(self.s.get(bad)["failures"], 1)
        # repeated failures back off beyond the base interval
        for _ in range(4):
            self.clock.advance(10**5)
            self.s.tick(runner)
        j = self.s.get(bad)
        self.assertGreaterEqual(j["next_run"] - self.clock.now(), 60 * 2 ** 4)

    def test_gives_up_after_many_failures(self):
        j = self.s.add_job("alice", "bad", "t", every_s=60, start_now=True)
        for _ in range(10):
            self.s.tick(lambda job: {"ok": False})
            self.clock.advance(10**5)
        self.assertEqual(self.s.get(j)["enabled"], 0)

    def test_lease_prevents_double_run(self):
        self.s.add_job("alice", "n", "t", every_s=60, start_now=True)
        other = Scheduler(self.tmp, self.clock)  # a second daemon on the same DB
        runs = []

        def runner(job):
            runs.append(job["id"])
            other.tick(lambda j: runs.append("DOUBLE") or {"ok": True})  # tries while we hold the lease
            return {"ok": True}
        self.s.tick(runner)
        self.assertEqual(len(runs), 1)

    def test_run_history(self):
        j = self.s.add_job("alice", "n", "t", every_s=60, start_now=True)
        self.s.tick(ok_runner)
        self.assertEqual(self.s.runs(j)[0]["status"], "answered")

    def test_directory_watcher(self):
        self.s.add_job("alice", "n", "t", event="file_arrived")
        d = self.tmp / "in"
        w = DirectoryWatcher(self.s, d, user="alice")
        (d / "x.csv").write_text("1")
        self.assertEqual(w.poll(), ["x.csv"])
        self.assertEqual(w.poll(), [])
        self.assertEqual(len(self.s.due()), 1)
