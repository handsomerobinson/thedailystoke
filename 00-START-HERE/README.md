# 10-4 Vault — start here

A private cloud on hardware you own. Photos, files, notes and a full iPhone
replica, encrypted on your machine and backed up off-site where nobody —
including Backblaze, including me — can read a word of it.

**Read [../docs/WHAT-IS-POSSIBLE.md](../docs/WHAT-IS-POSSIBLE.md) first.** It is
short, and it is the difference between selling something you can deliver and
selling something you cannot.

---

## Order of operations

```
sudo ./01-provision.sh     # installs docker, tailscale, restic, iphone tools
sudo tailscale up --ssh    # join the tailnet (by hand — needs your login)
                           # then fill in /srv/vault/vault.env
sudo ./02-deploy.sh        # brings up Immich + Nextcloud, publishes on tailnet
sudo ./03-verify.sh        # health AND exposure checks
sudo ./backup.sh           # first off-site backup (long — it is the whole library)
sudo ./restore-test.sh     # PROVES it. do not skip. do not delete anything before this.
sudo ./04-iphone-pull.sh   # full encrypted device backup, phone on a cable
sudo ./05-coverage.sh      # is everything actually in there, and current?
```

Every script is safe to re-run.

---

## Doing this today

You need a machine that can stay on and run Linux. An old laptop or desktop is
fine to start — you can move to real hardware later, the install is identical.

1. Ubuntu Server 24.04 on the box, on the network, SSH working.
2. `01-provision.sh` → `tailscale up` → fill in `vault.env` → `02-deploy.sh`.
   Budget an hour, most of it downloads.
3. Set up the phone — [../docs/IPHONE.md](../docs/IPHONE.md). Three free apps,
   ten minutes. Watch your own photos land in your own vault.
4. `backup.sh`, then `restore-test.sh`.

**That is the demo.** Your own working cocoon, your own photos, restored in
front of someone from an encrypted off-site copy. It sells far harder than a
mockup, and you will know your real hours before you quote anyone.

---

## The files

| | |
|---|---|
| `lib.sh` | Shared helpers. Sourced by everything, run directly by nothing. |
| `01-provision.sh` | Docker, Tailscale, restic, libimobiledevice, firewall, directory layout. |
| `02-deploy.sh` | Starts the stack, publishes it on the tailnet, installs the nightly timer. |
| `03-verify.sh` | Is it healthy — and is it accidentally exposed to the internet? |
| `04-iphone-pull.sh` | Full encrypted iPhone backup into the vault. |
| `backup.sh` | Nightly. Dumps both databases, then encrypts and ships to B2. |
| `05-coverage.sh` | What is in the vault, how stale each source is, what is still only on the phone. |
| `restore-test.sh` | Pulls it back out and proves it. The one that matters. |

Configuration is one file: `/srv/vault/vault.env`, from
[`../stack/vault.env.example`](../stack/vault.env.example). One per deployment.

---

## The one warning

The restic passphrase in `vault.env` is the only key to the off-site backup.
Backblaze cannot reset it. You cannot reset it. Nobody can — that is precisely
why the data is safe there.

**Write it on paper. Put the paper somewhere physical. Do it before you run
the first backup, not after.**

---

## Where things live

```
/srv/vault/
├── vault.env              the only file you edit
├── immich/library/        photos and video (the originals)
├── immich/postgres/       Immich database
├── nextcloud/data/        files, notes, contacts, calendars
├── nextcloud/postgres/    Nextcloud database
├── iphone/<udid>/         full encrypted device backups
├── dumps/                 nightly database dumps (what actually gets backed up)
└── stack/                 generated compose files — do not hand-edit
```

## More

- [IPHONE.md](../docs/IPHONE.md) — the phone side: apps, what syncs, the monthly ritual.
- [COSTS.md](../docs/COSTS.md) — what it costs to build and run, versus iCloud.
- [WHAT-IS-POSSIBLE.md](../docs/WHAT-IS-POSSIBLE.md) — the boundaries. Read before selling.
- [HARDWARE.md](../docs/HARDWARE.md) — what to buy, and capacity math for multiple people.
- [MIGRATION.md](../docs/MIGRATION.md) — getting a life out of iCloud.
- [RUNBOOK.md](../docs/RUNBOOK.md) — when something breaks.
- [CLIENT-PLAYBOOK.md](../docs/CLIENT-PLAYBOOK.md) — doing this for money.
- [COCOON.md](../docs/COCOON.md) — phase 2: making it searchable.
