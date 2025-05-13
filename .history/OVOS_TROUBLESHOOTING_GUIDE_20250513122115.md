# OVOS Docker Compose Troubleshooting Guide

This guide covers common issues and solutions for running OpenVoiceOS (OVOS) and ovos_messagebus in Docker Compose, based on the current working stack (as of May 2025).

---

## 1. Messagebus Connection Refused
- Ensure both `websocket` and `message_bus_client` sections in `mycroft.conf` use:
  - `"host": "ovos_messagebus"`
  - `"port": 8181"`
  - `"route": "/core"`
  - `"ssl": false"`
- Confirm both services are on the same Docker network.
- Make sure the `ovos` service has the correct `MESSAGEBUS_*` environment variables in Compose (these take precedence for the client).
- Restart both containers after config changes.

## 2. mycroft.conf Not Loaded or Invalid
- Check that `mycroft.conf` is valid JSON (no comments, trailing commas, or syntax errors).
- The config should be mounted to `/home/ovos/.config/mycroft/mycroft.conf` in both containers.
- Use the canonical config example from the setup guide.

## 3. File Permissions (Windows)
- If you see `PermissionError` for `/home/ovos/.local/state`, run in PowerShell:
  ```powershell
  icacls ".\ovos_config\data" /grant Everyone:(OI)(CI)F /T
  icacls ".\ovos_config\config" /grant Everyone:(OI)(CI)F /T
  ```

## 4. Dependency or Build Failures
- If you see errors about `swig` or `libfann-dev` missing, ensure these are installed in your Dockerfile:
  ```Dockerfile
  RUN apt-get update && \
      apt-get install -y --no-install-recommends tini build-essential libglib2.0-0 libsm6 libxext6 libxrender-dev swig libfann-dev && \
      rm -rf /var/lib/apt/lists/*
  ```
- Pin `websocket-client==0.57.0` in `requirements.txt` to avoid compatibility issues.

## 5. Testing Connectivity
- To test OVOS <-> messagebus connection:
  ```powershell
  docker-compose -f docker-compose.ai.yml exec ovos python3 /home/ovos/ovos_test_connection.py
  ```
- To check messagebus health:
  ```powershell
  docker-compose -f docker-compose.ai.yml exec ovos curl -v http://ovos_messagebus:8181/core
  ```

## 6. General Tips
- Always restart containers after changing configs or environment variables.
- Check logs with:
  ```powershell
  docker-compose -f docker-compose.ai.yml logs --tail=100 ovos
  docker-compose -f docker-compose.ai.yml logs --tail=100 ovos_messagebus
  ```
- If all else fails, prune Docker system and rebuild images:
  ```powershell
  docker system prune -a
  docker-compose -f docker-compose.ai.yml build --no-cache
  ```

## 7. Persistent 'Connection Refused' Errors (Advanced Diagnostics)
- If you still see repeated 'Connection Refused' errors in ovos-core logs, even when direct Python test scripts (like `ovos_test_connection.py`) can connect to the messagebus:
  - This confirms Docker networking and config are correct, but ovos-core's main process is failing to connect.
  - Possible causes:
    - Race condition: ovos-core may start before the messagebus is fully ready, even with `depends_on` and healthchecks.
    - Config/env loading order: ovos-core may not be reading the correct environment variables or config at the right time.
    - Internal bug or version mismatch in ovos-core or ovos-bus-client.
  - Steps to try:
    1. Add a startup delay to the ovos-core service (e.g., `command: ["sh", "-c", "sleep 10 && ovos-start"]` in Compose).
    2. Ensure both `websocket` and `message_bus_client` sections in `mycroft.conf` are correct and match the Docker Compose service name.
    3. Use only essential config in `mycroft.conf` to rule out parsing issues.
    4. Update ovos-core and ovos-bus-client to the latest versions.
    5. Check for permission issues on config/data volumes.
    6. Review full ovos-core logs for clues about config loading order or errors.

---

_Last updated: May 13, 2025_
