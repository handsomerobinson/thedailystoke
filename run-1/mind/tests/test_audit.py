import json
import threading

from mind.audit import AuditLog
from tests.helpers import TempDirCase


class AuditTests(TempDirCase):
    def test_chain_verifies_and_detects_edit(self):
        log = AuditLog(self.tmp / "a.jsonl", self.clock)
        for i in range(5):
            log.write("tool.decision", user="u", n=i)
        ok, msg = log.verify()
        self.assertTrue(ok, msg)
        lines = (self.tmp / "a.jsonl").read_text().splitlines()
        rec = json.loads(lines[2])
        rec["n"] = 99
        lines[2] = json.dumps(rec)
        (self.tmp / "a.jsonl").write_text("\n".join(lines) + "\n")
        ok, msg = log.verify()
        self.assertFalse(ok)
        self.assertIn("line 3", msg)

    def test_deleted_line_breaks_chain(self):
        log = AuditLog(self.tmp / "a.jsonl", self.clock)
        for i in range(4):
            log.write("e", n=i)
        lines = (self.tmp / "a.jsonl").read_text().splitlines()
        del lines[1]
        (self.tmp / "a.jsonl").write_text("\n".join(lines) + "\n")
        self.assertFalse(log.verify()[0])

    def test_secrets_redacted_and_reserved_fields_protected(self):
        log = AuditLog(self.tmp / "a.jsonl", self.clock)
        rec = log.write("e", args={"code": "key=sk-ant-abcdefghijk12345"}, seq=999, prev="x")
        self.assertNotIn("abcdefghijk12345", json.dumps(rec))
        self.assertEqual(rec["seq"], 1)
        self.assertTrue(log.verify()[0])

    def test_concurrent_writers_keep_chain_valid(self):
        log = AuditLog(self.tmp / "a.jsonl", self.clock)
        log2 = AuditLog(self.tmp / "a.jsonl", self.clock)  # second handle ~ second process

        def w(lg):
            for i in range(25):
                lg.write("e", n=i)
        ts = [threading.Thread(target=w, args=(lg,)) for lg in (log, log2, log, log2)]
        for t in ts:
            t.start()
        for t in ts:
            t.join()
        ok, msg = log.verify()
        self.assertTrue(ok, msg)
        self.assertEqual(len(log.records()), 100)

    def test_records_filter_by_user(self):
        log = AuditLog(self.tmp / "a.jsonl", self.clock)
        log.write("e", user="a")
        log.write("e", user="b")
        self.assertEqual(len(log.records(user="a")), 1)
