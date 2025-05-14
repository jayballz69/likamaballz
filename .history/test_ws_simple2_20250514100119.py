# Pytest-based tests for WebSocket functionality
import pytest
import websocket
import socket

def test_dns_resolution_localhost():
    """Ensure DNS resolution works for localhost on port 8181."""
    ip_info = socket.getaddrinfo('localhost', 8181)
    assert ip_info, "DNS resolution for localhost failed"

def test_websocket_simple2_connection():
    """Test WebSocket connection to ovos_messagebus on localhost."""
    ws = websocket.create_connection("ws://localhost:8181/core", timeout=5)
    assert ws.connected, "Failed to connect to WebSocket at localhost:8181/core"
    ws.close()
