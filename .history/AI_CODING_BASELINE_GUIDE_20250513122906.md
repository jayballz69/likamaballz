# AI Coding Baseline Guide

This document defines the baseline rules and best practices that all AI agents, assistants, or automated code generation tools must follow when contributing to this project. **This guide must be referenced and adhered to whenever writing or reviewing any new code.**

---

## 1. Configuration Consistency
- Always use the Docker Compose service name (e.g., `ovos_messagebus`) for all inter-container host references in configuration files.
- Never use `0.0.0.0` or a static container IP for inter-container communication in Docker Compose.
- Ensure all critical configuration sections (such as `websocket` and `message_bus_client` in `mycroft.conf`) match the canonical examples in the setup guide.

## 2. Environment Variables
- Set all required environment variables in `docker-compose.ai.yml` as specified in the setup guide.
- Do not override critical environment variables with hardcoded values in code or scripts.

## 3. Volume Mounts and Permissions
- Always mount configuration and data directories as described in the setup guide.
- Ensure permissions are set so containers can read/write as needed, especially on Windows hosts.

## 4. Healthchecks and Dependencies
- Use `depends_on` and healthchecks in Docker Compose to ensure service startup order and readiness.
- Never remove or bypass healthchecks for critical services.

## 5. Version Pinning
- Pin Python and package versions (e.g., `websocket-client==0.57.0`) as required for compatibility.
- Do not upgrade or change pinned versions without explicit review and testing.

## 6. Testing and Verification
- Always provide or update test scripts to verify connectivity and service health after changes.
- Run all relevant tests after making changes to configuration or code.

## 7. Documentation
- Update the setup guide and this baseline guide with any new rules or changes to the stack.
- Reference this guide in all code reviews and when writing new code: **"See AI_CODING_BASELINE_GUIDE.md for required practices."**

---

**This guide is mandatory. All new code, configuration, and documentation must comply with these rules.**
