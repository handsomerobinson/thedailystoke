from mind.memory import MemoryStore, stem, tokenize
from mind.util import InvalidName
from tests.helpers import TempDirCase


class MemoryTests(TempDirCase):
    def store(self, user="alice", clock=None):
        m = MemoryStore(self.tmp, user, **({"clock": clock} if clock else {}))
        self.addCleanup(m.close)
        return m

    def test_persistence_across_instances(self):
        m = self.store()
        m.add("fact", "Alice prefers metric units")
        m.close()
        m2 = self.store()
        self.assertEqual(m2.search("what units does alice prefer")[0].text, "Alice prefers metric units")

    def test_per_user_isolation(self):
        a, b = self.store("alice"), self.store("bob")
        a.add("fact", "secret project codename bluebird")
        self.assertEqual(b.search("codename bluebird"), [])
        self.assertEqual(b.count(), 0)
        self.assertNotEqual(a.path, b.path)

    def test_owner_column_defense_in_depth(self):
        a = self.store("alice")
        a.add("fact", "alice fact")
        # simulate a mis-wired path: bob's store opened on alice's file
        b = MemoryStore(self.tmp, "bob")
        b._db.close()
        import sqlite3
        b._db = sqlite3.connect(str(a.path), check_same_thread=False)
        b._db.row_factory = sqlite3.Row
        self.assertEqual(b.search("alice fact"), [])
        self.assertEqual(b.count(), 0)
        b.close()

    def test_rejects_traversal_user(self):
        with self.assertRaises(InvalidName):
            MemoryStore(self.tmp, "../alice")

    def test_dedupe(self):
        m = self.store()
        i1 = m.add("fact", "Likes tea.")
        i2 = m.add("fact", "likes   TEA")
        self.assertEqual(i1, i2)
        self.assertEqual(m.count(), 1)

    def test_retrieval_ranks_relevant_first_and_filters_noise(self):
        m = self.store()
        m.add("fact", "The user's dog is named Biscuit")
        m.add("fact", "The user works as a nurse on night shifts")
        m.add("fact", "Favourite cuisine is Ethiopian food")
        hits = m.search("what is my dog called")
        self.assertEqual(hits[0].text, "The user's dog is named Biscuit")
        self.assertEqual(m.search("quantum chromodynamics lattice"), [])

    def test_morphology_via_stemming_and_trigrams(self):
        m = self.store()
        m.add("fact", "prefers running in the mornings")
        self.assertTrue(m.search("preference: morning run"))
        self.assertEqual(stem("preferences"), "prefer")
        self.assertIn("run", tokenize("running"))

    def test_kinds_filter_and_recent(self):
        m = self.store()
        m.add("fact", "apples are tasty")
        m.add("note", "apples cost 2 dollars")
        self.assertEqual({h.kind for h in m.search("apples", kinds=["note"])}, {"note"})
        self.assertEqual(len(m.recent("fact")), 1)

    def test_reflection_utility_and_archiving(self):
        m = self.store()
        good = m.add("reflection", "lesson about widgets: check the widget count")
        bad = m.add("reflection", "lesson about widgets: always double the widgets")
        m.record_outcome([good], helped=True)
        for _ in range(3):
            m.record_outcome([bad], helped=False)
        hits = m.search("widgets lesson", kinds=["reflection"])
        self.assertEqual([h.id for h in hits], [good])  # bad one archived
        self.assertGreater(m.get(good).utility, 0.5)

    def test_recency_breaks_ties(self):
        t = [1_000_000.0]
        m = self.store(clock=lambda: t[0])
        old = m.add("fact", "meeting with Sam about budget")
        t[0] += 90 * 86400
        new = m.add("fact", "meeting with Sam about roadmap")
        hits = m.search("meeting with Sam")
        self.assertEqual(hits[0].id, new)
        self.assertIn(old, [h.id for h in hits])

    def test_bad_inputs(self):
        m = self.store()
        with self.assertRaises(ValueError):
            m.add("fact", "   ")
        with self.assertRaises(ValueError):
            m.add("gossip", "x")

    def test_extra_scorer_plugin_and_failure_tolerance(self):
        m = self.store()
        m.add("fact", "owns an automobile")
        self.assertEqual(m.search("car"), [])  # honest: no synonyms lexically
        syn = lambda q, it: 1.0 if "car" in q and "automobile" in it.text else 0.0  # noqa: E731
        self.assertEqual(len(m.search("car", extra_scorer=syn)), 1)
        boom = lambda q, it: 1 / 0  # noqa: E731
        self.assertEqual(m.search("automobile", extra_scorer=boom)[0].text, "owns an automobile")
