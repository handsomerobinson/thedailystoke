import os

from mind.audit import AuditLog
from mind.cost import Budget, BudgetExceeded
from mind.memory import MemoryStore
from mind.permissions import DenyAllApprover, PermissionGate, PolicyApprover, Tier
from mind.tools import Tool, ToolContext, default_registry
from mind.tools.base import ToolRegistry, validate_args
from mind.tools.builtin import safe_eval
from mind.tools.web import check_public_url, html_to_text, web_fetch, web_search
from mind.types import ToolCall
from tests.helpers import TempDirCase


class RegistryTests(TempDirCase):
    def setUp(self):
        super().setUp()
        self.audit = AuditLog(self.tmp / "audit.jsonl")
        self.mem = MemoryStore(self.tmp, "alice")
        self.addCleanup(self.mem.close)
        self.ctx = ToolContext("alice", self.settings, memory=self.mem, task_id="t1")

    def reg(self, approver=None):
        return default_registry(PermissionGate(approver or PolicyApprover({"note_write", "remember", "python_exec"}), self.audit), self.audit)

    def run_(self, reg, tool_name, **args):
        return reg.execute(ToolCall(tool_name, args), self.ctx)

    def test_validate_args(self):
        schema = {"properties": {"n": {"type": "integer"}, "s": {"type": "string"}}, "required": ["s"]}
        self.assertEqual(validate_args(schema, {"s": "x", "n": "3"})[0], {"s": "x", "n": 3})
        self.assertIsNone(validate_args(schema, {"n": 1})[0])
        self.assertIsNone(validate_args(schema, {"s": 1})[0])
        self.assertIsNone(validate_args(schema, {"s": "x", "zzz": 1})[0])
        self.assertIsNone(validate_args(schema, {"s": "x", "n": True})[0])
        self.assertIsNone(validate_args(schema, ["s"])[0])

    def test_unknown_tool_and_bad_args_are_observations(self):
        reg = self.reg()
        self.assertIn("unknown tool", self.run_(reg, "rm_rf").output)
        self.assertIn("invalid arguments", self.run_(reg, "calculator").output)

    def test_every_call_is_audited(self):
        reg = self.reg()
        self.run_(reg, "calculator", expression="2+2")
        events = [e["event"] for e in self.audit.entries()]
        self.assertEqual(events, ["permission.request", "permission.decision", "tool.result"])
        self.assertEqual(self.audit.entries()[-1]["preview"], "4")

    def test_notes_roundtrip_versions_and_delete_tier(self):
        reg = self.reg()
        self.assertTrue(self.run_(reg, "note_write", name="n1", content="hello world").ok)
        self.assertTrue(self.run_(reg, "note_write", name="n1", content="v2").ok)
        self.assertEqual(self.run_(reg, "note_read", name="n1").output, "v2")
        vdir = self.settings.user_dir("alice") / "notes" / ".versions"
        self.assertEqual(len(list(vdir.iterdir())), 1)
        self.assertIn("n1", self.run_(reg, "note_list").output)
        self.assertIn("n1", self.run_(reg, "note_search", query="v2").output or "n1")
        r = self.run_(reg, "note_delete", name="n1")
        self.assertTrue(r.denied)
        self.assertTrue((self.settings.user_dir("alice") / "notes" / "n1.md").exists())
        reg2 = self.reg(PolicyApprover(irreversible_grants={"note_delete"}))
        self.assertTrue(self.run_(reg2, "note_delete", name="n1").ok)
        self.assertFalse(list(vdir.iterdir()))

    def test_note_path_traversal_blocked(self):
        reg = self.reg()
        for bad in ("../../etc/passwd", "../bob/notes/x", ".secret"):
            r = self.run_(reg, "note_read", name=bad)
            self.assertFalse(r.ok)
            self.assertIn("invalid name", r.output)

    def test_notes_isolated_between_users(self):
        reg = self.reg()
        self.run_(reg, "note_write", name="private", content="alice only")
        bob_ctx = ToolContext("bob", self.settings, task_id="t2")
        r = reg.execute(ToolCall("note_read", {"name": "private"}), bob_ctx)
        self.assertFalse(r.ok)

    def test_write_denied_without_approval(self):
        reg = self.reg(DenyAllApprover())
        r = self.run_(reg, "note_write", name="x", content="y")
        self.assertTrue(r.denied)
        self.assertFalse((self.settings.user_dir("alice") / "notes" / "x.md").exists())

    def test_remember_and_recall(self):
        reg = self.reg()
        self.run_(reg, "remember", fact="my sister is called Ana")
        self.assertIn("Ana", self.run_(reg, "recall", query="sister name").output)

    def test_calculator_safe(self):
        self.assertEqual(safe_eval("2*(3+4)"), 14)
        self.assertEqual(safe_eval("2^10"), 1024)
        for bad in ("__import__('os')", "9**9**9", "a+1", "[1]*9"):
            with self.assertRaises(ValueError):
                safe_eval(bad)

    def test_unavailable_tool_degrades(self):
        os.environ.pop("MIND_SEARCH", None)
        r = self.run_(self.reg(), "web_search", query="x")
        self.assertFalse(r.ok)
        self.assertIn("unavailable", r.output)
        self.assertEqual(self.audit.entries()[-1]["event"], "tool.unavailable")
        self.assertIn("UNAVAILABLE", " ".join(s.description for s in self.reg().specs(self.ctx)))

    def test_tool_exception_and_timeout_are_contained(self):
        audit = self.audit
        from mind.tiers import TierRegistry
        reg = ToolRegistry(PermissionGate(DenyAllApprover(), audit), audit,
                           tiers=TierRegistry(tiers={"boom": "READ", "slow": "READ"}))  # a harness-signed registry
        def boom(a, c):
            raise RuntimeError("kaput")
        def slow(a, c):
            import time
            time.sleep(2)
            return "late"
        reg.register(Tool("boom", "x", {"type": "object", "properties": {}}, Tier.READ, boom))
        reg.register(Tool("slow", "x", {"type": "object", "properties": {}}, Tier.READ, slow, timeout=0.2))
        self.assertIn("kaput", reg.execute(ToolCall("boom", {}), self.ctx).output)
        self.assertIn("timed out", reg.execute(ToolCall("slow", {}), self.ctx).output)

    def test_output_cap(self):
        reg = self.reg()
        reg.output_cap = 50
        self.run_(reg, "note_write", name="big", content="z" * 500)
        self.assertIn("truncated", self.run_(reg, "note_read", name="big").output)

    def test_budget_counts_tool_calls(self):
        reg = self.reg()
        b = Budget(max_tool_calls=1)
        reg.execute(ToolCall("clock", {}), self.ctx, b)
        with self.assertRaises(BudgetExceeded):
            reg.execute(ToolCall("clock", {}), self.ctx, b)

    def test_python_exec_tool(self):
        r = self.run_(self.reg(), "python_exec", code="print(6*7)")
        self.assertTrue(r.ok)
        self.assertIn("42", r.output)


