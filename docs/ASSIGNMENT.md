# CloudNotes Service Troubleshooting: Assignment Brief

## Scenario
You are a Cloud Engineer on-call. A critical background utility—**CloudNotes API** (a local note-taking index service)—has failed in production. The application was recently updated, but the automated deployment pipeline failed, leaving the service in an inoperable state.

Your teammates complain that:
1. The start script fails immediately with error traces.
2. The health check fails or reports abnormal/untrusted server states.
3. The database cannot be loaded, and logs are missing.

Your task is to restore the **CloudNotes API** to a fully operational state, document your findings, and provide evidence of recovery.

---

## Objectives
Using your system administration, Linux networking, and file permissions troubleshooting skills:
1. **Observe**: Run the start script and examine the immediate error.
2. **Investigate & Diagnose**: Read configuration files, check file attributes/permissions, inspect port status, and trace active processes.
3. **Fix**: Repair syntax/logic configurations, adjust file permissions, and terminate rogue processes.
4. **Verify**: Ensure the application server starts successfully, writes logs correctly, and responds with a healthy HTTP status on the correct port.

---

## Tasks

### Task 1: Initialize the Incident
To recreate the exact state of the broken production environment, run the simulation script in your terminal:
```bash
./scripts/simulate_incident.sh
```
This script will configure the files and launch the background services in their broken configuration.

### Task 2: Service Diagnostics & Repair
Attempt to start the service:
```bash
./scripts/start.sh
```
Analyze the failure. You must fix the application configuration so that the application can successfully parse its inputs and reach the initialization phase.

### Task 3: Resolve Permissions Defect
Once the configuration is corrected, restart the service. You will encounter a file/permission error.
Investigate the file permissions of the logging directory and log file. Resolve the permission block so the application can write execution traces.

### Task 4: Resolve Network Bind Conflict
After fixing permissions, attempt to start the service again. The server will fail to start due to a port bind conflict (Address already in use).
1. Query the network ports to identify the process ID (PID) holding the target port.
2. Verify the identity of the process to ensure it is the rogue script.
3. Terminate the conflicting process.
4. Start the CloudNotes service and verify it stays running.

### Task 5: Final Validation
Verify the service is responsive and healthy:
```bash
./scripts/healthcheck.sh
```

---

## Expected Learning Outcomes
By completing this assignment, you will demonstrate the ability to:
- Trace process failures using application standard error (stderr) outputs.
- Query and modify Unix file permissions (`chmod`, `ls -l`) to allow daemon processes to access resources.
- Scan listening network sockets and map ports to process IDs (`lsof`, `netstat`, or `ss`).
- Read and edit structured configuration files (`JSON`) to correct runtime options.
- Manage Unix background processes (`ps`, `kill`, `pgrep`).

---

## Submission Guidelines
Create a short report (`SUBMISSION.md` or a PDF) containing:
1. **Incident Timeline**: A list of the steps you took, showing the commands run and outputs received.
2. **Root Cause Analysis (RCA)**: Explain why each of the three faults caused a failure:
   - What key was wrong in the configuration?
   - What permissions blocked the log file?
   - What was the PID and filename of the rogue process occupying the port?
3. **Recovery Verification**: Provide the full command outputs for:
   - `ls -l logs/application.log` showing corrected permissions.
   - The command used to search for the process holding port `8080` (e.g., `lsof` or `ss`).
   - The output of `./scripts/healthcheck.sh` showing a `200 OK` and a healthy response.
