# DOCKER_SETUP_GUIDE.md

## Home Automation Stack: Docker Setup Guide

> **This guide provides the baseline steps for setting up, running, and maintaining the home automation stack using Docker and Docker Compose. All practices must comply with [AI_CODING_BASELINE_RULES.md](./AI_CODING_BASELINE_RULES.md).**

---

## Containers/Services in This Stack

| Service                | Recommended Image Tag | Upstream Registry / How to Check Versions |
|------------------------|----------------------|-------------------------------------------|
| ovos_messagebus        | (specify tag used)   | [Docker Hub](https://hub.docker.com/) or project docs |
| ovos_core              | (specify tag used)   | [Docker Hub](https://hub.docker.com/) or project docs |
| whisper                | (specify tag used)   | [Docker Hub](https://hub.docker.com/) or project docs |
| xtts                   | (specify tag used)   | [Docker Hub](https://hub.docker.com/) or project docs |
| tgi (text-gen-inf)     | (specify tag used)   | [Docker Hub](https://hub.docker.com/) or project docs |
| qdrant                 | (specify tag used)   | [Qdrant Docker Hub](https://hub.docker.com/r/qdrant/qdrant/tags) |
| frigate                | stable               | [Frigate Docker Hub](https://hub.docker.com/r/blakeblackshear/frigate/tags) |
| ollama                 | (specify tag used)   | [Ollama Docker Hub](https://hub.docker.com/r/ollama/ollama/tags) |
| homeassistant          | (specify tag used)   | [Home Assistant Docker Hub](https://hub.docker.com/r/homeassistant/home-assistant/tags) |
| cloudflared            | latest               | [Cloudflared Docker Hub](https://hub.docker.com/r/cloudflare/cloudflared/tags) |
| portainer              | latest               | [Portainer Docker Hub](https://hub.docker.com/r/portainer/portainer-ce/tags) |
| stable-diffusion       | (specify tag used)   | [Docker Hub](https://hub.docker.com/) or project docs |
| text-generation-webui  | (specify tag used)   | [Docker Hub](https://hub.docker.com/) or project docs |
| zigbee2mqtt            | (specify tag used)   | [Zigbee2MQTT Docker Hub](https://hub.docker.com/r/koenkk/zigbee2mqtt/tags) |
| tailscale              | latest               | [Tailscale Docker Hub](https://hub.docker.com/r/tailscale/tailscale/tags) |
| nginx-proxy-manager    | (specify tag used)   | [Nginx Proxy Manager Docker Hub](https://hub.docker.com/r/jc21/nginx-proxy-manager/tags) |

> **Note:** Always check the upstream registry for available and recommended tags before updating. Replace `(specify tag used)` with the actual tag in use in your Compose files. Pin to stable, published tags for reproducibility.

---

## Key Baseline Practices (Summary)
- All configuration, Docker Compose, and service setup must follow the rules in [AI_CODING_BASELINE_RULES.md](./AI_CODING_BASELINE_RULES.md).
- Use only Linux-based images for all containers.
- Always use relative paths for volume mounts (e.g., `./config:/app/config`).
- Pin all image and dependency versions; avoid `latest` tags.
- All containers must run as non-root unless explicitly documented.
- Use healthchecks with `exec` form and appropriate intervals/timeouts.
- Tag all AI-generated or AI-reviewed config/code with standardized comments.
- No secrets or credentials in committed files; use environment variables or Docker secrets.
- Document all online requirements and support offline operation where possible.
- Use `.env` files for environment variables (do not commit secrets).
- All changes must be committed with Conventional Commits and reviewed before merge.
- Maintain a `CHANGELOG.md` and update this guide as new services are added.
- Reference the baseline guide in all service-specific documentation and Compose files.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Starting the Stack](#starting-the-stack)
4. [Adding/Updating Services](#addingupdating-services)
5. [Offline Deployment & Maintenance](#offline-deployment--maintenance)
6. [Image Tagging and Docker Compose Best Practices (Lessons Learned)](#image-tagging-and-docker-compose-best-practices-lessons-learned)
7. [Troubleshooting](#troubleshooting)
8. [References](#references)

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

## Image Tagging and Docker Compose Best Practices (Lessons Learned)

### Use Only Valid, Published Image Tags
- Always use image tags that are published and visible in the upstream registry (e.g., Docker Hub, GitHub Container Registry).
- Never invent, guess, or use future-dated tags. If a tag is not listed upstream, it will not work.
- Avoid using `latest` unless the upstream project officially recommends it and you understand the risks.
- Pin to stable or official tags as recommended by upstream documentation.

### Troubleshooting "Image Not Found" and Tag Errors
1. **Identify the Failing Service:**
   - Check the error message for the service and image name.
2. **Locate the Image Reference:**
   - Search for the `image:` line in the relevant `docker-compose.*.yml` file.
3. **Verify Tag Upstream:**
   - Visit the image's registry page (e.g., Docker Hub) and confirm the tag exists.
   - If the tag is missing, select a valid, stable tag and update the Compose file.
4. **Update and Re-Test:**
   - Edit the Compose file to use the correct tag.
   - Run `docker compose config` to validate the file.
   - Run `docker compose up -d --force-recreate` to retry.
5. **Iterate as Needed:**
   - Repeat for each service with errors until all images pull successfully.

### Lessons Learned
- Always check upstream documentation and registry listings before updating image tags.
- Hardcode image tags in Compose files for reproducibility and reliability.
- Avoid variable-based image references unless strictly necessary and well-documented.
- Use `docker compose config` and `docker compose pull` to validate changes before starting services.
- Document all troubleshooting steps and resolutions for future maintainers.

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
- [DOCKER_TROUBLESHOOTING_GUIDE.md](./DOCKER_TROUBLESHOOTING_GUIDE.md)

---

*Update this guide incrementally as new containers/services are added or requirements change.*
