#!/bin/bash
# 🏴‍☠️ Pirate's Ultimate Home AI Stack Installer 🏴‍☠️

echo "⚓️ Avast! We be settin' sail on the seven containers!"

# Update yer system, lest ye be caught with barnacles!
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker Compose if the bilge rat ain't got it
if ! command -v docker compose &> /dev/null; then
  echo "🦜 Docker Compose be missin'! Installin' it now, matey!"
  sudo apt-get install docker-compose-plugin -y
fi

# Pull all the images fer yer stack, so there be no delays when ye run 'em!
echo "🦑 Pullin' the main fleet o' images..."
docker pull ghcr.io/blakeblackshear/frigate:stable
docker pull ollama/ollama:latest
docker pull ghcr.io/home-assistant/home-assistant:stable
docker pull koenkk/zigbee2mqtt
docker pull portainer/portainer-ce:latest
docker pull containrrr/watchtower:latest
docker pull jc21/nginx-proxy-manager:latest
docker pull tailscale/tailscale:latest
docker pull cloudflare/cloudflared:latest

docker pull qdrant/qdrant:latest         # Vector database fer yer AI memory
docker pull ghcr.io/huggingface/text-generation-inference:latest  # HuggingFace LLM server
docker pull ghcr.io/ollama/whisper:latest # Whisper voice-to-text, if ye want it
docker pull ghcr.io/automatic1111/stable-diffusion-webui:latest   # Image generation, arrr!

echo "🦜 All images be pulled from the depths!"

# Make sure yer compose files be ready, else the kraken will rise!
if [ ! -f docker-compose.ai.yml ] || [ ! -f docker-compose.home.yml ]; then
  echo "☠️ Compose files be missin'! Run yer generate_compose_files.sh script, matey!"
  exit 1
fi

# Start the main fleet!
echo "🏴‍☠️ Hoistin' the main sails! Startin' all containers!"
docker compose -f docker-compose.ai.yml up -d
docker compose -f docker-compose.home.yml up -d

# Start yer extra treasures, if ye want 'em!
echo "🦜 Startin' Portainer, Watchtower, NGINX Proxy Manager, Tailscale, and Cloudflared!"
docker run -d --name portainer --restart=unless-stopped -p 9000:9000 -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest
docker run -d --name watchtower --restart=unless-stopped -v /var/run/docker.sock:/var/run/docker.sock containrrr/watchtower:latest
docker run -d --name nginx-proxy-manager --restart=unless-stopped -p 81:81 -p 80:80 -p 443:443 -v npm_data:/data -v letsencrypt:/etc/letsencrypt jc21/nginx-proxy-manager:latest
docker run -d --name tailscale --restart=unless-stopped --network host --privileged tailscale/tailscale:latest
docker run -d --name cloudflared --restart=unless-stopped cloudflare/cloudflared:latest tunnel run

echo "🏴‍☠️ Yarrr! Yer ultimate home AI stack be runnin'! Set yer course fer http://localhost:5000 (Frigate), http://localhost:11434 (Ollama), http://localhost:8123 (Home Assistant), and more! Now go plunder the future, ye salty dog!"
