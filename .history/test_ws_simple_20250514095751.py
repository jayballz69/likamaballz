# test_ws_simple.py
# Pytest-based test for websocket-client import
import pytest
import websocket

def test_websocket_client_import():
    """Test that websocket-client can be imported and has a version attribute."""
    assert websocket is not None, "Failed to import websocket-client"
    assert hasattr(websocket, "__version__"), "websocket-client has no __version__ attribute"
    print(f"websocket-client version: {websocket.__version__}")
