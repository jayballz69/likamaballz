print("--- Final WebSocket Test: Script Started ---")
import sys # For sys.exit

try:
    print("DEBUG: Importing websocket, ssl, traceback...")
    import websocket
    import ssl
    import traceback # Ensure traceback is imported for use in except blocks
    print(f"DEBUG: Imports successful. websocket version: {websocket.__version__}")

    ws_url = "ws://172.20.0.2:8181/core"
    print(f"DEBUG: Attempting to connect to WebSocket: {ws_url}")

    websocket.enableTrace(True)

    ws = websocket.create_connection(ws_url, timeout=20)

    print("--- Final WebSocket Test: WebSocket connection established! ---")

    ws.close()
    print("--- Final WebSocket Test: WebSocket connection closed. ---")
    print("--- Final WebSocket Test: SUCCESS ---")
    sys.exit(0)

except ConnectionRefusedError as e:
    print(f"!!! Final WebSocket Test: ConnectionRefusedError: {e}")
    traceback.print_exc()
except websocket._exceptions.WebSocketTimeoutException as e:
    print(f"!!! Final WebSocket Test: WebSocketTimeoutException: {e}")
    traceback.print_exc()
except websocket._exceptions.WebSocketConnectionClosedException as e:
    print(f"!!! Final WebSocket Test: WebSocketConnectionClosedException: {e}")
    traceback.print_exc()
except websocket._exceptions.WebSocketBadStatusException as e:
    print(f"!!! Final WebSocket Test: WebSocketBadStatusException: {e}")
    print(f"    DEBUG: HTTP Status Code: {e.status_code}")
    traceback.print_exc()
except websocket._exceptions.WebSocketException as e:
    print(f"!!! Final WebSocket Test: WebSocketException ({type(e).__name__}): {e}")
    traceback.print_exc()
except ImportError as e:
    print(f"!!! Final WebSocket Test: ImportError: {e}")
    traceback.print_exc()
except Exception as e:
    print(f"!!! Final WebSocket Test: An unexpected Python error occurred: {type(e).__name__} - {e}")
    traceback.print_exc()

print("--- Final WebSocket Test: Script Finished (likely on an error path if not exited yet) ---")
sys.exit(1)
