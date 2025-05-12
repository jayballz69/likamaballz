import sys
import traceback

WS_URL = "ws://172.20.0.2:8181/core"
CONNECTION_TIMEOUT = 20  # seconds

try:
    print(f"DEBUG: Importing websocket library...")
    import websocket
    print(f"DEBUG: websocket library imported. Version: {websocket.__version__}")

    print(f"DEBUG: Attempting websocket.create_connection(url='{WS_URL}', timeout={CONNECTION_TIMEOUT})...")
    ws = websocket.create_connection(WS_URL, timeout=CONNECTION_TIMEOUT)
    print("--- Minimal WebSocket Test: SUCCESS! WebSocket connection established. ---")
    print(f"DEBUG: Websocket object: {ws}")
    print(f"DEBUG: Websocket connected: {ws.connected}")
    ws.close()
    print("DEBUG: WebSocket connection closed.")
    print("--- Minimal WebSocket Test: Finished Successfully ---")
    sys.exit(0)

except ConnectionRefusedError as e:
    print(f"!!! Minimal WebSocket Test: ConnectionRefusedError: {e}")
    traceback.print_exc()
except websocket._exceptions.WebSocketTimeoutException as e:
    print(f"!!! Minimal WebSocket Test: WebSocketTimeoutException: {e}")
    traceback.print_exc()
except websocket._exceptions.WebSocketConnectionClosedException as e:
    print(f"!!! Minimal WebSocket Test: WebSocketConnectionClosedException: {e}")
    traceback.print_exc()
except websocket._exceptions.WebSocketBadStatusException as e:
    print(f"!!! Minimal WebSocket Test: WebSocketBadStatusException: {e.status_code} - {e}")
    traceback.print_exc()
except websocket._exceptions.WebSocketException as e:
    print(f"!!! Minimal WebSocket Test: WebSocketException ({type(e).__name__}): {e}")
    traceback.print_exc()
except ImportError as e:
    print(f"!!! Minimal WebSocket Test: ImportError: {e}")
    traceback.print_exc()
except Exception as e:
    print(f"!!! Minimal WebSocket Test: An unexpected Python error occurred: {type(e).__name__} - {e}")
    traceback.print_exc()

print("--- Minimal WebSocket Test: Finished (likely on an error path if not exited yet) ---")
sys.exit(1)
