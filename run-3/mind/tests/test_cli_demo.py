import contextlib
import io

from mind.cli import main
from tests.helpers import TempDirCase


class CLITests(TempDirCase):
    def cli(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            code = main(["--data-dir", str(self.tmp), "--provider", "mock", *argv])
        return code, out.getvalue()

    def test_run_with_expectation_and_reflection(self):
        self.note("alice", "n", "a  b c")
        code, out = self.cli("run", "--user", "alice", "--approve", "python_exec", "--expect", "3",
                             "Count the words in note n")
        self.assertEqual(code, 0, out)
        self.assertIn("status: success", out)
        self.assertIn("reflection stored", out)

    def test_run_json(self):
        code, out = self.cli("run", "--user", "alice", "--json", "what is 2+2")
        self.assertIn('"status": "answered"', out)

    def test_memory_commands(self):
        self.cli("memory", "add", "--user", "alice", "likes", "hiking")
        code, out = self.cli("memory", "search", "--user", "alice", "hiking")
        self.assertIn("likes hiking", out)
        code, out = self.cli("memory", "search", "--user", "bob", "hiking")
        self.assertNotIn("hiking", out)

    def test_schedule_tick_reports(self):
        code, out = self.cli("schedule", "add", "--user", "alice", "--every", "60", "--now", "what", "is", "5*5")
        self.assertIn("job #1", out)
        code, out = self.cli("tick")
        self.assertIn("25", out)
        code, out = self.cli("reports", "--user", "alice")
        self.assertIn("5*5 = 25", out)
        code, out = self.cli("schedule", "list", "--user", "alice")
        self.assertIn("answered", out)

    def test_event_and_approvals_flow(self):
        self.note("alice", "old", "bye")
        self.cli("schedule", "add", "--user", "alice", "--on-event", "cleanup", "Delete", "the", "note", "old")
        self.cli("event", "emit", "--user", "alice", "cleanup")
        self.cli("tick")
        code, out = self.cli("approvals", "list", "--user", "alice")
        self.assertIn("note_delete old", out)
        code, out = self.cli("approvals", "confirm", "1", "--user", "alice", "--phrase", "wrong")
        self.assertEqual(code, 1)
        self.assertTrue((self.settings.user_dir("alice") / "notes" / "old.md").exists())
        code, out = self.cli("approvals", "confirm", "1", "--user", "bob", "--phrase", "note_delete old")
        self.assertEqual(code, 1)  # other users cannot confirm alice's queue
        code, out = self.cli("approvals", "confirm", "1", "--user", "alice", "--phrase", "note_delete old")
        self.assertEqual(code, 0, out)
        self.assertFalse((self.settings.user_dir("alice") / "notes" / "old.md").exists())
        code, out = self.cli("audit", "verify")
        self.assertIn("OK", out)

    def test_status_and_bad_input(self):
        code, out = self.cli("status")
        self.assertIn("web_search", out)
        self.assertIn("unavailable", out)
        code, _ = self.cli("run", "--user", "../evil", "what is 1+1")
        self.assertEqual(code, 2)


class DemoTest(TempDirCase):
    def test_demo_all_checks_pass(self):
        from mind.demo import main as demo
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            code = demo(data_dir=str(self.tmp / "demo"))
        self.assertEqual(code, 0, out.getvalue()[-3000:])
        self.assertIn("20/20 demo checks passed", out.getvalue())
