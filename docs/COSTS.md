# What it costs

Prices checked September 2026. Verify Backblaze's current rate before quoting
anyone — it has moved once already.

---

## One-time

| | |
|---|---|
| Mini PC — 16GB RAM, 500GB NVMe for the OS | $250–400 |
| Data disk — 4TB HDD + powered USB enclosure **(recommended)** | $135 |
| *or* data disk — 4TB SSD (no practical benefit for media) | ~$300 |
| UPS (optional, prevents corruption on power cuts) | $60–100 |

**Realistic total: $425**, or $495 with a UPS.

The mini PC's own 500GB NVMe is the fast tier — it holds the databases, which
is the only place SSD speed matters. Media goes on the hard drive. Paying $300
for a 4TB SSD instead buys you nothing you can perceive: photos and video are
read sequentially and a hard drive streams them faster than you can look.
See [STORAGE.md](STORAGE.md).

An old desktop or laptop you already own costs $0 and works fine to start.
The install is identical, so you can begin today and buy hardware later.

---

## Monthly

Only two things cost anything. Immich, Nextcloud, restic and Tailscale
(personal tier) are all free.

**Backblaze B2 — $6.95/TB/month**, charged on your *backed-up* size, which is
smaller than your library: restic deduplicates and compresses, and thumbnails
and transcoded video are excluded because Immich can regenerate them.

**Electricity** — a mini PC averages ~18W, so about 13 kWh/month, roughly
$2–4 depending on your rate.

| Backed-up size | B2 | Power | **Total** |
|---|---|---|---|
| 250 GB | $1.74 | ~$2.20 | **~$4** |
| 500 GB | $3.48 | ~$2.20 | **~$6** |
| 1 TB | $6.95 | ~$2.20 | **~$9** |
| 2 TB | $13.90 | ~$2.20 | **~$16** |
| 4 TB | $27.80 | ~$2.20 | **~$30** |

Restoring is free. B2 gives free egress up to 3× what you store each month,
so pulling your whole vault back does not generate a bill.

---

## The honest comparison

| iCloud+ | |
|---|---|
| 2 TB | $9.99/mo |
| 6 TB | $29.99/mo |
| 12 TB | $59.99/mo |

Put side by side:

| Your library | Vault | iCloud | |
|---|---|---|---|
| ~500 GB | ~$6/mo | $9.99 (2TB tier) | vault cheaper |
| ~1 TB | ~$9/mo | $9.99 | a wash |
| ~2 TB | ~$16/mo | $9.99 | **iCloud cheaper** |
| ~6 TB | ~$44/mo | $29.99 | **iCloud cheaper** |

**So: this does not save you money at typical sizes, and above about 1.5TB it
costs more.** Apple prices its large tiers aggressively. Add $425–500 of
hardware and the payback period on cost alone is somewhere between long and
never.

Do this because you want to own it, because nobody else can read it, because
it holds things iCloud never will — your Messages, Notes, Health and voice
memos in one place — and because it is the foundation for the cocoon. Those
are good reasons. "It's cheaper" is not one, and you would find that out
eventually anyway.

---

## The lever that changes the math

**The off-site copy does not have to be Backblaze.** restic backs up over SSH
just as happily as to B2:

| | |
|---|---|
| Raspberry Pi 5 | ~$80 |
| 4TB external drive | ~$100 |
| **Total** | **~$180 once, then $0/month** |

Put it at a relative's house on their wifi, join it to your tailnet, and point
`RESTIC_REPOSITORY` at it:

```
RESTIC_REPOSITORY=sftp:vault-offsite:/mnt/backup/ryan
```

Still encrypted before it leaves your house — the box at the other end holds
ciphertext it cannot read, exactly like Backblaze. It pays for itself against
B2 in about 8 months at 2TB, and it is the right answer for a large library.

The trade-off is honest: a drive at a relative's house is one drive. It can
die, and nobody is monitoring it but you. Backblaze replicates and never
forgets. `restore-test.sh` matters more, not less, if you go this way.

**Best of both, once you care enough:** B2 for the irreplaceable core (photos,
documents — small, professionally managed), a second box for the bulk (device
backups, video). Set `BACKUP_IPHONE_OFFSITE=0` to keep the heavy device
backups out of B2 and cut that bill substantially.

---

## Bottom line for one person, ~1TB

| | |
|---|---|
| Hardware, once | ~$425 |
| Running cost | **~$9/month** |
| With a Pi off-site instead of B2 | ~$180 more once, then **~$3/month** |

Then cancel the iCloud storage plan and keep the free 5GB tier for Find My and
device backup.
