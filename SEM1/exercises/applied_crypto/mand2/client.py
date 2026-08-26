import socket
import threading
import os
import time
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

TCP_PORT = 5000
UDP_PORT = 5001

server_ip = input("Server IP: ").strip()
username  = input("Username: ").strip()

key    = os.urandom(32)
aesgcm = AESGCM(key)

# Connect TCP first -> know our local port
tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.connect((server_ip, TCP_PORT))
my_tcp_port = tcp_sock.getsockname()[1]  # our local port
print(f"[TCP] Connected from local port {my_tcp_port}")

# Send: tcp_port (2 bytes) + key (32 bytes) via UDP
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.sendto(my_tcp_port.to_bytes(2, 'big') + key, (server_ip, UDP_PORT))
udp_sock.close()
print(f"[UDP] Key sent (port {my_tcp_port}): {key.hex()}")

time.sleep(0.3)

def receive():
    while True:
        data = tcp_sock.recv(4096)
        if not data:
            break
        plaintext = aesgcm.decrypt(data[:12], data[12:], None)
        print(f"\n{plaintext.decode()}")

threading.Thread(target=receive, daemon=True).start()

print("Type a message and press Enter. Ctrl+C to quit.\n")
while True:
    msg   = input()
    nonce = os.urandom(12)
    ct    = aesgcm.encrypt(nonce, f"{username}: {msg}".encode(), None)
    tcp_sock.sendall(nonce + ct)