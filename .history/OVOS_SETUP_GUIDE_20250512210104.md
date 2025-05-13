# OVOS Docker Setup Guide (2025-05-12)

## Overview
This guide provides a concise, step-by-step process for setting up OpenVoiceOS (OVOS) in Docker, including best practices for configuration, plugin management, and troubleshooting. It reflects lessons learned from real-world issues and is designed for reliability and clarity.

---

## 1. Prerequisites
- Docker and Docker Compose installed
- (Windows) Docker Desktop with WSL2 backend recommended
- Sufficient disk space for models and data

---

## 2. File Structure
- `docker-compose.ai.yml` — Compose file for AI/ML services (including ovos and ovos_messagebus)
- `ovos-docker/Dockerfile.custom-ovos-core` — Custom Dockerfile for ovos-core
- `ovos-docker/requirements.txt` — Python dependencies for ovos-core
- `ovos_config/config/mycroft.conf` — OVOS configuration file
- `ovos_test_connection.py` — Test script for messagebus connectivity

---

## 3. Configuration
### mycroft.conf (Client Example)
```json
{
  "websocket": {
    "host": "ovos_messagebus",
    "port": 8181,
    "route": "/core",
    "ssl": false
  }
}
```
- For the messagebus server, use `"host": "0.0.0.0"`.
- For the ovos-core client, use `"host": "ovos_messagebus"` (the Docker service name).
- Prefer environment variables for the ovos-core client:
  - `MESSAGEBUS_HOST=ovos_messagebus`
  - `MESSAGEBUS_PORT=8181`
  - `MESSAGEBUS_ROUTE=/core`

---

## 4. Building and Running
1. **Update requirements.txt**
   - Include all required OVOS core packages and plugins
   - Pin `websocket-client==0.57.0`
2. **Build the ovos-core image**
   ```sh
   docker-compose -f docker-compose.ai.yml build ovos
   ```
3. **Start the stack**
   ```sh
   docker-compose -f docker-compose.ai.yml up -d
   ```
4. **Check logs**
   ```sh
   docker-compose -f docker-compose.ai.yml logs --tail=100 ovos
   ```
5. **Test messagebus connectivity**
   ```sh
   docker-compose -f docker-compose.ai.yml exec ovos python3 /ovos/ovos_test_connection.py
   ```

---

## 5. Troubleshooting
- If you see "Connection Refused" errors:
  - Check that the ovos_messagebus container is healthy and listening on `/core`.
  - Confirm the ovos-core container is using the correct environment variables and/or `mycroft.conf`.
  - Use the test script to verify direct connectivity.
  - Prune Docker system and restart Docker Desktop if builds hang (on Windows).
- If skills or plugins fail to load:
  - Ensure all dependencies are listed in `requirements.txt`.
  - Install system dependencies in the Dockerfile as needed.

---

## 6. Backup
Backup these files/directories:
- `docker-compose.ai.yml`
- `ovos-docker/Dockerfile.custom-ovos-core`
- `ovos-docker/requirements.txt`
- `ovos_config/config/mycroft.conf`
- `ovos_test_connection.py`
- `ovos_config/` (for skills and data)

---

## 7. GitHub Push
1. Commit all relevant files:
   ```sh
   git add docker-compose.ai.yml ovos-docker/Dockerfile.custom-ovos-core ovos-docker/requirements.txt ovos_config/config/mycroft.conf ovos_test_connection.py OVOS_TROUBLESHOOTING_GUIDE.md
   git commit -m "Update OVOS Docker setup and troubleshooting guide for reliable deployment"
   git push
   ```
2. Ensure `.gitignore` does not exclude these files.

---

For more details, see `OVOS_TROUBLESHOOTING_GUIDE.md` and the troubleshooting log in `docker-compose.ai.yml`.