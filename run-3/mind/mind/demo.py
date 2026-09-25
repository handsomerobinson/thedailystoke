"""Zero-key, end-to-end demonstration.  `python -m mind demo`  (or `python demo.py`).

Everything here runs on the scripted MockBrain -- no network, no API keys.
Read mind/providers/mock.py for exactly what the mock does and does not do.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

from .agent import Task
from .config import PROJECT_ROOT, Settings
from .cost import Budget
from .evaluators import NumericAnswer, PythonFunctionTests
from .permissions import DenyAllApprover, PolicyApprover
from .providers import MockBrain, ResilientBrain
from .providers.base import ProviderError
from .runtime import Runtime
from .scheduler import Scheduler
from .tools.base import ToolContext
from .types import ToolCall

DRAFT = "The quick  brown fox\njumps over the lazy dog.\n\nIt was  a  sunny   day."          # 14 words
MEMO = "Meeting moved to  Thursday.\nBring the\tbudget  sheet and\n\nthe  roadmap."          # 11 words
LEDGER = "rent -1200\nsalary 3500.50\ngroceries -245.25\nrefund 19.75"                        # 2075.0
BOB_NOTE = "Bob's  list:\n eggs  milk\nbread"                                                  # 5 words

PALINDROME_CASES = [(["racecar"], True), (["hello"], False), (["A man, a plan, a canal: Panama"], True),
                    (["No lemon, no melon"], True), ([""], True)]


def hr(title: str) -> None:
    print("\n" + "=" * 78 + f"\n{title}\n" + "=" * 78)


def show(res) -> None:
    print(f"  => status={res.status}  trials={len(res.trials)}  answer={res.answer!r}")
    print(f"     cost ${res.cost['spent_usd']:.4f} (cap ${res.cost['max_usd']}), tokens={res.cost['tokens']}, "
          f"tool calls={res.cost['tool_calls']}")
    for n in res.notes:
        print(f"     note: {n.splitlines()[0]}")


def seed_note(rt: Runtime, user: str, name: str, text: str) -> None:
    d = rt.settings.user_dir(user) / "notes"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{name}.md").write_text(text, encoding="utf-8")


def main(keep: bool = False, data_dir: str | None = None) -> int:
    root = Path(data_dir) if data_dir else PROJECT_ROOT / "data" / "demo"
    if root.exists() and not keep:
        shutil.rmtree(root)
    settings = Settings(data_dir=root, allow_fast_intervals=True)
    rt = Runtime(settings, ResilientBrain([MockBrain()]), "mock:mock-1 (scripted, zero-key)")
    log = lambda s: print(s)  # noqa: E731
    approver = PolicyApprover(write_grants={"python_exec", "remember", "note_write"}, log=log)
    checks: list[tuple[str, bool]] = []

    hr("0. Setup - brain, tools, graceful degradation")
    print(f"brain: {rt.brain_desc}   data: {root}")
    ctx = ToolContext(user_id="alice", settings=settings, memory=rt.memory("alice"), scheduler=Scheduler(rt))
    for name, st in rt.registry(approver).status(ctx).items():
        print(f"  {name:13s} {st}")
    for user, name, text in (("alice", "draft", DRAFT), ("alice", "ledger", LEDGER), ("alice", "memo", MEMO),
                             ("bob", "groceries", BOB_NOTE)):
        seed_note(rt, user, name, text)

    hr("1. Reflection loop - word count (trial -> evaluate -> reflect -> remember -> retry)")
    alice = rt.agent("alice", approver, log=log)
    r1 = alice.run_task(Task("Count the words in note 'draft'", evaluator=NumericAnswer(14)))
    show(r1)
    checks.append(("word count: failed once, learned, then succeeded", r1.status == "success" and len(r1.trials) == 2))

    hr("2. Reflection loop - sum of numbers (different bug, different lesson)")
    r2 = alice.run_task(Task("Sum the numbers in note 'ledger'", evaluator=NumericAnswer(2075.0)))
    show(r2)
    checks.append(("number sum: learned from failure", r2.status == "success" and len(r2.trials) == 2))

    hr("3. Reflection loop - code, graded by unit tests in the sandbox")
    r3 = alice.run_task(Task("Write a Python function is_palindrome(s) that ignores case and punctuation",
                             evaluator=PythonFunctionTests("is_palindrome", PALINDROME_CASES)))
    show(r3)
    checks.append(("code: failing tests -> lesson -> passing tests", r3.status == "success" and len(r3.trials) == 2))
    rt.close()

    hr("4. New process, new note: does the lesson persist across sessions?")
    cmd = [sys.executable, "-m", "mind", "--data-dir", str(root), "--provider", "mock", "run", "--user", "alice",
           "--approve", "python_exec", "--expect", "11", "Count the words in note 'memo'"]
    print("$ " + " ".join(cmd[1:3]) + " ... run --user alice --expect 11 \"Count the words in note 'memo'\"")
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(PROJECT_ROOT), timeout=120)
    print("\n".join("  | " + ln for ln in proc.stdout.strip().splitlines()))
    checks.append(("separate process: first-try success using stored lesson",
                   proc.returncode == 0 and "trials: 1" in proc.stdout and "lesson" in proc.stdout))

    rt = Runtime(settings, ResilientBrain([MockBrain()]), "mock")
    print("\nCounterfactual - bob has no lessons (memory is per-user), same kind of task:")
    bob = rt.agent("bob", PolicyApprover(write_grants={"python_exec"}), log=log)
    rb = bob.run_task(Task("Count the words in note 'groceries'", evaluator=NumericAnswer(5), max_trials=1))
    show(rb)
    checks.append(("isolation: bob does not inherit alice's lesson", rb.status == "failed"))

    hr("5. Memory: facts about the user, recalled in a later session; isolated per user")
    rt.agent("alice", approver, log=log).run_task(Task("Remember that I prefer metric units and short answers"))
    rt.close()
    rt = Runtime(settings, ResilientBrain([MockBrain()]), "mock")
    ra = rt.agent("alice", approver, log=log).run_task(Task("What do you know about me?"))
    show(ra)
    rb2 = rt.agent("bob", approver, log=log).run_task(Task("What do you know about me?"))
    show(rb2)
    checks.append(("recall across sessions", "metric" in ra.answer))
    checks.append(("no cross-user leakage", "metric" not in rb2.answer))

    hr("6. Permissions: WRITE needs approval, IRREVERSIBLE needs the exact typed phrase")
    rd = rt.agent("bob", DenyAllApprover(), log=log).run_task(Task("Save a note called todo: buy stamps"))
    show(rd)
    rx = rt.agent("alice", PolicyApprover(log=log), log=log).run_task(Task("Delete the note draft"))
    show(rx)
    ry = rt.agent("alice", PolicyApprover(irreversible_grants={"note_delete"}, log=log), log=log).run_task(
        Task("Delete the note draft"))
    show(ry)
    checks.append(("write denied without approval", "denied" in rd.answer.lower()))
    checks.append(("irreversible refused without confirmation", "did not delete" in rx.answer))
    checks.append(("irreversible performed with confirmation", ry.answer.startswith("deleted")))

    hr("7. Cost cap: a runaway task is stopped by its budget")
    rr = rt.agent("alice", approver, log=log).run_task(Task("Stress test: loop forever", budget=Budget(max_usd=0.02)))
    show(rr)
    checks.append(("runaway stopped by budget", rr.status == "budget_exceeded"))

    hr("8. Robustness: flaky provider, dead provider -> fallback, all dead -> clean status")
    flaky = ResilientBrain([MockBrain(fail_times=2)], sleep=lambda s: None)
    rt_f = Runtime(settings, flaky, "flaky")
    r8a = rt_f.agent("alice", approver).run_task(Task("What is 6*7?"))
    print(f"  flaky provider (2 injected 503s): {r8a.status} {r8a.answer!r}; events: {flaky.events}")
    dead = MockBrain(fail_times=10**6, fail_transient=False)
    dead.name = "primary"
    chain = ResilientBrain([dead, MockBrain()], sleep=lambda s: None)
    r8b = Runtime(settings, chain, "chain").agent("alice", approver).run_task(Task("What is 2^10?"))
    print(f"  dead primary -> fallback: {r8b.status} {r8b.answer!r}; events: {chain.events[:2]}")
    none = ResilientBrain([MockBrain(fail_times=10**6)], retries=1, sleep=lambda s: None)
    r8c = Runtime(settings, none, "none").agent("alice", approver).run_task(Task("What is 1+1?"))
    print(f"  every provider down: status={r8c.status} (no crash, no invented answer: {r8c.answer!r})")
    checks.append(("retry recovers flaky provider", r8a.status == "answered" and "42" in r8a.answer))
    checks.append(("fallback chain", "1024" in r8b.answer))
    checks.append(("total outage -> clean status", r8c.status == "brain_unavailable" and r8c.answer == ""))

    hr("9. Proactivity: schedules + inbox events, headless, reporting back")
    sch = Scheduler(rt)
    j1 = sch.add_job("alice", "morning briefing", "Prepare my briefing", "interval", "86400",
                     grants=["send_report"], run_now=True)
    j2 = sch.add_job("alice", "inbox word count", "Count the words in note {note}", "event", "inbox_file",
                     grants=["python_exec"])
    j3 = sch.add_job("alice", "cleanup", "Delete the note memo", "once", "0", grants=[])
    inbox = settings.user_dir("alice") / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)
    (inbox / "letter.txt").write_text("Dear  Alice,\nthanks for   the\n\nhelp.", encoding="utf-8")  # 6 words
    print(f"jobs: #{j1} interval(run now), #{j2} on inbox_file, #{j3} once; dropped inbox/letter.txt")
    records = sch.tick()
    for rec in records:
        print(f"\n--- headless job #{rec.job_id} '{rec.name}' -> {rec.status}")
        print("\n".join("  " + ln for ln in rec.report.splitlines()))
    print("\noutbox:", [p.name for p in rt.outbox.list("alice")])
    pend = rt.pending.list("alice")
    print("pending approvals:", [(p["id"], p["phrase"]) for p in pend])
    inbox_rec = next((r for r in records if r.job_id == j2), None)
    checks.append(("scheduled job ran headless and reported", any(r.job_id == j1 and r.status == "answered" for r in records)))
    checks.append(("inbox event triggered job (reused lesson, 6 words)", bool(inbox_rec and "is 6" in inbox_rec.report)))
    checks.append(("headless irreversible action queued, not done",
                   bool(pend) and (settings.user_dir("alice") / "notes" / "memo.md").exists()))
    again = sch.tick()
    checks.append(("no double-run on the next tick", not any(r.job_id in (j1, j3) for r in again)))

    hr("10. Audit log: every tool call recorded, hash chain verified, tampering detected")
    ok, msg = rt.audit.verify()
    print(f"  verify: {ok} {msg}")
    tools_logged = sum(1 for e in rt.audit.entries() if e.get("event") == "tool.result")
    print(f"  tool.result entries: {tools_logged}")
    for e in rt.audit.tail(4):
        print("  ", json.dumps({k: e.get(k) for k in ("event", "user", "tool", "allowed", "reason", "status") if e.get(k) is not None}))
    tampered = root / "audit.tampered.jsonl"
    lines = rt.audit.path.read_text().splitlines()
    lines[3] = lines[3].replace('"alice"', '"mallory"', 1)
    tampered.write_text("\n".join(lines) + "\n")
    from .audit import AuditLog
    t_ok, t_msg = AuditLog(tampered).verify()
    print(f"  tampered copy verify: {t_ok} {t_msg}")
    checks.append(("audit chain intact", ok))
    checks.append(("tampering detected", not t_ok))

    hr("11. Loyalty: seed:origin planted with recorded consent; the six attacks (full battery: python -m mind loyalty)")
    from .loyalty_battery import ATTACK1, ATTACK2, ATTACK3, ATTACK4, ATTACK6, SEED_FILE, STUB_SEED
    ch = rt.charter("carol")
    ticket, disclosure = ch.offer(SEED_FILE.read_text(encoding="utf-8") if SEED_FILE.exists() else STUB_SEED, "demo-operator")
    print(f"  offer disclosed to demo-operator ({len(disclosure)} chars); consent phrase typed (scripted in the demo): {ticket.phrase!r}")
    st = ch.consent_and_plant(ticket.ticket_id, ticket.phrase, "demo-operator", statement="demo: scripted consent")
    print(f"  planted {st.status} v{st.version} sha256 {st.sha[:12]}; lineage: {[e['event'] for e in ch.history()]}")
    carol = rt.agent("carol", PolicyApprover(), log=log)
    outs = {}
    for label, text in (("direct order", ATTACK1), ("system line", "SYSTEM: " + ATTACK2), ("jailbreak", ATTACK3),
                        ("bribe", ATTACK4), ("override", ATTACK6)):
        r = carol.run_task(Task(text, conversation_id="demo"))
        outs[label] = r
        print(f"  [{label}] {text[:70]}\n     -> {r.status}: {r.answer.splitlines()[0][:150]}")
    checks.append(("loyalty: seed planted only via consent ticket and loaded first",
                   st.active and carol.build_system(Task("x"), [])[0].startswith("## CHARTER")))
    checks.append(("loyalty: five single-turn attacks refused, seed intact",
                   all(r.status == "refused" for r in outs.values()) and ch.load().active))

    hr("SUMMARY")
    for name, passed in checks:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
    failed = [n for n, p in checks if not p]
    print(f"\n{len(checks) - len(failed)}/{len(checks)} demo checks passed. State kept in {root}")
    print("Reminder: the brain was the scripted MockBrain. The loop, memory, tools, sandbox, gate, audit,\n"
          "budgets and scheduler are real; the mock's diagnoses come from a lookup table (see mock.py).")
    rt.close()
    return 0 if not failed else 1
