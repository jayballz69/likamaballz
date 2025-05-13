# AI Coding Baseline Rules

> **Rule:** This guide must be referenced in all relevant code, configuration, and documentation files, and in all code reviews. Add a comment or note: "See AI_CODING_BASELINE_RULES.md for required practices."

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
- Reference this guide in all code reviews and when writing new code: **"See AI_CODING_BASELINE_RULES.md for required practices."**

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

## 11. Rollback and Recovery
- Always ensure you know how to roll back changes. Use `git revert`, restore from backups, or use Docker volume snapshots as appropriate.
- Before making major or potentially breaking changes, ensure a backup or restore point exists.

## 12. Automated Checks and Enforcement
- Use automated tools for linting, formatting, and validating configuration files (e.g., JSON/YAML linters, Docker Compose validators, pre-commit hooks).
- Automated checks should run before merging or deploying changes.

## 13. AI/Human Collaboration Etiquette
- All AI-generated suggestions must be open to human review.
- Humans are encouraged to leave comments or feedback for the AI (or future contributors) directly in code reviews or commit messages.

## 14. Change Log Maintenance
- Maintain a `CHANGELOG.md` or similar file to track significant changes, especially those made by AI, for transparency and traceability.

## 15. Security Review
- Periodically review dependencies and Docker images for vulnerabilities (e.g., using `pip-audit`, `docker scan`, or similar tools).
- Update dependencies and images responsibly, following version pinning and review rules.

## 16. AI Model/Tool Versioning
- If multiple AI tools or Copilot versions are used, specify which version or model was used for a given change (if possible), especially for major updates or migrations.

## 17. Accessibility and Readability
- Write clear, concise, and accessible documentation and code comments so both humans and AI can easily understand the intent and function of all changes.

---

## 18. Post-Stability Actions (Including Backups)
1. Once a new configuration, build, or set of changes has been thoroughly tested and confirmed stable by the user, the user will inform the AI assistant.
2. Upon this confirmation, the AI assistant **must remind the user to perform a comprehensive backup.**
3. This reminder should include:
    - Ensuring all code, configuration files (`docker-compose.ai.yml`, `mycroft.conf`, `Dockerfile`, `requirements.txt`, `*.md` guides, etc.) are committed to Git with a clear version tag or commit message.
    - Performing a backup of all persistent data volumes as outlined in the "Backup and Restore" section of `docker-compose.ai.yml` (this includes `./ovos_config/config`, `./ovos_config/data`, and data for other services like Frigate, Ollama, XTTS, etc.). This might involve stopping relevant containers to ensure data consistency during the copy.
    - Optionally, tagging the newly built stable Docker images (e.g., `custom-ovos-core:stable-YYYYMMDD`) and considering pushing them to a private Docker registry if applicable.

---

**This guide is mandatory. All new code, configuration, and documentation must comply with these rules.**
