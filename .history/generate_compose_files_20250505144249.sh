#!/bin/bash
# generate_compose_files.sh
# Generates docker-compose files for AI and Home Assistant stacks

# AI Stack Compose File
echo "version: '3.8'
services:
  frigate:
    image: blakeblackshear/frigate:stable
    container_name: frigate
    restart: unless-stopped
    privileged: true
    shm_size: '64mb'
    devices:
      - /dev/bus/usb:/dev/bus/usb
    volumes:
      - ./frigate/config:/config
      - ./frigate/media:/media/frigate
      - /etc/localtime:/etc/localtime:ro
    ports:
      - '5000:5000' # Frigate UI
      - '8554:8554' # RTSP
      - '8555:8555/tcp' # WebRTC
    environment:
      - FRIGATE_RTSP_PASSWORD=changeme

  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    restart: unless-stopped
    volumes:
      - ./ollama:/root/.ollama
    ports:
      - '11434:11434'

# Add more AI/video services as needed
" > docker-compose.ai.yml

echo "AI stack docker-compose file generated: docker-compose.ai.yml"

# Home Assistant Stack Compose File
echo "version: '3.8'
services:
  homeassistant:
    image: ghcr.io/home-assistant/home-assistant:stable
    container_name: homeassistant
    restart: unless-stopped
    network_mode: host
    privileged: true
    volumes:
      - ./homeassistant/config:/config
      - /etc/localtime:/etc/localtime:ro
    environment:
      - TZ=Australia/Brisbane

  zigbee2mqtt:
    image: koenkk/zigbee2mqtt
    container_name: zigbee2mqtt
    restart: unless-stopped
    volumes:
      - ./zigbee2mqtt/data:/app/data
      - /run/udev:/run/udev:ro
    devices:
      - /dev/ttyUSB0:/dev/ttyUSB0
    environment:
      - TZ=Australia/Brisbane

# Add more smart home services as needed
" > docker-compose.home.yml

echo "Home Assistant stack docker-compose file generated: docker-compose.home.yml"
