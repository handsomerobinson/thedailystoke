import shutil
import tempfile
import unittest
from pathlib import Path

from mind.audit import AuditLog
from mind.costs import CostCapExceeded, CostTracker
from mind.permissions import IRREVERSIBLE_CONFIRM_PHRASE, PermissionTier, auto_approver


class TestPermissions(unittest.TestCase):
    def test_read_only_always_allowed(self):
        approve = auto_approver(state_changing_ok=False, irreversible_ok=False)
        self.assertTrue(approve("x", PermissionTier.READ_ONLY))

    def test_state_changing_gated(self):
        approve = auto_approver(state_changing_ok=False)
        self.assertFalse(approve("x", PermissionTier.STATE_CHANGING))
        approve2 = auto_approver(state_changing_ok=True)
        self.assertTrue(approve2("x", PermissionTier.STATE_CHANGING))

    def test_irreversible_denied_by_default(self):
        approve = auto_approver()
        self.assertFalse(approve("x", PermissionTier.IRREVERSIBLE))

    def test_confirm_phrase_constant_exists(self):
        self.assertEqual(IRREVERSIBLE_CONFIRM_PHRASE, "CONFIRM IRREVERSIBLE")


class TestAuditLog(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.path = self.tmp / "audit.jsonl"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_record_and_read_back(self):
        log = AuditLog(path=self.path)
        log.record(user_id="alice", actor="agent", action="notes.write", tier="state_changing", granted=True)
        log.record(user_id="bob", actor="agent", action="notes.write", tier="state_changing", granted=False)
        all_entries = list(log.read_all())
        self.assertEqual(len(all_entries), 2)
        alice_entries = log.for_user("alice")
        self.assertEqual(len(alice_entries), 1)
        self.assertTrue(alice_entries[0]["granted"])

    def test_appends_across_instances(self):
        AuditLog(path=self.path).record(user_id="a", actor="x", action="y", tier="read_only", granted=True)
        AuditLog(path=self.path).record(user_id="a", actor="x", action="y2", tier="read_only", granted=True)
        self.assertEqual(len(list(AuditLog(path=self.path).read_all())), 2)


class TestCostTracker(unittest.TestCase):
    def test_charges_within_cap(self):
        c = CostTracker(cap_usd=1.0)
        c.charge(0.4, reason="a")
        c.charge(0.4, reason="b")
        self.assertAlmostEqual(c.spent_usd, 0.8)
        self.assertAlmostEqual(c.remaining(), 0.2)

    def test_raises_over_cap(self):
        c = CostTracker(cap_usd=0.5)
        c.charge(0.4)
        with self.assertRaises(CostCapExceeded):
            c.charge(0.2)
        # spent should not have changed on the rejected charge
        self.assertAlmostEqual(c.spent_usd, 0.4)

    def test_negative_charge_rejected(self):
        c = CostTracker(cap_usd=1.0)
        with self.assertRaises(ValueError):
            c.charge(-0.1)


if __name__ == "__main__":
    unittest.main()
