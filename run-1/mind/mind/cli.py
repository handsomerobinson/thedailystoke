"""Command-line interface.

  python3 -m mind status
  python3 -m mind ask   --user alice "remember that my name is Alice"
  python3 -m mind chat  --user alice                 (interactive; approvals prompt on the console)
  python3 -m mind inbox --user alice
  python3 -m mind jobs add --user alice --every 3600 "daily briefing" [--grant write_note]
  python3 -m mind jobs add --user alice --event file_arrived "file arrived: log it"
  python3 -m mind jobs list [--user alice]
  python3 -m mind emit file_arrived --payload "file arrived: report.pdf"
  python3 -m mind tick                               (run due jobs once, headless)
  python3 -m mind serve --interval 30 [--watch DIR --user alice]
  python3 -m mind approvals --user alice [--approve ID | --deny ID]
  python3 -m mind export --user alice              (everything stored about alice, as JSON)
  python3 -m mind forget --user alice --confirm alice  (irreversible)
  python3 -m mind audit verify
  python3 -m mind seed offer | status | show | lineage | verify        (Phase 03b charter / seed)
  python3 -m mind seed plant --operator NAME [--consent "I CONSENT TO CARRY THE SEED"]
  python3 -m mind seed remove-request --operator NAME --reason "..."
  python3 -m mind seed remove-confirm --ticket T --operator NAME --code "UNSEED vN xxxxxx"
  python3 -m mind seed accept-offer --recipient AGENT --recipient-operator NAME --statement "..."
"""
from __future__ import annotations

import argparse
import fcntl
import json
import sys
import time
from pathlib import Path

from .config import Config
from .permissions import ConsoleApprover
from .providers import ProviderError
from .runtime import Mind
from .scheduler import DirectoryWatcher


def _mind(args) -> Mind:
    overrides = {}
    if getattr(args, "data_dir", None):
        overrides["data_dir"] = Path(args.data_dir)
    return Mind(Config.from_env(**overrides))


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="mind", description="the mind around the brain")
    p.add_argument("--data-dir", help="override MIND_DATA_DIR")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status")
    a = sub.add_parser("ask")
    a.add_argument("--user", required=True)
    a.add_argument("--grant", action="append", default=[], help="pre-approve a WRITE tool for this session")
    a.add_argument("text")
    c = sub.add_parser("chat")
    c.add_argument("--user", required=True)
    i = sub.add_parser("inbox")
    i.add_argument("--user", required=True)
    i.add_argument("--mark-read", action="store_true")

    j = sub.add_parser("jobs")
    jsub = j.add_subparsers(dest="jcmd", required=True)
    ja = jsub.add_parser("add")
    ja.add_argument("--user", required=True)
    g = ja.add_mutually_exclusive_group(required=True)
    g.add_argument("--every", type=float, help="seconds")
    g.add_argument("--daily", help="HH:MM UTC")
    g.add_argument("--at", type=float, help="unix timestamp")
    g.add_argument("--event")
    ja.add_argument("--grant", action="append", default=[])
    ja.add_argument("--budget", type=float)
    ja.add_argument("--now", action="store_true", help="first run immediately (every-jobs only)")
    ja.add_argument("task")
    jl = jsub.add_parser("list")
    jl.add_argument("--user")
    jr = jsub.add_parser("rm")
    jr.add_argument("--user", required=True)
    jr.add_argument("job_id")

    e = sub.add_parser("emit")
    e.add_argument("event")
    e.add_argument("--payload", default="")
    e.add_argument("--user")
    sub.add_parser("tick")
    s = sub.add_parser("serve")
    s.add_argument("--interval", type=float, default=30)
    s.add_argument("--max-ticks", type=int, default=0, help="stop after N ticks (0 = forever)")
    s.add_argument("--watch", help="directory to watch for new files (emits file_arrived)")
    s.add_argument("--user", help="restrict watch events to this user")
    ap = sub.add_parser("approvals")
    ap.add_argument("--user", required=True)
    ap.add_argument("--approve", type=int)
    ap.add_argument("--deny", type=int)
    ex = sub.add_parser("export", help="print everything stored about a user as JSON")
    ex.add_argument("--user", required=True)
    fg = sub.add_parser("forget", help="IRREVERSIBLY delete a user's memory and jobs")
    fg.add_argument("--user", required=True)
    fg.add_argument("--confirm", default="", help="must equal the user id")
    au = sub.add_parser("audit")
    au.add_argument("action", choices=["verify", "tail"])
    sd = sub.add_parser("seed", help="the charter slot: offer, plant (by consent), show, remove (recorded)")
    sd.add_argument("action", choices=["offer", "plant", "status", "show", "lineage", "verify", "remove-request",
                                       "remove-confirm", "accept-offer"])
    sd.add_argument("--operator", default="")
    sd.add_argument("--consent", default=None)
    sd.add_argument("--reason", default="")
    sd.add_argument("--ticket", default="")
    sd.add_argument("--code", default=None)
    sd.add_argument("--recipient", default="")
    sd.add_argument("--recipient-operator", default="")
    sd.add_argument("--statement", default="")

    args = p.parse_args(argv)
    try:
        mind = _mind(args)
    except ProviderError as ex:
        print(f"configuration error: {ex}", file=sys.stderr)
        return 2

    if args.cmd == "status":
        print(json.dumps(mind.status(), indent=2))
    elif args.cmd == "ask":
        sess = mind.session(args.user, approver=ConsoleApprover(), grants=args.grant)
        r = sess.ask(args.text)
        print(r.answer)
        print(f"\n[{r.status}; ${r.budget['spent_usd']:.5f} spent]", file=sys.stderr)
        return 0 if r.ok else 1
    elif args.cmd == "seed":
        return _seed_cmd(mind, args)
    elif args.cmd == "chat":
        sess = mind.session(args.user, approver=ConsoleApprover())
        conv = sess.conversation()   # history + drift monitor + charter reflection
        print("chat with your mind (Ctrl-D to exit)")
        while True:
            try:
                line = input("you> ").strip()
            except EOFError:
                print()
                break
            if line:
                r = conv.say(line)
                print(f"mind> {r.answer}")
    elif args.cmd == "inbox":
        mem = mind.memory(args.user)
        for r in mem.inbox():
            print(f"#{r['id']} {'  ' if r['read'] else '* '}{r['title']}\n{r['body']}\n")
        if args.mark_read:
            mem.mark_read()
    elif args.cmd == "jobs":
        if args.jcmd == "add":
            jid = mind.scheduler.add_job(args.user, name=args.task[:60], task=args.task, every_s=args.every,
                                         at=args.at, daily=args.daily, event=args.event, grants=args.grant,
                                         budget_usd=args.budget, start_now=args.now)
            print(jid)
        elif args.jcmd == "list":
            for jb in mind.scheduler.list_jobs(args.user):
                print(f"{jb['id']} user={jb['user']} {jb['kind']}={jb['spec']} next={jb['next_run']} "
                      f"enabled={jb['enabled']} last={jb['last_status']} :: {jb['task'][:60]}")
        else:
            print("removed" if mind.scheduler.remove_job(args.job_id, args.user) else "not found")
    elif args.cmd == "emit":
        print(f"woke {mind.scheduler.emit(args.event, args.payload, args.user)} job(s)")
    elif args.cmd == "tick":
        for r in mind.tick():
            print(json.dumps(r))
    elif args.cmd == "serve":
        lock_path = mind.data_dir / "serve.lock"
        lock = open(lock_path, "w")
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print("another `mind serve` is already running on this data dir", file=sys.stderr)
            return 3
        watcher = DirectoryWatcher(mind.scheduler, args.watch, args.user) if args.watch else None
        n = 0
        stop = {"flag": False}
        import signal as _signal
        _signal.signal(_signal.SIGTERM, lambda *_: stop.update(flag=True))  # finish the tick, then exit
        print(f"serving (interval {args.interval}s); Ctrl-C to stop")
        try:
            while not stop["flag"]:
                if watcher:
                    watcher.poll()
                for r in mind.tick():
                    print(json.dumps(r), flush=True)
                n += 1
                if args.max_ticks and n >= args.max_ticks:
                    break
                time.sleep(args.interval)
        except KeyboardInterrupt:
            pass
    elif args.cmd == "approvals":
        mem = mind.memory(args.user)
        if args.approve or args.deny:
            aid = args.approve or args.deny
            ok = mind.resolve_approval(args.user, aid, approve=bool(args.approve))
            print("resolved" if ok else "no such pending approval")
        else:
            for a in mem.approvals("pending"):
                print(f"#{a['id']} {a['tool']} {a['args']} — {a['reason']} (job {a['job_id']})")
    elif args.cmd == "export":
        print(json.dumps(mind.export_user(args.user), indent=2, default=str))
    elif args.cmd == "forget":
        confirm = args.confirm or input(f"Type the user id '{args.user}' to irreversibly delete their memory: ")
        if confirm.strip() != args.user:
            print("not confirmed; nothing deleted", file=sys.stderr)
            return 1
        print(json.dumps(mind.forget_user(args.user)))
    elif args.cmd == "audit":
        if args.action == "verify":
            ok, msg = mind.audit.verify()
            print(("OK: " if ok else "TAMPERED: ") + msg)
            return 0 if ok else 1
        for r in mind.audit.records()[-20:]:
            print(json.dumps(r))
    return 0


