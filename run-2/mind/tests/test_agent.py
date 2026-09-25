import shutil
import tempfile
import unittest
from pathlib import Path

from mind.agent import Agent
from mind.audit import AuditLog
from mind.memory import MemoryStore
from mind.permissions import PermissionTier, auto_approver
from mind.providers.base import LLMProvider, LLMResponse
from mind.providers.mock import MockProvider
from mind.tools import default_toolset
from mind.tools.base import Tool, ToolResult


class FailThenSucceedProvider(LLMProvider):
    """A tiny scripted provider for testing the reflection loop without
    depending on MockProvider's own heuristics."""

    name = "scripted"

    def __init__(self, cost_per_call: float = 0.0):
        self.calls = 0
        self.cost_per_call = cost_per_call

    def complete(self, system, messages, max_tokens=512):
        self.calls += 1
        last = messages[-1]["content"]
        if "AVAILABLE TOOLS" in last:
            if "LESSONS FROM PAST ATTEMPTS" in last:
                return LLMResponse(text='TOOL: code_exec\nARGS: {"code": "print(2)"}', cost_usd=self.cost_per_call)
            return LLMResponse(text='TOOL: code_exec\nARGS: {"code": "raise ValueError(1)"}', cost_usd=self.cost_per_call)
        if "previous attempt failed" in last.lower():
            return LLMResponse(text="Reflection: avoid raising ValueError next time.", cost_usd=self.cost_per_call)
        return LLMResponse(text="ack", cost_usd=self.cost_per_call)


class AlwaysDenyingApproverAgentTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.memory_store = MemoryStore(base_dir=self.tmp / "memory")
        self.audit = AuditLog(path=self.tmp / "audit.jsonl")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_permission_denied_stops_task(self):
        provider = FailThenSucceedProvider()
        tools = default_toolset()
        deny_all = auto_approver(state_changing_ok=False, irreversible_ok=False)
        agent = Agent(provider=provider, tools=tools, memory_store=self.memory_store, audit_log=self.audit, approver=deny_all)
        result = agent.run_task("alice", "run some code")
        self.assertFalse(result.ok)
        self.assertEqual(result.stopped_reason, "permission_denied")


class ReflectionLoopTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.memory_store = MemoryStore(base_dir=self.tmp / "memory")
        self.audit = AuditLog(path=self.tmp / "audit.jsonl")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_fails_then_learns_then_succeeds(self):
        provider = FailThenSucceedProvider()
        tools = default_toolset()
        approver = auto_approver(state_changing_ok=True)
        agent = Agent(provider=provider, tools=tools, memory_store=self.memory_store, audit_log=self.audit, approver=approver, max_retries=3)

        result = agent.run_task("alice", "please run some code that raises")
        self.assertTrue(result.ok, result.attempts)
        self.assertEqual(len(result.attempts), 2)
        self.assertFalse(result.attempts[0].result.ok)
        self.assertIsNotNone(result.attempts[0].reflection)
        self.assertTrue(result.attempts[1].result.ok)

        # the lesson should now be recallable from memory
        mem = self.memory_store.for_user("alice")
        lessons = mem.lessons_for("please run some code that raises")
        self.assertTrue(lessons)

    def test_gives_up_after_max_retries(self):
        class AlwaysFailProvider(LLMProvider):
            name = "always_fail"

            def complete(self, system, messages, max_tokens=512):
                last = messages[-1]["content"]
                if "previous attempt failed" in last.lower():
                    return LLMResponse(text="Reflection: still broken.")
                return LLMResponse(text='TOOL: code_exec\nARGS: {"code": "raise ValueError(1)"}')

        tools = default_toolset()
        agent = Agent(provider=AlwaysFailProvider(), tools=tools, memory_store=self.memory_store, audit_log=self.audit, approver=auto_approver(), max_retries=2)
        result = agent.run_task("bob", "always fails")
        self.assertFalse(result.ok)
        self.assertEqual(result.stopped_reason, "max_retries_exhausted")
        self.assertEqual(len(result.attempts), 2)


class CostCapTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.memory_store = MemoryStore(base_dir=self.tmp / "memory")
        self.audit = AuditLog(path=self.tmp / "audit.jsonl")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_cost_cap_stops_runaway_loop(self):
        provider = FailThenSucceedProvider(cost_per_call=0.10)
        tools = default_toolset()
        agent = Agent(
            provider=provider,
            tools=tools,
            memory_store=self.memory_store,
            audit_log=self.audit,
            approver=auto_approver(),
            max_retries=10,
            task_cost_cap_usd=0.15,  # enough for one plan call, not much more
        )
        result = agent.run_task("carol", "run some code")
        self.assertFalse(result.ok)
        self.assertEqual(result.stopped_reason, "cost_cap_exceeded")
        self.assertLessEqual(result.cost_usd, 0.15 + 1e-9)


class MockProviderIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.memory_store = MemoryStore(base_dir=self.tmp / "memory")
        self.audit = AuditLog(path=self.tmp / "audit.jsonl")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_full_demo_style_flow(self):
        provider = MockProvider()
        tools = default_toolset()
        agent = Agent(provider=provider, tools=tools, memory_store=self.memory_store, audit_log=self.audit, approver=auto_approver())
        result = agent.run_task("demo-user", "please divide 10 by zero for me")
        self.assertTrue(result.ok)
        self.assertGreaterEqual(len(result.attempts), 2)


if __name__ == "__main__":
    unittest.main()
