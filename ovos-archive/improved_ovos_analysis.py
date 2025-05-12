import os
import sys
import json
import time
import logging
from ovos_config import Configuration
from ovos_bus_client import MessageBusClient
from ovos_utils.log import LOG

# Set up logging
logging.basicConfig(level=logging.DEBUG)

print("---- OVOS Configuration and MessageBusClient Analysis ----")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")

# Environment variables
print("\nEnvironment Variables:")
for key in sorted([k for k in os.environ.keys() if "MYCROFT" in k or "OVOS" in k or "MESSAGEBUS" in k]):
    print(f"  {key}: {os.environ.get(key)}")

# Check if mycroft_minimal.conf exists and print its content
minimal_conf_path = "/home/ovos/.config/mycroft/mycroft_minimal.conf"
if os.path.exists(minimal_conf_path):
    print(f"\nContents of {minimal_conf_path}:")
    with open(minimal_conf_path, "r") as f:
        print(f.read())
else:
    print(f"\n{minimal_conf_path} does not exist!")

# Check configuration
conf = Configuration()
print("\nFinal Configuration loaded by OVOS:")
print("message_bus_client:")
print(json.dumps(conf.get("message_bus_client", {}), indent=2))
print("\nwebsocket:")
print(json.dumps(conf.get("websocket", {}), indent=2))

# Try with explicit parameters first
print("\n1. Testing MessageBusClient with explicit parameters from environment:")
host = os.environ.get("MESSAGEBUS_HOST", "172.20.0.2")
port = int(os.environ.get("MESSAGEBUS_PORT", "8181"))
route = os.environ.get("MESSAGEBUS_ROUTE", "/core")

print(f"  Creating client with: host={host}, port={port}, route={route}")
test_client = MessageBusClient(host=host, port=port, route=route)

print("\n  Starting client...")
test_client.run_in_thread()
time.sleep(5)

print(f"  Connected: {test_client.started_running}")
if not test_client.started_running:
    print("  Connection FAILED with explicit parameters!")
else:
    print("  Connection SUCCEEDED with explicit parameters!")

# Try with default parameters (from Configuration)
print("\n2. Testing MessageBusClient with default parameters (from Configuration):")
default_client = MessageBusClient()
print("  Starting client...")
default_client.run_in_thread()
time.sleep(5)

print(f"  Connected: {default_client.started_running}")
if not default_client.started_running:
    print("  Connection FAILED with default parameters!")
else:
    print("  Connection SUCCEEDED with default parameters!")

# Check websocket-client version
print("\nWebSocket Client Info:")
try:
    import websocket
    print(f"  websocket-client version: {websocket.__version__}")
except ImportError:
    print("  websocket-client not found!")

print("\nTest complete.")
