# test_ws.py
import websocket # Using the common 'websocket-client' library
import ssl
import sys

ws_url = "ws://172.20.0.2:8181/core" # Use the direct IP of ovos_messagebus

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
    sys.exit(0) # Exit with success code

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

sys.exit(1) # Exit with error code if any exception occurred
