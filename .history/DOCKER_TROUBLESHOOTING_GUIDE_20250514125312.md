# DOCKER_TROUBLESHOOTING_GUIDE.md

## Docker Compose Troubleshooting Guide for Home Automation Stack

This guide summarizes common Docker and Docker Compose errors, diagnostic steps, and best practices for resolving issues in this stack. It is intended for both new and experienced contributors.

---

## Common Error Patterns

### 1. Image Not Found / Tag Not Found
- **Symptoms:**
  - `manifest for <image>:<tag> not found`
  - `pull access denied for <image>`
  - `repository does not exist or may require 'docker login'`
- **Causes:**
  - Typo in image name or tag
  - Tag does not exist upstream (invented, future-dated, or misspelled)
  - Image is private or requires authentication
  - Network issues

### 2. Service Fails to Start
- **Symptoms:**
  - `Container exited with code ...`
  - `Error response from daemon: ...`
- **Causes:**
  - Invalid configuration (env vars, volumes, ports)
  - Missing dependencies or files
  - Permission issues

### 3. Volume/Bind Mount Errors
- **Symptoms:**
  - `Mounts denied: ...`
  - `No such file or directory`
- **Causes:**
  - Host directory does not exist
  - Incorrect path or permissions

---

## Step-by-Step Diagnostic Workflow

1. **Check Image and Tag:**
   - Locate the `image:` line in the relevant Compose file.
   - Search the upstream registry (e.g., Docker Hub, GitHub Container Registry) for the image and tag.
   - Use only published, official tags. Avoid `latest` unless required by upstream.
   - Update the Compose file to use a valid tag.

2. **Validate Compose File:**
   - Run: `docker compose config` to check for syntax and reference errors.

3. **Pull Images Manually:**
   - Run: `docker compose pull` to verify all images can be pulled.
   - If an image fails, repeat step 1.

4. **Start Services with Logs:**
   - Run: `docker compose up -d --force-recreate`
   - Check logs: `docker compose logs -f <service_name>`

5. **Check Volumes and Permissions:**
   - Ensure all host directories exist and have correct permissions.
   - For Windows/WSL2, ensure file sharing is enabled for the relevant drives.

6. **Iterate and Document:**
   - For each error, document the cause and resolution in this guide or service-specific docs.

---

## Best Practices for Compose Files and Image Tags
- Always use valid, published image tags. Never invent or future-date tags.
- Pin to stable or official tags as recommended by upstream documentation.
- Avoid variable-based image references unless strictly necessary and well-documented.
- Regularly review and update image tags to track upstream security and stability updates.
- Document all changes and troubleshooting steps for future maintainers.

---

*Update this guide as new error patterns and solutions are discovered.*
