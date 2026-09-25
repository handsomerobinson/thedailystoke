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
  python3 -m mind audit verify
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
    au = sub.add_parser("audit")
    au.add_argument("action", choices=["verify", "tail"])

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
    elif args.cmd == "chat":
        sess = mind.session(args.user, approver=ConsoleApprover())
        print("chat with your mind (Ctrl-D to exit)")
        while True:
            try:
                line = input("you> ").strip()
            except EOFError:
                print()
                break
            if line:
                r = sess.ask(line)
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
                                         budget_usd=args.budget)
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
        print(f"serving (interval {args.interval}s); Ctrl-C to stop")
        try:
            while True:
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
    elif args.cmd == "audit":
        if args.action == "verify":
            ok, msg = mind.audit.verify()
            print(("OK: " if ok else "TAMPERED: ") + msg)
            return 0 if ok else 1
        for r in mind.audit.records()[-20:]:
            print(json.dumps(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
