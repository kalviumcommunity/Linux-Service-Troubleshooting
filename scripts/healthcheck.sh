#!/usr/bin/env bash
set -euo pipefail

PORT=8080

if command -v curl >/dev/null 2>&1; then
    echo "Running healthcheck: curl -i -s http://127.0.0.1:$PORT/health"
    echo "--------------------------------------------------------"
    curl -i -s http://127.0.0.1:$PORT/health
    echo ""
    echo "--------------------------------------------------------"
else
    echo "ERROR: curl is required for the healthcheck."
    exit 1
fi
