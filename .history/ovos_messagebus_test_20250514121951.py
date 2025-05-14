# See AI_CODING_BASELINE_RULES.md for required practices.
import sys
import time
from ovos_bus_client import MessageBusClient

HOST = "ovos_messagebus"
PORT = 8181
ROUTE = "/core"

print("===================================")
print("OVOS Messagebus Connectivity Test")
print("===================================")

try:
    print(f"Connecting to ws://{HOST}:{PORT}{ROUTE} ...")
    client = MessageBusClient(host=HOST, port=PORT, route=ROUTE)
    client.run_in_thread()
    time.sleep(2)  # Allow time to connect
    if client.connected:
        print("SUCCESS: Connected to OVOS messagebus!")
        client.disconnect()
        sys.exit(0)
    else:
        print("FAIL: Could not connect to OVOS messagebus.")
        sys.exit(1)
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(2)