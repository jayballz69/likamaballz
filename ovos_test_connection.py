#!/usr/bin/env python3
"""
OVOS MessageBus Connection Test Script
Purpose: Test if ovos container can connect to ovos_messagebus service via WebSocket

This test script:
1. Uses the same WebSocket client library as OVOS itself
2. Uses the exact MessageBus client connection parameters from mycroft.conf
3. Attempts to establish a WebSocket connection
4. Reports success or detailed failure information
"""

import sys
import traceback
import socket
import json
from time import sleep

def log(msg):
    """Print message with timestamp."""
    print(f"[TEST] {msg}")
    sys.stdout.flush()

log("Starting OVOS MessageBus connection test...")

try:
    import websocket
    log(f"Using websocket-client version: {websocket.__version__}")
except ImportError:
    log("ERROR: websocket-client module not found. Install with: pip install websocket-client")
    sys.exit(1)

# Connection parameters - should match mycroft.conf
HOST = "ovos_messagebus"  # Same as specified in mycroft.conf
PORT = 8181
ROUTE = "/core"
USE_SSL = False

url = f"{'wss' if USE_SSL else 'ws'}://{HOST}:{PORT}{ROUTE}"
log(f"Attempting to connect to: {url}")

# Try DNS resolution first
try:
    log(f"Resolving hostname {HOST}...")
    ip = socket.gethostbyname(HOST)
    log(f"✅ DNS resolution successful: {HOST} -> {ip}")
except socket.gaierror as e:
    log(f"❌ DNS resolution failed for {HOST}: {e}")
    # Try alternative using direct IP if needed
    log("Trying alternative methods...")
    # Continue with the test anyway

# Test TCP connection first
log(f"Testing TCP connection to {HOST}:{PORT}...")
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect((HOST, PORT))
    s.close()
    log(f"✅ TCP connection successful to {HOST}:{PORT}")
except Exception as e:
    log(f"❌ TCP connection failed to {HOST}:{PORT}: {e}")
    log("This suggests a networking issue or the messagebus service is not running.")
    # Continue anyway to see the specific WebSocket error

# Now test WebSocket connection
log(f"Testing WebSocket connection to {url}...")

# Disable tracing as it might cause issues
websocket.enableTrace(False)

# Define callback handlers
def on_message(ws, message):
    log(f"✅ Received message: {message[:100]}...")
    
def on_error(ws, error):
    log(f"❌ WebSocket error: {error}")
    if isinstance(error, ConnectionRefusedError):
        log("Connection was refused. This indicates the messagebus service is not running or not accepting connections.")
    
def on_close(ws, close_status_code, close_msg):
    reason = f" (Code: {close_status_code}, Message: {close_msg})" if close_status_code or close_msg else ""
    log(f"WebSocket connection closed{reason}")
    
def on_open(ws):
    log("✅ WebSocket connection established!")
    # Send a test message to the bus
    message = {
        "type": "test.connection",
        "data": {"source": "test_script"},
        "context": {"client_name": "test_script"}
    }
    log(f"Sending test message: {json.dumps(message)}")
    ws.send(json.dumps(message))
    # Wait briefly for any response
    sleep(2)
    log("Test complete, closing connection...")
    ws.close()

try:
    # Create WebSocket connection
    ws = websocket.WebSocketApp(url,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
      # Connect with a timeout (older websocket-client doesn't support reconnect)
    log("Running WebSocket connection...")
    ws.run_forever()
    log("WebSocket test completed")
    
except Exception as e:
    log(f"❌ Exception during WebSocket connection: {e}")
    traceback.print_exc()
    
log("Test script finished.")
