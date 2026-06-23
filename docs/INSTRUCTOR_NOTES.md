# CloudNotes Service Troubleshooting: Instructor Notes & Solutions Guide

This document is intended for instructors and grading mentors. It explains the design of the three intentional faults, their solutions, and provides a grading rubric.

---

## Fault Design & Solution Key

### Fault 1: Configuration Typo (Key Error)
*   **Symptom**: When running `./scripts/start.sh`, the service fails to start and outputs:
    ```text
    CRITICAL: Configuration error: Missing required setting 'database_file_path'
    ```
*   **Root Cause**: The application config file `app/config.json` uses the key `"db_file_path"` instead of `"database_file_path"`, which is expected by the Python server script `app/server.py` on line 36.
*   **Resolution**: 
    1. Open `app/config.json` in an editor.
    2. Change the key `"db_file_path"` to `"database_file_path"`.
    3. The updated `app/config.json` should look like this:
        ```json
        {
          "host": "127.0.0.1",
          "port": 8080,
          "log_file_path": "logs/application.log",
          "database_file_path": "data/notes.json"
        }
        ```

### Fault 2: Write-Protected Log File (Permission Error)
*   **Symptom**: After fixing Fault 1 and running `./scripts/start.sh`, the service fails with:
    ```text
    CRITICAL: Permission denied when opening log file at /.../logs/application.log. Run 'ls -l' to check ownership and permissions.
    ```
*   **Root Cause**: The log file `logs/application.log` has its permissions set to `400` (`-r--------`), which prevents the application from opening it in append (`'a'`) mode.
*   **Resolution**:
    1. Inspect file permissions: `ls -l logs/application.log`.
    2. Update permissions to allow write access:
        ```bash
        chmod 644 logs/application.log
        ```
        *(Alternatively, `chmod 664` or `chmod +w logs/application.log` are also acceptable).*

### Fault 3: Network Bind Conflict (Address Already in Use)
*   **Symptom**: After fixing Faults 1 and 2 and running `./scripts/start.sh`, the service fails with:
    ```text
    CRITICAL: Port conflict. Address 127.0.0.1:8080 is already in use.
    ```
    Additionally, querying the health endpoint returns a JSON payload indicating a conflict:
    ```bash
    $ ./scripts/healthcheck.sh
    {"error": "Port conflict detected", "message": "Port 8080 is occupied by rogue_service.py", "pid": 12345}
    ```
*   **Root Cause**: A background python process (`scripts/rogue_service.py`) is already listening on port `8080`, blocking `server.py` from binding to it.
*   **Resolution**:
    1. Scan the port to identify the conflicting process. Students can use:
        *   `lsof -i :8080` (Standard on macOS and Linux)
        *   `ss -tulpn` or `ss -lpt` (Linux/WSL)
        *   `netstat -tulpn` (Linux/WSL)
        *   `ps aux | grep rogue_service.py` (Fallback process search)
    2. Identify the process ID (PID) (e.g., `12345`).
    3. Kill the rogue process:
        ```bash
        kill 12345
        ```
        *(Or `kill -9 12345` if it does not respond immediately).*
    4. Start the service: `./scripts/start.sh` (which should now succeed).

---

## Grading Rubric (100 Points Total)

| Criteria | Points | Description |
| :--- | :---: | :--- |
| **Fault 1: Config Typo Resolution** | **25 pts** | Correctly identifies the configuration key mismatch and updates `app/config.json` from `"db_file_path"` to `"database_file_path"`. |
| **Fault 2: Log File Permissions** | **25 pts** | Correctly identifies the `PermissionError` on `logs/application.log` and uses `chmod` (to `644`, `664`, or `+w`) to grant write permissions. |
| **Fault 3: Port Bind Resolution** | **30 pts** | Explains the port binding conflict, shows evidence of searching for the PID using network commands (`lsof`, `ss`, or `netstat`), and successfully terminates the rogue PID. |
| **Verification Evidence** | **20 pts** | Submits valid evidence of a working state, including the output of `./scripts/healthcheck.sh` showing `HTTP/1.1 200 OK` and `{"status": "healthy"}`. |

---

## Common Student Mistakes & Troubleshooting Tips
1.  **Editing Python Server Files instead of Config**:
    - *Mistake*: Editing `app/server.py` to match the typo in `app/config.json` (i.e. changing the server logic code to search for `db_file_path`).
    - *Grading Guidance*: This is technically a valid logic fix, but in a real-world setting, application source code should not be modified to accommodate bad configurations. Award partial marks (e.g., 15/25 pts) if they edit `server.py` instead of `config.json`, and note this best-practice feedback.
2.  **Using Sudo Prematurely**:
    - *Mistake*: Running the application with `sudo python3 app/server.py` to try and bypass the permissions issue.
    - *Result*: This will bypass the `logs/application.log` file permissions, but it runs the app as root (security risk) and does not fix the root cause (bad permission settings). It will also fail if the root user tries to bind to the port while the rogue service is running under standard user space.
    - *Grading Guidance*: Deduct 10 points if they run the server as `root`/`sudo` rather than properly fixing file permissions.
3.  **WSL Metadata Perm issues**:
    - *Issue*: In rare cases where students run WSL in a directory mounted directly to Windows (`/mnt/c/...`), `chmod` may silently do nothing.
    - *Guidance*: Instructors should advise students to clone the repository into the native Linux partition (e.g. `~/projects/` or `/home/<user>/`) where Unix file permissions are fully simulated.
