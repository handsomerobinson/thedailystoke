#!/usr/bin/env bash
# =============================================================================
#  BACKUP   Encrypted off-site snapshot of the whole vault -> Backblaze B2.
# =============================================================================
#  Runs nightly via ten4-backup.timer. Also safe to run by hand at any time.
#
#  Order matters here:
#    1. Dump both databases to plain files FIRST. You cannot back up a running
#       Postgres data directory by copying it — you get a torn snapshot that
#       restores into a corrupt database, and you find out on the worst day.
#    2. Then restic the dumps alongside the media.
#
#  restic encrypts on this machine before anything leaves it. Backblaze stores
#  ciphertext and cannot read a byte of it.
#
#  Usage:  sudo ./backup.sh
# =============================================================================
set -euo pipefail
cd "$(dirname "$0")"
. ./lib.sh

load_env
set_paths
need_cmd restic
need_cmd docker

# Never let a manual run collide with the nightly timer — two restic processes
# against one repository is how you get a lock nobody can explain later.
exec 9>/var/lock/ten4-backup.lock
flock -n 9 || die "Another backup is already running."

START=$(date +%s)
step "10-4 vault backup — $VAULT_NAME — $(date '+%Y-%m-%d %H:%M:%S')"

mkdir -p "$DUMPS_DIR"; chmod 700 "$DUMPS_DIR"

# --- Nextcloud maintenance mode -----------------------------------------------
# Read-only for the ~30 seconds of the dump, so the database and the files on
# disk agree with each other. The trap is not optional: without it, a failed
# dump leaves the client's Nextcloud stuck offline until someone notices.
NC_MAINT_ON=0
cleanup() {
  if [ "$NC_MAINT_ON" = "1" ]; then
    docker exec -u www-data nextcloud_app php occ maintenance:mode --off >/dev/null 2>&1 \
      && ok "Nextcloud maintenance mode off" \
      || warn "COULD NOT LEAVE MAINTENANCE MODE. Run: docker exec -u www-data nextcloud_app php occ maintenance:mode --off"
  fi
}
trap cleanup EXIT

# --- Immich database ----------------------------------------------------------
step "Dumping the Immich database"
if docker ps --format '{{.Names}}' | grep -qx immich_postgres; then
  # pg_dumpall per Immich's documented backup procedure:
  # https://docs.immich.app/administration/backup-and-restore
  # NOTE: deliberately no -t. Allocating a pty here makes Docker translate
  # LF into CRLF inside the dump, producing a file that gunzips fine and then
  # fails to import with a syntax error thousands of lines in.
  docker exec immich_postgres pg_dumpall --clean --if-exists --username=postgres \
    | gzip > "$DUMPS_DIR/immich.sql.gz.tmp"
  # Only replace the good dump once the new one is complete, so an interrupted
  # run never leaves a truncated file as the thing you restore from.
  gzip -t "$DUMPS_DIR/immich.sql.gz.tmp" || die "Immich dump failed its integrity check — keeping the previous dump."
  mv "$DUMPS_DIR/immich.sql.gz.tmp" "$DUMPS_DIR/immich.sql.gz"
  ok "immich.sql.gz ($(du -h "$DUMPS_DIR/immich.sql.gz" | cut -f1))"
else
  warn "immich_postgres is not running — skipping its dump"
fi

# --- Nextcloud database -------------------------------------------------------
step "Dumping the Nextcloud database"
if docker ps --format '{{.Names}}' | grep -qx nextcloud_db; then
  if docker exec -u www-data nextcloud_app php occ maintenance:mode --on >/dev/null 2>&1; then
    NC_MAINT_ON=1
    ok "Nextcloud in maintenance mode"
  else
    warn "Could not enter maintenance mode — dumping live (slightly less consistent)"
  fi
  docker exec nextcloud_db pg_dump --clean --if-exists -U nextcloud nextcloud \
    | gzip > "$DUMPS_DIR/nextcloud.sql.gz.tmp"
  gzip -t "$DUMPS_DIR/nextcloud.sql.gz.tmp" || die "Nextcloud dump failed its integrity check — keeping the previous dump."
  mv "$DUMPS_DIR/nextcloud.sql.gz.tmp" "$DUMPS_DIR/nextcloud.sql.gz"
  ok "nextcloud.sql.gz ($(du -h "$DUMPS_DIR/nextcloud.sql.gz" | cut -f1))"
  cleanup; NC_MAINT_ON=0
else
  warn "nextcloud_db is not running — skipping its dump"
fi

# --- Repository ---------------------------------------------------------------
step "Opening the restic repository"
if ! restic snapshots >/dev/null 2>&1; then
  warn "No repository found at $RESTIC_REPOSITORY — initialising a new one."
  restic init
  ok "repository created"
else
  ok "repository reachable"
fi

# --- Snapshot -----------------------------------------------------------------
step "Backing up"
# thumbs/ and encoded-video/ are excluded on purpose: Immich regenerates both
# from the originals, and together they are often a third of the library. There
# is no reason to pay to store, upload, and encrypt derivatives every night.
# backups/ is Immich's own dump directory — we make our own above.
# Optionally keep the bulky device backups on local disk only. See docs/COSTS.md.
IPHONE_PATHS=("$IPHONE_DIR")
if [ "${BACKUP_IPHONE_OFFSITE:-1}" != "1" ]; then
  IPHONE_PATHS=()
  warn "BACKUP_IPHONE_OFFSITE=0 — device backups stay on this machine only"
fi

restic backup \
  --tag "$VAULT_NAME" \
  --exclude "$IMMICH_LIBRARY/thumbs" \
  --exclude "$IMMICH_LIBRARY/encoded-video" \
  --exclude "$IMMICH_LIBRARY/backups" \
  --exclude "$IMMICH_PGDATA" \
  --exclude "$NC_PGDATA" \
  --exclude-caches \
  "$DUMPS_DIR" \
  "$IMMICH_LIBRARY" \
  "$NC_DATA" \
  "$NC_HTML" \
  ${IPHONE_PATHS[@]+"${IPHONE_PATHS[@]}"} \
  "$VAULT_ENV"
# vault.env is included so a rebuild recovers the database and admin passwords.
# Its restic passphrase is of no use inside the repository it unlocks — that
# one only ever exists on paper.
ok "snapshot written"

# --- Retention ----------------------------------------------------------------
step "Applying retention policy"
restic forget \
  --tag "$VAULT_NAME" \
  --keep-daily   "${KEEP_DAILY:-7}" \
  --keep-weekly  "${KEEP_WEEKLY:-5}" \
  --keep-monthly "${KEEP_MONTHLY:-12}" \
  --keep-yearly  "${KEEP_YEARLY:-3}" \
  --prune
ok "old snapshots pruned"

ELAPSED=$(( $(date +%s) - START ))
step "Done in $((ELAPSED/60))m $((ELAPSED%60))s"
restic snapshots --tag "$VAULT_NAME" --latest 3
say ""
say "A backup that has never been restored is a rumour. Run ./restore-test.sh."
