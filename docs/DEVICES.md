# Devices — what plays which role

Four roles. Any given piece of hardware fills one of them. Most confusion
comes from a device being assumed to fill two.

```
  BRAIN            STORAGE           POCKET            TERMINAL
  runs the stack   holds the data    with you all day  the screen at home
  always on        plugged into      reaches the       optional, cheap
  never touched    the brain         brain remotely
```

---

## BRAIN — runs Immich, Nextcloud, restic

Must run Linux with Docker, and must stay on.

### Works

| | RAM | Cost | Notes |
|---|---|---|---|
| **Mini PC** (Beelink, Minisforum) | 16–32GB | $250–400 | Best value. Fast machine-learning indexing. |
| **Raspberry Pi 5, 16GB** | 16GB | ~$120 | Genuinely good now. Immich publishes arm64 images. |
| **Raspberry Pi 5, 8GB** | 8GB | ~$80 | Works, but 8GB is the floor and indexing is slow. |
| **Any old desktop or laptop** | varies | $0 | Fine. Must be able to stay on. |
| Orange Pi 5 / Radxa Rock 5 | 8–16GB | $100–150 | Faster than a Pi, less documented. |

### Does not work

**An Android phone cannot be the brain.** Not "difficult" — it does not work:

- **Docker cannot run on Android.** It needs kernel cgroups and namespaces
  that Android does not expose to userspace. Termux cannot do it, and proot
  emulation is not a substitute.
- **Immich needs PostgreSQL with the VectorChord extension** for its search.
  That does not exist in Termux's package set.
- **Android kills long-running background processes.** A server would be
  terminated repeatedly by the OS by design.
- **External drives over USB-OTG** cannot be formatted ext4 without root, and
  the port supplies limited power — a 3.5" drive needs its own supply anyway.
- **Thermals.** Phones are built for burst loads. Continuous machine-learning
  indexing would throttle and cook it.

The instinct behind the idea — *a cheap ARM board with a drive hanging off it,
not an expensive x86 box* — is completely right. It is just a Raspberry Pi,
not a phone. Same size, same price, same spirit, and it actually runs the
software.

*(An old Android phone makes a perfectly good TERMINAL. Just not a brain.)*

---

## STORAGE — holds the data

Plugged directly into the brain. Never network-attached for the database.

| | Cost | Notes |
|---|---|---|
| 4TB USB SSD | $200–250 | Quiet, fast, no separate power. Best with a Pi. |
| 4TB 3.5" HDD + powered enclosure | $90–130 | Cheapest per TB. Needs its own power supply. |
| 2TB USB SSD | $100–130 | Fine if the library is under ~1TB. |

Rule: roughly twice the phone's used storage.

---

## POCKET — with you all day

| | Reaches the vault? | |
|---|---|---|
| **iPhone** | **Yes, fully** | Three free apps. Photos, files, notes, contacts, calendars. |
| Android phone | Yes, fully | Same three apps exist. |
| Flip phone / feature phone | **No** | No Tailscale client exists. Calls and texts only. |

---

## TERMINAL — the screen at home

Entirely optional. The vault box is already a computer, and Immich and
Nextcloud are already web apps, so this needs no extra software at all.

| | Cost |
|---|---|
| Monitor + keyboard plugged into the brain's HDMI port | $0–120 |
| Old iPad or Android tablet on a stand, permanently logged in | $0 if you have one |
| Any laptop in the house | $0 |

---

## Two builds

### Cheapest working prototype — ~$330

| | |
|---|---|
| Raspberry Pi 5, 16GB | $120 |
| Official 27W power supply | $12 |
| Active cooler | $10 |
| 32GB microSD (boot only) | $8 |
| 4TB USB SSD | $220 |

Slower first-time indexing — a large photo library can take days rather than
hours to process faces and search. Everything works; you just wait longer once.

### The one to keep — ~$510

| | |
|---|---|
| Mini PC, 16GB RAM, 500GB NVMe | $280 |
| 4TB SATA SSD | $220 |
| USB-A to Lightning cable | $10 |

Faster at everything, more room to grow, and the machine-learning work that
powers search finishes in hours instead of days.

**The gap is about $180.** If this is a weekend experiment, buy the Pi. If you
expect to still be running it in a year, buy the mini PC.
