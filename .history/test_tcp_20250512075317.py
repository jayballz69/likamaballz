import socket

HOST = "ovos_messagebus"  # Docker service name resolves via Docker network
PORT = 8181

print("--- TCP Socket Test Started ---")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)
try:
    s.connect((HOST, PORT))
    print(f"SUCCESS: Connected to {HOST}:{PORT}")
except Exception as e:
    print(f"FAIL: Could not connect to {HOST}:{PORT} - {e}")
finally:
    s.close()
print("--- TCP Socket Test Finished ---")
