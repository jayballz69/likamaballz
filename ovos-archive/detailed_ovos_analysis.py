import os
import sys
import json
from ovos_config import Configuration
from ovos_bus_client import MessageBusClient
from ovos_utils.log import LOG

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
    with open(minimal_conf_path, 'r') as f:
        print(f.read())
else:
    print(f"\n{minimal_conf_path} does not exist!")

# Check configuration
conf = Configuration()
print("\nFinal Configuration loaded by OVOS:")
print("message_bus_client:")
print(json.dumps(conf.get('message_bus_client', {}), indent=2))
print("\nwebsocket:")
print(json.dumps(conf.get('websocket', {}), indent=2))

# Monkey patch the MessageBusClient class to log connection parameters
original_init = MessageBusClient.__init__

def patched_init(self, host=None, port=None, route=None, ssl=None, *args, **kwargs):
    print(f"\nMessageBusClient.__init__ called with:")
    print(f"  host: {host}")
    print(f"  port: {port}")
    print(f"  route: {route}")
    print(f"  ssl: {ssl}")
    print(f"  kwargs: {kwargs}")
    
    # Call original init
    original_init(self, host=host, port=port, route=route, ssl=ssl, *args, **kwargs)

# Apply the monkey patch
MessageBusClient.__init__ = patched_init

# Initialize a client like OVOS would
print("\nCreating a test MessageBusClient with no explicit parameters:")
print("(This should use values from the Configuration)")
client = MessageBusClient()

# Print actual connection data
print(f"\nResulting client connection data:")
print(f"  host: {client.host}")
print(f"  port: {client.port}")
print(f"  route: {client.route}")
print(f"  ssl: {client.ssl}")

# Try to connect
print("\nAttempting connection with these parameters...")
client.run_in_thread()
import time
time.sleep(5)
if client.started_running:
    print("SUCCESS: Connected to messagebus!")
else:
    print("FAILED: Could not connect to messagebus.")

print("\nTest complete.")
