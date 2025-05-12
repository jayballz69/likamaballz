# OpenVoiceOS (OVOS) Docker Compose Setup Guide

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
Located at `ovos_config/config/mycroft.conf` on the host and mounted into both `ovos_messagebus` and `ovos` containers at `/home/ovos/.config/mycroft/mycroft.conf`.

**Key Sections:**
```json
{
  "lang": "en-us",
  "log_level": "DEBUG",
  "websocket": {                // Used by ovos_messagebus to configure its SERVER
    "host": "0.0.0.0",          // Server binds to all interfaces in its container
    "port": 8181,
    "route": "/core",           // Server listens on this route
    "ssl": false
  },
  "message_bus_client": {       // Used by ovos-core CLIENT as a fallback
    "host": "ovos_messagebus",  // Client targets the ovos_messagebus service name
    "port": 8181,
    "route": "/core",           // Client connects to this specific route
    "ssl": false
  },
  "gui_websocket": {            // For ovos-core's own GUI server endpoint
    "host": "0.0.0.0",
    "port": 8181,               // Internal port for GUI server
    "route": "/gui",
    "ssl": false
  },
  "enclosure": {
    "module": "ovos-PHAL-plugin-shell"
  },
  "stt": {
    "module": "ovos-stt-plugin-wyoming",
    "ovos-stt-plugin-wyoming": {
      "host": "whisper",
      "port": 10300
    }
  },
  "tts": {
    "module": "ovos-tts-plugin-coqui",
    "ovos-tts-plugin-coqui": {
      "host": "http://xtts:5002",
      "voice": "Claribel Dervla",
      "lang": "en",
      "api_path": "api/tts"
    }
  }
  // ...other sections as needed
}
```
- **For `ovos_messagebus` (Server):** This service reads the `websocket` section to configure its own server. `host` should be `"0.0.0.0"` to listen on all interfaces within its container, and `route` must be `"/core"` for the healthcheck and clients to connect correctly.
- **For `ovos` (Core Client):** This service primarily uses the `MESSAGEBUS_HOST`, `MESSAGEBUS_PORT`, and `MESSAGEBUS_ROUTE` environment variables set in `docker-compose.ai.yml` for its connection parameters. The `message_bus_client` section in `mycroft.conf` serves as a fallback. The key is consistency in targeting `host: "ovos_messagebus"`, `port: 8181`, and `route: "/core"`.
- **Configuration Precedence:**
  1. Explicit arguments to `MessageBusClient()`
  2. Environment variables (`MESSAGEBUS_HOST`, etc.)
  3. `mycroft.conf` file (`message_bus_client` section)
  4. Internal defaults

---

## Building and Running
1. **Build the custom OVOS image:**
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

*Last updated: May 12, 2025*