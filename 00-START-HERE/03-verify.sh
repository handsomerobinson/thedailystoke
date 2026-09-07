#!/usr/bin/env bash
# =============================================================================
#  03 — VERIFY   Confirms the vault is actually working and actually private.
# =============================================================================
#  Run after deploying, after any change, and before handing a vault to a
#  client. Checks health AND exposure — a working vault that is reachable from
#  the open internet is a failure, not a success.
#
#  Usage:  sudo ./03-verify.sh
# =============================================================================
set -euo pipefail
cd "$(dirname "$0")"
. ./lib.sh

load_env
set_paths
FAILURES=0
fail() { printf '  %s✗%s %s\n' "$c_red" "$c_off" "$*"; FAILURES=$((FAILURES+1)); }

step "10-4 vault verification — $VAULT_NAME"

step "Containers"
for c in immich_server immich_machine_learning immich_postgres immich_redis \
         nextcloud_app nextcloud_db nextcloud_redis nextcloud_cron; do
  if docker ps --format '{{.Names}}' | grep -qx "$c"; then
    STATE=$(docker inspect -f '{{.State.Health.Status}}' "$c" 2>/dev/null || echo "no-healthcheck")
    case "$STATE" in
      healthy|no-healthcheck|"<no value>") ok "$c running" ;;
      starting) warn "$c still starting" ;;
      *) fail "$c is $STATE" ;;
    esac
  else
    fail "$c is NOT running"
  fi
done

step "Application endpoints"
if curl -fsS --max-time 10 http://127.0.0.1:2283/api/server/ping >/dev/null 2>&1; then
  ok "Immich API responding"
else
  fail "Immich API not responding on 127.0.0.1:2283"
fi
NC_CODE=$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 http://127.0.0.1:11000/status.php || echo 000)
if [ "$NC_CODE" = "200" ]; then
  ok "Nextcloud responding"
else
  fail "Nextcloud returned HTTP $NC_CODE on 127.0.0.1:11000"
fi

step "Privacy — nothing may be exposed beyond the tailnet"
# The whole security model is "Tailscale is the only door". Verify it rather
# than trusting it: a stray published port here means a client's entire photo
# library is one port scan away.
EXPOSED=$(ss -tlnp 2>/dev/null | awk '{print $4}' \
  | grep -E '^(0\.0\.0\.0|\[::\]|\*):(2283|11000)$' || true)
if [ -z "$EXPOSED" ]; then
  ok "Immich and Nextcloud are bound to loopback only"
else
  fail "PUBLICLY BOUND: $EXPOSED — the override file is not being applied"
fi

if tailscale serve status 2>/dev/null | grep -q .; then
  ok "tailscale serve is publishing:"
  tailscale serve status 2>/dev/null | sed 's/^/      /'
else
  fail "tailscale serve is not configured — re-run 02-deploy.sh"
fi

# `serve` is tailnet-only; `funnel` is the public internet. Confirm no funnel.
if tailscale funnel status 2>/dev/null | grep -qiE 'https://|proxy'; then
  fail "TAILSCALE FUNNEL IS ON — this vault is exposed to the public internet. Turn it off: tailscale funnel reset"
else
  ok "Tailscale Funnel is off (not publicly exposed)"
fi

if ufw status 2>/dev/null | grep -q "Status: active"; then
  ok "firewall active"
else
  fail "ufw is not active"
fi

step "Storage"
check_disk() {  # check_disk <path> <label>
  [ -d "$1" ] || return 0
  local use avail
  use=$(df -h "$1" | awk 'NR==2{print $5}' | tr -d '%')
  avail=$(df -h "$1" | awk 'NR==2{print $4}')
  if   [ "$use" -ge 90 ]; then fail "$2 $1 is ${use}% full — only $avail left"
  elif [ "$use" -ge 75 ]; then warn "$2 $1 is ${use}% full ($avail free) — plan more storage"
  else                         ok   "$2 $1 is ${use}% full ($avail free)"
  fi
}
check_disk "$VAULT_ROOT" "fast tier —"
if [ "$MEDIA_ROOT" != "$VAULT_ROOT" ]; then
  check_disk "$MEDIA_ROOT" "bulk tier —"
else
  mountpoint -q "$VAULT_ROOT" 2>/dev/null || warn "vault is on the OS disk, not a dedicated data disk"
fi

step "Off-site backup"
if systemctl is-enabled ten4-backup.timer >/dev/null 2>&1; then
  ok "nightly timer enabled — next run $(systemctl show ten4-backup.timer -p NextElapseUSecRealtime --value 2>/dev/null | cut -c1-25)"
else
  fail "ten4-backup.timer is not enabled"
fi
if restic snapshots --tag "$VAULT_NAME" --latest 1 >/dev/null 2>&1; then
  LAST=$(restic snapshots --tag "$VAULT_NAME" --latest 1 --json 2>/dev/null | jq -r '.[0].time // empty')
  if [ -n "$LAST" ]; then
    AGE_H=$(( ( $(date +%s) - $(date -d "$LAST" +%s) ) / 3600 ))
    [ "$AGE_H" -le 48 ] && ok "last off-site snapshot ${AGE_H}h ago" || fail "last snapshot was ${AGE_H}h ago"
  fi
else
  warn "no snapshots yet — run ./backup.sh once by hand"
fi

step "Result"
if [ "$FAILURES" -eq 0 ]; then
  printf '%s  ALL CHECKS PASSED%s\n\n' "$c_grn$c_bld" "$c_off"
  say "    Photos: $VAULT_URL"
  say "    Files:  $NC_URL"
  say ""
  say "  Health is not the same as recoverable. Run ./restore-test.sh next."
else
  printf '%s  %d CHECK(S) FAILED%s — see docs/RUNBOOK.md\n' "$c_red$c_bld" "$FAILURES" "$c_off"
fi
say ""
[ "$FAILURES" -eq 0 ]
