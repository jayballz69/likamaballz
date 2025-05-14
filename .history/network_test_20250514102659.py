# See AI_CODING_BASELINE_RULES.md for required practices.
import pytest
import socket

try:
    import websocket
except ImportError:
    websocket = None

def test_dns_resolution_localhost():
    """Ensure DNS resolution works for localhost on port 8181."""
    ip_info = socket.getaddrinfo('localhost', 8181)
    assert ip_info, "DNS resolution for localhost failed"

def test_tcp_socket_connection_localhost():
    """Ensure TCP socket connection to localhost:8181."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    result = s.connect_ex(('localhost', 8181))
    s.close()
    assert result == 0, f"TCP connection failed with error code {result}"

@pytest.mark.skipif(websocket is None, reason="websocket-client not available")
def test_websocket_connection_localhost():
    """Ensure WebSocket connection to localhost:8181/core."""
    ws = websocket.create_connection("ws://localhost:8181/core", timeout=5)
    assert ws.connected, "WebSocket connection failed"
    ws.close()
