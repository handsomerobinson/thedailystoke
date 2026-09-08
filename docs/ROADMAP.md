# Roadmap — paused, and the order to unpause in

Project is on hold pending cash. Nothing is at risk while it waits: the data
is in iCloud, already paid for. There is no clock on this.

---

## What changed

Two things, both significant:

- The library is **~25TB**, not 7TB.
- The target is an **adventure van** with Starlink, with a fixed home base
  only later.

Together those invert the plan.

---

## The van: three hard constraints

**Power.** A mini PC plus four spinning drives is 50–80W continuous, which is
1.2–2 kWh a day. On a typical 200–400Ah van bank that is a large fraction of
daily solar harvest, running around the clock, forever. A vault is a 24/7
service; a van is an energy-budgeted system. They fight.

**Vibration.** Hard drives are rated for operating shock, not for continuous
washboard road. Spinning platters while driving is how you kill drives, and
25TB of them is not a cheap mistake. SSDs solve it and cost roughly nine times
as much per TB — about $3,600 for 25TB at current prices.

**Starlink upload.** Roam gives 10–20 Mbps up, variable and deprioritized.
25TB over that link is not slow, it is **arithmetically impossible** — years,
not weeks. Any plan where the van is the primary copy and something else is
the backup dies right here.

## So the data does not live in the van

```
BASE  (fixed, mains power, cheap drives)    the 25TB vault
 │
 │  Tailscale, syncing on real wifi only
 ▼
VAN   (laptop + 2-4TB SSD)                  the working subset
```

The van carries what you are actually using — recent photos, current projects,
anything you want offline. The base holds everything, on mains power, on cheap
drives that never move.

**The base does not have to be your home.** A relative's house, a friend's
garage, a powered storage unit. It needs power, an internet connection, and
somewhere out of the way. Roughly 60W and a corner. That also makes it the
off-site copy, which you need regardless.

New photos taken in the van land on the laptop and its SSD immediately, and
sync to base next time you have real wifi. Nothing is ever only in one place.

---

## Order of operations

**Phase 0 — now. $0.**
Paused. Stay on iCloud. Nothing at risk, nothing urgent.
The stack is already proven end to end on a MacBook: phone uploading, semantic
search working, three bugs found and fixed. That work is done and keeps.

**Phase 1 — a client install. ~$500 of their money, ~$2,000 revenue.**
A normal 1–2TB library in a house on ordinary wifi. Cheap, quick, and the
proven case. Fund the next phase with it.

**Phase 2 — the base vault. ~$1,500.**
Mini PC, 32GB RAM, 4×8TB or 2×16TB drives, at whatever fixed location you can
get. This is the 25TB vault. Migrate out of iCloud here, over months, and
cancel the $59.99/month plan when it is done.

**Phase 3 — the van node. ~$400.**
Laptop plus a 2–4TB SSD. Tailscale back to base. Syncs on real wifi, never on
Starlink.

**Phase 4 — the base moves home** when there is a home.

---

## Why a client goes first now

Earlier the advice was the opposite: build yours first, never make a friend the
guinea pig. That was right when nothing had been proven.

It has been now. The stack ran end to end on a laptop — phone to server to
search — and the three bugs that surfaced were all Docker Desktop's macOS file
sharing, none of them the design. On Linux they do not exist.

What is left is a different objection, and it is about scale rather than risk:
**your own setup is the hardest possible case** — 25TB, mobile, satellite
internet, battery power. A client with a 1TB library in a house is the easy
one. Proving the hard case first, with money you do not have, in order to
service the easy case, is backwards.

Do the easy one. It pays for the hard one.

---

## The money, plainly

| | |
|---|---|
| Currently paying Apple | $720/year |
| One client install | ~$2,000 revenue, ~$500 cost |
| Two client installs | funds the entire base vault outright |

Two jobs and the whole thing is paid for, with the Apple bill cancelled on top.
