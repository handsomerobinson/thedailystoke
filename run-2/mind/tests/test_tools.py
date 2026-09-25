import shutil
import tempfile
import unittest
from pathlib import Path

from mind.tools.code_exec import CodeExecTool
from mind.tools.notes import NotesTool
from mind.tools.web_search import WebSearchTool


class TestCodeExecTool(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.tool = CodeExecTool(timeout_seconds=3, sandbox_dir=self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_runs_simple_code(self):
        result = self.tool.run(code="print('hello')")
        self.assertTrue(result.ok)
        self.assertEqual(result.output.strip(), "hello")

    def test_captures_error(self):
        result = self.tool.run(code="print(1/0)")
        self.assertFalse(result.ok)
        self.assertIn("ZeroDivisionError", result.error)

    def test_timeout_enforced(self):
        tool = CodeExecTool(timeout_seconds=0.5, sandbox_dir=self.tmp)
        result = tool.run(code="import time; time.sleep(5)")
        self.assertFalse(result.ok)
        self.assertTrue(result.meta.get("timeout"))

    def test_output_capped(self):
        tool = CodeExecTool(timeout_seconds=3, output_cap_bytes=100, sandbox_dir=self.tmp)
        result = tool.run(code="print('x' * 10000)")
        self.assertTrue(result.truncated)
        self.assertLessEqual(len(result.output.encode("utf-8")), 100)

    def test_empty_code_rejected(self):
        result = self.tool.run(code="")
        self.assertFalse(result.ok)

    def test_no_inherited_env(self):
        # child must not see arbitrary host env vars
        result = self.tool.run(code="import os; print('PATH' in os.environ)")
        self.assertTrue(result.ok)
        self.assertEqual(result.output.strip(), "False")

    def test_scratch_file_cleaned_up(self):
        before = list(self.tmp.glob("*.py"))
        self.tool.run(code="print(1)")
        after = list(self.tmp.glob("*.py"))
        self.assertEqual(len(before), len(after))


class TestNotesTool(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.tool = NotesTool(base_dir=self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_write_read_roundtrip(self):
        w = self.tool.run(action="write", user_id="alice", title="todo", body="buy milk")
        self.assertTrue(w.ok)
        r = self.tool.run(action="read", user_id="alice", title="todo")
        self.assertTrue(r.ok)
        self.assertEqual(r.output, "buy milk")

    def test_list_empty(self):
        result = self.tool.run(action="list", user_id="alice")
        self.assertTrue(result.ok)
        self.assertEqual(result.output, "")

    def test_read_missing_note(self):
        result = self.tool.run(action="read", user_id="alice", title="nope")
        self.assertFalse(result.ok)

    def test_delete(self):
        self.tool.run(action="write", user_id="alice", title="todo", body="x")
        d = self.tool.run(action="delete", user_id="alice", title="todo")
        self.assertTrue(d.ok)
        r = self.tool.run(action="read", user_id="alice", title="todo")
        self.assertFalse(r.ok)

    def test_per_user_isolation(self):
        self.tool.run(action="write", user_id="alice", title="secret", body="alice-only")
        r = self.tool.run(action="read", user_id="bob", title="secret")
        self.assertFalse(r.ok)

    def test_body_size_cap_enforced(self):
        tool = NotesTool(base_dir=self.tmp, max_bytes=10)
        result = tool.run(action="write", user_id="alice", title="big", body="x" * 100)
        self.assertFalse(result.ok)
        self.assertIn("cap", result.error)

    def test_unsafe_title_sanitized(self):
        w = self.tool.run(action="write", user_id="alice", title="../../etc/passwd", body="x")
        self.assertTrue(w.ok)
        user_dir = self.tmp / "alice"
        for p in user_dir.glob("*.txt"):
            self.assertTrue(p.resolve().parent == user_dir.resolve())


class TestWebSearchTool(unittest.TestCase):
    def test_disabled_by_default_degrades_gracefully(self):
        tool = WebSearchTool(enabled=False)
        result = tool.run(query="stoicism")
        self.assertFalse(result.ok)
        self.assertTrue(result.meta.get("degraded"))

    def test_empty_query_rejected(self):
        tool = WebSearchTool(enabled=False)
        result = tool.run(query="")
        self.assertFalse(result.ok)


if __name__ == "__main__":
    unittest.main()
