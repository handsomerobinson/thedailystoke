#!/usr/bin/env bash
# =============================================================================
#  01 — PROVISION   Prepares a bare Ubuntu/Debian box to be a 10-4 vault.
# =============================================================================
#  Installs Docker, Tailscale, restic and the iPhone tools, locks the firewall
#  down to Tailscale only, and creates the directory layout.
#
#  Safe to re-run. It installs what is missing and leaves the rest alone.
#
#  Usage:  sudo ./01-provision.sh
# =============================================================================
set -euo pipefail
cd "$(dirname "$0")"
. ./lib.sh

need_root

step "Checking the operating system"
[ -f /etc/os-release ] || die "Cannot identify this OS. These scripts target Ubuntu 24.04+ or Debian 12+."
. /etc/os-release
case "${ID:-}${ID_LIKE:-}" in
  *debian*|*ubuntu*) ok "Found ${PRETTY_NAME}" ;;
  *) die "This targets Ubuntu/Debian. Found: ${PRETTY_NAME:-unknown}" ;;
esac

step "Installing base packages"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq ca-certificates curl gnupg jq ufw rsync gzip >/dev/null
ok "base packages present"

step "Installing Docker Engine (official repository)"
if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  ok "Docker already installed: $(docker --version)"
else
  install -m 0755 -d /etc/apt/keyrings
  curl -fsSL "https://download.docker.com/linux/${ID}/gpg" -o /etc/apt/keyrings/docker.asc
  chmod a+r /etc/apt/keyrings/docker.asc
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/${ID} ${VERSION_CODENAME} stable" \
    > /etc/apt/sources.list.d/docker.list
  apt-get update -qq
  apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin >/dev/null
  systemctl enable --now docker
  ok "Docker installed: $(docker --version)"
fi

step "Installing Tailscale"
if command -v tailscale >/dev/null 2>&1; then
  ok "Tailscale already installed: $(tailscale version | head -1)"
else
  curl -fsSL https://tailscale.com/install.sh | sh
  ok "Tailscale installed"
fi

step "Installing restic"
if ! command -v restic >/dev/null 2>&1; then
  apt-get install -y -qq restic >/dev/null
fi
# Distribution packages lag badly, and restic's B2 backend gets real fixes.
restic self-update >/dev/null 2>&1 || warn "restic self-update failed (not fatal) — continuing with $(restic version | head -1)"
ok "restic ready: $(restic version | head -1)"

step "Installing iPhone tools (libimobiledevice)"
apt-get install -y -qq libimobiledevice-utils libimobiledevice6 usbmuxd ifuse >/dev/null 2>&1 \
  || apt-get install -y -qq libimobiledevice-utils usbmuxd >/dev/null 2>&1 \
  || warn "libimobiledevice did not install. Photos and files still work; only 04-iphone-pull.sh needs it."
systemctl enable --now usbmuxd >/dev/null 2>&1 || true
if command -v idevicebackup2 >/dev/null 2>&1; then
  ok "idevicebackup2 present"
  warn "Distro libimobiledevice often lags new iOS releases. If 04-iphone-pull.sh"
  warn "reports an unsupported device, see docs/RUNBOOK.md > iPhone pull fails."
fi

step "Creating the vault directory layout"
VR="${VAULT_ROOT:-/srv/vault}"
if ! mountpoint -q "$VR" 2>/dev/null; then
  warn "$VR is not a separate mount point."
  warn "You are about to store a whole photo library on the OS disk."
  warn "If you have a data disk, mount it at $VR first. See docs/HARDWARE.md."
fi
mkdir -p "$VR"/{immich/library,immich/postgres,nextcloud/html,nextcloud/data,nextcloud/postgres,iphone,dumps,stack,restore-test}
chmod 700 "$VR"
ok "layout created under $VR"

step "Locking down the firewall"
# Everything is reachable over Tailscale only. Nothing is published to the
# internet or even to the client's own home wifi.
ufw --force default deny incoming >/dev/null
ufw --force default allow outgoing >/dev/null
ufw allow in on tailscale0 >/dev/null
ufw allow 41641/udp >/dev/null   # Tailscale direct connections; without this you get slow relayed routes
if ! ufw status | grep -q "Status: active"; then
  # SSH is normally over Tailscale. Keep a LAN door open only if we are on SSH now.
  if [ -n "${SSH_CONNECTION:-}" ]; then
    warn "You are connected over SSH — allowing port 22 so this does not lock you out."
    warn "Once Tailscale SSH works, remove it with: ufw delete allow 22/tcp"
    ufw allow 22/tcp >/dev/null
  fi
  ufw --force enable >/dev/null
fi
ok "firewall active — inbound allowed on tailscale0 only"

step "Docker and Tailscale service state"
systemctl enable --now docker >/dev/null 2>&1 || true
systemctl enable --now tailscaled >/dev/null 2>&1 || true
ok "services enabled at boot"

cat <<'NEXT'

-----------------------------------------------------------------------------
 PROVISIONING COMPLETE
-----------------------------------------------------------------------------

 Two things to do by hand, because they need your accounts:

  1. Join this machine to your tailnet:

       sudo tailscale up --ssh

     Open the URL it prints, approve the machine, then confirm:

       tailscale status --self

     Note the hostname and the tail____.ts.net suffix — both go in vault.env.

  2. Create the config file:

       sudo cp stack/vault.env.example /srv/vault/vault.env
       sudo chmod 600 /srv/vault/vault.env
       sudo nano /srv/vault/vault.env

     Generate secrets with:
       DB_PASSWORD / NC_DB_PASSWORD : openssl rand -hex 24
       NC_ADMIN_PASSWORD            : openssl rand -base64 18
       RESTIC_PASSWORD              : openssl rand -base64 32

     WRITE THE RESTIC PASSPHRASE ON PAPER BEFORE YOU GO ANY FURTHER.
     It is the only key. Nobody can reset it — that is the point.

 Then run:  sudo ./02-deploy.sh
-----------------------------------------------------------------------------
NEXT
