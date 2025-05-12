#!/usr/bin/env python3
# Test script for ovos_bus_client connection issues
import time
import os
from ovos_bus_client import MessageBusClient

# Print debug info
print("--- OVOS MessageBusClient Test ---")
print(f"Current directory: {os.getcwd()}")
print(f"Environment variables:")
for key in ["MESSAGEBUS_HOST", "MESSAGEBUS_PORT"]:
    print(f"  {key}: {os.environ.get(key)}")

# Try both service name and direct IP
hosts_to_try = [
    ("ovos_messagebus", 8181),
    ("172.20.0.2", 8181)
]

for host, port in hosts_to_try:
    print(f"\nTrying to connect to {host}:{port}...")
    
    try:
        # Connect with various configurations
        print(f"  * Connecting with route='/core'...")
        bus = MessageBusClient(host=host, port=port, route="/core")
        # Attempt connection
        bus.run_in_thread()
        time.sleep(2)
        connected = bus.started_running
        print(f"    Connected: {connected}")
        if connected:
            print("    ✓ SUCCESS!")
        else:
            print("    ✗ FAILED!")
        bus.close()
    except Exception as e:
        print(f"    ✗ ERROR: {type(e).__name__}: {e}")

    try:
        # Connect without the '/core' route
        print(f"  * Connecting without route parameter...")
        bus = MessageBusClient(host=host, port=port)
        # Attempt connection
        bus.run_in_thread()
        time.sleep(2)
        connected = bus.started_running
        print(f"    Connected: {connected}")
        if connected:
            print("    ✓ SUCCESS!")
        else:
            print("    ✗ FAILED!")
        bus.close()
    except Exception as e:
        print(f"    ✗ ERROR: {type(e).__name__}: {e}")

print("\n--- Test Complete ---")
