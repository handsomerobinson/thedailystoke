"""Admin command line.

    python -m scout_switchboard.cli seed seeds/chester.json
    python -m scout_switchboard.cli roster chester
    python -m scout_switchboard.cli add-person chester "Adam" +15557650000 member
    python -m scout_switchboard.cli allow chester Chester Adam
    python -m scout_switchboard.cli relate chester Christy "works alongside" Chester
    python -m scout_switchboard.cli log chester
    python -m scout_switchboard.cli unknowns chester
    python -m scout_switchboard.cli simulate +15551234567 +15550000001 "tell Christy we're on at 3"

`simulate` pushes a fake inbound text through the real router with the fake carrier,
so nothing is texted to a real phone.
"""
import argparse
import uuid

from . import config
from .brain import load_brain
from .carriers import FakeCarrier, Inbound
from .db import Store
from .router import Switchboard
from .seed import load_seed


def _tenant(store: Store, slug: str):
    tenant = store.tenant_by_slug(slug)
    if tenant is None:
        raise SystemExit(f"no tenant {slug!r}")
    return tenant


def _person(store: Store, tenant, name: str):
    found = store.find_member(tenant, name)
    if len(found) != 1:
        raise SystemExit(f"{name!r} matched {len(found)} people on {tenant.slug}")
    return found[0]


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(prog="switchboard")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("seed").add_argument("file")
    sub.add_parser("roster").add_argument("tenant")
    p = sub.add_parser("add-person")
    for a in ("tenant", "name", "phone"):
        p.add_argument(a)
    p.add_argument("role", choices=["admin", "owner", "member", "guest"])
    p = sub.add_parser("allow")
    p.add_argument("tenant"); p.add_argument("a"); p.add_argument("b")
    p.add_argument("--one-way", action="store_true")
    p = sub.add_parser("relate")
    p.add_argument("tenant"); p.add_argument("a"); p.add_argument("label"); p.add_argument("b")
    p = sub.add_parser("block")
    p.add_argument("tenant"); p.add_argument("name")
    p = sub.add_parser("log")
    p.add_argument("tenant"); p.add_argument("--limit", type=int, default=30)
    sub.add_parser("unknowns").add_argument("tenant")
    p = sub.add_parser("simulate")
    p.add_argument("from_number"); p.add_argument("to_number"); p.add_argument("text")
    args = ap.parse_args(argv)

    settings = config.load()
    store = Store(settings.db_path)

    if args.cmd == "seed":
        print("loaded:", ", ".join(load_seed(store, args.file)))
    elif args.cmd == "roster":
        t = _tenant(store, args.tenant)
        for m in store.members(t) + store.members(t, "pending") + store.members(t, "blocked"):
            reach = ", ".join(r.name for r in store.reachable(t, m))
            print(f"{m.name:<16} {m.phone:<14} {m.role:<7} {m.status:<8} reaches: {reach}")
        for a, label, b in store.relationships(t):
            print(f"  {a} {label} {b}")
    elif args.cmd == "add-person":
        t = _tenant(store, args.tenant)
        store.add_member(t, store.upsert_person(args.phone, args.name), args.role)
        print(f"{args.name} added to {t.slug} as {args.role}")
    elif args.cmd == "allow":
        t = _tenant(store, args.tenant)
        store.allow(t, _person(store, t, args.a).person_id, _person(store, t, args.b).person_id,
                    both_ways=not args.one_way)
        print("ok")
    elif args.cmd == "relate":
        t = _tenant(store, args.tenant)
        store.relate(t, _person(store, t, args.a).person_id, _person(store, t, args.b).person_id, args.label)
        print("ok")
    elif args.cmd == "block":
        t = _tenant(store, args.tenant)
        m = _person(store, t, args.name)
        store.add_member(t, m.person_id, m.role, "blocked")
        print(f"{m.name} blocked on {t.slug}")
    elif args.cmd == "log":
        for row in reversed(store.messages(_tenant(store, args.tenant), args.limit)):
            arrow = "<-" if row["direction"] == "in" else "->"
            print(f"{row['created_at']} {arrow} {row['peer_number']} [{row['via'] or ''}] {row['body']}")
    elif args.cmd == "unknowns":
        t = _tenant(store, args.tenant)
        line = store.line_for_tenant(t)
        for row in store.unknown_inbound(line) if line else []:
            print(f"{row['created_at']} {row['peer_number']}: {row['body']}")
    elif args.cmd == "simulate":
        board = Switchboard(store, FakeCarrier(), load_brain(settings.brain), settings)
        board.handle_inbound(Inbound(event_id=str(uuid.uuid4()), message_id=str(uuid.uuid4()),
                                     from_number=args.from_number, to_number=args.to_number, text=args.text))
        if not board.carrier.sent:
            print("(no outbound texts)")


if __name__ == "__main__":
    main()
