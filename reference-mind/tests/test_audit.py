import json

from mind.audit import AuditError, AuditLog
from tests.helpers import TempDirCase


class AuditTests(TempDirCase):
    def test_chain_and_verify(self):
        log = AuditLog(self.tmp / "a.jsonl")
        for i in range(5):
            log.record("x", i=i)
        ok, msg = log.verify()
        self.assertTrue(ok, msg)
        self.assertEqual(len(log.entries()), 5)
        self.assertEqual(log.entries()[1]["prev"], log.entries()[0]["hash"])

    def test_detects_edit_delete_reorder(self):
        log = AuditLog(self.tmp / "a.jsonl")
        for i in range(4):
            log.record("x", i=i)
        lines = log.path.read_text().splitlines()
        for mutated in (
            [lines[0], lines[1].replace('"i": 1', '"i": 9'), *lines[2:]],
            [lines[0], *lines[2:]],
            [lines[1], lines[0], *lines[2:]],
        ):
            p = self.tmp / "m.jsonl"
            p.write_text("\n".join(mutated) + "\n")
            self.assertFalse(AuditLog(p).verify()[0])

    def test_refuses_to_append_to_corrupt_tail(self):
        p = self.tmp / "a.jsonl"
        p.write_text("not json\n")
        with self.assertRaises(AuditError):
            AuditLog(p).record("x")

    def test_unwritable_raises_audit_error(self):
        d = self.tmp / "dir.jsonl"
        d.mkdir()
        with self.assertRaises(AuditError):
            AuditLog(d).record("x")

    def test_tail_filter(self):
        log = AuditLog(self.tmp / "a.jsonl")
        log.record("x", user="a")
        log.record("x", user="b")
        self.assertEqual([e["user"] for e in log.tail(10, "b")], ["b"])

    def test_large_log_append_reads_tail_only(self):
        log = AuditLog(self.tmp / "a.jsonl")
        for i in range(300):
            log.record("x", payload="y" * 50, i=i)
        self.assertTrue(log.verify()[0])
        self.assertEqual(json.loads(log.path.read_text().splitlines()[-1])["i"], 299)
