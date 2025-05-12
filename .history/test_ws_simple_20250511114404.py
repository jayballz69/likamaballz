# test_ws_simple.py
print("--- Simple Test Script Started ---")
try:
    import websocket
    print(f"websocket-client version: {websocket.__version__}")
    print("Import successful.")
except Exception as e:
    print(f"Error importing websocket: {e}")
print("--- Simple Test Script Finished ---")
