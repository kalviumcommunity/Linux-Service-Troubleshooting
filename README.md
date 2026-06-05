# Linux-Service-Troubleshooting

## Scenario

CloudNotes is a simple Flask-based note service that is deployed as a Linux service. This repository is designed as a diagnostic assignment: the application does not run successfully until students identify and fix multiple faults.

## What is included

- `app/` with a small Flask application and configuration.
- `logs/application.log` containing real-looking startup evidence.
- `data/notes.db` containing sample note data.
- `scripts/` with start, stop, and healthcheck helpers.
- `service/cloudnotes.service` showing a realistic systemd unit.
- `rogue_service.py` to simulate a port conflict on `5000`.
- `docs/README.md` containing environment setup and submission requirements.

## Learning objectives

Students will diagnose:
- service startup failure from a broken configuration,
- permission problems for a Linux service log file,
- process port conflicts blocking application startup.

## Verification

After fixing all faults, the service should respond successfully to:

```bash
curl http://127.0.0.1:5000/health
```

Expected output:

```json
{"status":"healthy"}
```
