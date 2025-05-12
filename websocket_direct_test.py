import time
import websocket
import sys

# Direct WebSocket URL for messagebus
websocket_url = "ws://ovos_messagebus:8181"

try:
    print(f"Connecting to {websocket_url}...")
    # Without /core path
    ws = websocket.create_connection(websocket_url, timeout=10)
    print(f"Connection established to {websocket_url}")
    
    # Try to send a ping message
    print("Sending a ping message")
    ws.send('{"type": "mycroft.ping"}')
    
    # Wait for response
    print("Waiting for response...")
    response = ws.recv()
    print(f"Response: {response}")
    
    # Close the connection
    ws.close()
    print("Connection closed")
    
except websocket.WebSocketException as e:
    print(f"WebSocket error: {e}")

# Try again with /core path
try:
    websocket_url_core = f"{websocket_url}/core"
    print(f"Connecting to {websocket_url_core}...")
    
    ws = websocket.create_connection(websocket_url_core, timeout=10)
    print(f"Connection established to {websocket_url_core}")
    
    # Try to send a ping message
    print("Sending a ping message")
    ws.send('{"type": "mycroft.ping"}')
    
    # Wait for response
    print("Waiting for response...")
    response = ws.recv()
    print(f"Response: {response}")
    
    # Close the connection
    ws.close()
    print("Connection closed")
    
except websocket.WebSocketException as e:
    print(f"WebSocket error with /core path: {e}")
