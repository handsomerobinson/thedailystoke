from mind.memory import MemoryIsolationError, MemoryStore, user_db_path
from tests.helpers import TempDirCase


class MemoryTests(TempDirCase):
    def mem(self, user="alice", **kw):
        return MemoryStore(self.tmp, user, self.clock, **kw)

    def test_facts_persist_across_reopen(self):
        m = self.mem()
        m.set_fact("Name", "Alice")
        m.close()
        self.assertEqual(self.mem().get_fact("name"), "Alice")

    def test_per_user_files_and_isolation(self):
        a, b = self.mem("alice"), self.mem("bob")
        a.set_fact("secret", "a-only")
        a.add_item("lesson", "alice lesson about palindromes")
        self.assertIsNone(b.get_fact("secret"))
        self.assertEqual(b.search("palindromes"), [])
        self.assertNotEqual(user_db_path(self.tmp, "alice"), user_db_path(self.tmp, "bob"))

    def test_owner_mismatch_is_refused(self):
        a = self.mem("alice")
        a.set_fact("x", "1")
        a.close()  # checkpoint WAL so the copied file contains the owner row
        # simulate a mis-routed file: copy alice's db to where bob's should be
        import shutil
        shutil.copy(user_db_path(self.tmp, "alice"), user_db_path(self.tmp, "bob"))
        with self.assertRaises(MemoryIsolationError):
            self.mem("bob")

    def _ranking(self, **kw):
        m = self.mem(**kw)
        m.add_item("reflection", "Sorting numbers: remember to handle empty lists", "", "s1")
        good = m.add_item("reflection", "Palindromes must ignore case and punctuation; normalize first", "", "s2")
        m.add_item("episode", "Asked about the weather in Paris")
        hits = m.search("check if a string is a palindrome ignoring punctuation")
        self.assertTrue(hits)
        self.assertEqual(hits[0].id, good)
        return m

    def test_search_ranks_relevant_first_fts(self):
        m = self._ranking()
        self.assertTrue(m.use_fts)

    def test_search_python_bm25_fallback(self):
        m = self._ranking(use_fts=False)
        self.assertFalse(m.use_fts)

    def test_stemming_recall(self):
        m = self.mem()
        i = m.add_item("lesson", "splitting words needs whitespace normalization")
        self.assertEqual(m.search("split word")[0].id, i)

    def test_kind_filter_and_sig_boost(self):
        m = self.mem()
        a = m.add_item("reflection", "generic advice about strings", "", "sigA")
        m.add_item("episode", "generic advice about strings too", "", "sigB")
        hits = m.search("strings", kinds=["reflection"], task_sig="sigA")
        self.assertEqual([h.id for h in hits], [a])

    def test_feedback_changes_ranking_and_harmful_items_are_forgotten(self):
        m = self.mem()
        a = m.add_item("reflection", "approach one for parsing dates")
        b = m.add_item("reflection", "approach two for parsing dates")
        for _ in range(3):
            m.feedback(a, helpful=False)
        ids = [h.id for h in m.search("parsing dates")]
        self.assertEqual(ids, [b])
        m.feedback(b, helpful=True)
        self.assertEqual(m.search("parsing dates")[0].helpful, 1)

    def test_recency_prefers_newer_on_tie(self):
        m = self.mem()
        old = m.add_item("lesson", "use utc timestamps")
        self.clock.advance(200 * 86400)
        new = m.add_item("lesson", "use utc timestamps")
        self.assertEqual(m.search("utc timestamps")[0].id, new)
        self.assertNotEqual(old, new)

    def test_notes_versioned_restorable_and_purgeable(self):
        m = self.mem()
        self.assertEqual(m.write_note("t", "v1"), 1)
        self.assertEqual(m.write_note("t", "v2"), 2)
        self.assertEqual(m.note_history("t")[0]["body"], "v1")
        self.assertTrue(m.restore_note("t", 1))
        self.assertEqual(m.read_note("t")["body"], "v1")
        self.assertTrue(m.purge_note("t"))
        self.assertIsNone(m.read_note("t"))
        self.assertEqual(m.note_history("t"), [])

    def test_approvals_are_one_shot(self):
        m = self.mem()
        aid = m.add_approval("send_message", {"to": "x"}, "d1", "why")
        self.assertEqual(m.add_approval("send_message", {"to": "x"}, "d1", "why"), aid)  # deduped
        self.assertFalse(m.consume_approval("d1"))  # still pending
        m.resolve_approval(aid, True)
        self.assertTrue(m.consume_approval("d1"))
        self.assertFalse(m.consume_approval("d1"))

    def test_spend_ledger_and_inbox(self):
        m = self.mem()
        m.add_spend("2026-01-01", 0.1)
        m.add_spend("2026-01-01", 0.2)
        self.assertAlmostEqual(m.spent_on("2026-01-01"), 0.3)
        m.add_report("job:1", "t", "b")
        self.assertEqual(len(m.inbox(unread_only=True)), 1)
        m.mark_read()
        self.assertEqual(m.inbox(unread_only=True), [])

    def test_in_memory_degraded_mode(self):
        m = MemoryStore(None, "alice", self.clock, in_memory=True)
        m.set_fact("a", "b")
        self.assertTrue(m.stats()["degraded"])

    def test_search_handles_fts_special_characters(self):
        m = self.mem()
        m.add_item("lesson", 'quote " and * and NEAR( and -minus')
        m.search('"unbalanced * NEAR( OR AND -')


class Round1MemoryTests(TempDirCase):
    def test_kind_filter_is_applied_before_limit(self):
        m = MemoryStore(self.tmp, "alice", self.clock)
        for i in range(150):
            m.add_item("episode", f"widget episode {i} widget widget")
        lesson = m.add_item("lesson", "widget lesson")
        hits = m.search("widget", kinds=["lesson"])
        self.assertEqual([h.id for h in hits], [lesson])


class CompactTests(TempDirCase):
    def test_compact_removes_harmful_and_oldest_but_keeps_lessons(self):
        m = MemoryStore(self.tmp, "alice", self.clock)
        bad = m.add_item("reflection", "misleading advice")
        m.feedback(bad, False)
        m.feedback(bad, False)
        lessons = [m.add_item("lesson", f"lesson {i}") for i in range(3)]
        for i in range(20):
            m.add_item("episode", f"episode {i}")
        removed = m.compact(max_items=10)
        self.assertGreaterEqual(removed, 1)
        self.assertIsNone(m.get_item(bad))
        self.assertTrue(all(m.get_item(i) for i in lessons))
        self.assertLessEqual(len(m.items(limit=1000)), 10)
        self.assertEqual(m.search("misleading"), [])
