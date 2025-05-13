# DOCKER_SETUP_GUIDE.md

## Home Automation Stack: Docker Setup Guide

> **This guide provides the baseline steps for setting up, running, and maintaining the home automation stack using Docker and Docker Compose. All practices must comply with [AI_CODING_BASELINE_RULES.md](./AI_CODING_BASELINE_RULES.md).**

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Starting the Stack](#starting-the-stack)
4. [Adding/Updating Services](#addingupdating-services)
5. [Offline Deployment & Maintenance](#offline-deployment--maintenance)
6. [Troubleshooting](#troubleshooting)
7. [References](#references)

---

## Prerequisites
- **Docker**: Install the latest stable version for your OS ([Docker Desktop](https://www.docker.com/products/docker-desktop/) for Windows/Mac, [Docker Engine](https://docs.docker.com/engine/install/) for Linux).
- **Docker Compose**: Included with Docker Desktop; for Linux, install [Compose V2](https://docs.docker.com/compose/install/).
- **Git**: For version control and pulling updates.
- **Windows Users**: Use WSL2 for best compatibility. Ensure file sharing is enabled for relevant drives.
- **Linux Base Images**: All containers use Linux-based images (see baseline rules).

---

## Initial Setup
1. **Clone the Repository:**
   ```sh
   git clone <your-repo-url>
   cd <repo-folder>
   ```
2. **Review and Edit Environment Variables:**
   - Check `docker-compose.*.yml` files for required `environment:` variables.
   - Create or update a `.env` file as needed (do not commit secrets).
3. **Review Volume Mounts:**
   - Ensure all host directories to be mounted exist and have correct permissions (see baseline rules).
4. **Pull Images:**
   ```sh
   docker compose -f docker-compose.ai.yml pull
   docker compose -f docker-compose.home.yml pull
   docker compose -f docker-compose.utils.yml pull
   ```

---

## Starting the Stack
- **Start All Services:**
  ```sh
  docker compose -f docker-compose.ai.yml up -d
  docker compose -f docker-compose.home.yml up -d
  docker compose -f docker-compose.utils.yml up -d
  ```
- **Check Status:**
  ```sh
  docker compose ps
  ```
- **Logs:**
  ```sh
  docker compose logs -f <service_name>
  ```

---

## Adding/Updating Services
- **Incremental Onboarding:**
  - As new containers/services are brought online, update the relevant `docker-compose.*.yml` file and add a section to this guide with:
    - Service purpose
    - Required environment variables
    - Volume mounts
    - Exposed ports
    - Healthcheck details
    - Any special setup or troubleshooting notes
  - Reference the [AI_CODING_BASELINE_RULES.md](./AI_CODING_BASELINE_RULES.md) for all configuration, security, and collaboration practices.

---

## Offline Deployment & Maintenance
- **Offline Image Management:**
  - Pre-pull all required images while online:
    ```sh
    docker compose -f docker-compose.ai.yml pull
    # Repeat for other compose files as needed
    ```
  - Save images for transfer/backup:
    ```sh
    docker save <image>:<tag> -o <image>.tar
    ```
  - Load images on offline hosts:
    ```sh
    docker load -i <image>.tar
    ```
- **Offline Dependency/Model Management:**
  - Place all required models, data, or dependencies in the appropriate local directories before going offline.
  - Update service configs to point to local resources (see baseline rules).
- **Document any online requirements for each service in its setup section.**

---

## Troubleshooting
- See [OVOS_TROUBLESHOOTING_GUIDE.md](./OVOS_TROUBLESHOOTING_GUIDE.md) and service-specific troubleshooting sections as they are added.
- Common commands:
  - Restart a service: `docker compose restart <service_name>`
  - Remove a stopped container: `docker rm <container_name>`
  - Prune unused images/volumes: `docker system prune`

---

## References
- [AI_CODING_BASELINE_RULES.md](./AI_CODING_BASELINE_RULES.md)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)

---

*Update this guide incrementally as new containers/services are added or requirements change.*
