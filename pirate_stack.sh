#!/bin/bash
# 🏴‍☠️ Pirate's Ultimate Home AI Stack Installer v2 🏴‍☠️

echo "⚓️ Avast! We be settin' sail on the seven containers (and more)!"

# --- Prerequisites ---

echo "🔄 Update yer system, lest ye be caught with barnacles!"
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker Compose if the bilge rat ain't got it
if ! command -v docker compose &> /dev/null; then
  echo "🦜 Docker Compose be missin'! Installin' it now, matey!"
  sudo apt-get install docker-compose-plugin -y
fi

# --- Configuration Files Check ---
echo "🗺️ Checkin' the charts (compose files)..."
COMPOSE_FILES=("docker-compose.ai.yml" "docker-compose.home.yml" "docker-compose.utils.yml")
for file in "${COMPOSE_FILES[@]}"; do
  if [ ! -f "$file" ]; then
    echo "☠️ Compose file '$file' be missin'! Make sure all yer charts be in order, matey!"
    # Consider running generate_compose_files.sh if applicable
    exit 1
  fi
done
echo "✅ Charts look good!"

# --- Pull Images --- 
echo "🦑 Pullin' the fleet o' images defined in yer compose files..."
# Combine all compose files to pull images efficiently
docker compose -f docker-compose.ai.yml -f docker-compose.home.yml -f docker-compose.utils.yml pull

# Check for pull errors (optional but good practice)
if [ $? -ne 0 ]; then
  echo "⚠️ Shiver me timbers! Some images failed to pull. Check the logs above! Ye might need to log in to ghcr.io or fix image names."
  # Optionally exit here if pulls are critical: exit 1
fi

echo "🦜 All available images be pulled from the depths!"

# --- Stop & Remove Conflicting Containers (from previous manual runs) ---
echo "🧹 Scuttlin' old manually-run utility containers to avoid conflicts..."
OLD_CONTAINERS=("portainer" "watchtower" "nginx-proxy-manager" "tailscale" "cloudflared")
for container in "${OLD_CONTAINERS[@]}"; do
  if [ "$(docker ps -q -f name=^/${container}$)" ]; then
    echo "  - Stoppin' $container..."
    docker stop "$container" > /dev/null
    echo "  - Removin' $container..."
    docker rm "$container" > /dev/null
  fi
done
echo "✅ Decks cleared!"

# --- Start Containers --- 
echo "🏴‍☠️ Hoistin' the main sails! Startin' all containers from compose files!"
docker compose -f docker-compose.ai.yml up -d
docker compose -f docker-compose.home.yml up -d
docker compose -f docker-compose.utils.yml up -d

# --- Final Message --- 
echo "🎉 Yarrr! Yer ultimate home AI stack be runnin'! Set yer course to yer services:"
echo "  - Frigate: http://localhost:5000"
echo "  - Ollama: http://localhost:11434"
echo "  - Home Assistant: http://localhost:8123"
echo "  - Portainer: https://localhost:9443 (or http://localhost:9000)"
echo "  - NGINX Proxy Manager: http://localhost:81"
echo "  - Stable Diffusion: http://localhost:7860 (if started)"
echo "  - ...and the rest o' yer treasures!"
echo "🏴‍☠️ Now go plunder the future, ye salty dog!"
