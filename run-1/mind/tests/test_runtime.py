import contextlib
import io
import os

from mind import Mind, PythonTests, ScriptedApprover, TaskSpec
from mind.cli import main as cli
from mind.providers import MockBrain
from tests.helpers import TempDirCase


class RuntimeTests(TempDirCase):
    def mind(self, **kw):
        return Mind(self.config(**kw), clock=self.clock)

    def test_session_ask_and_episode(self):
        m = self.mind()
        r = m.session("alice").ask("calculate 2+2")
        self.assertTrue(r.ok)
        self.assertEqual(len(m.memory("alice").items(kind="episode")), 1)

    def test_headless_job_reports_and_defers(self):
        m = self.mind()
        m.scheduler.add_job("alice", "note", "save a note titled x: y", every_s=60, start_now=True)
        res = m.tick()
        self.assertEqual(res[0]["status"], "needs_approval")
        mem = m.memory("alice")
        self.assertIsNone(mem.read_note("x"))
        self.assertEqual(len(mem.approvals()), 1)
        self.assertIn("Waiting for your approval", mem.inbox()[0]["body"])
        m.resolve_approval("alice", mem.approvals()[0]["id"], True)
        self.assertEqual(mem.read_note("x")["body"], "y")          # executed on approval
        self.assertIn("approved action write_note", mem.inbox()[-1]["title"])
        self.assertEqual(mem.approvals(), [])

    def test_denied_approval_does_not_execute(self):
        m = self.mind()
        m.scheduler.add_job("alice", "note", "save a note titled x: y", every_s=60, start_now=True)
        m.tick()
        mem = m.memory("alice")
        m.resolve_approval("alice", mem.approvals()[0]["id"], False)
        self.assertIsNone(mem.read_note("x"))

    def test_daily_cap_across_tasks(self):
        m = self.mind(mock_price_in_per_mtok=5, mock_price_out_per_mtok=25, task_budget_usd=0.05,
                      daily_budget_usd=0.04, max_steps=500, max_output_tokens=1024)
        a = m.session("dave").ask("keep going forever until you find it")
        b = m.session("dave").ask("keep going forever until you find it")
        self.assertEqual(a.status, "budget_exceeded")
        self.assertLessEqual(a.budget["spent_usd"] + b.budget["spent_usd"], 0.04 + 1e-9)
        self.assertEqual(m.task_budget("erin").limit_usd, 0.04)  # other users unaffected

    def test_solve_via_session(self):
        m = self.mind()
        t = TaskSpec("Write a python function dedupe(xs) removing duplicates, keeping first-seen order.",
                     checker=PythonTests("dedupe", [([[3, 1, 3, 2, 1]], [3, 1, 2])]))
        self.assertTrue(m.session("alice").solve(t).success)

    def test_schedule_task_tool_from_conversation(self):
        m = self.mind()
        r = m.session("alice", approver=ScriptedApprover({"schedule_task": True})).ask(
            "every 2 hours, prepare my daily briefing")
        self.assertTrue(r.ok, r.answer)
        jobs = m.scheduler.list_jobs("alice")
        self.assertEqual(float(jobs[0]["spec"]), 7200.0)

    def test_status(self):
        st = self.mind().status()
        self.assertIn("mock", st["provider"])

    def test_injected_provider(self):
        m = Mind(self.config(), clock=self.clock, provider=MockBrain(model="custom"))
        self.assertTrue(m.session("a").ask("calculate 1+1").ok)


class CLITests(TempDirCase):
    def run_cli(self, *args):
        buf, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(err):
            code = cli(["--data-dir", str(self.tmp), *args])
        return code, buf.getvalue() + err.getvalue()

    def test_status_ask_jobs_tick_inbox_audit(self):
        code, out = self.run_cli("status")
        self.assertEqual(code, 0)
        self.assertIn("mock", out)
        code, out = self.run_cli("ask", "--user", "alice", "calculate 6*7")
        self.assertIn("42", out)
        code, out = self.run_cli("jobs", "add", "--user", "alice", "--every", "60", "prepare my daily briefing")
        jid = out.strip()
        self.assertTrue(jid.startswith("job_"))
        _, out = self.run_cli("jobs", "list")
        self.assertIn(jid, out)
        self.assertEqual(self.run_cli("emit", "nothing")[0], 0)
        _, out = self.run_cli("approvals", "--user", "alice")
        self.assertEqual(out.strip(), "")
        code, out = self.run_cli("audit", "verify")
        self.assertEqual(code, 0)
        self.assertIn("OK", out)
        self.assertEqual(self.run_cli("inbox", "--user", "alice")[0], 0)
        self.assertEqual(self.run_cli("serve", "--interval", "0", "--max-ticks", "1")[0], 0)

    def test_misconfigured_provider_exits_2(self):
        old = os.environ.get("MIND_PROVIDER")
        os.environ["MIND_PROVIDER"] = "anthropic"
        key = os.environ.pop("ANTHROPIC_API_KEY", None)
        try:
            code, out = self.run_cli("status")
        finally:
            if old is None:
                os.environ.pop("MIND_PROVIDER", None)
            else:
                os.environ["MIND_PROVIDER"] = old
            if key:
                os.environ["ANTHROPIC_API_KEY"] = key
        self.assertEqual(code, 2)
        self.assertIn("ANTHROPIC_API_KEY", out)


