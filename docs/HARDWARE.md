# Hardware

## One person (you, or Dan on his own box)

| Part | Spec | Rough cost |
|---|---|---|
| Mini PC | N100/N150 or Ryzen, **16GB RAM**, 500GB NVMe for the OS | $250–400 |
| Data disk | 2TB–4TB SSD or 3.5" HDD | $100–200 |
| UPS (optional) | Small battery, protects against corruption on power cuts | $60–100 |

**16GB is the floor, not 8GB.** Immich's machine-learning container — the thing
doing face recognition and semantic search — is the memory hog. On 8GB it gets
killed mid-job and search quietly stops working.

Storage rule of thumb: **twice the phone's used space per person**, minimum.
A 256GB iPhone that is nearly full wants 512GB, because thumbnails and
transcoded video land on top of the originals.

Any x86 machine works. An old desktop is fine. It must be able to stay on.

---

## Your box, serving 5–10 people

Immich and Nextcloud are both natively multi-user. **One stack, many accounts,
fully separate libraries.** You do not run ten copies — you could not anyway,
since each Immich needs its own ~4GB machine-learning container.

| Part | Spec |
|---|---|
| Machine | 32GB RAM, 6+ cores |
| Storage | **Mirrored.** Two drives in RAID1 or a ZFS mirror. |
| Capacity | ~300GB/person average → 4TB usable for 10 people |
| Network | Wired ethernet, never wifi |

### The two things that will actually limit you

**Your home upload speed.** This is the real ceiling, not CPU or disk.
10 people × 300GB = 3TB. Pushing that to Backblaze the first time:

| Upload speed | First full backup |
|---|---|
| 10 Mbps | ~28 days saturated |
| 20 Mbps | ~14 days saturated |
| 50 Mbps | ~6 days |
| 500 Mbps (fibre) | ~14 hours |

Also check your ISP's data cap. Comcast and similar cap around 1.2TB/month,
and 3TB of backup plus ongoing sync will blow straight through it. **Measure
your actual upload speed before you sell a hosted seat to anyone.**

**Redundancy stops being optional.** One person on one disk plus off-site
backup is a fine risk. Ten people on one disk is ten simultaneous outages
when it dies, and restoring 3TB from Backblaze over that same slow uplink
takes weeks. Mirror the drives.

---

## Running costs

Backblaze B2 is $6/TB/month. Backups are compressed and deduplicated, so the
stored size is usually well under the raw library size.

| Vault size | B2 per month |
|---|---|
| 250 GB | ~$1.50 |
| 1 TB | ~$6 |
| 3 TB | ~$18 |

Electricity for a mini PC running continuously: roughly $3–6/month.

> The "two cents a month" figure from the original core7 setup was for 3GB of
> text and configuration. A photo library is a hundred to a thousand times
> that. Still far cheaper than iCloud — just do not quote anyone two cents.

---

## Which model to sell

**Client-owned box** — Dan buys the hardware, opens his own Backblaze account,
holds his own passphrase. You install and maintain it.
*You never hold his data or his key.* Lowest liability, simplest conversation,
and it survives you losing interest. **Start here.**

**Your hosted box** — you own the hardware and the bucket, clients get accounts.
Better margins and no hardware conversation, but you become the custodian of
other people's irreplaceable photos, on your home internet, with an uptime
obligation. Different business. Do it second, deliberately, and read the
liability section in [CLIENT-PLAYBOOK.md](CLIENT-PLAYBOOK.md) first.
