#!/usr/bin/python3

import socket
import threading
import sys
import random
import hashlib
import base64
from cryptography.fernet import Fernet

private_key = None
public_key = None
shared_secret = None
cipher = None
p = None
g = None

def receive(sock, signal):
    global private_key, public_key, shared_secret, cipher, p, g

    while signal:
        try:
            data = sock.recv(1024)

            # MODTAG PARAMS
            if data.startswith(b"PARAMS:"):
                params = data.decode().split(":")[1]
                p, g = map(int, params.split(","))
                print(f"Received p={p}, g={g}")

            # NYT: REQUEST fra anden klient
            elif data.startswith(b"REQUEST:"):
                sender_id = data.decode().split(":")[1]
                print(f"Client {sender_id} wants to connect. Type: ACCEPT:{sender_id}")

            # NYT: START_DH → start key exchange
            elif data.startswith(b"START_DH"):
                print("Starting Diffie-Hellman...")

                private_key = random.randint(1, 10)
                public_key = pow(g, private_key, p)

                sock.sendall(f"KEY:{public_key}".encode())

            # MODTAG KEY
            elif data.startswith(b"KEY:"):
                other_public = int(data.decode().split(":")[1])

                shared_secret = pow(other_public, private_key, p)
                print(f"Shared secret: {shared_secret}")

                # NYT: lav encryption key
                key = hashlib.sha256(str(shared_secret).encode()).digest()
                key = base64.urlsafe_b64encode(key)
                cipher = Fernet(key)

                print("Secure channel established")

            # MODTAG BESKED
            elif data.startswith(b"MSG:"):
                encrypted = data[4:]
                decrypted = cipher.decrypt(encrypted)
                print("Received:", decrypted.decode())

            else:
                print(data.decode())

        except:
            print("Disconnected from server")
            break


# connect
host = input("Host: ")
port = int(input("Port: "))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

threading.Thread(target=receive, args=(sock, True), daemon=True).start()

# NYT: brugeren vælger hvem der skal connectes til
print("Type CONNECT:<id> to start connection")

while True:
    message = input()

    # NYT: CONNECT / ACCEPT sendes raw
    if message.startswith("CONNECT:") or message.startswith("ACCEPT:"):
        sock.sendall(message.encode())

    # NYT: kun send encrypted hvis cipher findes
    elif cipher:
        encrypted = cipher.encrypt(message.encode())
        sock.sendall(b"MSG:" + encrypted)

    else:
        print("No secure connection yet")
