#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_PY="$ROOT/app/app.py"
LOG_FILE="$ROOT/logs/application.log"

if [ "$(id -u)" -ne 0 ]; then
  echo "This script must be run with sudo or as root."
  echo "Example: sudo $0"
  exit 1
fi

if ! id cloudnotes >/dev/null 2>&1; then
  echo "Creating system user cloudnotes for service execution."
  useradd --system --home-dir "$ROOT" --shell /usr/sbin/nologin cloudnotes
fi

mkdir -p "$ROOT/logs"

exec sudo -u cloudnotes /usr/bin/env python3 "$APP_PY"
