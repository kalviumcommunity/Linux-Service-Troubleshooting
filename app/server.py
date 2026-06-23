#!/usr/bin/env python3
import http.server
import json
import os
import sys
from datetime import datetime, timezone

# Determine base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, 'app', 'config.json')

def log_message(log_file, level, message):
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] [{level}] {message}\n"
    # Write to stdout for system logging
    sys.stdout.write(log_line)
    sys.stdout.flush()
    # Append to the log file if available
    if log_file:
        with open(log_file, 'a') as f:
            f.write(log_line)

def main():
    # 1. Load config
    if not os.path.exists(CONFIG_PATH):
        sys.stderr.write(f"CRITICAL: Configuration file not found at {CONFIG_PATH}\n")
        sys.exit(1)
        
    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
    except Exception as e:
        sys.stderr.write(f"CRITICAL: Failed to parse config file: {e}\n")
        sys.exit(1)

    # Fault 1: KeyError on database_file_path
    try:
        host = config.get('host', '127.0.0.1')
        port = config.get('port', 8080)
        log_file_rel = config.get('log_file_path', 'logs/application.log')
        db_file_rel = config['database_file_path'] # Key error here!
    except KeyError as e:
        sys.stderr.write(f"CRITICAL: Configuration error: Missing required setting {e}\n")
        sys.exit(1)

    log_file = os.path.join(BASE_DIR, log_file_rel)
    db_file = os.path.join(BASE_DIR, db_file_rel)

    # 2. Setup logging and check permissions (Fault 2)
    log_dir = os.path.dirname(log_file)
    os.makedirs(log_dir, exist_ok=True)
    
    try:
        # Check write access to log file
        with open(log_file, 'a') as f:
            f.write("")
    except PermissionError as e:
        sys.stderr.write(f"CRITICAL: Permission denied when opening log file at {log_file}. Run 'ls -l' to check ownership and permissions.\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"CRITICAL: Unexpected error opening log file: {e}\n")
        sys.exit(1)

    log_message(log_file, "INFO", "Starting CloudNotes Service...")
    log_message(log_file, "INFO", f"Loading database from {db_file}")

    # 3. Load database
    db_dir = os.path.dirname(db_file)
    os.makedirs(db_dir, exist_ok=True)
    
    if not os.path.exists(db_file):
        initial_data = [
            {"id": 1, "title": "Welcome to CloudNotes", "content": "This is your first note. Keep it safe!"},
            {"id": 2, "title": "Troubleshooting Tip", "content": "Always check application logs and active ports."}
        ]
        try:
            with open(db_file, 'w') as f:
                json.dump(initial_data, f, indent=2)
        except Exception as e:
            log_message(log_file, "ERROR", f"Failed to initialize database file: {e}")
            sys.stderr.write(f"CRITICAL: Failed to write database: {e}\n")
            sys.exit(1)

    # Define HTTP Request Handler
    class CloudNotesHandler(http.server.BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            message = format % args
            log_message(log_file, "INFO", f"Request: {message}")

        def send_json(self, status_code, data):
            self.send_response(status_code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode('utf-8'))

        def do_GET(self):
            if self.path == '/' or self.path == '':
                self.send_json(200, {
                    "service": "CloudNotes API",
                    "status": "running",
                    "version": "1.0.0",
                    "endpoints": {
                        "/health": "Check service health",
                        "/notes": "Retrieve list of notes"
                    }
                })
            elif self.path == '/health':
                self.send_json(200, {"status": "healthy"})
            elif self.path == '/notes':
                try:
                    with open(db_file, 'r') as f:
                        notes = json.load(f)
                    self.send_json(200, {"notes": notes})
                except Exception as e:
                    log_message(log_file, "ERROR", f"Failed to read database: {e}")
                    self.send_json(500, {"error": "Internal database read error"})
            else:
                self.send_json(404, {"error": "Endpoint not found"})

    # 4. Bind and run HTTP Server (Fault 3)
    try:
        server = http.server.HTTPServer((host, port), CloudNotesHandler)
    except OSError as e:
        log_message(log_file, "ERROR", f"Failed to bind to {host}:{port} - {e}")
        sys.stderr.write(f"CRITICAL: Port conflict. Address {host}:{port} is already in use.\n")
        sys.stderr.write(f"Error details: {e}\n")
        sys.exit(1)

    log_message(log_file, "INFO", f"CloudNotes Service is successfully running on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log_message(log_file, "INFO", "Service stopped by user.")
        server.server_close()

if __name__ == '__main__':
    main()
