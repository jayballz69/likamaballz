# OpenVoiceOS (OVOS) Docker Compose Setup Guide

> **Note:** All code, configuration, and documentation changes must follow the rules in [AI_CODING_BASELINE_RULES.md](./AI_CODING_BASELINE_RULES.md). Reference this guide in all new code and reviews.

- For all custom Python code, see Section 23.8 of `AI_CODING_BASELINE_RULES.md` for required style, testing, and security practices. This is mandatory for all OVOS skills, integrations, and any Python-based service or script.

## Overview
This guide explains how to set up, configure, and troubleshoot OpenVoiceOS (OVOS) and its messagebus using Docker Compose, as implemented in this stack. It summarizes the key steps, configuration requirements, and common issues, based on the detailed logs and documentation in `docker-compose.ai.yml`.

---

## Prerequisites
- **Docker** and **Docker Compose** installed
- **Windows** host (instructions use PowerShell syntax)
- Workspace directory structure as in this repository (see `docker-compose.ai.yml`)

---

## Directory Structure
- `ovos_config/config/` — contains `mycroft.conf` (main OVOS configuration)
- `ovos_config/data/` — persistent data for OVOS
- `ovos-docker/` — contains `Dockerfile.custom-ovos-core` and `requirements.txt` for custom OVOS builds

---

## Compose Services
- `ovos_messagebus`: Messagebus server (image: `smartgic/ovos-messagebus:latest`)
- `ovos`: OVOS Core (custom build from `ovos-docker/Dockerfile.custom-ovos-core`)

### Example Compose Service Snippet
See `docker-compose.ai.yml` for the full configuration. Key points:
- Both services are on the `ovos_network` bridge network
- `ovos_messagebus` exposes port 8181
- `ovos` depends on `ovos_messagebus` (with healthcheck)
- Volumes mount `ovos_config/config` and `ovos_config/data` into the containers

---

## Configuration: `mycroft.conf`

> **⚠️ CRITICAL CONFIGURATION NOTE:**
> 
> The values for `websocket` and `message_bus_client` in `mycroft.conf` **must** be set as follows for OVOS to function in Docker Compose:
> 
> - `"host": "ovos_messagebus"`
> - `"port": 8181`
> - `"route": "/core"`
> - `"ssl": false`
> 
> These must match **exactly** for both the `websocket` and `message_bus_client` sections. If you use any other value (such as `0.0.0.0` or a container IP), OVOS will fail to connect to the messagebus, resulting in repeated connection errors and non-functional voice services. The Docker Compose service name (`ovos_messagebus`) is required for reliable service discovery and networking between containers.
> 
> **Do not use `0.0.0.0` for the host in Docker Compose configs.** That is only for standalone/server mode, not for inter-container communication.

Located at `ovos_config/config/mycroft.conf` on the host and mounted into both `ovos_messagebus` and `ovos` containers at `/home/ovos/.config/mycroft/mycroft.conf`.

**Canonical Example for Docker Compose:**
```json
{
  "lang": "en-us",
  "log_level": "DEBUG",
  "websocket": {
    "host": "ovos_messagebus",
    "port": 8181,
    "route": "/core",
    "ssl": false
  },
  "message_bus_client": {
    "host": "ovos_messagebus",
    "port": 8181,
    "route": "/core",
    "ssl": false
  },
  "PHAL": {
    "admin": {
      // "ovos-PHAL-plugin-gui_notifications_service": { // Removed as it was causing build issues and GUI notifications are not essential for core functionality at this stage (2025-05-14).
      //   "enabled": true
      // },
      "ovos-PHAL-plugin-system": { // Provides system-level commands (reboot, NTP sync, etc.).
        "enabled": false // Set to true to enable system control functionalities.
      }
    }
  }
  // ...other config sections (units, location, stt, tts, etc.) ...
}
```
> **Note:** For Docker Compose, the same config is mounted into both containers. Using `host: "ovos_messagebus"` in both `websocket` and `message_bus_client` ensures both the server and client work correctly. This is required for OVOS to connect reliably in this stack. If you use separate configs, the server can use `0.0.0.0` for `websocket`, but this is not recommended here.

