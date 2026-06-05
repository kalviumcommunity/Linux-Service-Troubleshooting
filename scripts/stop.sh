#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${ROOT}/app/app.py"

pkill -f "python3 ${TARGET}" || true
pkill -f "python ${TARGET}" || true

echo "Stopped CloudNotes processes if any were running."
