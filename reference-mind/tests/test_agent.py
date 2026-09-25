from mind.agent import Task
from mind.cost import Budget
from mind.evaluators import NumericAnswer, PythonFunctionTests
from mind.permissions import DenyAllApprover, PolicyApprover
from mind.providers import Brain, MockBrain, ResilientBrain
from mind.reflection import Reflector, task_shape
from mind.types import BrainResponse, ToolCall, Usage
from tests.helpers import TempDirCase

TEXT = "one  two\nthree   four five"  # 5 words; split(' ') says 8
APPROVE = PolicyApprover({"python_exec", "remember", "note_write", "send_report"})


class ReflexionLoopTests(TempDirCase):
    def test_fail_reflect_retry_succeed(self):
        rt = self.runtime()
        self.note("alice", "n", TEXT)
        res = rt.agent("alice", APPROVE).run_task(Task("Count the words in note 'n'", evaluator=NumericAnswer(5)))
        self.assertEqual(res.status, "success")
        self.assertEqual(len(res.trials), 2)
        self.assertFalse(res.trials[0].success)
        self.assertIn("AVOID strategy split_on_space", res.trials[0].reflection)
        self.assertEqual(len(res.trials[1].lessons_used), 1)
        refl = rt.memory("alice").search("count words", kinds=["reflection"])
        self.assertEqual(len(refl), 1)
        self.assertEqual(refl[0].helped, 1)  # credited because the retry succeeded

    def test_lesson_transfers_to_new_session_and_new_instance(self):
        rt = self.runtime()
        self.note("alice", "a", TEXT)
        self.note("alice", "b", "x  y z")
        rt.agent("alice", APPROVE).run_task(Task("Count the words in note 'a'", evaluator=NumericAnswer(5)))
        rt.close()
        rt2 = self.runtime()
        res = rt2.agent("alice", APPROVE).run_task(Task("Count the words in note b", evaluator=NumericAnswer(3)))
        self.assertEqual((res.status, len(res.trials)), ("success", 1))

    def test_deleting_the_lesson_removes_the_learning(self):
        """Proves the improvement lives in stored language, not hidden state."""
        rt = self.runtime()
        self.note("alice", "a", TEXT)
        rt.agent("alice", APPROVE).run_task(Task("Count the words in note 'a'", evaluator=NumericAnswer(5)))
        mem = rt.memory("alice")
        for item in mem.recent("reflection", 10):
            mem.delete(item.id)
        res = rt.agent("alice", APPROVE).run_task(Task("Count the words in note 'a'", evaluator=NumericAnswer(5), max_trials=1))
        self.assertEqual(res.status, "failed")

    def test_lessons_do_not_leak_across_users(self):
        rt = self.runtime()
        self.note("alice", "a", TEXT)
        self.note("bob", "a", TEXT)
        rt.agent("alice", APPROVE).run_task(Task("Count the words in note 'a'", evaluator=NumericAnswer(5)))
        res = rt.agent("bob", APPROVE).run_task(Task("Count the words in note 'a'", evaluator=NumericAnswer(5), max_trials=1))
        self.assertEqual(res.status, "failed")
        self.assertEqual(res.trials[0].lessons_used, [])

    def test_code_task_with_unit_tests(self):
        rt = self.runtime()
        ev = PythonFunctionTests("slugify", [(["Hello, World!"], "hello-world"), (["a  b"], "a-b")])
        res = rt.agent("alice", APPROVE).run_task(Task("Write a Python function slugify(s)", evaluator=ev))
        self.assertEqual(res.status, "success")
        self.assertEqual(len(res.trials), 2)

    def test_exhausts_trials_honestly(self):
        rt = self.runtime()
        self.note("alice", "n", TEXT)
        res = rt.agent("alice", APPROVE).run_task(Task("Count the words in note 'n'", evaluator=NumericAnswer(999), max_trials=3))
        self.assertEqual(res.status, "failed")
        self.assertEqual(len(res.trials), 3)

    def test_irrelevant_lessons_not_injected(self):
        rt = self.runtime()
        self.note("alice", "n", TEXT)
        rt.agent("alice", APPROVE).run_task(Task("Count the words in note 'n'", evaluator=NumericAnswer(5)))
        agent = rt.agent("alice", APPROVE)
        system, ids = agent.build_system(Task("Remember that I like tea"), [])
        self.assertEqual(ids, [])
        self.assertNotIn("Lessons", system)

    def test_task_shape(self):
        self.assertEqual(task_shape("Count the words in note 'a'"), task_shape("count the words in note b2"))
        self.assertEqual(task_shape("sum 3 and 4.5"), "sum <n> and <n>")


