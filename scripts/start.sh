#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PID_FILE="$ROOT/scripts/service.pid"
APP_SCRIPT="$ROOT/app/server.py"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" >/dev/null 2>&1; then
        echo "CloudNotes service is already running (PID: $PID)."
        exit 0
    else
        rm -f "$PID_FILE"
    fi
fi

echo "Starting CloudNotes service..."
mkdir -p "$ROOT/scripts"
# Execute python application in the background
python3 "$APP_SCRIPT" > "$ROOT/scripts/stdout.log" 2> "$ROOT/scripts/stderr.log" &
APP_PID=$!

# Wait briefly for startup validation
sleep 1.5

if kill -0 "$APP_PID" >/dev/null 2>&1; then
    echo "CloudNotes service started successfully in background (PID: $APP_PID)."
    echo "$APP_PID" > "$PID_FILE"
    exit 0
else
    echo "ERROR: CloudNotes service failed to start immediately."
    echo "=== Service Diagnostics ==="
    if [ -f "$ROOT/scripts/stderr.log" ] && [ -s "$ROOT/scripts/stderr.log" ]; then
        echo "Stderr Logs:"
        cat "$ROOT/scripts/stderr.log"
    else
        echo "No stderr log output. The script may have failed silently or had config-level errors."
    fi
    exit 1
fi
