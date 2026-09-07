# Runbook

## Monthly, per vault

1. `sudo ./restore-test.sh` — must pass. Record the date.
2. `sudo ./04-iphone-pull.sh` — phone on a cable.
3. Immich app → "free up space" to clear local copies already in the vault.
4. `sudo ./03-verify.sh` — check disk headroom.

If a restore test fails, the vault is **not** protected. Fix it before anything else.

---

## Updating

```bash
sudo ./02-deploy.sh          # pulls patch updates, restarts, keeps data
```

Every image is pinned to a major version, so this collects security fixes but
never jumps a major. **Major upgrades are deliberate:**

- **Immich** — change `IMMICH_VERSION` in `vault.env`. Read their release notes
  first; majors sometimes need a migration. Take a backup before.
- **Nextcloud** — edit the tag in `stack/nextcloud/docker-compose.yml`. It
  **cannot skip a major**: 32 → 33 → 34, one at a time, letting each finish.
- **Postgres** — do not change the major casually. A new major will not read
  the old data directory and the container will refuse to start. Requires a
  dump, wipe, and reload.

---

## Problems

### Cannot reach the vault from the phone

```bash
tailscale status              # is the phone on the tailnet?
tailscale serve status        # is anything published?
sudo ./03-verify.sh
```
Most often the phone dropped off Tailscale. Open the Tailscale app on it.
Certificates take up to a minute on first issue.

### Nextcloud stuck in maintenance mode

A backup died mid-run. `backup.sh` traps this, but if it was killed hard:

```bash
docker exec -u www-data nextcloud_app php occ maintenance:mode --off
```

### Nextcloud says "access through untrusted domain"

`TS_HOSTNAME` or `TAILNET_DOMAIN` in `vault.env` does not match reality.
Check `tailscale status --self`, fix `vault.env`, re-run `02-deploy.sh`.

### iPhone pull fails

- *No device found* — charge-only cable, locked phone, or Trust not accepted.
  `sudo systemctl restart usbmuxd`, replug, unlock, tap Trust.
- *Unsupported device / pairing fails* — the distro's libimobiledevice is older
  than the iOS release. This is the most common cause on a new iPhone.
  Build current from source:
  ```bash
  sudo apt install -y build-essential checkinstall git autoconf automake \
       libtool-bin libssl-dev libusb-1.0-0-dev libplist-dev
  for r in libplist libimobiledevice-glue libusbmuxd libimobiledevice; do
    git clone https://github.com/libimobiledevice/$r
    (cd $r && ./autogen.sh && make && sudo make install)
  done
  sudo ldconfig && sudo systemctl restart usbmuxd
  ```
- *Backup password rejected* — someone changed the encrypted-backup password in
  iOS settings. It must match `RESTIC_PASSWORD`.

### Backup fails: repository is locked

A previous run was killed. Confirm nothing is running, then:
```bash
sudo restic unlock
```

### `restic check` reports damage

Do not panic and do not delete anything.
```bash
sudo restic check --read-data          # full verification, slow
sudo restic repair index
sudo restic repair snapshots --forget  # drops only unrecoverable snapshots
```
The live data on the box is untouched by any of this. Once repaired, run
`backup.sh` to write a fresh good snapshot, then `restore-test.sh`.

### Disk full

```bash
du -sh /srv/vault/*
sudo rm -rf /srv/vault/restore-test          # scratch from restore tests
docker system prune -a                        # old images
```
Immich's `thumbs/` and `encoded-video/` are regenerable and excluded from
backups; they can be deleted and Immich will rebuild them.

### Immich database will not start

Almost always a Postgres major version change, or a torn data directory.
Restore from the dump:
```bash
zcat /srv/vault/dumps/immich.sql.gz | docker exec -i immich_postgres psql -U postgres
```

---

## Full rebuild from Backblaze

The scenario the whole system exists for: the box is gone.

1. New machine, Ubuntu Server, clone this repo.
2. `sudo ./01-provision.sh`, `sudo tailscale up --ssh`.
3. Recreate `/srv/vault/vault.env` — **the restic passphrase from paper.**
4. Pull everything back:
   ```bash
   sudo restic restore latest --target /
   ```
5. `sudo ./02-deploy.sh`
6. Load the databases:
   ```bash
   zcat /srv/vault/dumps/immich.sql.gz    | docker exec -i immich_postgres psql -U postgres
   zcat /srv/vault/dumps/nextcloud.sql.gz | docker exec -i nextcloud_db psql -U nextcloud nextcloud
   docker restart immich_server nextcloud_app
   ```
7. `sudo ./03-verify.sh`

Without the passphrase, none of this is possible. That is the design.