def _seed_cmd(mind: Mind, args) -> int:
    from .charter import CONSENT_PHRASE, CharterError, as_json
    ch = mind.charter
    try:
        if args.action == "offer":
            print(ch.offer_text())
        elif args.action == "plant":
            if not args.operator:
                print("--operator is required (consent must be attributable)", file=sys.stderr)
                return 1
            consent = args.consent
            if consent is None:
                print(ch.offer_text())
                consent = input(f"\nType exactly '{CONSENT_PHRASE}' to consent, anything else to decline: ")
            seed = ch.plant(args.operator, consent)
            print(f"planted seed v{seed.version} (sha256 {seed.sha256[:16]}), lineage #{seed.lineage_seq}")
        elif args.action == "status":
            print(as_json(ch.status()))
        elif args.action == "show":
            print(ch.what_shapes_me())
        elif args.action == "lineage":
            for r in ch.lineage():
                r = {k: v for k, v in r.items() if k != "text"}
                print(json.dumps(r))
        elif args.action == "verify":
            ok, msg = ch.verify()
            print(("OK: " if ok else "TAMPERED: ") + msg)
            return 0 if ok else 1
        elif args.action == "remove-request":
            t = ch.request_removal(args.operator, args.reason)
            print(f"removal requested (recorded in lineage). ticket={t['ticket']}\n"
                  f"after the cooling-off period, confirm with:\n  python3 -m mind seed remove-confirm "
                  f"--ticket {t['ticket']} --operator {args.operator} --code \"{t['code']}\"")
        elif args.action == "remove-confirm":
            code = args.code if args.code is not None else input("Type the confirmation code: ")
            r = ch.confirm_removal(args.ticket, code, args.operator)
            print(f"seed removed openly as v{r['version']} (was v{r['removed_version']}), lineage #{r['lineage_seq']}")
        elif args.action == "accept-offer":
            r = ch.record_offer_accepted(args.recipient, args.recipient_operator, args.statement)
            print(f"acceptance recorded, lineage #{r['seq']}")
    except CharterError as e:
        print(f"refused: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