class Round1RuntimeTests(TempDirCase):
    def test_live_daily_guard_blocks_concurrent_overspend(self):
        m = Mind(self.config(mock_price_in_per_mtok=5, mock_price_out_per_mtok=25, task_budget_usd=0.05,
                             daily_budget_usd=0.05, max_output_tokens=1024), clock=self.clock)
        b1 = m.task_budget("dave")
        b2 = m.task_budget("dave")      # both created before any spend (concurrent tasks)
        self.assertEqual((b1.limit_usd, b2.limit_usd), (0.05, 0.05))
        b1.preflight(100, 1024, (5, 25))
        b1.record(100, 1500, (5, 25))   # ~0.038 recorded in the shared ledger
        from mind.cost import BudgetExceeded
        with self.assertRaises(BudgetExceeded):
            b2.preflight(100, 1024, (5, 25))   # b2's own cap is fine, the live daily guard is not

    def test_recall_ignores_stopwords(self):
        m = Mind(self.config(), clock=self.clock)
        mem = m.memory("alice")
        mem.set_fact("name", "Alice")
        mem.set_fact("city", "Oslo")
        from mind.tools import Recall, ToolContext
        r = Recall().run({"query": "what is my city"}, ToolContext("alice", mem, m.config, self.clock))
        self.assertIn("city", r.content)
        self.assertNotIn("name", r.content)


class Round2RuntimeTests(TempDirCase):
    def mind(self, **kw):
        return Mind(self.config(**kw), clock=self.clock)

    def test_headless_failure_writes_a_reflection_the_next_run_reads(self):
        m = self.mind(max_steps=3)
        jid = m.scheduler.add_job("alice", "runaway", "keep going forever until you find it", every_s=60,
                                  start_now=True)
        m.tick()
        mem = m.memory("alice")
        refl = mem.items(kind="reflection")
        self.assertEqual(len(refl), 1)
        self.assertIn("step_limit", refl[0]["text"])
        from mind.reflexion import task_signature
        self.assertEqual(refl[0]["task_sig"], task_signature("keep going forever until you find it"))
        sysprompts = []
        orig = m.provider.complete

        def spy(system, *a, **k):
            sysprompts.append(system)
            return orig(system, *a, **k)
        m.provider.complete = spy
        self.clock.advance(120)
        m.tick()
        self.assertIn("step_limit", sysprompts[0])   # the lesson is in the next run's prompt
        self.assertTrue(jid)

    def test_export_and_forget_user(self):
        m = self.mind()
        m.session("alice", approver=ScriptedApprover({"remember_fact": True})).ask("remember that my city is Oslo")
        m.scheduler.add_job("alice", "n", "t", every_s=60)
        data = m.export_user("alice")
        self.assertEqual(data["facts"]["city"], "Oslo")
        self.assertEqual(len(data["jobs"]), 1)
        out = m.forget_user("alice")
        self.assertTrue(out["files_removed"])
        self.assertEqual(m.scheduler.list_jobs("alice"), [])
        self.assertIsNone(m.memory("alice").get_fact("city"))
        self.assertEqual(m.audit.records()[-1]["event"], "user.forgotten")

    def test_maintenance_compacts(self):
        m = self.mind()
        mem = m.memory("alice")
        for i in range(30):
            mem.add_item("episode", f"episode {i}")
        m._last_maint = -10**12
        m.maintenance(max_items=10)
        self.assertEqual(len(mem.items(limit=1000)), 10)


class Round2CLITests(TempDirCase):
    def run_cli(self, *args):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            code = cli(["--data-dir", str(self.tmp), *args])
        return code, buf.getvalue()

    def test_forget_requires_matching_confirmation(self):
        self.run_cli("ask", "--user", "alice", "calculate 1+1")
        code, _ = self.run_cli("forget", "--user", "alice", "--confirm", "bob")
        self.assertEqual(code, 1)
        code, out = self.run_cli("export", "--user", "alice")
        self.assertIn('"user": "alice"', out)
        code, out = self.run_cli("forget", "--user", "alice", "--confirm", "alice")
        self.assertEqual(code, 0)
        self.assertIn("files_removed", out)
