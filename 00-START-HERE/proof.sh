#!/usr/bin/env bash
# =============================================================================
#  PROOF   Stand up Immich on any computer you already own, in about 10 minutes.
# =============================================================================
#  This is NOT the real install. It is the shortest path to seeing your own
#  photos land in your own vault, so you know the concept works before you
#  spend a cent on hardware.
#
#  Differences from the real thing (01/02), on purpose:
#    - runs anywhere with Docker: a laptop, a Mac, a desktop
#    - LAN only, no Tailscale — your phone must be on the same wifi
#    - no off-site backup, no Nextcloud, no firewall
#    - stores data in ./proof-vault next to this script
#
#  Because it binds to your local network rather than loopback, anyone on your
#  wifi can reach it. Fine for an afternoon at home. Not a vault. Do not put
#  anything in here you would be upset to lose or to leak, and tear it down
#  when you are done.
#
#  Usage:   ./proof.sh          start it
#           ./proof.sh stop     stop it, keep the photos
#           ./proof.sh destroy  stop it and delete everything
# =============================================================================
set -euo pipefail
cd "$(dirname "$0")"
DIR="$PWD/proof-vault"

c_grn=$'\033[0;32m'; c_bld=$'\033[1m'; c_off=$'\033[0m'
ok()   { printf '  %s✓%s %s\n' "$c_grn" "$c_off" "$*"; }
die()  { printf '\nFAILED: %s\n\n' "$*" >&2; exit 1; }

command -v docker >/dev/null 2>&1 || die "Docker is not installed.
   Mac/Windows: install Docker Desktop from docker.com
   Linux:       curl -fsSL https://get.docker.com | sh"
docker compose version >/dev/null 2>&1 || die "Docker Compose plugin missing. Update Docker."
docker info >/dev/null 2>&1 || die "Docker is installed but not running. Start Docker Desktop."

case "${1:-start}" in
  stop)
    docker compose -f "$DIR/docker-compose.yml" --env-file "$DIR/.env" down
    ok "stopped — photos kept in $DIR"; exit 0 ;;
  destroy)
    docker compose -f "$DIR/docker-compose.yml" --env-file "$DIR/.env" down -v 2>/dev/null || true
    rm -rf "$DIR"; ok "destroyed"; exit 0 ;;
esac

# Find the address the phone should point at.
IP=""
if command -v ipconfig >/dev/null 2>&1; then          # macOS
  for i in en0 en1; do IP=$(ipconfig getifaddr $i 2>/dev/null) && [ -n "$IP" ] && break; done
fi
if [ -z "$IP" ] && command -v ip >/dev/null 2>&1; then # Linux
  IP=$(ip -4 route get 1.1.1.1 2>/dev/null | awk '{for(i=1;i<=NF;i++) if($i=="src") print $(i+1)}')
fi
[ -n "$IP" ] || IP="<this computer's IP address>"

printf '\n%s==> Setting up in %s%s\n' "$c_bld" "$DIR" "$c_off"
mkdir -p "$DIR/library" "$DIR/postgres"

[ -f "$DIR/docker-compose.yml" ] || {
  curl -fsSL "https://github.com/immich-app/immich/releases/latest/download/docker-compose.yml" \
    -o "$DIR/docker-compose.yml" || die "Could not download the Immich compose file."
  ok "downloaded Immich"
}

cat > "$DIR/.env" <<EOF
UPLOAD_LOCATION=$DIR/library
DB_DATA_LOCATION=$DIR/postgres
IMMICH_VERSION=v3
DB_PASSWORD=proofonlynotsecret
DB_USERNAME=postgres
DB_DATABASE_NAME=immich
EOF
ok "configured"

printf '\n%s==> Starting (first run downloads a few GB, be patient)%s\n' "$c_bld" "$c_off"
docker compose -f "$DIR/docker-compose.yml" --env-file "$DIR/.env" up -d

printf '\n%s==> Waiting for Immich to come up%s\n' "$c_bld" "$c_off"
# First boot is genuinely slow: Postgres initialises, Immich runs its database
# migrations, and the machine-learning container unpacks its models. On a
# laptop running Docker in a VM this regularly takes 5+ minutes. Later starts
# are seconds. Waiting 12 minutes here beats telling someone it failed when it
# was merely still working.
echo "   First boot takes several minutes — database migrations and ML models."
UP=0
for i in $(seq 1 240); do
  if curl -fsS --max-time 3 "http://127.0.0.1:2283/api/server/ping" >/dev/null 2>&1; then
    printf '\n'; ok "Immich is up"; UP=1; break
  fi
  printf '.'; sleep 3
done
if [ "$UP" = 0 ]; then
  printf '\n'
  echo "Immich has not answered after 12 minutes. It may still be starting."
  echo "Watch what it is doing with:"
  echo "    docker logs immich_server --tail 40 -f"
  echo "Then open http://localhost:2283 — it often comes up shortly after."
  exit 1
fi

cat <<NEXT

-----------------------------------------------------------------------------
 ${c_bld}IT IS RUNNING${c_off}
-----------------------------------------------------------------------------

 1. On this computer, open:      http://localhost:2283
    Create the admin account. That is your vault.

 2. On your iPhone, on the SAME WIFI:
      - Install "Immich" from the App Store
      - Server URL:  http://$IP:2283
      - Log in with the account you just made
      - Settings > Backup > select all albums > enable background backup

 3. Leave the phone on the charger on wifi. Come back later.

 Then go and look at http://localhost:2283 and search your own photos for
 something you never tagged — "beach", "dog", "whiteboard". That search is
 running on your own machine, against your own library, and no part of it
 touched anyone else's computer.

 ${c_bld}That is the concept proven.${c_off}

 When you are done:
     ./proof.sh stop        keep the photos
     ./proof.sh destroy     delete everything

 Then build the real one: see 00-START-HERE/README.md
-----------------------------------------------------------------------------
NEXT
