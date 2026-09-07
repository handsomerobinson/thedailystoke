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

  local missing=()
  for v in VAULT_NAME VAULT_ROOT TZ TAILNET_DOMAIN TS_HOSTNAME \
           DB_PASSWORD NC_DB_PASSWORD NC_ADMIN_USER NC_ADMIN_PASSWORD \
           B2_ACCOUNT_ID B2_ACCOUNT_KEY RESTIC_REPOSITORY RESTIC_PASSWORD; do
    [ -n "${!v:-}" ] || missing+=("$v")
  done
  [ ${#missing[@]} -eq 0 ] || die "vault.env is missing values for: ${missing[*]}"

  # Immich builds its database URL by string concatenation; a special character
  # here produces a connection error that looks nothing like its actual cause.
  [[ "$DB_PASSWORD" =~ ^[A-Za-z0-9]+$ ]] || \
    die "DB_PASSWORD must be letters and digits only (Immich requirement). Regenerate: openssl rand -hex 24"

  export B2_ACCOUNT_ID B2_ACCOUNT_KEY RESTIC_REPOSITORY RESTIC_PASSWORD
}

# Paths, derived once so no script invents its own layout.
set_paths() {
  IMMICH_DIR="$VAULT_ROOT/immich"
  IMMICH_LIBRARY="$IMMICH_DIR/library"
  IMMICH_PGDATA="$IMMICH_DIR/postgres"
  NC_DIR="$VAULT_ROOT/nextcloud"
  IPHONE_DIR="$VAULT_ROOT/iphone"
  DUMPS_DIR="$VAULT_ROOT/dumps"
  STACK_DIR="$VAULT_ROOT/stack"
  SCRATCH_DIR="$VAULT_ROOT/restore-test"
  VAULT_URL="https://${TS_HOSTNAME}.${TAILNET_DOMAIN}"
  NC_URL="https://${TS_HOSTNAME}.${TAILNET_DOMAIN}:${NEXTCLOUD_HTTPS_PORT:-8443}"
}
