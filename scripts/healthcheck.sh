#!/usr/bin/env bash
set -euo pipefail
if command -v curl >/dev/null 2>&1; then
  curl -fsS http://127.0.0.1:5000/health
else
  echo "curl is required for healthcheck."
  exit 1
fi
