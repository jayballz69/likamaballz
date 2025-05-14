import websocket
import ssl
import pytest
import traceback

ws_url = "ws://localhost:8181/core"  # Use host-mapped port for ovos_messagebus

def test_final_messagebus_connection():
    """Final WebSocket connectivity test for ovos_messagebus via localhost."""
    ws = None
    try:
        websocket.enableTrace(True)
        ws = websocket.create_connection(ws_url, sslopt={"cert_reqs": ssl.CERT_NONE}, timeout=20)
        assert ws.connected, f"Connection not established to {ws_url}"
    except websocket._exceptions.WebSocketTimeoutException as e:
        pytest.fail(f"WebSocketTimeoutException when connecting to {ws_url}: {e}")
    except ConnectionRefusedError as e:
        pytest.fail(f"ConnectionRefusedError when connecting to {ws_url}: {e}")
    except Exception as e:
        traceback.print_exc()
        pytest.fail(f"Unexpected error during WebSocket test: {type(e).__name__} - {e}")
    finally:
        if ws:
            ws.close()
            print("DEBUG: WebSocket connection closed in final test.")
    print("--- Final WebSocket Test: Completed ---")
