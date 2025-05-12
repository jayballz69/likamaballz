# test_ws_minimal.py
print("--- Minimal WebSocket Test: BEFORE ---")
try:
    import websocket
    ws = websocket.create_connection("ws://172.20.0.2:8181/core", timeout=10)
    print("--- Minimal WebSocket Test: CONNECTED ---")
    ws.close()
except Exception as e:
    print(f"!!! Minimal WebSocket Test: ERROR: {type(e).__name__} - {e}")
print("--- Minimal WebSocket Test: FINISHED ---")
