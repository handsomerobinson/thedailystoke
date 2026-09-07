# Storage

Prices verified September 2026. NAND is expensive right now — AI demand plus
production cuts, with no new fab capacity until late 2027 — so SSD pricing is
roughly double its 2023 low and is not expected to fall soon. Re-check before
buying.

---

## The market, as it actually is

| | $/TB | What that means |
|---|---|---|
| NVMe SSD, 4TB | $70–90 | ~$300. Best value point in SSDs. |
| NVMe SSD, 2TB | ~$129 | ~$260 |
| SSD, 8TB | ~$144 | **~$1,150.** And 8TB is the consumer ceiling. |
| Hard drive, 16TB | $14–18 | **~$250** |

**There is no 16TB consumer SSD worth buying.** Consumer SSDs stop at 8TB, and
16TB of SSD means two 8TB drives at roughly $2,300. A 16TB hard drive is $250.

That is a 9× difference, and for this workload you cannot feel it.

---

## So: two tiers

Photos and video are read **sequentially** — a hard drive streams them as fast
as anyone can look at them. Databases are read **randomly**, and that is where
an SSD is worth every cent.

So split them:

| Tier | Holds | Size | Hardware |
|---|---|---|---|
| **Fast** (`VAULT_ROOT`) | Both databases, dumps, Nextcloud app | Under 200GB even for a huge vault | NVMe SSD, 1–2TB |
| **Bulk** (`VAULT_MEDIA`) | Photo/video originals, iPhone backups | All of it | Hard drive, 4–24TB |

In `vault.env`:

```
VAULT_ROOT=/srv/vault          # SSD
VAULT_MEDIA=/mnt/media         # the big drive
```

Leave `VAULT_MEDIA` blank and everything lives on one disk. **That is the right
answer under about 4TB** — do not add complexity you do not need yet.

---

## What to buy, by capacity

| Their library | Fast tier | Bulk tier | Bulk cost |
|---|---|---|---|
| Under 2TB | 4TB NVMe, no split | — | $300 total |
| 2–4TB | 1TB NVMe | 4TB HDD + USB enclosure | ~$120 |
| 4–8TB | 1TB NVMe | 8TB HDD + powered USB enclosure | ~$190 |
| 8–16TB | 2TB NVMe | 16TB HDD + powered USB enclosure | ~$290 |
| 16TB+, or several people | 2TB NVMe | 2× 16TB in a 2-bay DAS, mirrored | ~$600 |

### Ports and enclosures

- **3.5" hard drives need 12V.** They cannot run off a USB port. Always a
  **powered** enclosure — about $35 for single-bay.
- **Mini PC**: usually 1–2 M.2 NVMe slots, sometimes one 2.5" SATA bay, and
  2–4 USB 3.2 ports at 5–10Gbps. Put the NVMe inside, hang the big drive off USB.
- **Multi-bay DAS** (TerraMaster D4-300, OWC Mercury Elite Pro Quad): 4 bays,
  $150–220, one USB cable. This is how you get past 20TB or add mirroring.
- **Raspberry Pi 5**: 2× USB 3.0, plus NVMe via a PCIe HAT. Fine for the fast
  tier on the HAT and the bulk drive over USB.

USB 3.0 at 5Gbps moves ~450MB/s, comfortably faster than any hard drive. USB
is not the bottleneck.

### Redundancy

One person, one drive plus a verified off-site copy is a reasonable risk.
**Several people on one drive is not** — a failure is several simultaneous
losses, and restoring many TB takes weeks. Mirror it: two drives in a 2-bay
enclosure, `mdadm` RAID1 or a ZFS mirror.

---

## The thing that actually bites at 16TB

Not the disk. **The upload.**

A first full off-site backup of 16TB over a residential connection:

| Upload speed | Time |
|---|---|
| 20 Mbps | ~74 days |
| 50 Mbps | ~30 days |
| 500 Mbps fibre | ~3 days |

And 16TB on Backblaze is **$111/month**.

So above roughly 4TB, cloud off-site stops being practical on a home
connection — on time, before price.

### Seed locally, then relocate

The technique that solves it:

1. Plug the off-site drive into the vault box **directly over USB**.
2. Run the first `backup.sh` against it at local speed — 16TB in hours, not months.
3. Unplug it, physically take it to a relative's house, plug it into a Pi there.
4. Point `RESTIC_REPOSITORY` at it over Tailscale. From then on only nightly
   **incrementals** cross the wire — megabytes, not terabytes.

Cost, one time:

| | |
|---|---|
| Raspberry Pi 5 | $120 |
| 16TB HDD | $250 |
| Powered enclosure | $35 |
| **Total** | **~$405** |

Against $111/month for the same capacity on Backblaze, it pays for itself in
under four months, and it is the only version that is even physically possible
on a slow uplink.

Still encrypted before it leaves the house — the drive at the other end holds
ciphertext, exactly like Backblaze. The honest trade-off is that it is one
drive with nobody watching it, so `restore-test.sh` matters more, not less.

**Best of both at scale:** Backblaze for the irreplaceable core — photos and
documents, small enough to be cheap and professionally replicated — and the
relocated drive for the bulk. Set `BACKUP_IPHONE_OFFSITE=0` to keep the heavy
device backups out of the cloud bill.

---

## Optional: thumbnails on the SSD

With media on a hard drive, Immich's thumbnails live there too, and scrolling
the timeline pulls thousands of small files — the one place the hard drive is
noticeable.

To move just those to the SSD, add to
`/srv/vault/stack/immich/docker-compose.override.yml`:

```yaml
services:
  immich-server:
    volumes:
      - /srv/vault/immich/thumbs:/data/thumbs
```

Create the directory first, then re-run `02-deploy.sh`. Thumbnails are
regenerable and excluded from backups, so there is no risk in moving them.
Skip this unless browsing actually feels slow.
