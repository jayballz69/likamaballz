#!/usr/bin/env python3
import websocket
import time
import os
import json
from websocket import create_connection

# Get environment variables or use defaults
host = os.environ.get('MESSAGEBUS_HOST', 'ovos_messagebus')
port = os.environ.get('MESSAGEBUS_PORT', '8181')
route = os.environ.get('MESSAGEBUS_ROUTE', '/core')

# Try WebSocket connection
print(f"Attempting WebSocket connection to ws://{host}:{port}{route}")

try:
    ws = create_connection(f"ws://{host}:{port}{route}")
    print("WebSocket connection successful!")
    # Try sending a message
    message = {
        "type": "mycroft.echo",
        "data": {"message": "test"},
        "context": {}
    }
    ws.send(json.dumps(message))
    print("Message sent!")
    # Try receiving a response
    response = ws.recv()
    print(f"Response received: {response}")
    ws.close()
except Exception as e:
    print(f"WebSocket connection failed: {e}")

# Try a standard HTTP connection
import socket
print(f"\nAttempting TCP connection to {host}:{port}")
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect((host, int(port)))
    print("TCP connection successful!")
    s.close()
except Exception as e:
    print(f"TCP connection failed: {e}")

# Try using the MessageBusClient directly
print("\nAttempting connection with MessageBusClient")
try:
    from ovos_bus_client import MessageBusClient
    from ovos_bus_client.message import Message
    
    client = MessageBusClient(host=host, port=int(port), route=route)
    client.run_in_thread()
    
    time.sleep(3)  # Give it a moment to connect
    
    if client.started_running:
        print("MessageBusClient connection successful!")
        # Try emitting a message
        client.emit(Message('mycroft.echo', data={"message": "test"}))
        print("Message emitted!")
        time.sleep(1)  # Give it a moment to process
    else:
        print("MessageBusClient did not start successfully")
except Exception as e:
    print(f"MessageBusClient connection failed: {e}")

print("\nTest complete!")
