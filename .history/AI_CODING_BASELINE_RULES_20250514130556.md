# AI_CODING_BASELINE_RULES

## 0. In-File Banner (Top Priority)
<!-- id: BNR-01, priority: MUST, tags: [documentation,headers] -->
- MUST: Every code, configuration, and documentation file **must** include the following comment at the very top:
  "See AI_CODING_BASELINE_RULES.md for required practices."
- MUST: When creating **any** new file in the repository, add the banner comment before any other content.
---

### How to Read This Guide
This document uses RFC 2119 keywords (MUST, SHOULD, MUST NOT, MAY) to indicate rule priorities.¹  
Any deviation from a MUST-level rule must follow **Section 28: Handling Exceptions and Deviations to These Rules**.  

### Overarching Principle: Pragmatic Application & Benefit-Effort Assessment
- MUST: For any proposed new rule, adoption of a new tool/process, or significant effort driven by these guidelines, the **anticipated benefit versus required effort** (for both initial implementation and ongoing maintenance) **MUST** be assessed and documented.
- SHOULD: Solutions and efforts **SHOULD** be proportionate to the problem they solve and the tangible value they bring to the project's stability, security, maintainability, or efficiency.
- MAY: This benefit-effort assessment **MAY** be used as part of the justification when requesting an exception to a `SHOULD`-level rule as per Section 28.

