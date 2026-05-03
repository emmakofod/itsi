#!/usr/bin/python3

import socket
import threading
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

aes_key = None
aesgcm = None


def receive_tcp(sock):
    global aesgcm

    while True:
        try:
            data = sock.recv(1024)

            if data.startswith(b"MSG:"):
                nonce = data[4:16]
                ciphertext = data[16:]

                plaintext = aesgcm.decrypt(nonce, ciphertext, None)
                print("Received:", plaintext.decode())

        except:
            print("Disconnected")
            break


def receive_udp(udp_sock):
    global aes_key, aesgcm

    print("Waiting for AES key via UDP...")

    data, addr = udp_sock.recvfrom(1024)
    aes_key = data
    aesgcm = AESGCM(aes_key)

    print("\nKey received → secure chat ready")


def main():
    global aes_key, aesgcm

    host = input("Server IP: ")
    port = int(input("Server TCP port: "))

    # TCP connection
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.connect((host, port))

    # UDP socket
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_port = int(input("Your UDP port: "))
    udp_sock.bind(("", udp_port))

    # start UDP listener
    threading.Thread(target=receive_udp, args=(udp_sock,), daemon=True).start()

    choice = input("Send key? (y/n): ")

    if choice.lower() == "y":
        target_ip = input("Target IP: ")
        target_port = int(input("Target UDP port: "))

        aes_key = AESGCM.generate_key(bit_length=128)
        aesgcm = AESGCM(aes_key)

        udp_sock.sendto(aes_key, (target_ip, target_port))
        print("Key sent!")

    # start TCP receiver
    threading.Thread(target=receive_tcp, args=(tcp_sock,), daemon=True).start()

    # chat loop
    while True:
        message = input()

        if not aesgcm:
            print("No key yet")
            continue

        nonce = os.urandom(12)
        ciphertext = aesgcm.encrypt(nonce, message.encode(), None)

        tcp_sock.sendall(b"MSG:" + nonce + ciphertext)


main()
