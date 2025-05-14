import pytest
try:
    import websocket
except ImportError:
    import sys; print("websocket-client missing, skipping network tests"); sys.exit(0)

# Basic network test with direct file writing
import socket
import os
import traceback

# Open a file for writing
with open('/tmp/network_test.log', 'w') as f:
    f.write("Network test starting\n")
    
    # Try to get the local IP address
    f.write("Local hostname: " + socket.gethostname() + "\n")
    
    # Try to resolve ovos_messagebus
    try:
        f.write("Resolving ovos_messagebus...\n")
        ip_info = socket.getaddrinfo('ovos_messagebus', 8181)
        f.write(f"Resolution result: {ip_info}\n")
    except Exception as e:
        f.write(f"Resolution failed: {str(e)}\n")
        traceback.print_exc(file=f)
    
    # Try to connect to the message bus IP directly
    try:
        f.write("\nTrying socket connection to 172.20.0.2:8181...\n")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        result = s.connect_ex(('172.20.0.2', 8181))
        if result == 0:
            f.write("Socket connection successful!\n")
        else:
            f.write(f"Socket connection failed with error code: {result}\n")
        s.close()
    except Exception as e:
        f.write(f"Socket connection error: {str(e)}\n")
        traceback.print_exc(file=f)
    
    # Try WebSocket connection
    try:
        f.write("\nTrying WebSocket connection...\n")
        ws = websocket.create_connection("ws://172.20.0.2:8181/core", timeout=5)
        f.write("WebSocket connection successful!\n")
        ws.close()
    except Exception as e:
        f.write(f"WebSocket error: {type(e).__name__}: {str(e)}\n")
        traceback.print_exc(file=f)
    
    f.write("\nTest completed.\n")
