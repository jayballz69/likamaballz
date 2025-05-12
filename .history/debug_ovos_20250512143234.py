#!/usr/bin/env python3

"""
Debug script to check OVOS configuration and bus client setup
"""

import os
import sys
import json
from pprint import pprint

# Print environment variables related to messagebus
print("------ Environment Variables ------")
for key, value in os.environ.items():
    if "MESSAGE" in key or "MYCROFT" in key or "OVOS" in key:
        print(f"{key}={value}")
print("\n")

try:
    # Try to import ovos modules
    print("------ Importing Modules ------")
    import ovos_config
    print(f"ovos_config version: {ovos_config.__version__ if hasattr(ovos_config, '__version__') else 'unknown'}")
    import ovos_bus_client
    print(f"ovos_bus_client version: {ovos_bus_client.__version__ if hasattr(ovos_bus_client, '__version__') else 'unknown'}")
    
    # Get configuration
    print("\n------ Configuration Loading ------")
    from ovos_config import Configuration
    config = Configuration()
    
    # Print message bus client configuration
    print("\n------ Message Bus Client Configuration ------")
    if "message_bus_client" in config:
        print("From config object:")
        pprint(config["message_bus_client"])
    else:
        print("No message_bus_client section found in config!")
    
    # Print websocket configuration
    print("\n------ WebSocket Server Configuration ------")
    if "websocket" in config:
        print("From config object:")
        pprint(config["websocket"])
    else:
        print("No websocket section found in config!")
    
    # Try to create a MessageBusClient
    print("\n------ Creating MessageBusClient ------")
    from ovos_bus_client import MessageBusClient
    client = MessageBusClient()
    print(f"Client created, host: {client.host}, port: {client.port}, route: {client.route}")
    
    # Don't actually connect, just show the configured values
    print("\n------ Would connect to ------")
    protocol = "wss" if client.ssl else "ws"
    print(f"{protocol}://{client.host}:{client.port}{client.route}")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
