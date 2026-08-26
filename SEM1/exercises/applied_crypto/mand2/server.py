import socket
import threading
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

HOST = '0.0.0.0'
TCP_PORT = 5000
UDP_PORT = 5001

clients = {}  # { (ip, tcp_port): { 'conn': socket, 'key': bytes } }
clients_lock = threading.Lock()


def udp_key_listener():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind((HOST, UDP_PORT))
    print(f"[UDP] Listening for keys on port {UDP_PORT}")
    while True:
        data, addr = udp_sock.recvfrom(1024)
        # Client sends: tcp_port (2 bytes, big-endian) + key (32 bytes)
        tcp_port = int.from_bytes(data[:2], 'big')
        key = data[2:34]
        client_id = (addr[0], tcp_port)
        with clients_lock:
            if client_id not in clients:
                clients[client_id] = {}
            clients[client_id]['key'] = key
        print(f"[UDP] Key received from {client_id}")


def broadcast(plaintext, sender_id):
    with clients_lock:
        targets = {cid: info for cid, info in clients.items()
                   if cid != sender_id and 'conn' in info and 'key' in info}
    for cid, info in targets.items():
        nonce = os.urandom(12)
        cipherText = AESGCM(info['key']).encrypt(nonce, plaintext, None)
        info['conn'].sendall(nonce + cipherText)


def handle_client(conn, addr):
    client_id = addr  # (ip, tcp_port)
    print(f"[+] Connected: {client_id}")

    import time
    for _ in range(30):
        with clients_lock:
            if client_id in clients and 'key' in clients[client_id]:
                break
        time.sleep(0.1)

    with clients_lock:
        if 'key' not in clients.get(client_id, {}):
            print(f"[!] No key from {client_id}, closing")
            conn.close()
            return
        clients[client_id]['conn'] = conn

    while True:
        data = conn.recv(4096)
        if not data:
            break
        nonce = data[:12]
        cipherText = data[12:]
        with clients_lock:
            key = clients[client_id]['key']
        plaintext = AESGCM(key).decrypt(nonce, cipherText, None)
        print(f"[{client_id}] {plaintext.decode()}")
        broadcast(plaintext, client_id)

    conn.close()
    with clients_lock:
        clients.pop(client_id, None)
    print(f"[-] Disconnected: {client_id}")


threading.Thread(target=udp_key_listener, daemon=True).start()

tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_sock.bind((HOST, TCP_PORT))
tcp_sock.listen(10)
print(f"[TCP] Server listening on port {TCP_PORT}")

while True:
    conn, addr = tcp_sock.accept()
    threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()