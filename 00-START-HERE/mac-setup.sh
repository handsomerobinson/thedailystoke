#!/usr/bin/env bash
# =============================================================================
#  MAC SETUP   Installs Docker on a Mac, then runs proof.sh. One command.
# =============================================================================
#  Two things need a human and cannot be scripted: your password, and clicking
#  Accept in Docker Desktop the first time it opens. Everything else is here.
#
#  Usage:  ./mac-setup.sh
# =============================================================================
set -uo pipefail
cd "$(dirname "$0")"

say() { printf '\n\033[1m==> %s\033[0m\n' "$*"; }

[ "$(uname)" = "Darwin" ] || { echo "This is the macOS helper. On Linux run 01-provision.sh."; exit 1; }

if ! command -v brew >/dev/null 2>&1; then
  say "Installing Homebrew (it will ask for your password)"
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" || exit 1
fi
# Homebrew lives in different places on Apple Silicon and Intel.
for b in /opt/homebrew/bin/brew /usr/local/bin/brew; do
  [ -x "$b" ] && eval "$("$b" shellenv)" && break
done
command -v brew >/dev/null 2>&1 || { echo "Homebrew still not on PATH. Open a new Terminal and re-run."; exit 1; }

if ! command -v docker >/dev/null 2>&1; then
  say "Installing Docker Desktop (a ~1GB download, be patient)"
  brew install --cask docker || exit 1
fi

say "Opening Docker Desktop"
open -a Docker 2>/dev/null || open -a "Docker Desktop" 2>/dev/null

say "Waiting for Docker to be ready"
echo "   If a Docker window appears asking you to accept terms, click Accept."
echo "   This waits up to 5 minutes."
for i in $(seq 1 100); do
  if docker info >/dev/null 2>&1; then echo "   Docker is running."; break; fi
  [ "$i" = 100 ] && { echo "
   Docker did not come up. Open Docker Desktop from Applications, click through
   any prompts until it says 'Engine running', then run ./proof.sh"; exit 1; }
  printf '.'; sleep 3
done

say "Starting your vault"
exec ./proof.sh
