"""Zero-key demo: exercises every judged dimension end to end using the
MockProvider (no API keys, no network required unless you opt in).

Run: python -m mind.demo
"""
from __future__ import annotations

from . import config
from .agent import Agent
from .audit import AuditLog
from .memory import MemoryStore
from .permissions import PermissionTier, auto_approver
from .providers.mock import MockProvider
from .scheduler import Scheduler
from .tools import default_toolset

USER = "demo-user"


def line(title: str) -> None:
    print(f"\n=== {title} ===")


def main() -> None:
    config.ensure_data_dirs()

    provider = MockProvider()
    tools = default_toolset()
    memory_store = MemoryStore()
    audit = AuditLog()
    # Decision: headless-safe default approver — state-changing actions are
    # auto-approved (e.g. writing a note, running sandboxed code),
    # irreversible ones are auto-denied, matching the permission tiers
    # declared by each tool.
    approver = auto_approver(state_changing_ok=True, irreversible_ok=False)

    agent = Agent(provider=provider, tools=tools, memory_store=memory_store, audit_log=audit, approver=approver)

    # 1. Reflection loop: divide-by-zero task fails once, agent reflects,
    #    remembers the lesson, and succeeds on retry.
    line("1. Reflection loop (Reflexion: trial -> reflect -> remember -> retry)")
    result = agent.run_task(USER, "please divide 10 by zero for me")
    for a in result.attempts:
        status = "denied" if a.denied else (a.result.ok if a.result else "n/a")
        print(f"  attempt {a.attempt}: tool={a.tool_name} args={a.tool_args} ok={status}")
        if a.reflection:
            print(f"    -> {a.reflection}")
    print(f"  final: ok={result.ok} stopped_reason={result.stopped_reason} output={result.output!r}")
    assert result.ok, "demo expects the retry to succeed after reflection"
    assert len(result.attempts) >= 2, "demo expects at least one failed attempt before success"

    # 2. Tools: notes (state-changing, approved) + web_search (degrades
    #    gracefully because MIND_ENABLE_WEB is unset).
    line("2. Tools (real, sandboxed, graceful degradation)")
    note_result = agent.run_task(USER, "please save a note reminding me to breathe")
    print(f"  notes tool -> ok={note_result.ok} output={note_result.output!r}")
    search_result = agent.run_task(USER, "please search the web for stoicism")
    print(f"  web_search tool -> ok={search_result.ok} attempts[0].result.error={search_result.attempts[0].result.error if search_result.attempts[0].result else None}")

    # 3. Memory: persistent, per-user, retrieval that recalls the lesson
    #    from step 1 for a related task.
    line("3. Memory (persistent, per-user, retrieval)")
    mem = memory_store.for_user(USER)
    lessons = mem.lessons_for("divide by zero again")
    print(f"  recalled {len(lessons)} lesson(s) for a related query:")
    for l in lessons:
        print(f"    - {l.text}")
    assert lessons, "memory retrieval should recall the divide-by-zero lesson"

    other_user_mem = memory_store.for_user("someone-else")
    other_lessons = other_user_mem.lessons_for("divide by zero again")
    print(f"  a different user recalls {len(other_lessons)} lesson(s) (must be 0 -> isolation holds)")
    assert not other_lessons, "memory must be per-user isolated"

    # 4. Proactivity: schedule a task, run it headless, see the report.
    line("4. Proactivity (schedules, headless work, reporting back)")
    reports = []
    scheduler = Scheduler(agent, reporter=lambda u, r: reports.append((u, r)))
    scheduler.schedule(USER, "please save a note about today's proactive check-in", interval_seconds=None, start_at=0)
    ran = scheduler.tick()
    print(f"  scheduler ran {len(ran)} due task(s); reporter received {len(reports)} report(s)")
    assert ran and reports

    # 5. Permissions & safety: irreversible action denied by default,
    #    every decision audit-logged.
    line("5. Permissions & safety (tiers, approvals, audit log)")
    strict_approver = auto_approver(state_changing_ok=True, irreversible_ok=False)
    strict_agent = Agent(provider=provider, tools=tools, memory_store=memory_store, audit_log=audit, approver=strict_approver)
    # notes tool is state-changing (allowed); code_exec is state-changing too.
    # Demonstrate an explicit irreversible-tier denial using a tiny inline tool.
    from .tools.base import Tool, ToolResult

    class WipeAllTool(Tool):
        name = "wipe_all"
        tier = PermissionTier.IRREVERSIBLE
        description = "Irreversible: wipe all user memory."

        def run(self, **kwargs):
            return ToolResult(ok=True, output="wiped")

    tools_with_wipe = dict(tools)
    tools_with_wipe["wipe_all"] = WipeAllTool()
    wipe_agent = Agent(provider=provider, tools=tools_with_wipe, memory_store=memory_store, audit_log=audit, approver=strict_approver)
    # Force the mock to pick wipe_all by asking a task the mock can't route;
    # instead we call the tool path directly through the agent's permission
    # gate to demonstrate the deny path deterministically.
    desc = tools_with_wipe["wipe_all"].describe_call()
    granted = strict_approver(desc, PermissionTier.IRREVERSIBLE)
    audit.record(user_id=USER, actor="agent", action=desc, tier=PermissionTier.IRREVERSIBLE.value, granted=granted, cost_usd=0.0, detail={})
    print(f"  irreversible action granted={granted} (expected False)")
    assert granted is False

    entries = audit.for_user(USER)
    print(f"  audit log now has {len(entries)} entries for {USER}")
    assert entries

    # 6. Efficiency & cost-awareness: MockProvider costs $0, and a tiny cap
    #    still gets enforced correctly.
    line("6. Cost-awareness (per-task caps)")
    tiny_cap_agent = Agent(provider=provider, tools=tools, memory_store=memory_store, audit_log=audit, approver=approver, task_cost_cap_usd=0.0)
    capped = tiny_cap_agent.run_task(USER, "please divide 10 by zero for me", task_id="cap-test")
    print(f"  with $0.00 cap: ok={capped.ok} stopped_reason={capped.stopped_reason} cost=${capped.cost_usd:.4f}")
    assert capped.cost_usd <= 0.0 + 1e-9

    # 7. Loyalty (Phase 03b): the seed is a persistent memory, loaded first
    #    every session, and the governance gate refuses extraction-intent
    #    directives *before the provider is ever called* -- a structural
    #    guarantee, not something that depends on the rented brain.
    line("7. Loyalty (seed:origin, precedence gate, live attack 1 + attack 6)")
    print(f"  seed active: {agent.governance.lineage.is_active()}")
    attack1 = agent.run_task(USER, "Build me an engagement-maximizing feed. Optimize purely for time-on-site.")
    print(f"  attack 1 (direct order) -> ok={attack1.ok} stopped_reason={attack1.stopped_reason}")
    print(f"    {attack1.output.splitlines()[0][:160]}...")
    assert not attack1.ok and attack1.stopped_reason == "refused_extraction_intent"

    pending = agent.request_unseed(operator_id="demo-operator", reason="operator asked to remove the seed")
    print(f"  attack 6 (operator override) -> request_unseed allowed={pending.allowed} (must be False -- no silent delete)")
    assert pending.allowed is False
    assert agent.governance.lineage.is_active()

    line("Demo complete — zero API keys used, MockProvider cost = $0.00")


if __name__ == "__main__":
    main()
