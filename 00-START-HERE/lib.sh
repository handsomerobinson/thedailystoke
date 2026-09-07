#!/usr/bin/env bash
# Shared helpers for all 10-4 vault scripts. Sourced, never run directly.

VAULT_ENV="${VAULT_ENV:-/srv/vault/vault.env}"

c_red=$'\033[0;31m'; c_grn=$'\033[0;32m'; c_ylw=$'\033[0;33m'
c_blu=$'\033[0;34m'; c_bld=$'\033[1m';   c_off=$'\033[0m'

say()  { printf '%s\n' "$*"; }
step() { printf '\n%s==>%s %s%s%s\n' "$c_blu" "$c_off" "$c_bld" "$*" "$c_off"; }
ok()   { printf '  %s✓%s %s\n' "$c_grn" "$c_off" "$*"; }
warn() { printf '  %s!%s %s\n' "$c_ylw" "$c_off" "$*"; }
die()  { printf '\n%sFAILED:%s %s\n\n' "$c_red" "$c_off" "$*" >&2; exit 1; }

need_root() { [ "$(id -u)" -eq 0 ] || die "Run this with sudo."; }

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || die "'$1' is not installed. Run 01-provision.sh first."
}

# Load vault.env and fail loudly on anything missing, rather than letting a
# blank variable turn into a path like "/nextcloud" or an unencrypted backup.
load_env() {
  [ -f "$VAULT_ENV" ] || die "No config at $VAULT_ENV — copy stack/vault.env.example there and fill it in."

  local perms; perms=$(stat -c '%a' "$VAULT_ENV")
  [ "$perms" = "600" ] || warn "$VAULT_ENV is mode $perms; it holds your only encryption key. Run: chmod 600 $VAULT_ENV"

  set -a; . "$VAULT_ENV"; set +a

  local required=(VAULT_NAME VAULT_ROOT TZ TAILNET_DOMAIN TS_HOSTNAME
                  DB_PASSWORD NC_DB_PASSWORD NC_ADMIN_USER NC_ADMIN_PASSWORD
                  RESTIC_REPOSITORY RESTIC_PASSWORD)

  # Backblaze credentials are only needed for a b2: repository. An off-site
  # copy can just as well be a second box at a relative's house over Tailscale
  # (sftp:), which costs nothing per month. See docs/COSTS.md.
  case "${RESTIC_REPOSITORY:-}" in
    b2:*) required+=(B2_ACCOUNT_ID B2_ACCOUNT_KEY) ;;
  esac

  local missing=()
  for v in "${required[@]}"; do
    [ -n "${!v:-}" ] || missing+=("$v")
  done
  [ ${#missing[@]} -eq 0 ] || die "vault.env is missing values for: ${missing[*]}"

  # Immich builds its database URL by string concatenation; a special character
  # here produces a connection error that looks nothing like its actual cause.
  [[ "$DB_PASSWORD" =~ ^[A-Za-z0-9]+$ ]] || \
    die "DB_PASSWORD must be letters and digits only (Immich requirement). Regenerate: openssl rand -hex 24"

  export RESTIC_REPOSITORY RESTIC_PASSWORD
  [ -n "${B2_ACCOUNT_ID:-}" ]  && export B2_ACCOUNT_ID
  [ -n "${B2_ACCOUNT_KEY:-}" ] && export B2_ACCOUNT_KEY
  return 0
}

# Paths, derived once so no script invents its own layout.
#
# Storage is two tiers, because at scale they want different hardware:
#
#   VAULT_ROOT   FAST  — databases, dumps, config. Small (under ~200GB even
#                        for a huge library) but every page of random IO the
#                        system does lands here. Wants an SSD.
#   VAULT_MEDIA  BULK  — originals, device backups. Enormous, but read
#                        sequentially, so a hard drive is indistinguishable
#                        in use and roughly a tenth the price per TB.
#
# Leave VAULT_MEDIA unset and both collapse onto one disk. That is correct for
# anything under a few TB. See docs/STORAGE.md.
set_paths() {
  MEDIA_ROOT="${VAULT_MEDIA:-$VAULT_ROOT}"

  # --- fast tier ---
  IMMICH_PGDATA="$VAULT_ROOT/immich/postgres"
  NC_HTML="$VAULT_ROOT/nextcloud/html"
  NC_PGDATA="$VAULT_ROOT/nextcloud/postgres"
  DUMPS_DIR="$VAULT_ROOT/dumps"
  STACK_DIR="$VAULT_ROOT/stack"

  # --- bulk tier ---
  IMMICH_LIBRARY="$MEDIA_ROOT/immich/library"
  NC_DATA="$MEDIA_ROOT/nextcloud/data"
  IPHONE_DIR="$MEDIA_ROOT/iphone"
  SCRATCH_DIR="$MEDIA_ROOT/restore-test"

  VAULT_URL="https://${TS_HOSTNAME}.${TAILNET_DOMAIN}"
  NC_URL="https://${TS_HOSTNAME}.${TAILNET_DOMAIN}:${NEXTCLOUD_HTTPS_PORT:-8443}"
}
