# test_ws_to_file.py
import sys
import websocket # Using the common 'websocket-client' library
import ssl
import traceback

# Redirect stdout and stderr to a file
output_file_path = '/tmp/test_output.txt'
original_stdout = sys.stdout
original_stderr = sys.stderr

with open(output_file_path, 'w') as f:
    sys.stdout = f
    sys.stderr = f

    ws_url = "ws://172.20.0.2:8181/core" # Using the direct IP of ovos_messagebus

    print(f"--- Python WebSocket Test Script Started ---")
    print(f"Attempting to connect to WebSocket: {ws_url}")
    
    try:
        # For verbose output from the websocket-client library itself
        websocket.enableTrace(True) 
        
        # Attempt to create a connection
        ws = websocket.create_connection(ws_url,
                                        sslopt={"cert_reqs": ssl.CERT_NONE},
                                        timeout=15) # Increased timeout slightly
        
        print("WebSocket connection established!")
        
        # Optional: Send a simple message if you want to test communication
        # message = '{ "type": "mycroft.echo", "data": { "message": "Hello from client" } }'
        # print(f"Sending: {message}")
        # ws.send(message)
        # response = ws.recv()
        # print(f"Received: {response}")
        
        ws.close()
        print("WebSocket connection closed.")
        print("--- Test Script Successful ---")

    except ConnectionRefusedError as e:
        print(f"!!! ConnectionRefusedError: {e}")
        traceback.print_exc()
    except websocket._exceptions.WebSocketTimeoutException as e:
        print(f"!!! WebSocketTimeoutException: {e}")
        traceback.print_exc()
    except websocket._exceptions.WebSocketConnectionClosedException as e:
        print(f"!!! WebSocketConnectionClosedException: {e}")
        traceback.print_exc()
    except websocket._exceptions.WebSocketException as e:
        print(f"!!! WebSocketException ({type(e).__name__}): {e}")
        traceback.print_exc()
    except Exception as e:
        print(f"!!! An unexpected error occurred: {type(e).__name__} - {e}")
        traceback.print_exc()
    
    print(f"--- Python WebSocket Test Script Finished ---")

# Restore stdout and stderr
sys.stdout = original_stdout
sys.stderr = original_stderr