---

## Building and Running
1. **Build the custom OVOS image:**
   The `ovos-docker/requirements.txt` file manages Python dependencies for the custom OVOS image.
   - `ovos-PHAL-plugin-gui_notifications_service` was removed (2025-05-14) as it was causing build failures and GUI notification functionality was deemed non-essential for the current goals.
   - `ovos-PHAL-plugin-system` was added (2025-05-14) to provide system control capabilities. It is not enabled by default in `mycroft.conf`.
   ```powershell
   docker-compose -f "docker-compose.ai.yml" build ovos
   ```
2. **Start the services:**
   ```powershell
   docker-compose -f "docker-compose.ai.yml" up -d ovos_messagebus ovos
   ```
3. **Check logs:**
   ```powershell
   docker-compose -f "docker-compose.ai.yml" logs -f ovos_messagebus ovos
   ```

---

## Common Issues & Fixes

### 1. Image Not Found
- If `openvoiceos/ovos-core:latest` fails to pull, use `smartgic/ovos-core:latest` or build your own image as in this stack.

### 2. Timezone TypeError
- If you see `TypeError: string indices must be integers, not 'str'` in OVOS logs, ensure the `TZ` environment variable is set in the `ovos` service.

### 3. Messagebus Connection Refused
- Ensure both `websocket` and `message_bus_client` sections in `mycroft.conf` use the correct values as above.
- Confirm both services are on the same Docker network.
- Use the healthcheck and `depends_on` as in the Compose file.
- Ensure the `ovos` service has the correct `MESSAGEBUS_*` environment variables set in Compose (these take precedence for the client).

### 4. File Permissions (Windows)
- If you see `PermissionError` for `/home/ovos/.local/state`, run:
   ```powershell
   icacls ".\ovos_config\data" /grant Everyone:(OI)(CI)F /T
   icacls ".\ovos_config\config" /grant Everyone:(OI)(CI)F /T
   ```

### 5. Python/WebSocket Issues
- If Python test scripts fail silently, check for:
  - Version mismatches in `websocket-client` (pin to `0.57.0` in `requirements.txt`)
  - Avoid using `websocket.enableTrace(True)` in test scripts (can cause silent crashes)
- Use provided test scripts (`test_tcp.py`, `test_ws_minimal.py`) to verify connectivity.

### 6. Dependency Build Failures
- If you see errors about `swig` or `libfann-dev` missing, ensure these are installed in your Dockerfile:
   ```Dockerfile
   RUN apt-get update && \
       apt-get install -y --no-install-recommends tini build-essential libglib2.0-0 libsm6 libxext6 libxrender-dev swig libfann-dev && \
       rm -rf /var/lib/apt/lists/*
   ```

---

## Testing Connectivity
- To test OVOS <-> messagebus connection:
   ```powershell
   docker-compose -f docker-compose.ai.yml exec ovos python3 /home/ovos/ovos_test_connection.py
   ```
- To check messagebus health:
   ```powershell
   docker-compose -f docker-compose.ai.yml exec ovos curl -v http://ovos_messagebus:8181/core
   ```

---

## Resetting the OVOS Environment
If you need to start fresh:
1. Remove all OVOS-related Docker images:
   ```powershell
   docker rmi custom-ovos-core:latest smartgic/ovos-core:0.1.0 smartgic/ovos-core:latest smartgic/ovos-messagebus:latest
   ```
2. Delete the config/data directories:
   ```powershell
   Remove-Item -Path ".\ovos_config" -Recurse -Force
   ```
3. Remove the Docker network:
   ```powershell
   docker network rm ovos_network
   ```
4. Recreate the Compose services and config as above.

---

## References
- See `docker-compose.ai.yml` for the most up-to-date, detailed logs and troubleshooting notes.
- All test scripts and troubleshooting tools are in the workspace root.

---

*Last updated: May 14, 2025*