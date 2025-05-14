# See AI_CODING_BASELINE_RULES.md for required practices.
# test_ws.py
import websocket # Using the common 'websocket-client' library
import ssl

ws_url = "ws://localhost:8181/core"  # Use host-mapped port for ovos_messagebus

print(f"Attempting to connect to WebSocket: {ws_url}")
try:
    # For verbose output from the websocket-client library itself
    websocket.enableTrace(True) 

    # Attempt to create a connection
    ws = websocket.create_connection(ws_url,
                                    sslopt={"cert_reqs": ssl.CERT_NONE},
                                    timeout=10) # Added a 10-second timeout

    print("WebSocket connection established!")

    # Optional: Send a simple message if you want to test communication
    # message = '{ "type": "mycroft.echo", "data": { "message": "Hello from client" } }'
    # print(f"Sending: {message}")
    # ws.send(message)
    # response = ws.recv()
    # print(f"Received: {response}")

    ws.close()
    print("WebSocket connection closed.")

except ConnectionRefusedError as e:
    print(f"ConnectionRefusedError: {e}")
except websocket._exceptions.WebSocketTimeoutException as e:
    print(f"WebSocketTimeoutException: {e}")
except websocket._exceptions.WebSocketConnectionClosedException as e:
    print(f"WebSocketConnectionClosedException: {e}")
except websocket._exceptions.WebSocketException as e:
    print(f"WebSocketException ({type(e).__name__}): {e}")
except Exception as e:
    print(f"An unexpected error occurred: {type(e).__name__} - {e}")
    import traceback
    traceback.print_exc()

# For pytest, define a test function instead of exiting at module level
def test_can_connect_to_messagebus():
    """Tests that a WebSocket connection can be established to ovos_messagebus."""
    ws = None
    try:
        ws = websocket.create_connection(
            ws_url,
            sslopt={"cert_reqs": ssl.CERT_NONE},
            timeout=10
        )
        assert ws.connected, f"Failed to connect to {ws_url}"
    finally:
        if ws:
            ws.close()
            print("WebSocket connection closed in test.")
