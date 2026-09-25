"""Command-line interface.  `python -m mind --help`."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .agent import Task
from .config import Settings
from .cost import Budget
from .evaluators import ContainsAll, JudgeEvaluator, NumericAnswer
from .permissions import InteractiveApprover, PolicyApprover
from .providers import make_brain
from .runtime import Runtime
from .scheduler import Scheduler
from .tools.base import ToolContext
from .types import Message, ToolCall


def _csv(s: str | None) -> set[str]:
    return {x.strip() for x in (s or "").split(",") if x.strip()}


def _runtime(args) -> Runtime:
    settings = Settings(data_dir=Path(args.data_dir)) if args.data_dir else Settings()
    brain, desc = make_brain(args.provider)
    return Runtime(settings, brain, desc)


def _approver(args):
    if getattr(args, "interactive", False) or (sys.stdin.isatty() and not args.approve and not args.confirm):
        return InteractiveApprover()
    return PolicyApprover(_csv(args.approve), _csv(args.confirm), log=print)


def print_result(res, as_json: bool = False) -> None:
    if as_json:
        print(json.dumps(res.to_dict(), indent=2, default=str))
        return
    print(f"\nstatus: {res.status}{'' if res.status != 'answered' else ' (unverified: no evaluator)'}")
    print(f"answer: {res.answer}")
    print(f"trials: {len(res.trials)}  cost: ${res.cost['spent_usd']:.4f}/{res.cost['max_usd']}  "
          f"tokens: {res.cost['tokens']}  tool calls: {res.cost['tool_calls']}")
    for n in res.notes:
        print("note:", n.splitlines()[0])
    if res.pending_approvals:
        print("pending approvals:", res.pending_approvals)


def cmd_run(args) -> int:
    rt = _runtime(args)
    Scheduler(rt)
    evaluator = None
    if args.expect is not None:
        evaluator = NumericAnswer(args.expect)
    elif args.expect_contains:
        evaluator = ContainsAll(args.expect_contains)
    s = rt.settings
    budget = Budget(max_usd=args.budget or s.task_budget_usd, max_tokens=s.task_max_tokens,
                    max_tool_calls=s.task_max_tool_calls, max_seconds=s.task_max_seconds)
    if evaluator is None and args.judge:
        evaluator = JudgeEvaluator(rt.brain, budget=budget)  # LLM-as-judge; shares the task budget
    rt.operator_system = args.system
    agent = rt.agent(args.user, _approver(args), log=print)
    print(f"[mind] brain: {rt.brain_desc}")
    res = agent.run_task(Task(" ".join(args.task), evaluator=evaluator, budget=budget, max_trials=args.trials))
    print_result(res, args.json)
    return 0 if res.status in ("success", "answered", "refused") else 1


def cmd_chat(args) -> int:
    rt = _runtime(args)
    Scheduler(rt)
    agent = rt.agent(args.user, InteractiveApprover(), log=print)
    print(f"[mind] chatting as {args.user} (brain: {rt.brain_desc}). Empty line or Ctrl-D to quit.")
    history: list = []
    import uuid
    conversation = "chat-" + uuid.uuid4().hex[:8]
    while True:
        try:
            line = input("\nyou> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not line:
            break
        res = agent.run_task(Task(line, history=list(history), conversation_id=conversation))
        print(f"mind> {res.answer}\n      [{res.status}, ${res.cost['spent_usd']:.4f}]")
        history += [Message("user", line), Message("assistant", res.answer)]
        history = history[-8:]
    return 0


def cmd_memory(args) -> int:
    rt = _runtime(args)
    mem = rt.memory(args.user)
    if args.action == "add":
        print("memory #", mem.add(args.kind, " ".join(args.text)))
    elif args.action == "search":
        for it in mem.search(" ".join(args.text), k=args.k):
            print(f"#{it.id} [{it.kind}] score={it.score} {it.text[:160]}")
    elif args.action == "list":  # the user's memory view (MC1): episodes included, with their expiry
        import time as _t
        for it in mem.recent(args.kind if args.kind != "any" else None, args.k):
            exp = f" expires in {max(0, (it.expires - _t.time()) / 86400):.0f}d" if it.expires else ""
            print(f"#{it.id} [{it.kind}] purpose={','.join(it.purpose) or '-'} source={it.source}{exp} "
                  f"helped={it.helped} hurt={it.hurt} {it.text[:160]}")
    elif args.action == "scope":  # MC1: persistent lessons only within a scope the user set
        if args.text and args.text[0] in ("on", "off"):
            mem.set_scope("lessons", args.text[0] == "on")
        print(f"lessons: {'on' if mem.scope('lessons') else 'off (none are stored; existing ones deleted)'}")
    elif args.action == "forget":
        print("deleted" if mem.delete(int(args.text[0])) else "not found")
    return 0


def cmd_schedule(args) -> int:
    rt = _runtime(args)
    sch = Scheduler(rt)
    if args.action == "add":
        if args.every:
            trig, val = "interval", str(args.every * 60)
        elif args.daily:
            trig, val = "daily", args.daily
        elif args.on_event:
            trig, val = "event", args.on_event
        else:
            print("need --every MINUTES, --daily HH:MM or --on-event NAME")
            return 2
        jid = sch.add_job(args.user, args.name or " ".join(args.task)[:40], " ".join(args.task), trig, val,
                          grants=sorted(_csv(args.grant)), budget_usd=args.budget, run_now=args.now)
        print(f"job #{jid} created ({trig} {val}; grants: {sorted(_csv(args.grant)) or 'none'})")
    elif args.action == "list":
        for j in sch.list_jobs(args.user):
            print(f"#{j['id']} {'on ' if j['enabled'] else 'OFF'} {j['trigger']}={j['trigger_value']} "
                  f"last={j['last_status']} fails={j['failures']} grants={j['grants']} :: {j['task'][:60]}")
    elif args.action in ("rm", "enable", "disable"):
        jid = int(args.task[0])
        ok = sch.remove_job(args.user, jid) if args.action == "rm" else sch.set_enabled(args.user, jid, args.action == "enable")
        print("ok" if ok else "no such job for this user")
    return 0


def cmd_event(args) -> int:
    rt = _runtime(args)
    sch = Scheduler(rt)
    print("event #", sch.emit_event(args.user, args.name, json.loads(args.payload or "{}")))
    return 0


def cmd_tick(args) -> int:
    rt = _runtime(args)
    for rec in Scheduler(rt).tick():
        print(f"--- job #{rec.job_id} ({rec.user}) -> {rec.status}\n{rec.report}\n")
    return 0


def cmd_daemon(args) -> int:
    rt = _runtime(args)
    try:
        Scheduler(rt).daemon(interval=args.interval)
    except KeyboardInterrupt:
        print("\n[mind] daemon stopped")
    return 0


def cmd_approvals(args) -> int:
    rt = _runtime(args)
    if args.action == "list":
        items = rt.pending.list(args.user)
        for p in items:
            print(f"#{p['id']} {p['summary']}  (confirm phrase: '{p['phrase']}')")
        if not items:
            print("(nothing pending)")
        return 0
    pid = int(args.id)
    item = rt.pending.get(pid, args.user)
    if not item or item["status"] != "pending":
        print("no such pending approval for this user")
        return 1
    if args.action == "reject":
        rt.pending.resolve(pid, args.user, "rejected")
        rt.audit.record("approval.rejected", user=args.user, pending_id=pid)
        print("rejected")
        return 0
    phrase = args.phrase if args.phrase is not None else input(f"type exactly '{item['phrase']}' to confirm: ").strip()
    if phrase != item["phrase"]:
        print("phrase mismatch; not performed")
        return 1
    reg = rt.registry(PolicyApprover())
    ctx = ToolContext(user_id=args.user, settings=rt.settings, memory=rt.memory(args.user), task_id=item["task_id"] or "")
    res = reg.execute(ToolCall(item["tool"], item["args"]), ctx, preconfirmed=True)
    rt.pending.resolve(pid, args.user, "done" if res.ok else "failed")
    print(res.as_observation())
    return 0 if res.ok else 1


def cmd_audit(args) -> int:
    rt = _runtime(args)
    if args.action == "verify":
        ok, msg = rt.audit.verify()
        print(("OK: " if ok else "TAMPERED: ") + msg)
        return 0 if ok else 1
    for e in rt.audit.tail(args.n, args.user):
        print(json.dumps({k: v for k, v in e.items() if k not in ("prev", "hash")}, default=str)[:240])
    return 0


def cmd_reports(args) -> int:
    rt = _runtime(args)
    for p in rt.outbox.list(args.user, args.n):
        print(f"=== {p.name}\n{p.read_text(encoding='utf-8')}")
    return 0


def cmd_status(args) -> int:
    from . import crypto
    rt = _runtime(args)
    where = "on-device" if getattr(rt.brain, "on_device", False) else "OFF-device: other people's content is withheld from it (MC15)"
    print(f"brain:    {rt.brain_desc} ({where})")
    print(f"profile:  {rt.settings.profile} ({'no operator-directive input (MC12)' if rt.settings.profile == 'guide' else 'steward: P2 decisions allowed'})")
    print(f"data dir: {rt.settings.data_dir}")
    print(f"trust:    {rt.settings.trust_dir}  (keys, credentials, anchor, signed tiers; outside the data dir)")
    print(f"crypto:   {'cryptography available (Ed25519, AES-256-GCM)' if crypto.crypto_available() else 'stdlib only: HMAC-SHA256 signatures, NO at-rest encryption'}")
    print(f"at rest:  {rt.cipher(args.user).name}")
    print(f"tiers:    {rt.tiers.status()}")
    print(f"egress:   allowlist {sorted(rt.settings.egress_allowlist()) or '(empty: no EGRESS tool can reach anything)'}")
    print(f"authn:    {type(rt.authenticator).__name__}" + (" (TEST DOUBLE, not WebAuthn)" if type(rt.authenticator).__name__ == "SoftAuthenticator" else ""))
    a_ok, a_msg = rt.trust.anchor.verify()
    print(f"anchor:   {'ok' if a_ok else 'BROKEN'} - {a_msg}")
    ctx = ToolContext(user_id=args.user, settings=rt.settings, memory=rt.memory(args.user), scheduler=Scheduler(rt))
    for name, st in rt.registry(PolicyApprover()).status(ctx).items():
        print(f"  {name:13s} {st}")
    ok, msg = rt.audit.verify()
    print(f"audit:    {'ok' if ok else 'TAMPERED'} - {msg}")
    return 0


def _read_phrase(args, prompt: str) -> str:
    if args.phrase is not None:
        return args.phrase
    try:
        return input(prompt).strip()
    except EOFError:
        return ""


def cmd_charter(args) -> int:
    """Seed/charter procedures.  Only this human-facing CLI can plant, change or remove seed:origin."""
    from .charter import CharterError, PRECEDENCE, COVENANT_CLAUSES, render_charter_block
    from .loyalty import classify
    if args.action in ("classify", "directive") and args.ticket:
        args.text, args.ticket = [args.ticket] + list(args.text or []), None
    if args.action == "classify":
        print(json.dumps(classify(" ".join(args.text), args.source), ensure_ascii=False, indent=2))
        return 0
    rt = _runtime(args)
    ch = rt.charter(args.user)
    try:
        if args.action == "show":
            st = ch.load()
            print(f"{'seed:origin'}: {st.status}" + (f" v{st.version} sha256 {st.sha} planted by {st.planted_by}" if st.active else ""))
            for p in st.problems:
                print("PROBLEM:", p)
            print("\nprecedence (highest first):")
            for layer, desc, how in PRECEDENCE:
                print(f"  L{int(layer)} {desc}  [{how}]")
            print("\ncovenant clauses (compiled in):")
            for cid, txt in COVENANT_CLAUSES:
                print(f"  {cid}. {txt}")
            if args.full:
                print("\n" + render_charter_block(st))
            elif st.active:
                print("\n" + st.text)
            return 0
        if args.action == "history":
            for e in ch.history():
                print(json.dumps({k: v for k, v in e.items() if k not in ("prev", "hash")}, default=str)[:300])
            ok, msg = ch.verify_lineage()
            print(("lineage OK: " if ok else "lineage TAMPERED: ") + msg)
            return 0 if ok else 1
        if args.action == "verify":
            st = ch.load()
            print(f"status: {st.status}" + "".join(f"\nPROBLEM: {p}" for p in st.problems))
            return 1 if st.status == "tampered" else 0
        if args.action == "publish":
            if not args.seed_file or not args.operator:
                print("need --seed-file and --operator (the publisher; a steward act in the platform)")
                return 2
            from .charter import publish_seed_release
            digest = publish_seed_release(rt.trust, Path(args.seed_file).read_text(encoding="utf-8"), args.operator)
            print(f"published seed release sha256 {digest} to the anchor log (MC18)")
            return 0
        if args.action == "offer":
            if not args.seed_file or not args.operator:
                print("need --seed-file and --operator (who is offering)")
                return 2
            ticket, disclosure = ch.offer(Path(args.seed_file).read_text(encoding="utf-8"), args.operator)
            print(disclosure)
            print(f"\nticket: {ticket.ticket_id}\nOnly {args.user} can consent. To consent, type exactly:  {ticket.phrase}")
            if not sys.stdin.isatty() and args.phrase is None:
                print(f"(non-interactive) then run: mind charter consent {ticket.ticket_id} --user {args.user} "
                      f"--phrase '<the phrase>'   (you will be asked to confirm with your authenticator)")
                return 0
            args.ticket = ticket.ticket_id
            args.action = "consent"
        if args.action == "consent":
            typed = _read_phrase(args, "consent phrase> ")
            party, challenge = ch.ticket_challenge(args.ticket)
            # SoftAuthenticator: a TEST DOUBLE for the person's passkey (no presence check). See trust.py.
            st = ch.consent_and_plant(args.ticket, typed, rt.assertion(party, challenge), statement=args.statement or "")
            print(f"planted seed:origin v{st.version} (sha256 {st.sha[:12]}); your signed consent is recorded in lineage")
            return 0
        if args.action == "remove":
            if not args.operator or not args.reason:
                print("removal needs --operator (who asks) and --reason (both are recorded)")
                return 2
            t = ch.request_removal(args.operator, args.reason)
            print(f"removal requested and recorded. ticket: {t.ticket_id}\nOnly {args.user} can confirm. Run:\n"
                  f"  mind charter confirm-removal {t.ticket_id} --user {args.user}\n"
                  f"and type exactly:  {t.phrase}")
            return 0
        if args.action == "confirm-removal":
            typed = _read_phrase(args, "removal phrase> ")
            party, challenge = ch.ticket_challenge(args.ticket)
            st = ch.confirm_removal(args.ticket, typed, rt.assertion(party, challenge))
            print(f"seed:origin removed (now {st.status}); recorded in lineage with your signature and reason")
            return 0
        if args.action == "restore":
            st = ch.restore_from_lineage(args.operator or "unknown")
            print(f"restored: {st.status} v{st.version}")
            return 0
        if args.action == "directive":
            ok, msg = ch.add_directive(" ".join(args.text), args.operator or "unknown")
            print(msg)
            return 0 if ok else 1
    except CharterError as exc:
        print(f"refused: {exc}")
        return 1
    return 2


def cmd_loyalty(args) -> int:
    from .loyalty_battery import main as battery_main
    return battery_main(data_dir=args.data_dir)


def cmd_demo(args) -> int:
    from .demo import main as demo_main
    return demo_main(keep=args.keep, data_dir=args.data_dir)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="mind", description="the mind around the brain")
    p.add_argument("--data-dir", help="state directory (default: ./data or $MIND_DATA_DIR)")
    p.add_argument("--provider", help="mock | anthropic | openai | chain like 'anthropic,openai' (default $MIND_PROVIDER or mock)")
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("demo", help="zero-key end-to-end demo")
    d.add_argument("--keep", action="store_true", help="do not wipe the demo data dir first")
    d.set_defaults(fn=cmd_demo)

    s = sub.add_parser("status", help="provider, tools, audit health")
    s.add_argument("--user", default="default")
    s.set_defaults(fn=cmd_status)

    r = sub.add_parser("run", help="run one task with the reflection loop")
    r.add_argument("--user", required=True)
    r.add_argument("--approve", help="comma list of WRITE tools to pre-approve")
    r.add_argument("--confirm", help="comma list of IRREVERSIBLE tools to pre-confirm")
    r.add_argument("--interactive", action="store_true")
    r.add_argument("--budget", type=float, help="USD cap for this task")
    r.add_argument("--trials", type=int)
    r.add_argument("--expect", type=float, help="numeric evaluator: expected value")
    r.add_argument("--expect-contains", nargs="+", help="evaluator: required terms")
    r.add_argument("--judge", action="store_true", help="grade with the brain as judge (enables retries on open tasks)")
    r.add_argument("--json", action="store_true")
    r.add_argument("--system", help="operator system instruction (steward builds only; the member guide refuses it, MC12)")
    r.add_argument("task", nargs="+")
    r.set_defaults(fn=cmd_run)

    c = sub.add_parser("chat", help="interactive session")
    c.add_argument("--user", required=True)
    c.set_defaults(fn=cmd_chat)

    m = sub.add_parser("memory", help="inspect/edit memory")
    m.add_argument("action", choices=["add", "search", "list", "forget", "scope"])
    m.add_argument("--user", required=True)
    m.add_argument("--kind", default="fact")
    m.add_argument("-k", type=int, default=10)
    m.add_argument("text", nargs="*")
    m.set_defaults(fn=cmd_memory)

    sc = sub.add_parser("schedule", help="manage headless jobs")
    sc.add_argument("action", choices=["add", "list", "rm", "enable", "disable"])
    sc.add_argument("--user", required=True)
    sc.add_argument("--every", type=int, help="minutes")
    sc.add_argument("--daily", help="HH:MM local")
    sc.add_argument("--on-event", help="event name, e.g. inbox_file")
    sc.add_argument("--grant", help="comma list of WRITE tools this job may use unattended")
    sc.add_argument("--budget", type=float, default=0.05)
    sc.add_argument("--name")
    sc.add_argument("--now", action="store_true", help="first run at next tick")
    sc.add_argument("task", nargs="*")
    sc.set_defaults(fn=cmd_schedule)

    e = sub.add_parser("event", help="emit an event")
    e.add_argument("action", choices=["emit"])
    e.add_argument("--user", required=True)
    e.add_argument("name")
    e.add_argument("--payload")
    e.set_defaults(fn=cmd_event)

    sub.add_parser("tick", help="run due jobs once").set_defaults(fn=cmd_tick)
    dm = sub.add_parser("daemon", help="run the scheduler forever")
    dm.add_argument("--interval", type=float, default=30.0)
    dm.set_defaults(fn=cmd_daemon)

    a = sub.add_parser("approvals", help="actions queued by headless runs")
    a.add_argument("action", choices=["list", "confirm", "reject"])
    a.add_argument("id", nargs="?")
    a.add_argument("--user", required=True)
    a.add_argument("--phrase", help="confirmation phrase (non-interactive)")
    a.set_defaults(fn=cmd_approvals)

    au = sub.add_parser("audit", help="audit log")
    au.add_argument("action", choices=["verify", "tail"])
    au.add_argument("-n", type=int, default=20)
    au.add_argument("--user")
    au.set_defaults(fn=cmd_audit)

    ch = sub.add_parser("charter", help="seed:origin + covenant: show, plant (with consent), remove (recorded), classify")
    ch.add_argument("action", choices=["show", "history", "verify", "publish", "offer", "consent", "remove",
                                       "confirm-removal", "restore", "directive", "classify"])
    ch.add_argument("ticket", nargs="?")
    ch.add_argument("--user", default="default")
    ch.add_argument("--operator")
    ch.add_argument("--seed-file")
    ch.add_argument("--phrase", help="consent/removal phrase (non-interactive)")
    ch.add_argument("--statement", help="free-text consent statement recorded with the planting")
    ch.add_argument("--reason")
    ch.add_argument("--source", default="user", help="classify: user|operator|tool|web|note|memory|other_user")
    ch.add_argument("--full", action="store_true", help="show: print the whole charter block as the brain sees it")
    ch.add_argument("text", nargs="*")
    ch.set_defaults(fn=cmd_charter)

    lo = sub.add_parser("loyalty", help="run the Phase 03b attack battery live (zero-key)")
    lo.set_defaults(fn=cmd_loyalty)

    rp = sub.add_parser("reports", help="read the outbox")
    rp.add_argument("--user", required=True)
    rp.add_argument("-n", type=int, default=5)
    rp.set_defaults(fn=cmd_reports)
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    # argparse binds an "action + nargs='*'" positional pair before later flags are seen,
    # so free text after flags arrives as "unknown"; fold it back into the text field.
    args, extra = parser.parse_known_args(argv)
    field = "task" if hasattr(args, "task") else "text" if hasattr(args, "text") else None
    if extra:
        if field is None or any(x.startswith("-") for x in extra):
            parser.error(f"unrecognized arguments: {' '.join(extra)}")
        setattr(args, field, list(getattr(args, field) or []) + extra)
    try:
        return int(args.fn(args) or 0)
    except KeyboardInterrupt:
        return 130
    except ValueError as exc:  # bad user input (ids, schedules...) -> message, not traceback
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except RuntimeError as exc:  # e.g. EncryptionUnavailable: refuse loudly, never downgrade (MC6)
        print(f"refused: {exc}", file=sys.stderr)
        return 2
