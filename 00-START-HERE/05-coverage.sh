#!/usr/bin/env bash
# =============================================================================
#  05 — COVERAGE   Answers "is everything actually in the vault, and current?"
# =============================================================================
#  03-verify says the machine is healthy. restore-test says the backup works.
#  This one says whether your LIFE is actually flowing into it — how much is
#  in there, and how stale each source is.
#
#  Run it whenever you want to trust the thing.
#
#  Usage:  sudo ./05-coverage.sh
# =============================================================================
set -euo pipefail
cd "$(dirname "$0")"
. ./lib.sh

load_env
set_paths

age_days() { echo $(( ( $(date +%s) - $1 ) / 86400 )); }
stale() {  # stale <days> <warn-after> <label>
  if   [ "$1" -le "$2" ]; then ok   "$3 — ${1}d ago"
  else                         warn "$3 — ${1}d ago (getting stale)"; fi
}

step "10-4 COVERAGE — $VAULT_NAME — $(date '+%Y-%m-%d %H:%M')"

# --- Photos -------------------------------------------------------------------
step "Photos and video  [ automatic — Immich app ]"
if docker ps --format '{{.Names}}' | grep -qx immich_postgres; then
  # Table naming has changed across Immich majors, so discover it rather than
  # guessing and printing a confusing zero.
  TBL=$(docker exec immich_postgres psql -U postgres -d immich -tAc \
        "SELECT table_name FROM information_schema.tables
          WHERE table_schema='public' AND table_name IN ('assets','asset') LIMIT 1" 2>/dev/null || true)
  if [ -n "$TBL" ]; then
    COUNT=$(docker exec immich_postgres psql -U postgres -d immich -tAc \
            "SELECT count(*) FROM \"$TBL\"" 2>/dev/null || echo 0)
    NEWEST=$(docker exec immich_postgres psql -U postgres -d immich -tAc \
            "SELECT EXTRACT(EPOCH FROM max(\"createdAt\"))::bigint FROM \"$TBL\"" 2>/dev/null || echo 0)
    ok "$COUNT items in the vault"
    if [ "${NEWEST:-0}" -gt 0 ]; then
      stale "$(age_days "$NEWEST")" 3 "newest upload"
    fi
  else
    warn "could not read the Immich database — is it still starting?"
  fi
  say "    Size on disk: $(du -sh "$IMMICH_LIBRARY" 2>/dev/null | cut -f1)"
else
  warn "Immich is not running"
fi
say "    Check against the phone: Settings > General > iPhone Storage > Photos"

# --- Files --------------------------------------------------------------------
step "Files, contacts, calendars  [ automatic — Nextcloud app + iOS sync ]"
if [ -d "$NC_DATA" ]; then
  NF=$(find "$NC_DATA" -type f 2>/dev/null | wc -l)
  ok "$NF files ($(du -sh "$NC_DATA" 2>/dev/null | cut -f1))"
  NEWEST_F=$(find "$NC_DATA" -type f -printf '%T@\n' 2>/dev/null | sort -rn | head -1 | cut -d. -f1)
  [ -n "${NEWEST_F:-}" ] && stale "$(age_days "$NEWEST_F")" 7 "newest file"
else
  warn "no Nextcloud data directory yet"
fi

# --- Phone pull ---------------------------------------------------------------
step "Messages, Notes, voice memos, Health  [ MANUAL — needs the cable ]"
if [ -d "$IPHONE_DIR" ] && [ -n "$(ls -A "$IPHONE_DIR" 2>/dev/null)" ]; then
  for d in "$IPHONE_DIR"/*/; do
    [ -f "$d/PULL-LOG.txt" ] || continue
    PULLED=$(stat -c %Y "$d/PULL-LOG.txt")
    DEV=$(grep -m1 '^Device' "$d/PULL-LOG.txt" | cut -d: -f2- | xargs)
    D=$(age_days "$PULLED")
    if [ "$D" -le 35 ]; then ok "$DEV — pulled ${D}d ago ($(du -sh "$d" | cut -f1))"
    else warn "$DEV — pulled ${D}d ago. Run ./04-iphone-pull.sh"; fi
  done
else
  warn "NEVER PULLED. Messages, Notes, voice memos and Health are"
  warn "only on the phone right now. Run ./04-iphone-pull.sh"
fi

# --- Off-site -----------------------------------------------------------------
step "Off-site copy  [ automatic — nightly ]"
if restic snapshots --tag "$VAULT_NAME" --latest 1 >/dev/null 2>&1; then
  LAST=$(restic snapshots --tag "$VAULT_NAME" --latest 1 --json 2>/dev/null | jq -r '.[0].time // empty')
  if [ -n "$LAST" ]; then
    stale "$(age_days "$(date -d "$LAST" +%s)")" 2 "last snapshot"
  fi
  restic stats --tag "$VAULT_NAME" --mode raw-data 2>/dev/null | grep -i 'Total Size' | sed 's/^/    /' || true
  say "    (this figure x \$6.95/TB is roughly your Backblaze bill — see docs/COSTS.md)"
else
  warn "nothing backed up off-site yet — run ./backup.sh"
fi

# --- Known gaps ---------------------------------------------------------------
step "Known gaps"
say "    Apple Notes and Apple Voice Memos do not sync live — iOS allows no"
say "    app to reach them. They are captured only by the monthly cable pull."
say ""
say "    To close that gap permanently, move your capture habit:"
say "      Notes       -> Nextcloud Notes app  (syncs continuously)"
say "      Voice memos -> any recorder that saves into Files > Nextcloud"
say ""
say "    See docs/IPHONE.md."
say ""