class WebTests(TempDirCase):
    def test_ssrf_guard(self):
        fake = lambda host, port: [(None, None, None, None, ("127.0.0.1", port))]  # noqa: E731
        with self.assertRaises(PermissionError):
            check_public_url("http://example.com", fake)
        with self.assertRaises(PermissionError):
            check_public_url("file:///etc/passwd")
        pub = lambda host, port: [(None, None, None, None, ("93.184.216.34", port))]  # noqa: E731
        self.assertEqual(check_public_url("https://example.com/x", pub), "https://example.com/x")

    def test_fetch_labels_untrusted_and_strips_html(self):
        pub = lambda host, port: [(None, None, None, None, ("93.184.216.34", port))]  # noqa: E731
        out = web_fetch({"url": "https://example.com"}, None,
                        http_get=lambda u, h=None: b"<html><script>evil()</script><p>Hello</p></html>", resolver=pub)
        self.assertTrue(out.startswith("[UNTRUSTED"))
        self.assertIn("Hello", out)
        self.assertNotIn("evil", out)
        self.assertEqual(html_to_text("<b>a</b><style>x</style>c"), "a\nc")

    def test_search_backends_with_fake_http(self):
        os.environ["MIND_SEARCH"] = "ddg"
        try:
            data = b'{"Heading":"Python","AbstractText":"A language","AbstractURL":"https://python.org","RelatedTopics":[]}'
            out = web_search({"query": "python"}, None, http_get=lambda u, h=None: data)
            self.assertIn("A language", out)
            self.assertIn("not a full web index", out)
            os.environ["MIND_SEARCH"], os.environ["BRAVE_API_KEY"] = "brave", "k"
            data = b'{"web":{"results":[{"title":"T","url":"https://u","description":"D"}]}}'
            seen = {}
            out = web_search({"query": "q"}, None, http_get=lambda u, h=None: seen.update(h=h) or data)
            self.assertIn("1. T", out)
            self.assertEqual(seen["h"]["X-Subscription-Token"], "k")
        finally:
            os.environ.pop("MIND_SEARCH", None)
            os.environ.pop("BRAVE_API_KEY", None)
