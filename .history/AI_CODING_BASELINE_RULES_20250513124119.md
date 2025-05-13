# Stack Management & AI Collaboration Baseline Guide

> **Rule:** This guide must be referenced in all relevant code, configuration, and documentation files, and in all code reviews. Add a comment or note: "See STACK_MANAGEMENT_AI_BASELINE_GUIDE.md for required practices."

This document defines the baseline rules and best practices that all AI agents, assistants, or automated code generation tools must follow when contributing to this project. **This guide must be referenced and adhered to whenever writing or reviewing any new code or documentation for any service in the stack.**

---

## 1. Configuration Consistency
- Always use the Docker Compose service name (e.g., `ovos_messagebus`, `ollama`, `whisper`, `xtts`, etc.) for all inter-container host references in configuration files or environment variables.
- For a **server process inside a container that needs to listen for incoming connections** (e.g., a web server, a database, or `ovos_messagebus`), its `host` configuration should typically be set to `0.0.0.0` to bind to all available network interfaces within its container, making it accessible via its service name from other containers.
- Ensure all critical configuration sections for each service match the canonical examples provided in its dedicated setup guide (e.g., `[ServiceName]_SETUP_GUIDE.md`).

## 2. Environment Variables
- Set all required environment variables for each service in the relevant `docker-compose.*.yml` file as specified in the service's setup guide.
- Do not override critical, Compose-defined environment variables with hardcoded values in application code or entrypoint scripts unless explicitly documented and understood.

## 3. Volume Mounts and Permissions
- Always mount configuration and data directories for each service as described in its setup guide, clearly distinguishing between read-only (`:ro`) and read-write mounts.
- Modifications to files on host-mounted volumes directly affect the containers. AI agents must clearly state if they intend to modify files in these mounted directories and explain the impact.
- Ensure host directory permissions (especially on Windows, e.g., using `icacls`) and in-Dockerfile permissions (`chown`, `chmod` for the container user) are correctly set to allow necessary read/write access for each service.

## 4. Healthchecks and Dependencies
- Utilize `depends_on` (with `condition: service_healthy` where applicable) and robust `healthchecks` in Docker Compose to manage service startup order and ensure dependencies are truly ready.
- Healthcheck `test` commands should accurately reflect the service's ability to perform its core function (e.g., responding on a specific port/path, process status). Avoid healthchecks that always pass (e.g., ending with `|| true`) for critical services unless the reason is well-documented.

## 5. Version Pinning
- For stability and reproducibility, pin versions of base Docker images (e.g., `python:3.11-slim`), application versions (e.g., `smartgic/ovos-core:0.1.0`), and key software packages/libraries (e.g., in `requirements.txt`).
- Do not upgrade or change pinned versions without explicit review, testing (ideally on a separate branch), and documentation of the change and its impact.

## 6. Testing and Verification
- For each service, provide or update simple test scripts or manual verification procedures to confirm core functionality, health, and connectivity to its dependencies after any configuration or code changes.
- Always run relevant tests after making changes.

## 7. Documentation
- For **each distinct service/container** in the stack, create and maintain:
    - A `[ServiceName]_SETUP_GUIDE.md` detailing its purpose, configuration specifics, volume mounts, exposed ports, and any unique setup steps.
    - A `[ServiceName]_TROUBLESHOOTING_GUIDE.md` (or a dedicated section within its setup guide, or within the main troubleshooting log in the `docker-compose.*.yml` file for that service) documenting common issues, diagnostic commands, and known fixes.
- This overarching 'Stack Management & AI Collaboration Baseline Guide' must be referenced in all service-specific documentation and code reviews.

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

## 18. Standardized Logging Practices
- **Console Output:** Ensure all containerized applications log to `stdout` and `stderr` to be easily captured by `docker logs <container_name>`. Avoid logging only to internal files unless absolutely necessary and documented.
- **Log Levels:** Utilize configurable log levels (e.g., DEBUG, INFO, WARNING, ERROR) for each service. Document how to change the log level (e.g., via environment variable or config file) in the service's setup guide. Default to `INFO` for production-like stability, use `DEBUG` for troubleshooting.
- **Structured Logging (Optional):** Where possible, encourage structured logging (e.g., JSON format) for easier parsing and analysis by log management tools if you implement them later.

## 19. Network Design and Port Management
- **Explicit Networks:** Define explicit Docker bridge networks in your `docker-compose.*.yml` files for groups of related services (e.g., `ovos_network`, `monitoring_network`) rather than relying solely on the default bridge network. This improves isolation and service discovery predictability.
- **Port Conflicts:** Before assigning host ports in `ports:` mappings, check for existing port usage on the host to avoid conflicts. Document all exposed host ports clearly.
- **Inter-Service Dependencies:** Document which services need to communicate with each other and on which internal ports/routes in their respective setup guides.

## 20. Data Persistence and Backup Strategy
- **Volume Strategy:** Clearly define for each service which data is ephemeral and which requires persistent storage via named Docker volumes or host-mounted directories. Document this in the service's setup guide and the main "Backup and Restore" section of `docker-compose.ai.yml`.
- **Backup Reminders:** Reiterate that after significant stable changes, the AI should prompt for a backup of both version-controlled files (Git) and persistent data volumes.

## 21. Update and Upgrade Procedures
- **Image Updates:** Prefer specific version tags for images over `latest` for critical services to ensure predictability. Document the process for checking for updates and applying them (e.g., `docker-compose pull <service_name>`, then `docker-compose up -d --force-recreate <service_name>`).
- **Application/Library Updates:** Changes to internal libraries (e.g., in `requirements.txt`) should be tested on a branch before merging and deploying.
- **Breaking Changes:** Note any known breaking changes between versions of services or their key dependencies in the relevant troubleshooting or setup guides.

## 22. Post-Stability Actions (Including Backups)
1. Once a new configuration, build, or set of changes has been thoroughly tested and confirmed stable by the user, the user will inform the AI assistant.
2. Upon this confirmation, the AI assistant **must remind the user to perform a comprehensive backup.**
3. This reminder should include:
    - Ensuring all code, configuration files (`docker-compose.ai.yml`, `mycroft.conf`, `Dockerfile`, `requirements.txt`, `*.md` guides, etc.) are committed to Git with a clear version tag or commit message.
    - Performing a backup of all persistent data volumes as outlined in the "Backup and Restore" section of `docker-compose.ai.yml` (this includes `./ovos_config/config`, `./ovos_config/data`, and data for other services like Frigate, Ollama, XTTS, etc.). This might involve stopping relevant containers to ensure data consistency during the copy.
    - Optionally, tagging the newly built stable Docker images (e.g., `custom-ovos-core:stable-YYYYMMDD`) and considering pushing them to a private Docker registry if applicable.

---

**This guide is mandatory. All new code, configuration, and documentation must comply with these rules.**