class LoopSafetyTests(TempDirCase):
    def test_budget_stops_runaway_and_keeps_partial(self):
        rt = self.runtime()
        res = rt.agent("alice", APPROVE).run_task(Task("stress test", budget=Budget(max_usd=0.017)))
        self.assertEqual(res.status, "budget_exceeded")
        self.assertLessEqual(res.cost["spent_usd"], 0.017)
        self.assertEqual(len(res.trials), 1)
        self.assertIn("stopped", res.trials[0].feedback)

    def test_step_cap(self):
        rt = self.runtime()
        res = rt.agent("alice", APPROVE).run_task(Task("stress test", budget=Budget(max_usd=10)))
        self.assertEqual(res.status, "failed")
        self.assertIn("no final answer", res.trials[0].feedback)

    def test_repeat_loop_detection(self):
        class Repeater(Brain):
            name, model = "rep", "mock"
            def complete(self, system, messages, tools, max_tokens=1024):
                return BrainResponse("", [ToolCall("clock", {})], Usage(10, 10), model="mock")
        rt = self.runtime(Repeater())
        res = rt.agent("alice", APPROVE).run_task(Task("x", budget=Budget(max_usd=10)))
        self.assertIn("stuck", res.trials[0].feedback)
        self.assertLessEqual(res.cost["tool_calls"], 2)

    def test_brain_outage_is_a_status_not_a_crash(self):
        rt = self.runtime(ResilientBrain([MockBrain(fail_times=99)], retries=0, sleep=lambda s: None))
        res = rt.agent("alice", APPROVE).run_task(Task("what is 1+1"))
        self.assertEqual(res.status, "brain_unavailable")
        self.assertEqual(res.answer, "")

    def test_internal_bug_is_reported(self):
        class Broken(Brain):
            name, model = "broken", "mock"
            def complete(self, *a, **k):
                return None  # violates the interface
        res = self.runtime(Broken()).agent("alice", APPROVE).run_task(Task("x"))
        self.assertEqual(res.status, "error")
        self.assertTrue(any("internal error" in n for n in res.notes))

    def test_memory_failure_degrades(self):
        rt = self.runtime()
        agent = rt.agent("alice", APPROVE)
        agent.memory.close()  # memory now unusable
        res = agent.run_task(Task("what is 2+3"))
        self.assertEqual(res.status, "answered")
        self.assertIn("5", res.answer)
        self.assertTrue(any("memory degraded" in n for n in res.notes))

    def test_permission_denied_is_reported_not_faked(self):
        rt = self.runtime()
        res = rt.agent("alice", DenyAllApprover()).run_task(Task("Save a note called x: hello"))
        self.assertIn("denied", res.answer)
        self.assertTrue(any("permission denied" in n for n in res.notes))
        self.assertFalse((self.settings.user_dir("alice") / "notes" / "x.md").exists())

    def test_audit_covers_task_lifecycle(self):
        rt = self.runtime()
        rt.agent("alice", APPROVE).run_task(Task("what is 2+3"))
        events = [e["event"] for e in rt.audit.entries()]
        for ev in ("task.start", "permission.request", "tool.result", "task.end"):
            self.assertIn(ev, events)
        self.assertTrue(rt.audit.verify()[0])

    def test_episode_memory_written(self):
        rt = self.runtime()
        rt.agent("alice", APPROVE).run_task(Task("what is 2+3"))
        self.assertEqual(rt.memory("alice").count("episode"), 1)


class ReflectorTests(TempDirCase):
    def test_reflect_charges_budget_and_stores(self):
        rt = self.runtime()
        r = Reflector(rt.brain, rt.memory("alice"))
        b = Budget()
        text, mid = r.reflect("Count the words in note x", "CALL python_exec: # strategy: split_on_space", "too high", 1, b)
        self.assertEqual(b.brain_calls, 1)
        self.assertIn("AVOID", text)
        self.assertEqual(rt.memory("alice").get(mid).meta["shape"], task_shape("Count the words in note x"))
