# Simple WebSocket connection test with explicit error reporting
import websocket
import socket
import sys
import traceback

# Print basic system info
print("Starting WebSocket connection test")
print(f"Python version: {sys.version}")

# Try to resolve the hostname first to check DNS
try:
    print("Checking DNS resolution for 'ovos_messagebus'...")
    ip_info = socket.getaddrinfo('ovos_messagebus', 8181)
    print(f"DNS resolution successful: {ip_info}")
except Exception as e:
    print(f"DNS resolution failed: {e}")
    
# Now try with IP directly
try:
    print("\nAttempting WebSocket connection to ws://172.20.0.2:8181/core...")
    ws = websocket.create_connection("ws://172.20.0.2:8181/core", timeout=5)
    print("Connection successful!")
    ws.close()
    print("Connection closed properly.")
except Exception as e:
    print(f"Connection failed: {type(e).__name__}: {e}")
    traceback.print_exc()

print("\nTest completed.")
