print("--- Test Import Script Started ---")
try:
    import websocket
    print(f"DEBUG: websocket library imported successfully. Version: {websocket.__version__}")
    import ssl
    print("DEBUG: ssl library imported successfully.")
    import socket
    print("DEBUG: socket library imported successfully.")
except Exception as e:
    print(f"!!! ERROR during import: {type(e).__name__} - {e}")
    import traceback
    traceback.print_exc() # This will print the full traceback if an import fails
print("--- Test Import Script Finished ---")
