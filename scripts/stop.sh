#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PID_FILE="$ROOT/scripts/service.pid"
ROGUE_PID_FILE="$ROOT/scripts/rogue.pid"

echo "=== Stopping CloudNotes Processes ==="

# 1. Stop main application service
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" >/dev/null 2>&1; then
        echo "Stopping CloudNotes service (PID: $PID)..."
        kill "$PID" || kill -9 "$PID"
    fi
    rm -f "$PID_FILE"
else
    # Fallback lookup
    PIDS=$(pgrep -f "python3.*app/server.py" || true)
    if [ -n "$PIDS" ]; then
        echo "Stopping matching service processes..."
        kill $PIDS || kill -9 $PIDS
    fi
fi

# 2. Stop rogue service if requested/still running
if [ -f "$ROGUE_PID_FILE" ]; then
    PID=$(cat "$ROGUE_PID_FILE")
    if kill -0 "$PID" >/dev/null 2>&1; then
        echo "Stopping rogue service (PID: $PID)..."
        kill "$PID" || kill -9 "$PID"
    fi
    rm -f "$ROGUE_PID_FILE"
else
    # Fallback lookup
    PIDS=$(pgrep -f "python3.*scripts/rogue_service.py" || true)
    if [ -n "$PIDS" ]; then
        echo "Stopping matching rogue processes..."
        kill $PIDS || kill -9 $PIDS
    fi
fi

# Clean up local execution artifacts
rm -f "$ROOT/scripts/stdout.log" "$ROOT/scripts/stderr.log"

echo "CloudNotes service and rogue processes stopped."
