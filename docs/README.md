# Linux Service Troubleshooting: CloudNotes

This repository is a hands-on troubleshooting exercise for Linux service operations.
The task is to diagnose a cloud workload that fails to start, identify root cause, implement fixes, and verify recovery.

## Scenario

CloudNotes is a simple Flask application deployed as a Linux service. The target system is a standard Linux server with a dedicated service user and a service unit.

Students must use evidence from the service, logs, configuration, and networking tools to find and fix the failure.

## Environment Setup

1. Confirm the system is Linux.
2. Install Python 3 and `pip`.
3. Install dependencies:
   ```bash
   sudo pip3 install -r app/requirements.txt
   ```
4. Use the provided scripts in `scripts/` to start, stop, and verify the service.

## Installation Instructions

Do not change the service behavior until you have diagnosed the problem.

1. Inspect the repository structure.
2. Read `service/cloudnotes.service` and `app/config.py`.
3. Start the service with:
   ```bash
   sudo ./scripts/start.sh
   ```
4. Review failure evidence and log output.

## Submission Requirements

Provide a short report with:
- the root cause for each failure,
- the exact commands used to fix the issue,
- verification output from `curl http://127.0.0.1:5000/health`.

Do not include direct fixes in your report. Keep the exercise evidence-based.
