# OVOS Docker Setup Troubleshooting and Best Practices (2025-05-12)

## Summary
This guide documents the key issues, solutions, and best practices for running OpenVoiceOS (OVOS) in Docker as part of a home automation stack. It is based on real troubleshooting experience and is intended to help you avoid common pitfalls and quickly achieve a reliable setup.

---

## Key Issues & Solutions

### 1. Persistent "Connection Refused" from ovos-core to ovos_messagebus
- **Symptoms:** ovos-core logs show repeated connection errors to the messagebus, even though direct network tests (TCP, curl, WebSocket) succeed.
- **Root Cause:** ovos-core's `MessageBusClient()` (when called with no arguments) reads connection parameters from the `websocket` section of `mycroft.conf` if environment variables are not fully overriding. If this section is set for the server (e.g., `host: 0.0.0.0`), the client will fail to connect.
- **Solution:**
  - For the **messagebus server** (ovos_messagebus), set `"host": "0.0.0.0"` in the `websocket` section of `mycroft.conf`.
  - For the **ovos-core client**, set `"host": "ovos_messagebus"` (the Docker service name) in the `websocket` section, or ensure the correct `MESSAGEBUS_HOST`, `MESSAGEBUS_PORT`, and `MESSAGEBUS_ROUTE` environment variables are set in the ovos container.
  - **Best Practice:** Use environment variables for the client, and only use the config as a fallback.

### 2. Plugin and Dependency Issues
- **Symptoms:** Build failures due to missing or incompatible plugins (e.g., ovos_padatious, ovos-ww-plugin-vosk).
- **Solution:**
  - Pin `websocket-client==0.57.0` in requirements.txt for compatibility.
  - Add all required OVOS plugins and dependencies to `requirements.txt`.
  - Install system dependencies (e.g., `swig`, `libfann-dev`) in the Dockerfile as needed.

### 3. Docker Build and Runtime Issues (Windows)
- **Symptoms:** Stuck builds, permission errors, or Docker Desktop hangs.
- **Solution:**
  - Use `docker system prune` and restart Docker Desktop to resolve stuck builds.
  - Ensure correct file and directory permissions in the Dockerfile (e.g., `chown` for `/home/ovos/.local/state`).

---

## Step-by-Step Setup (Recommended)

1. **Prepare Configs:**
   - `ovos_config/config/mycroft.conf` (shared by both ovos_messagebus and ovos) should have a `websocket` section for the **server**:
     ```json
     {
       "websocket": {
         "host": "0.0.0.0",
         "port": 8181,
         "route": "/core",
         "ssl": false
       }
     }
     ```
   - This allows the ovos_messagebus server to bind to all interfaces. The ovos-core client will use its environment variables (`MESSAGEBUS_HOST`, `MESSAGEBUS_PORT`, `MESSAGEBUS_ROUTE`) to connect. If those are not set, you may add a `message_bus_client` section for fallback.

2. **Update requirements.txt:**
   - Include all required OVOS core packages and plugins.
   - Pin `websocket-client==0.57.0`.

3. **Build Custom Docker Image:**
   - Use a Dockerfile that installs all system and Python dependencies.
   - Example: `ovos-docker/Dockerfile.custom-ovos-core`.

4. **Use Docker Compose:**
   - Ensure `ovos_messagebus` and `ovos` are on the same Docker network.
   - Set up healthchecks for the messagebus.
   - Mount config and data volumes as needed.

5. **Test Connectivity:**
   - Use a test script (e.g., `ovos_test_connection.py`) to verify messagebus connectivity from within the ovos container.
   - Check logs for successful skill loading and absence of connection errors.

6. **Troubleshooting:**
   - If you see connection errors, check both environment variables and the `websocket` section in `mycroft.conf`.
   - Use direct WebSocket and MessageBusClient tests to isolate network vs. config issues.
   - Prune Docker system and restart Docker Desktop if builds hang (on Windows).

---

## Files to Backup
- `docker-compose.ai.yml` (and other compose files)
- `ovos-docker/Dockerfile.custom-ovos-core`
- `ovos-docker/requirements.txt`
- `ovos_config/config/mycroft.conf`
- `ovos_test_connection.py`
- Any custom skills or config data in `ovos_config/`

---

## GitHub Push Instructions
1. Commit all relevant files:
   ```sh
   git add docker-compose.ai.yml ovos-docker/Dockerfile.custom-ovos-core ovos-docker/requirements.txt ovos_config/config/mycroft.conf ovos_test_connection.py
   git commit -m "Restore and document working OVOS Docker setup with troubleshooting guide"
   git push
   ```
2. Ensure `.gitignore` does not exclude these files.

---

## Final Notes
- Always check both environment variables and config files for connection parameters.
- Use test scripts to verify connectivity before troubleshooting deeper.
- Document any changes or fixes for future reference.

---

For more details, see the in-file troubleshooting log in `docker-compose.ai.yml`.
