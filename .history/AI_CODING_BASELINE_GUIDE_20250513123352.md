# AI Coding Baseline Guide

> **Rule:** This guide must be referenced in all relevant code, configuration, and documentation files, and in all code reviews. Add a comment or note: "See AI_CODING_BASELINE_GUIDE.md for required practices."

This document defines the baseline rules and best practices that all AI agents, assistants, or automated code generation tools must follow when contributing to this project. **This guide must be referenced and adhered to whenever writing or reviewing any new code.**

---

## 1. Configuration Consistency
- For **client connections** targeting another service within Docker Compose, always use the Docker Compose service name (e.g., `ovos_messagebus`). Avoid static container IPs.
- For a **server process inside a container that needs to listen for incoming connections** (e.g., `ovos_messagebus` itself, or `ovos-core`'s GUI WebSocket), its `host` configuration should be set to `0.0.0.0` to bind to all available network interfaces within its container.
- Ensure all critical configuration sections (such as `websocket` and `message_bus_client` in `mycroft.conf`) match the canonical examples in the setup guide.

## 2. Environment Variables
- Set all required environment variables in `docker-compose.ai.yml` as specified in the setup guide.
- Do not override critical environment variables with hardcoded values in code or scripts.

## 3. Volume Mounts and Permissions
- Always mount configuration and data directories as described in the setup guide.
- Modifications to files on host-mounted volumes directly affect the containers. AI agents must clearly state if they intend to modify files in these mounted directories (e.g., `./ovos_config/config/mycroft.conf`) and explain the impact.
- For Windows hosts, refer to `icacls` commands documented in the main troubleshooting log for granting necessary permissions to Docker volumes. For custom Docker images, ensure in-Dockerfile `chown` and `chmod` commands are used to set correct user ownership and permissions for application directories (e.g., `/home/ovos/.local/state`).

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

## 8. Version Control (Git) Discipline
- **Commit All Changes:** All modifications to code, configuration files (Docker Compose, `mycroft.conf`, `requirements.txt`, Dockerfiles), documentation, and guides made by AI or human operators **must be committed to Git with clear, descriptive messages** detailing the change and its purpose.
- **Review Before Commit:** Human review of AI-generated changes is **mandatory** before committing, especially for critical configuration files or code. Use `git diff` to understand the exact changes.
- **Branching for Experiments:** For significant changes, experiments, or troubleshooting steps that might be reverted, use Git branches. Test thoroughly on a branch before considering a merge to the main working branch.
- **No Force Pushing:** Avoid `git push --force` on shared branches unless absolutely necessary and coordinated, as it can overwrite history.
- **Maintain `.gitignore`:** Ensure a comprehensive `.gitignore` file is used to exclude local state, logs, IDE settings, secrets, large data/model files, and other non-repository items. Periodically review and update it.

## 9. AI Interaction Protocol & Change Management
- **Explicit Confirmation for Destructive Actions:** AI assistants **must always seek explicit user confirmation** before performing any potentially destructive actions. This includes, but is not limited to:
    - Deleting files or directories (especially in mounted volumes).
    - Removing Docker images, containers, volumes, or networks.
    - Overwriting existing configuration files without backup.
- **State Intent and Preview Changes:** Before applying changes, the AI should clearly state:
    - What it intends to do.
    - Which files or services will be affected.
    - The expected outcome.
    - If possible, provide a preview (like a diff) of code or configuration changes.
- **Incremental Changes:** AI should prefer making small, atomic, and incremental changes. Each change should be testable and easy to review and revert if necessary.
- **Backup Critical Files:** Before an AI modifies a critical configuration file (e.g., `mycroft.conf`, `docker-compose.ai.yml`), it should prompt the user to ensure a backup is made (e.g., `mycroft.conf` to `mycroft.conf.bak`) or offer to create one.
- **Log AI Actions:** Briefly note significant actions taken by an AI (e.g., "Copilot updated `mycroft.conf` to change `websocket.host`") in the relevant troubleshooting log if not part of a direct commit message.

## 10. Secrets Management
- **No Hardcoded Secrets:** Credentials, API keys, or other secrets must **never** be hardcoded into configuration files, Dockerfiles, scripts, or committed to the Git repository.
- **Use Environment Variables & Externalized Config:** Prefer Docker secrets, environment variables passed at runtime (e.g., via a non-committed `.env` file referenced by Docker Compose), or secure vault solutions for managing secrets.

---

**This guide is mandatory. All new code, configuration, and documentation must comply with these rules.**
