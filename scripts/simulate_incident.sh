#!/usr/bin/env bash
# Exit on error
set -e

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PID_FILE="$ROOT/scripts/rogue.pid"

echo "=== Initializing Incident Simulation ==="

# 1. Stop any existing service or rogue processes
if [ -f "$PID_FILE" ]; then
    ROGUE_PID=$(cat "$PID_FILE")
    if kill -0 "$ROGUE_PID" >/dev/null 2>&1; then
        echo "Stopping previous rogue service (PID: $ROGUE_PID)..."
        kill "$ROGUE_PID" || kill -9 "$ROGUE_PID"
    fi
    rm -f "$PID_FILE"
fi

# Fallback cleanup
PIDS=$(pgrep -f "python3.*scripts/rogue_service.py" || true)
if [ -n "$PIDS" ]; then
    echo "Stopping background rogue processes..."
    kill $PIDS || kill -9 $PIDS
fi

# Stop main app if running
"$ROOT/scripts/stop.sh" || true

# 2. Reset app/config.json to the broken state
echo "Resetting app/config.json configuration (introducing Fault 1)..."
cat <<EOF > "$ROOT/app/config.json"
{
  "host": "127.0.0.1",
  "port": 8080,
  "log_file_path": "logs/application.log",
  "db_file_path": "data/notes.json"
}
EOF

# 3. Create log directory and file, then set bad permissions (Fault 2)
echo "Creating logs/application.log and setting write-restricted permissions (introducing Fault 2)..."
mkdir -p "$ROOT/logs"
rm -f "$ROOT/logs/application.log"
touch "$ROOT/logs/application.log"
chmod 400 "$ROOT/logs/application.log"

# 4. Start rogue service (Fault 3)
echo "Launching rogue service on port 8080 in the background (introducing Fault 3)..."
python3 "$ROOT/scripts/rogue_service.py" > /dev/null 2>&1 &
sleep 1

# Verify rogue service started
if [ -f "$PID_FILE" ]; then
    echo "Simulation initialized successfully!"
    echo "Faults introduced:"
    echo "  1. Config file 'app/config.json' has a key typo (db_file_path vs database_file_path)."
    echo "  2. Log file 'logs/application.log' is write-protected (chmod 400)."
    echo "  3. Port 8080 is blocked by a rogue service (PID: $(cat "$PID_FILE"))."
    echo ""
    echo "You can now begin troubleshooting. Try running './scripts/start.sh' to start."
else
    echo "ERROR: Failed to initialize rogue service. Check python3 command or port 8080 availability."
    exit 1
fi