## Table of Contents
1. [Configuration Consistency](#1-configuration-consistency)
2. [Environment Variables](#2-environment-variables)
3. [Volume Mounts and Permissions](#3-volume-mounts-and-permissions)
4. [Healthchecks and Dependencies](#4-healthchecks-and-dependencies)
5. [Version Pinning](#5-version-pinning)
6. [Testing and Verification](#6-testing-and-verification)
7. [Documentation](#7-documentation)
8. [Version Control (Git) Discipline](#8-version-control-git-discipline)
9. [AI Interaction Protocol & Change Management](#9-ai-interaction-protocol--change-management)
10. [Secrets Management](#10-secrets-management)
11. [Rollback and Recovery](#11-rollback-and-recovery)
12. [Automated Checks and Enforcement](#12-automated-checks-and-enforcement)
13. [AI/Human Collaboration Etiquette](#13-aihuman-collaboration-etiquette)
14. [Change Log Maintenance](#14-change-log-maintenance)
15. [Security Review](#15-security-review)
16. [AI Model/Tool Versioning](#16-ai-modeltool-versioning)
17. [Accessibility and Readability](#17-accessibility-and-readability)
18. [Standardized Logging Practices](#18-standardized-logging-practices)
19. [Network Design and Port Management](#19-network-design-and-port-management)
20. [Data Persistence and Backup Strategy](#20-data-persistence-and-backup-strategy)
21. [Update and Upgrade Procedures](#21-update-and-upgrade-procedures)
22. [Post-Stability Actions (Including Backups)](#22-post-stability-actions-including-backups)
23. [General Development Principles for Custom Code & Services](#23-general-development-principles-for-custom-code--services)
24. [Appendix: Example Automation Scripts & Templates](#appendix-example-automation-scripts--templates)
25. [Visualizations & Diagrams](#visualizations--diagrams)
26. [Periodic Review & Update Schedule](#periodic-review--update-schedule)
27. [Designing for Offline Capability & Portability](#27-designing-for-offline-capability--portability)
28. [Exceptions & Deviations (EXC-01)](#28-handling-exceptions-and-deviations-to-these-rules)
29. [Conflict Resolution Matrix (CRM-01)](#29-conflict-resolution-matrix)

## Quick Reference: Top 10 MUSTs
- MUST: Include the in-file banner comment at the top of every file: "See AI_CODING_BASELINE_RULES.md for required practices." (Section 0)
- MUST: Use Docker Compose service names for all inter-container host references (Section 1)
- MUST: Set all required environment variables for each service in Compose (Section 2)
- MUST: Mount configuration and data volumes correctly with proper permissions (Section 3)
- MUST: Define and use robust healthchecks; avoid always-passing checks (Section 4)
- MUST: Pin versions for base images and key dependencies (Section 5)
- MUST: Never hardcode credentials or secrets; use Docker secrets or environment variables (Section 10)
- MUST: Seek explicit user confirmation before any destructive action (Section 9)
- MUST: Prioritize and adhere to official documentation (Section 9)
- MUST: Document any deviations through the exception process (Section 28)

> **Rule:** This guide must be referenced in all relevant code, configuration, and documentation files, and in all code reviews. Add a comment or note: "See AI_CODING_BASELINE_RULES.md for required practices."

This document defines the baseline rules and best practices that all AI agents, assistants, or automated code generation tools must follow when contributing to this project. **This guide must be referenced and adhered to whenever writing or reviewing any new code or documentation for any service in the stack. It forms the foundation for how this project is managed and developed.**

*For detailed setup and troubleshooting for individual services (e.g., OVOS, XTTS, Frigate), please refer to their specific `[ServiceName]_SETUP_GUIDE.md` and `[ServiceName]_TROUBLESHOOTING_GUIDE.md` files located in the project's documentation directory (typically accessible via the main project README.md).*

---

## Reviewer Checklist

| Review Item                        | Verified |
|------------------------------------|:--------:|
| AI-generated content tagged        |   [ ]    |
| Non-root container verified        |   [ ]    |
| Healthchecks & dependencies        |   [ ]    |
| Version pinning verified           |   [ ]    |
| Documentation updated              |   [ ]    |
| Rollback/Recovery scenario defined |   [ ]    |
| Security/vulnerability scan run    |   [ ]    |
| Test coverage adequate             |   [ ]    |
| Accessibility (WCAG compliance)    |   [ ]    |
| Benchmark/performance checked      |   [ ]    |
| Secrets managed securely           |   [ ]    |

---

## 1. Configuration Consistency
<!-- id: CFG-01, priority: MUST, tags: [config] -->
- MUST: Always use the Docker Compose service name (e.g., `ovos_messagebus`) for all inter-container host references.
- SHOULD: Server processes SHOULD bind to `0.0.0.0` unless a specific interface is documented.
- SHOULD: Ensure all critical configuration sections match the canonical examples in `[ServiceName]_SETUP_GUIDE.md`, except under a documented exception.
- SHOULD: Namespace and document shared config file sections (e.g., `mycroft.conf`) per service in their setup guides.

## 2. Environment Variables
<!-- id: ENV-01, priority: MUST, tags: [environment] -->
- MUST: Set all required environment variables for each service in the relevant `docker-compose.*.yml` file as specified.
- MUST NOT: Override Compose-defined environment variables with hardcoded values in application code or entrypoint scripts unless explicitly documented.

## 3. Volume Mounts and Permissions
<!-- id: VOL-01, priority: MUST, tags: [volumes, permissions] -->
- MUST: Mount configuration and data directories exactly as described in each service’s setup guide, distinguishing read-only (`:ro`) vs. read-write.
- MUST: Clearly state in change previews if mounting or permission changes are intended.
- MUST: Ensure host and in-container permissions (`chmod`/`chown`) allow necessary access without granting excessive privileges.

---

## 4. Healthchecks and Dependencies
<!-- id: HC-01, priority: SHOULD, tags: [docker, healthchecks] -->
- SHOULD: Use `depends_on` with `condition: service_healthy` and robust healthcheck definitions. (see Conflict Resolution Matrix CRM-01)
- SHOULD: Prefer the exec form (`["CMD", …]`) over shell form for reliability.
- SHOULD: Tune `interval`, `timeout`, `retries`, and `start_period` to match service startup behavior.
- MUST NOT: Use always-passing healthchecks (e.g., ending in `|| true`) for critical services unless a documented exception exists. (see CRM-01)

## 5. Version Pinning
<!-- id: PIN-01, priority: SHOULD, tags: [docker, versioning] -->
- SHOULD: Pin base images, application versions, and key libraries (e.g., `python:3.11-slim`, `smartgic/ovos-core:0.1.0`).
- MUST: Document and test any version updates on a separate branch before merging.

## 6. Testing and Verification
<!-- id: TEST-01, priority: SHOULD, tags: [testing, verification] -->
- SHOULD: Provide test scripts or manual verification procedures for core functionality after changes.
- MUST: Run all relevant tests following modifications.
- SHOULD: Test on both Windows (Docker Desktop/WSL2) and native Linux hosts to catch cross-platform issues.

## 7. Documentation
<!-- id: DOC-01, priority: SHOULD, tags: [documentation] -->
- MUST: Maintain a `[ServiceName]_SETUP_GUIDE.md` and a `[ServiceName]_TROUBLESHOOTING_GUIDE.md` for each container.
- SHOULD: Reference this baseline guide in all service-specific documentation.
- SHOULD: Provide visual dependency diagrams (e.g., Mermaid, Graphviz) for complex stacks.
- SHOULD: Ensure documentation uses simple language and includes alt-text for images.

---

## 8. Version Control (Git) Discipline
<!-- id: VCS-01, priority: MUST, tags: [git,version-control] -->
- MUST: Commit all changes to code, configuration, and documentation with clear, descriptive messages following Conventional Commits.
- MUST: Require human review of AI-generated changes before commit; use `git diff` to inspect changes.
- SHOULD: Use branches for experiments and significant changes; test thoroughly on branches before merging.
- MUST NOT: Use `git push --force` on shared branches unless coordinated and documented. (see CRM-01)
- MUST: Maintain a comprehensive `.gitignore` and review it regularly.
- MUST: Pull latest changes before starting new work to avoid conflicts.
- MUST: Follow commit message format: summary line ~50 characters, body wrapped at 72 characters, using Conventional Commits.
- MUST: Enforce LF line endings for Linux files via `.gitattributes` and Git settings.
- MUST: Treat filenames, imports, and environment variable names as case-sensitive.
- SHOULD: Resolve merge conflicts by understanding all changes and testing thoroughly before finalizing.
- SHOULD: Use consistent branch naming conventions, e.g., `feature/<description>`, `fix/<issue-id>`, `docs/<topic>`, `chore/<task>`.

## 9. AI Interaction Protocol & Change Management
<!-- id: AIP-01, priority: MUST, tags: [ai,change-management] -->
- MUST: Seek explicit user confirmation before performing any destructive action.
- MUST: Clearly state intent, affected files/services, and expected outcomes before applying changes.
- MUST: Make changes incrementally and atomically; each change must be testable and reviewable.
- SHOULD: Prompt for backups of critical files before modification or advise user to back up large volumes.
- SHOULD: Log AI actions in commit messages or relevant logs with standardized tags (`AI-GENERATED`, `AI-REVIEWED`).
- MUST: Provide ready-to-use shell or CLI commands (e.g., PowerShell, Docker) formatted correctly for the user's environment to allow direct copy-paste execution.
- SHOULD: Automatically execute commands via the appropriate terminal tool (e.g., PowerShell) when the user has indicated such a preference.
- SHOULD: Ensure all generated commands use correct syntax for the target shell or tool (PowerShell, Docker CLI, bash) without requiring manual adjustments.
- **MUST: Prioritize and Adhere to Official Documentation (READMEs) for Setup, Configuration, and Troubleshooting:**
  - When tasked with integrating a new containerized service, configuring an existing one, or troubleshooting standard operational issues, the AI assistant (and human reviewer) **MUST** prioritize and diligently follow the instructions, default configurations, recommended environment variables, and volume mount strategies outlined in the **official README and primary documentation** for that specific service/image.
  - **Standard Setup and Configuration MUST faithfully reflect this official documentation.** AI assistants **MUST NOT** invent custom configuration parameters, deviate from documented setup procedures, or "get creative" with standard operational settings unless official documentation is missing, unclear, or a deviation is explicitly justified and approved (see rule below and Section 28).
  - **Fetching, Referencing, and Archiving Documentation:**
    - An attempt **MUST** first be made to locate and consult any locally archived official README or primary documentation for that service (e.g., within this project's `docs/[ServiceName]/` directory or linked from `[ServiceName]_SETUP_GUIDE.md`).
    - If a relevant local document is not available, is deemed insufficient, or might be outdated, the AI assistant (and human reviewer) **MUST** make reasonable efforts to find, cite (e.g., provide a URL), and consult the latest official online sources (e.g., Docker Hub page, GitHub repository, official project website).
    - Key information, setup procedures, and relevant excerpts from fetched official documentation **SHOULD** be used to update or create the project's corresponding `[ServiceName]_SETUP_GUIDE.md` and, where appropriate, a copy of the essential official document (or a link to a specific version/commit) **SHOULD** be archived locally for future reference (see Section 7 and Section 27).
  - **Justification for Deviation from Official Documentation:** Any proposed setup, configuration, or troubleshooting step that deviates from the clear guidance in the official documentation for a service **MUST** be explicitly highlighted, thoroughly justified (e.g., "Official README for X service suggests Y, but for integration with our Z service, we need to adapt it to Y-prime because..."), and approved as per **Section 28: Handling Exceptions and Deviations to These Rules**. The specific part of the official documentation being deviated from should be referenced.
- **MUST: Update Relevant Documentation Concurrently with Changes:**
  - When an AI assistant (or any contributor) proposes or implements changes to code, configuration, service behavior, dependencies, or operational procedures, they **MUST** also identify and make necessary updates to any relevant documentation to accurately reflect these changes.
  - This includes, but is not limited to:
    - `[ServiceName]_SETUP_GUIDE.md` (e.g., for new environment variables, changed port mappings, new setup steps, updated pinned versions).
    - `[ServiceName]_TROUBLESHOOTING_GUIDE.md` (e.g., if a change resolves a known issue, introduces new potential issues, or changes diagnostic steps).
    - The main `docker-compose.*.yml` troubleshooting logs (if relevant to a fix being implemented).
    - Code comments and function/module docstrings within the code itself.
    - This "AI_CODING_BASELINE_RULES.md" or the "CODING_STANDARDS_SUPPLEMENT.md" if a change impacts these guiding documents.
  - Proposed changes (e.g., in a Pull Request) **SHOULD** ideally include both the functional/configuration changes and the corresponding documentation updates together, or in closely related commits.
  - Human reviewers **MUST** verify that documentation has been appropriately updated as part of the review process for any significant code or configuration change.

## 10. Secrets Management
<!-- id: SEC-01, priority: MUST, tags: [secrets] -->
- MUST: Never hardcode credentials or secrets in code, configuration, or documentation.
- MUST: Use Docker secrets, environment variables, or external vaults for secret management.
- SHOULD: Define and document secret rotation intervals; rotate at least quarterly.
- SHOULD: Establish audit logging for secret access and changes.
- MUST: Have an emergency plan for secret revocation and rotation.

## 11. Rollback and Recovery
<!-- id: ROR-01, priority: MUST, tags: [rollback,recovery] -->
- MUST: Know rollback procedures (e.g., `git revert`, backup restore) before making significant changes.
- MUST: Ensure backups or restore points exist before breaking changes.
- SHOULD: Document rollback scenarios and examples in service-specific guides.

## 12. Automated Checks and Enforcement
<!-- id: AUTO-01, priority: SHOULD, tags: [automation,ci] -->
- SHOULD: Use linting, formatting, and validation tools (e.g., pre-commit hooks) before merges.
- MUST: Run automated checks on relevant files upon each change.
- SHOULD: Integrate commitlint or Husky to enforce Conventional Commits.
- MUST: Integrate commit message linting tools (e.g., commitlint) to enforce Conventional Commits.
- SHOULD: Instrument CI/CD to track build/test metrics and set alerts for failures.

## 13. AI/Human Collaboration Etiquette
<!-- id: AHC-01, priority: SHOULD, tags: [ai,collaboration] -->
- SHOULD: Always allow human review of AI-generated suggestions.
- SHOULD: Encourage human feedback in code reviews and commit messages.
- MUST: Document conflicting advice, decision process, and rationale in commits or guides.

## 14. Change Log Maintenance
<!-- id: CHG-01, priority: MUST, tags: [changelog] -->
- MUST: Maintain `CHANGELOG.md` to track significant changes.
- SHOULD: Note AI-made changes explicitly for transparency.

## 15. Security Review
<!-- id: SEC-REV-01, priority: SHOULD, tags: [security] -->
- SHOULD: Periodically scan dependencies and images for vulnerabilities (e.g., `pip-audit`, Trivy).
- SHOULD: Test updates on branches before merging.
- MUST: Run vulnerability scans using tools like Snyk or GitHub Advanced Security.
- MUST: Run containers as non-root users; document exceptions.
- MUST: Use Linux-based parent images; avoid Windows containers.

## 16. AI Model/Tool Versioning
<!-- id: MODEL-VER-01, priority: SHOULD, tags: [ai,versioning] -->
- SHOULD: Specify AI tool or model versions used for significant changes.

## 17. Accessibility and Readability
<!-- id: ACC-01, priority: SHOULD, tags: [accessibility] -->
- SHOULD: Write clear, concise documentation; strive for WCAG 2.1 compliance.
- SHOULD: Use automated accessibility tools (e.g., axe-core, Lighthouse).

## 18. Standardized Logging Practices
<!-- id: LOG-01, priority: SHOULD, tags: [logging] -->
- MUST: Log to stdout/stderr; avoid internal files unless documented.
- SHOULD: Use configurable log levels; default to INFO in production.
- SHOULD: Prefer structured logging (e.g., JSON) where feasible.

## 19. Network Design and Port Management
<!-- id: NET-01, priority: SHOULD, tags: [network] -->
- SHOULD: Define explicit Docker networks for related services.
- MUST: Check for host port conflicts before exposing.
- SHOULD: Document inter-service communication in setup guides.

## 20. Data Persistence and Backup Strategy
<!-- id: DATA-01, priority: MUST, tags: [data,persistence] -->
- MUST: Define ephemeral vs. persistent data per service; document in setup guides.
- SHOULD: Remind to backup version-controlled files and volumes after stable changes.

## 21. Update and Upgrade Procedures
<!-- id: UPG-01, priority: SHOULD, tags: [updates] -->
- SHOULD: Use specific version tags over `latest` for predictability.
- MUST: Test image and dependency updates on branches before merging.
- SHOULD: Document known breaking changes in troubleshooting guides.

## 22. Post-Stability Actions (Including Backups)
<!-- id: POST-01, priority: SHOULD, tags: [backup,post-deployment] -->
- MUST: Upon stability confirmation, remind user to backup code, configs, and volumes.

---

## 23. General Development Principles for Custom Code & Services

<!--
  The following sub-sections (23.1–23.8) are fully integrated for ease of reference and AI compliance. This content supersedes any separate supplement file.
-->

<!-- id: CQM-01, priority: MUST, tags: [code-quality,maintainability], last_reviewed: 2025-05-13 -->
### 23.1 Code Quality, Readability, and Maintainability
- MUST: Write clear, self-documenting code with meaningful identifiers and straightforward control flow.
- MUST: Adhere to language and framework-specific style guides (e.g., PEP 8 for Python) and enforce compliance via linters and formatters.
- SHOULD: Keep functions and methods small, focused on a single responsibility.
- SHOULD: Refactor duplicate or similar code to eliminate repetition and follow the DRY principle.
- SHOULD: Use comments judiciously to explain intent and rationale rather than restate code; include docstrings for public modules, classes, and methods.
- MAY: Provide illustrative code snippets for complex algorithms or patterns to aid understanding.
- MUST: Review and test code for readability and maintainability before merging.

<!-- id: DAP-01, priority: SHOULD, tags: [design,architecture], last_reviewed: 2025-05-13 -->
### 23.2 Design and Architecture Principles
- MUST: Design components to be modular with single responsibilities (SRP).
- SHOULD: Promote code reuse and reduce coupling through abstraction and interfaces (DIP, ISP).
- SHOULD: Design for extensibility (OCP) allowing new functionality with minimal changes.
- SHOULD: Implement and document design patterns (Factory, Observer, Strategy, Decorator) with rationale.
- SHOULD: Follow SOLID principles for flexible, maintainable design.
- SHOULD: Employ dependency injection to provide components with dependencies externally.

<!-- id: EH-01, priority: MUST, tags: [error-handling,robustness], last_reviewed: 2025-05-13 -->
### 23.3 Error Handling and Robustness
- MUST: Implement comprehensive error handling using language-appropriate constructs to catch and manage exceptions.
- MUST: Define and use custom exception types for application-specific error conditions.
- MUST: Log all exceptions and significant error states with sufficient context (stack trace, parameters).
- MUST: Rigorously validate all external inputs at component boundaries to prevent errors and vulnerabilities.

<!-- id: PERF-01, priority: SHOULD, tags: [performance,scalability], last_reviewed: 2025-05-13 -->
### 23.4 Performance and Scalability
- SHOULD: Choose efficient algorithms and data structures appropriate for task and data sizes.
- SHOULD: Utilize appropriate concurrency mechanisms (asyncio, threading, multiprocessing) for parallelism.
- SHOULD: Profile code to identify bottlenecks before optimizing critical paths.
- MUST: Manage system resources efficiently, ensuring proper cleanup of resources (context managers, finally blocks).
- SHOULD: Establish and rerun performance benchmarks after significant changes.

<!-- id: QA-01, priority: SHOULD, tags: [testing,qa], last_reviewed: 2025-05-13 -->
### 23.5 Testing and Quality Assurance
- MUST: Implement comprehensive unit tests covering new and modified code.
- MUST: Write integration tests for interactions between components or services.
- SHOULD: Aim for high test coverage of business logic and critical paths.
- MUST: Structure code to be easily testable (SRP, DI, limited global state).

<!-- id: SBP-01, priority: MUST, tags: [security], last_reviewed: 2025-05-13 -->
### 23.6 Security Best Practices
- MUST: Validate and sanitize all inputs from untrusted sources to prevent injection and traversal attacks.
- MUST: Enforce the principle of least privilege for processes and services.
- MUST: Regularly scan and update dependencies to patch known vulnerabilities.
- MUST: Protect sensitive data with encryption at rest and in transit, and avoid logging sensitive information.

<!-- id: CICD-02, priority: SHOULD, tags: [cicd,automation], last_reviewed: 2025-05-13 -->
### 23.7 CI/CD (Continuous Integration & Continuous Deployment)
- SHOULD: Automate build, test, and deployment processes through CI/CD pipelines.
- SHOULD: Maintain consistency between development, testing, and production environments.
- SHOULD: Integrate containerization and declarative configs to reduce environment drift.

<!-- id: PY-01, priority: SHOULD, tags: [python], last_reviewed: 2025-05-13 -->
### 23.8 Python-Specific Development Guidelines
- MUST: Adhere to PEP 8 style guide for Python code formatting.
- SHOULD: Use type hints for function arguments and return values where they improve clarity.
- MUST: Include docstrings for all public modules, classes, functions, and methods.
- SHOULD: Use linters (Flake8, Pylint) and formatters (Black, isort) via pre-commit hooks.
- SHOULD: Leverage Pythonic idioms (list comprehensions, context managers).
- SHOULD: Use Abstract Base Classes and decorators for interfaces and cross-cutting concerns.
- MUST: Catch specific exceptions and ensure resource cleanup with context managers.
- SHOULD: Utilize asyncio for I/O-bound concurrency and multiprocessing for CPU-bound tasks.
- SHOULD: Write tests with pytest or unittest, using mocking and measuring coverage.
- MUST: Isolate dependencies in virtual environments and pin versions in requirements.txt.
- SHOULD: Avoid unsafe use of pickle and sanitize inputs in web contexts.

---

## 24. Appendix: Example Automation Scripts & Templates

### Example Docker Compose Snippet (Healthchecks & Explicit Networks)

```yaml
version: '3.8'
services:
  example_service:
    image: example/image:1.0.0
    container_name: example_service
    restart: unless-stopped
    networks:
      - example_network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 15s
    environment:
      - EXAMPLE_ENV=production
    ports:
      - "8080:8080"
networks:
  example_network:
    driver: bridge
```

---

## 25. Visualizations & Diagrams

- For complex stacks, generate and include service dependency graphs or flowcharts.
- Tools: [Mermaid](https://mermaid-js.github.io/), [Graphviz](https://graphviz.gitlab.io/), or [draw.io](https://app.diagrams.net/).
- Example (Mermaid):

```mermaid
graph TD;
  ovos_core --> ovos_messagebus;
  ovos_core --> whisper;
  ovos_core --> xtts;
  ovos_core --> tgi;
  ovos_core --> qdrant;
  ovos_core --> frigate;
  ovos_core --> ollama;
```

---

## 26. Periodic Review & Update Schedule

- **Review Frequency:** These guidelines must be reviewed and updated at least quarterly (every 3 months) or after any major stack or process change.
- **Review Process:**
    - Assign a maintainer or rotating reviewer.
    - Solicit feedback from all contributors (AI and human).
    - Document all changes in `CHANGELOG.md`.
    - Confirm continued alignment with industry best practices and project needs.

---

## 27. Designing for Offline Capability & Portability

*To maximize the stack's ability to be deployed and maintained in offline or air-gapped environments, the following principles apply:*

1.  **Minimize Online Dependencies for Core Functionality:**
    * Services **should be designed and configured** to perform their core functions without requiring continuous internet access, where feasible.
    * Clearly differentiate between essential offline functionality and features that inherently require an internet connection (e.g., fetching live news, certain cloud-based AI models).
2.  **Explicitly Document Online Requirements:**
    * For any service, plugin, or feature that *does* require internet access (even if only for initial setup like model downloads or package installation), this dependency **must be clearly documented** in its respective `[ServiceName]_SETUP_GUIDE.md`. Include details about what is fetched and when.
3.  **Support for Localized Resources:**
    * Configurations **must** allow services to be pointed to locally hosted resources (e.g., local model directories, local package repositories, local service endpoints) instead of relying solely on hardcoded public internet URLs. This is crucial for offline operation.
4.  **Dockerfile and Build Process Considerations for Offline Builds:**
    * Custom Docker image builds **should strive to support offline assembly** once all initial base images and source dependencies (code, packages, models) have been pre-fetched during an online phase.
    * This may involve:
        * Using multi-stage Docker builds to separate online-dependent fetching/compilation from the final offline-buildable image.
        * Strategies for vendoring dependencies (e.g., Python wheels, system packages) if local mirrors are not used.
        * Ensuring build scripts do not attempt to reach the internet if an "offline build" mode is active or if local resources are present.
5.  **Configuration Over Internet Checks:**
    * Services should provide configuration options to disable automatic update checks or other non-essential internet call-outs if they might fail or cause issues in an offline environment.

---

## 28. Handling Exceptions and Deviations to These Rules
<!-- id: EXC-01, priority: MUST, tags: [compliance], last_reviewed: 2025-05-13 -->
Any intentional deviation from these baseline rules must be a conscious, documented exception:
1. **Identify:** Reference the baseline rule(s) being deviated from.
2. **Justify:** Provide clear rationale for the deviation.
3. **Document:** Record the exception, justification, risks, and alternative approach in the relevant `[ServiceName]_SETUP_GUIDE.md` or `[ServiceName]_TROUBLESHOOTING_GUIDE.md` with a link back to this guide.
4. **Approve:** Obtain explicit approval from the primary maintainer before finalizing.

---

## 29. Conflict Resolution Matrix
<!-- id: CRM-01, priority: SHOULD, tags: [conflict], last_reviewed: 2025-05-13 -->
### CRM-01: Resolving Conflicts in Code, Configuration, or Documentation
1. **Identify Conflict:** Clearly define the conflicting changes, configurations, or documentation sections; reference impacted rules.
2. **Analyze Impact:** Assess risks, benefits, and trade-offs against project priorities (security, performance, maintainability).
3. **Collaborate:** Engage stakeholders (AI and humans) via collaborative channels to gather input.
4. **Decide:** Reach consensus or escalate to primary maintainer; document rationale in commit messages or guides.
5. **Implement:** Apply resolution, test thoroughly, and update documentation/configuration.
6. **Review:** Conduct post-resolution review to confirm effective conflict resolution and capture lessons learned.

---

<!-- Footnotes -->

[1]: https://datatracker.ietf.org/doc/html/rfc2119  "RFC 2119: Key words for use in RFCs to Indicate Requirement Levels"

---

**This guide is mandatory. All new code, configuration, and documentation must comply with these rules.**
