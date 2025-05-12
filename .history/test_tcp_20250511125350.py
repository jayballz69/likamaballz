# test_tcp.py
print("--- TCP Test: BEFORE ---")
try:
    import socket
    s = socket.create_connection(("172.20.0.2", 8181), timeout=5)
    print("--- TCP Test: CONNECTED ---")
    s.close()
except Exception as e:
    print(f"!!! TCP Test: ERROR: {type(e).__name__} - {e}")
print("--- TCP Test: FINISHED ---")
