from mind.audit import AuditLog
from mind.permissions import (ActionRequest, DenyAllApprover, HeadlessApprover, InteractiveApprover,
                              PendingApprovals, PermissionGate, PolicyApprover, Tier)
from tests.helpers import TempDirCase


def req(tier, tool="t", headless=False):
    return ActionRequest("alice", tool, tier, {"a": 1}, f"{tool}(a=1)", f"{tool} x", headless=headless)


class GateTests(TempDirCase):
    def gate(self, approver):
        self.audit = AuditLog(self.tmp / "audit.jsonl")
        return PermissionGate(approver, self.audit)

    def test_read_is_free_and_logged(self):
        g = self.gate(DenyAllApprover())
        self.assertTrue(g.authorize(req(Tier.READ)).allowed)
        self.assertEqual([e["event"] for e in self.audit.entries()], ["permission.request", "permission.decision"])

    def test_write_needs_approval(self):
        self.assertFalse(self.gate(DenyAllApprover()).authorize(req(Tier.WRITE)).allowed)
        self.assertTrue(self.gate(PolicyApprover({"t"})).authorize(req(Tier.WRITE)).allowed)

    def test_irreversible_needs_exact_phrase(self):
        self.assertTrue(self.gate(PolicyApprover(irreversible_grants={"t"})).authorize(req(Tier.IRREVERSIBLE)).allowed)
        # write grant does NOT cover irreversible
        self.assertFalse(self.gate(PolicyApprover({"t"})).authorize(req(Tier.IRREVERSIBLE)).allowed)
        inter = InteractiveApprover(input_fn=lambda prompt: "y", output_fn=lambda s: None)
        d = self.gate(inter).authorize(req(Tier.IRREVERSIBLE))
        self.assertFalse(d.allowed)
        self.assertIn("did not match", d.reason)
        inter = InteractiveApprover(input_fn=lambda prompt: "t x", output_fn=lambda s: None)
        self.assertTrue(self.gate(inter).authorize(req(Tier.IRREVERSIBLE)).allowed)

    def test_interactive_always_this_session(self):
        answers = iter(["a"])
        inter = InteractiveApprover(input_fn=lambda p: next(answers), output_fn=lambda s: None)
        g = self.gate(inter)
        self.assertTrue(g.authorize(req(Tier.WRITE)).allowed)
        self.assertTrue(g.authorize(req(Tier.WRITE)).allowed)  # no second prompt (iterator exhausted otherwise)

    def test_interactive_eof_denies(self):
        def eof(p):
            raise EOFError
        g = self.gate(InteractiveApprover(input_fn=eof, output_fn=lambda s: None))
        self.assertFalse(g.authorize(req(Tier.WRITE)).allowed)
        self.assertFalse(g.authorize(req(Tier.IRREVERSIBLE)).allowed)

    def test_headless_grants_and_queue(self):
        pend = PendingApprovals(self.tmp / "p.db")
        g = self.gate(HeadlessApprover({"t"}, pend))
        self.assertTrue(g.authorize(req(Tier.WRITE, headless=True)).allowed)
        self.assertFalse(g.authorize(req(Tier.WRITE, tool="other", headless=True)).allowed)
        d = g.authorize(req(Tier.IRREVERSIBLE, headless=True))
        self.assertFalse(d.allowed)
        self.assertIsNotNone(d.pending_id)
        items = pend.list("alice")
        self.assertEqual(items[0]["phrase"], "t x")
        self.assertEqual(pend.list("bob"), [])
        pend.resolve(d.pending_id, "alice", "done")
        self.assertEqual(pend.list("alice"), [])

    def test_broken_approver_denies(self):
        class Boom(DenyAllApprover):
            def approve(self, r):
                raise RuntimeError("x")
        self.assertFalse(self.gate(Boom()).authorize(req(Tier.WRITE)).allowed)

    def test_fail_closed_when_audit_unwritable(self):
        d = self.tmp / "audit_dir"
        d.mkdir()
        g = PermissionGate(PolicyApprover({"t"}), AuditLog(d))
        self.assertFalse(g.authorize(req(Tier.WRITE)).allowed)
        self.assertTrue(g.authorize(req(Tier.READ)).allowed)
