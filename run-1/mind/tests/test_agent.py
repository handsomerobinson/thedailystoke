from mind.agent import Agent
from mind.audit import AuditLog
from mind.cost import Budget
from mind.memory import MemoryStore
from mind.permissions import DenyAll, PermissionGate, ScriptedApprover
from mind.prompts import FACTS_HEADER, LESSONS_HEADER
from mind.providers import LLMResponse, MockBrain, Provider, ProviderError, ToolCall
from mind.tools import ToolRegistry, default_tools
from tests.helpers import TempDirCase


class Scripted(Provider):
    """Replays a fixed list of responses; records the system prompts it saw."""
    name = "scripted"
    model = "scripted"

    def __init__(self, responses):
        self.responses = list(responses)
        self.systems = []

    def price(self):
        return (0.0, 0.0)

    def complete(self, system, messages, tools, max_tokens=1024):
        self.systems.append(system)
        r = self.responses.pop(0) if self.responses else LLMResponse("done")
        if isinstance(r, Exception):
            raise r
        return r


class AgentTests(TempDirCase):
    def setUp(self):
        super().setUp()
        self.mem = MemoryStore(self.tmp, "alice", self.clock)
        self.audit = AuditLog(self.tmp / "audit.jsonl", self.clock)

    def agent(self, provider, approver=None, **cfg):
        c = self.config(**cfg)
        reg = ToolRegistry(default_tools(), self.audit, PermissionGate(approver or DenyAll(), memory=self.mem))
        return Agent(provider, reg, self.mem, c, self.clock)

    def test_tool_loop_answers(self):
        t = self.agent(MockBrain()).run_trial("calculate 6*7", Budget(1))
        self.assertEqual(t.status, "answered")
        self.assertIn("42", t.answer)
        self.assertEqual(t.tool_calls, 1)

    def test_memory_injected_into_system_prompt(self):
        self.mem.set_fact("name", "Ada")
        self.mem.add_item("lesson", "When asked about palindromes normalize case first")
        p = Scripted([LLMResponse("ok")])
        self.agent(p).run_trial("palindromes question", Budget(1))
        self.assertIn(FACTS_HEADER, p.systems[0])
        self.assertIn("- name: Ada", p.systems[0])
        self.assertIn(LESSONS_HEADER, p.systems[0])

    def test_memory_context_is_bounded(self):
        for i in range(200):
            self.mem.add_item("lesson", f"palindrome lesson number {i} " + "x" * 300)
        p = Scripted([LLMResponse("ok")])
        self.agent(p, memory_context_chars=1000).run_trial("palindrome", Budget(1))
        self.assertLess(len(p.systems[0]), 3000)

    def test_step_limit(self):
        t = self.agent(MockBrain(), max_steps=3).run_trial("keep going forever until you find it", Budget(1))
        self.assertEqual(t.status, "step_limit")

    def test_loop_detection(self):
        same = LLMResponse("", [ToolCall("a", "calculator", {"expression": "1+1"})])
        t = self.agent(Scripted([same] * 10)).run_trial("x", Budget(1))
        self.assertEqual(t.status, "loop_detected")
        self.assertIn("already made this exact call", t.messages[4]["content"])

    def test_budget_exceeded_before_spending(self):
        t = self.agent(MockBrain(price=(100, 100))).run_trial("calculate 1+1", Budget(0.001))
        self.assertEqual(t.status, "budget_exceeded")

    def test_provider_error_is_graceful(self):
        t = self.agent(Scripted([ProviderError("down")])).run_trial("x", Budget(1))
        self.assertEqual(t.status, "provider_error")

    def test_unexpected_exception_is_contained(self):
        t = self.agent(Scripted([ZeroDivisionError("bug")])).run_trial("x", Budget(1))
        self.assertEqual(t.status, "error")

    def test_denied_tool_gets_honest_answer(self):
        t = self.agent(MockBrain()).run_trial("save a note titled a: b", Budget(1))
        self.assertEqual(t.status, "answered")
        self.assertEqual(t.denied, 1)
        self.assertIn("couldn't", t.answer)

    def test_malformed_tool_arguments_do_not_crash(self):
        bad = LLMResponse("", [ToolCall("a", "calculator", {"_invalid_json": "{"})])
        t = self.agent(Scripted([bad, LLMResponse("recovered")])).run_trial("x", Budget(1))
        self.assertEqual(t.answer, "recovered")
        self.assertIn("invalid arguments", t.messages[2]["content"])

    def test_approved_write(self):
        t = self.agent(MockBrain(), ScriptedApprover({"remember_fact": True})).run_trial(
            "remember that my city is Oslo", Budget(1))
        self.assertEqual(self.mem.get_fact("city"), "Oslo")
        self.assertEqual(t.status, "answered")
