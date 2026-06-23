# CloudNotes Service Troubleshooting Lab

Welcome to the CloudNotes Service Troubleshooting lab. This repository simulates a real-world production incident where a background microservice has crashed due to multiple deployment and configuration issues.

Your job as a Cloud Engineer / DevOps Engineer on-call is to investigate the symptoms, determine the root causes of the failures, implement permanent fixes, and verify that the application returns to a fully operational state.

---

## Lab Overview

**CloudNotes API** is a self-contained, lightweight python utility that manages note-taking indices. It reads configuration parameters, logs runtime diagnostic outputs to a log file, loads index data from a JSON store, and starts a local web server to expose API endpoints.

Currently, the service is in a degraded, non-running state. To complete the lab, you must resolve three distinct faults that block the application from successfully initializing and running.

---

## Setup and Initialization

### 1. Requirements
*   **Operating System**: Linux, macOS, or Windows Subsystem for Linux (WSL).
*   **Python**: Python 3.x (standard library only; no extra packages required).
*   **Utilities**: Standard Unix CLI tools and `curl`.

> [!IMPORTANT]
> **WSL Users**: It is highly recommended to clone this repository inside your native WSL filesystem (e.g., under `/home/<username>/projects/`) rather than the Windows shared partition `/mnt/c/`. This ensures that Unix file permissions and executable flags are fully simulated and behave correctly.

### 2. Clone and Setup
Run the following commands in your terminal to clone the workspace and navigate to the directory:
```bash
git clone https://github.com/kalviumcommunity/Linux-Service-Troubleshooting.git
cd Linux-Service-Troubleshooting
```

### 3. Initialize the Failure State
To simulate the incident and break the service, execute the simulation script:
```bash
./scripts/simulate_incident.sh
```
This script sets up the faulty environment configuration, restricts file permissions, and starts background conflict processes.

---

## General Troubleshooting Process

To identify and solve the faults, follow the standard debugging cycle:
$$\text{Observe} \rightarrow \text{Investigate} \rightarrow \text{Diagnose} \rightarrow \text{Fix} \rightarrow \text{Verify}$$

1.  **Observe**: Attempt to start the server:
    ```bash
    ./scripts/start.sh
    ```
    If it fails, review the immediate error console trace.
2.  **Investigate**: Look at the repository files and query system statuses.
    *   *Configuration files*: Review files in the `app/` directory.
    *   *Logs*: Review files in the `logs/` directory.
    *   *Processes and network state*: Check for running processes and bound network ports.
3.  **Diagnose**: Connect error messages to their root causes (e.g. why is a file unopenable? Why can a port not be bound?).
4.  **Fix**: Apply correct file changes, file permissions, or process actions.
5.  **Verify**: Restart the service using `./scripts/start.sh` and run `./scripts/healthcheck.sh`.

---

## Recommended Troubleshooting Tools

You are free to solve this lab using any standard utilities available on your system. You may find the following CLI tools helpful for investigation and repair:

*   **Process Inspection**: `ps`, `pgrep`, `top`
*   **Network & Ports Inspection**: `lsof`, `ss`, `netstat`
*   **File & Directory Metadata**: `ls -lh`, `file`
*   **File & Directory Permissions**: `chmod`, `chown`
*   **Content Inspection**: `cat`, `tail`, `grep`, `less`
*   **API Verification**: `curl`

---

## Task Verification & Submissions

To verify you have completed the lab:
1.  Run `./scripts/healthcheck.sh`.
2.  You should receive a `200 OK` HTTP status and the following JSON output:
    ```json
    {
      "status": "healthy"
    }
    ```
3.  Prepare your submission report as detailed in [docs/ASSIGNMENT.md](file:///Users/sriman/developer/projects/internship/devops_question/Linux-Service-Troubleshooting/Linux-Service-Troubleshooting/docs/ASSIGNMENT.md).
