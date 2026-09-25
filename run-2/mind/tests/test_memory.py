import shutil
import tempfile
import unittest
from pathlib import Path

from mind.memory import MemoryStore, UserMemory


class TestUserMemory(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_remember_and_recall(self):
        mem = UserMemory("alice", base_dir=self.tmp)
        mem.remember_lesson("t1", "Reflection: divided by zero, guard the denominator next time.")
        mem.remember_lesson("t2", "Reflection: forgot to sanitize the filename before writing a note.")

        recalled = mem.lessons_for("please divide something by zero again")
        self.assertEqual(len(recalled), 1)
        self.assertIn("denominator", recalled[0].text)

    def test_recall_no_match_returns_empty(self):
        mem = UserMemory("bob", base_dir=self.tmp)
        mem.remember_lesson("t1", "Reflection: divided by zero, guard the denominator.")
        self.assertEqual(mem.lessons_for("completely unrelated topic xyz"), [])

    def test_isolation_between_files(self):
        mem_a = UserMemory("alice", base_dir=self.tmp)
        mem_b = UserMemory("bob", base_dir=self.tmp)
        self.assertNotEqual(mem_a.db_path, mem_b.db_path)
        mem_a.remember_lesson("t1", "shared keyword lesson")
        self.assertEqual(mem_b.lessons_for("shared keyword lesson"), [])

    def test_unsafe_user_id_is_sanitized(self):
        mem = UserMemory("../../etc/passwd", base_dir=self.tmp)
        self.assertTrue(str(mem.db_path.resolve()).startswith(str(self.tmp.resolve())))

    def test_empty_user_id_rejected(self):
        with self.assertRaises(ValueError):
            UserMemory("", base_dir=self.tmp)

    def test_persists_across_instances(self):
        mem1 = UserMemory("carol", base_dir=self.tmp)
        mem1.remember_episode("t1", "did a thing")
        mem1.close()
        mem2 = UserMemory("carol", base_dir=self.tmp)
        items = mem2.all()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].text, "did a thing")

    def test_wipe_clears_all(self):
        mem = UserMemory("dave", base_dir=self.tmp)
        mem.remember_episode("t1", "x")
        mem.remember_lesson("t1", "y")
        self.assertEqual(len(mem.all()), 2)
        mem.wipe()
        self.assertEqual(len(mem.all()), 0)


class TestMemoryStore(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_caches_per_user(self):
        store = MemoryStore(base_dir=self.tmp)
        m1 = store.for_user("alice")
        m2 = store.for_user("alice")
        self.assertIs(m1, m2)
        m3 = store.for_user("bob")
        self.assertIsNot(m1, m3)


if __name__ == "__main__":
    unittest.main()
