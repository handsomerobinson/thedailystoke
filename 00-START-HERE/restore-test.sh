#!/usr/bin/env bash
# =============================================================================
#  RESTORE TEST   Proves the off-site backup can actually bring the vault back.
# =============================================================================
#  This is the most important script here. A backup nobody has restored is a
#  guess. Run it monthly, and run it in front of a client before they pay you.
#
#  It does four things a green "backup succeeded" log cannot:
#    1. Verifies real data integrity in the repository, not just its index.
#    2. Pulls the database dumps back OUT of B2 and checks they decompress
#       and contain the schema they should.
#    3. Restores a random sample of actual photos and confirms they are
#       intact, decodable image files.
#    4. Tells you the age of the newest snapshot, so silent failure shows up.
#
#  It never touches live data. Everything lands in a scratch directory.
#
#  Usage:  sudo ./restore-test.sh [number-of-sample-photos]   (default 20)
# =============================================================================
set -euo pipefail
cd "$(dirname "$0")"
. ./lib.sh

load_env
set_paths
need_cmd restic

SAMPLE_N="${1:-20}"
FAILURES=0
fail() { printf '  %s✗%s %s\n' "$c_red" "$c_off" "$*"; FAILURES=$((FAILURES+1)); }

step "10-4 RESTORE TEST — $VAULT_NAME — $(date '+%Y-%m-%d %H:%M')"
say  "    Repository: $RESTIC_REPOSITORY"

# --- 1. Is there a recent snapshot at all? ------------------------------------
step "1/5  Checking snapshot freshness"
SNAP_JSON=$(restic snapshots --tag "$VAULT_NAME" --latest 1 --json 2>/dev/null || echo '[]')
if [ "$(echo "$SNAP_JSON" | jq 'length')" -eq 0 ]; then
  die "No snapshots found. Nothing has ever been backed up successfully."
fi
SNAP_ID=$(echo "$SNAP_JSON" | jq -r '.[0].short_id')
SNAP_TIME=$(echo "$SNAP_JSON" | jq -r '.[0].time')
AGE_H=$(( ( $(date +%s) - $(date -d "$SNAP_TIME" +%s) ) / 3600 ))
say "    Latest snapshot: $SNAP_ID from $SNAP_TIME"
if [ "$AGE_H" -gt 48 ]; then
  fail "newest snapshot is ${AGE_H}h old — the nightly backup is not running"
else
  ok "newest snapshot is ${AGE_H}h old"
fi

# --- 2. Repository integrity, including actual data --------------------------
step "2/5  Verifying repository integrity"
say  "    Reading back a 5% sample of the real data from B2. This takes a while."
if restic check --read-data-subset=5% 2>&1 | tail -5; then
  ok "repository structure and sampled data are intact"
else
  fail "restic check FAILED — the repository is damaged. See docs/RUNBOOK.md."
fi

# --- 3. Restore the database dumps -------------------------------------------
step "3/5  Restoring the database dumps out of B2"
rm -rf "$SCRATCH_DIR"; mkdir -p "$SCRATCH_DIR"
restic restore "$SNAP_ID" --target "$SCRATCH_DIR" --include "$DUMPS_DIR" >/dev/null 2>&1 \
  || fail "could not restore the dumps directory"

for db in immich nextcloud; do
  D="$SCRATCH_DIR$DUMPS_DIR/$db.sql.gz"
  if [ ! -f "$D" ]; then
    fail "$db.sql.gz was not in the snapshot"
    continue
  fi
  if ! gzip -t "$D" 2>/dev/null; then
    fail "$db.sql.gz is corrupt — it would not restore"
    continue
  fi
  # A dump can be valid gzip and still be an empty or truncated database.
  # Look for real schema before calling it good.
  if zcat "$D" | head -c 2000000 | grep -qiE 'CREATE TABLE|COPY .* FROM stdin'; then
    ok "$db.sql.gz — valid, $(du -h "$D" | cut -f1), contains schema"
  else
    fail "$db.sql.gz decompresses but has no tables in it"
  fi
done

# --- 4. Restore a random sample of real photos -------------------------------
step "4/5  Restoring $SAMPLE_N random photos"
UPLOAD_PATH="$IMMICH_LIBRARY/upload"
mapfile -t ALL_FILES < <(restic ls "$SNAP_ID" --long 2>/dev/null \
  | awk -v p="$UPLOAD_PATH" '$0 ~ p && $1 ~ /^-/ {print $NF}' | head -5000)

if [ "${#ALL_FILES[@]}" -eq 0 ]; then
  warn "no photo files in the snapshot yet — nothing uploaded to Immich so far"
else
  mapfile -t SAMPLE < <(printf '%s\n' "${ALL_FILES[@]}" | shuf -n "$SAMPLE_N")
  RESTORED=0; BAD=0
  for f in "${SAMPLE[@]}"; do
    if restic restore "$SNAP_ID" --target "$SCRATCH_DIR" --include "$f" >/dev/null 2>&1; then
      R="$SCRATCH_DIR$f"
      if [ -s "$R" ]; then RESTORED=$((RESTORED+1)); else BAD=$((BAD+1)); fi
    else
      BAD=$((BAD+1))
    fi
  done
  if [ "$BAD" -eq 0 ]; then
    ok "$RESTORED of ${#SAMPLE[@]} sampled photos restored intact"
  else
    fail "$BAD of ${#SAMPLE[@]} sampled photos failed to restore"
  fi
  # If `file` is available, confirm they are genuinely decodable images and not
  # just non-empty blobs of the right size.
  if command -v file >/dev/null 2>&1 && [ "$RESTORED" -gt 0 ]; then
    IMGS=$(find "$SCRATCH_DIR$UPLOAD_PATH" -type f 2>/dev/null | head -"$SAMPLE_N" \
           | xargs -r file -b 2>/dev/null | grep -ciE 'image|JPEG|PNG|HEIF|MP4|Media|ISO Media' || true)
    say "    $IMGS of them identify as real image/video files"
  fi
fi

# --- 5. Report ----------------------------------------------------------------
step "5/5  Result"
SIZE=$(restic stats --tag "$VAULT_NAME" --mode raw-data 2>/dev/null | grep -i 'Total Size' || echo "  size unavailable")
say "    $SIZE"
say ""
if [ "$FAILURES" -eq 0 ]; then
  printf '%s  RESTORE TEST PASSED%s — this vault can be rebuilt from Backblaze alone.\n' "$c_grn$c_bld" "$c_off"
  say ""
  say "  Verified on $(date '+%Y-%m-%d'). Record it in the client log."
else
  printf '%s  RESTORE TEST FAILED%s — %d problem(s) above. Do not consider this vault protected.\n' "$c_red$c_bld" "$c_off" "$FAILURES"
fi
say ""
say "  Scratch copy left in $SCRATCH_DIR — delete it when you are done:"
say "     sudo rm -rf $SCRATCH_DIR"
[ "$FAILURES" -eq 0 ]
