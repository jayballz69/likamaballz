# See AI_CODING_BASELINE_RULES.md for required practices.
import pytest
import websocket

WS_URL = "ws://localhost:8181/core"
CONNECTION_TIMEOUT = 20  # seconds

def test_minimal_websocket_connection():
    """Ensure a minimal WebSocket connection can be made to ovos_messagebus."""
    ws = websocket.create_connection(WS_URL, timeout=CONNECTION_TIMEOUT)
    assert ws.connected, f"Failed to connect to {WS_URL}"
    ws.close()
