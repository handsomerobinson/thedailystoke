#!/usr/bin/env bash
# =============================================================================
#  04 — IPHONE PULL   Full encrypted device backup, straight into the vault.
# =============================================================================
#  Photos leave the phone continuously through the Immich app. This is for
#  everything else — the parts iOS will not let any app reach:
#
#      Messages and attachments      Notes            Voice memos
#      Call history                  Health data      Safari history
#      App data                      Contacts         Calendars
#
#  This is the "replica of the phone inside the vault" piece. It is also the
#  raw material the cocoon indexes later (see docs/COCOON.md).
#
#  The backup MUST be encrypted. Apple only includes Health, Keychain and
#  saved passwords in an encrypted backup — an unencrypted one silently omits
#  them, and you would not notice until you needed them.
#
#  Requires: iPhone connected by USB cable, unlocked, "Trust This Computer"
#            accepted. Takes 20 minutes to several hours the first time.
#
#  Usage:  sudo ./04-iphone-pull.sh
# =============================================================================
set -euo pipefail
cd "$(dirname "$0")"
. ./lib.sh

load_env
set_paths
need_cmd idevicebackup2

step "Looking for a connected iPhone"
UDID=$(idevice_id -l 2>/dev/null | head -1 || true)
if [ -z "$UDID" ]; then
  die "No device found.
       - Is the cable plugged in? (a charge-only cable will not work)
       - Is the phone unlocked?
       - Did you tap 'Trust' on the phone?
       - Try: sudo systemctl restart usbmuxd"
fi
NAME=$(ideviceinfo -u "$UDID" -k DeviceName 2>/dev/null || echo "iPhone")
IOS=$(ideviceinfo -u "$UDID" -k ProductVersion 2>/dev/null || echo "unknown")
ok "Found: $NAME (iOS $IOS)"
say "    UDID: $UDID"

step "Pairing"
if ! idevicepair -u "$UDID" validate >/dev/null 2>&1; then
  say "    Unlock the phone and tap 'Trust' when it asks."
  idevicepair -u "$UDID" pair || die "Pairing failed.
       If this says the device is unsupported, your libimobiledevice is older
       than this iOS release. See docs/RUNBOOK.md > iPhone pull fails."
fi
ok "paired"

DEST="$IPHONE_DIR/$UDID"
mkdir -p "$DEST"

step "Checking backup encryption"
# The passphrase is intentionally the same one that protects the off-site
# repository: one secret for the client to keep, not two. It never leaves
# this machine, and restic encrypts the resulting backup again on the way out.
if idevicebackup2 -u "$UDID" -i encryption 2>/dev/null | grep -qi 'backup encryption.*: *1\|enabled'; then
  ok "encryption already enabled on this device"
else
  warn "Enabling backup encryption on the device."
  warn "The phone will prompt for its passcode."
  if idevicebackup2 -u "$UDID" encryption on "$RESTIC_PASSWORD" "$DEST" 2>&1 | tail -3; then
    ok "encryption enabled"
    say ""
    say "    NOTE: this passphrase is now also the phone's backup password."
    say "    It is the same one already written on paper. Do not change it in"
    say "    iOS settings, or future pulls will fail to decrypt."
  else
    warn "Could not enable encryption automatically."
    warn "Set it by hand: Settings > General > Transfer or Reset iPhone >"
    warn "  ...or via Finder on a Mac: 'Encrypt local backup'."
    die  "Refusing to take an unencrypted backup — it would silently omit Health and Keychain."
  fi
fi

step "Backing up $NAME"
say  "    Destination: $DEST"
say  "    Leave the phone connected and unlocked. This can take hours the first"
say  "    time; later runs are incremental and much faster."
say ""
START=$(date +%s)
idevicebackup2 -u "$UDID" backup --full "$DEST" || die "Backup failed. See docs/RUNBOOK.md > iPhone pull fails."
ELAPSED=$(( $(date +%s) - START ))
ok "backup finished in $((ELAPSED/60))m $((ELAPSED%60))s"

step "Verifying what came off the phone"
if idevicebackup2 -u "$UDID" info "$DEST" >/dev/null 2>&1; then
  ok "backup manifest is readable"
else
  warn "could not read the manifest back — inspect $DEST by hand"
fi
SIZE=$(du -sh "$DEST" 2>/dev/null | cut -f1)
FILES=$(find "$DEST" -type f 2>/dev/null | wc -l)
ok "$SIZE across $FILES files"

# Record what was pulled and when — this is the client-facing evidence that
# the phone's contents are genuinely in the vault.
cat > "$DEST/PULL-LOG.txt" <<EOF
Device      : $NAME
iOS         : $IOS
UDID        : $UDID
Pulled      : $(date '+%Y-%m-%d %H:%M:%S %Z')
Size        : $SIZE ($FILES files)
Encrypted   : yes (passphrase = the vault restic passphrase)
Vault       : $VAULT_NAME
EOF
ok "wrote $DEST/PULL-LOG.txt"

cat <<NEXT

-----------------------------------------------------------------------------
 PHONE PULLED
-----------------------------------------------------------------------------

 This lands in the next nightly off-site backup automatically. To push it
 off-site right now instead:

     sudo ./backup.sh

 Repeat this pull monthly, or before any phone reset or upgrade.

 IMPORTANT — this backup is now in the vault, but it is still ON THE PHONE
 too. Nothing has been deleted. Read docs/WHAT-IS-POSSIBLE.md before you
 clear anything off the device, and never delete until restore-test.sh has
 passed at least once.
-----------------------------------------------------------------------------
NEXT
