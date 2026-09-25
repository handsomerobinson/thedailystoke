from mind.memory import MemoryStore
from mind.permissions import ActionRequest, ConsoleApprover, DenyAll, PermissionGate, ScriptedApprover, Tier
from tests.helpers import TempDirCase


def req(tool, tier, **kw):
    return ActionRequest("alice", tool, tier, kw.pop("args", {"x": 1}), **kw)


class PermissionTests(TempDirCase):
    def setUp(self):
        super().setUp()
        self.mem = MemoryStore(self.tmp, "alice", self.clock)

    def test_read_is_free(self):
        self.assertTrue(PermissionGate(DenyAll()).check(req("recall", Tier.READ)).allowed)

    def test_write_needs_approval_or_grant(self):
        self.assertFalse(PermissionGate(DenyAll()).check(req("write_note", Tier.WRITE)).allowed)
        self.assertTrue(PermissionGate(ScriptedApprover({"write_note": True})).check(req("write_note", Tier.WRITE)).allowed)
        self.assertTrue(PermissionGate(DenyAll(), grants={"write_note"}).check(req("write_note", Tier.WRITE)).allowed)

    def test_grants_never_cover_irreversible(self):
        g = PermissionGate(ScriptedApprover(default=True), grants={"delete_note"})
        self.assertFalse(g.check(req("delete_note", Tier.IRREVERSIBLE)).allowed)

    def test_headless_defers_and_one_shot_approval(self):
        g = PermissionGate(DenyAll(), memory=self.mem, headless=True)
        d = g.check(req("send_message", Tier.IRREVERSIBLE, headless=True))
        self.assertFalse(d.allowed)
        self.assertTrue(d.deferred)
        self.mem.resolve_approval(d.approval_id, True)
        self.assertTrue(g.check(req("send_message", Tier.IRREVERSIBLE, headless=True)).allowed)
        self.assertFalse(g.check(req("send_message", Tier.IRREVERSIBLE, headless=True)).allowed)

    def test_approval_is_bound_to_exact_arguments(self):
        g = PermissionGate(DenyAll(), memory=self.mem, headless=True)
        d = g.check(req("send_message", Tier.IRREVERSIBLE, args={"to": "bob"}))
        self.mem.resolve_approval(d.approval_id, True)
        self.assertFalse(g.check(req("send_message", Tier.IRREVERSIBLE, args={"to": "eve"})).allowed)

    def test_headless_write_with_grant_runs(self):
        g = PermissionGate(DenyAll(), memory=self.mem, grants={"write_note"}, headless=True)
        self.assertTrue(g.check(req("write_note", Tier.WRITE)).allowed)

    def test_console_requires_exact_confirmation_code(self):
        r = req("delete_note", Tier.IRREVERSIBLE)
        said = []
        yes = ConsoleApprover(input_fn=lambda _: "y", output_fn=said.append)
        self.assertFalse(PermissionGate(yes).check(r).allowed)
        exact = ConsoleApprover(input_fn=lambda _: r.confirmation_code, output_fn=said.append)
        self.assertTrue(PermissionGate(exact).check(r).allowed)
        self.assertIn(r.confirmation_code, said[-1])

    def test_console_eof_denies(self):
        def eof(_):
            raise EOFError
        self.assertFalse(PermissionGate(ConsoleApprover(input_fn=eof, output_fn=lambda _: None))
                         .check(req("write_note", Tier.WRITE)).allowed)

    def test_broken_approver_fails_closed(self):
        class Broken(DenyAll):
            def approve_write(self, r):
                raise RuntimeError("ui crashed")
        d = PermissionGate(Broken()).check(req("write_note", Tier.WRITE))
        self.assertFalse(d.allowed)
        self.assertIn("failing closed", d.reason)
