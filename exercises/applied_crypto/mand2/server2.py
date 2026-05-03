#!/usr/bin/python3

import socket
import threading

connections = []
total_connections = 0

class Client(threading.Thread):
    def __init__(self, sock, address, id):
        threading.Thread.__init__(self)
        self.socket = sock
        self.address = address
        self.id = id
        self.signal = True

    def run(self):
        while self.signal:
            try:
                data = self.socket.recv(1024)
                if not data:
                    continue

                print(f"[{self.id}] {data}")

                # broadcast til alle andre
                for client in connections:
                    if client.id != self.id:
                        client.socket.sendall(data)

            except:
                print(f"Client {self.id} disconnected")
                connections.remove(self)
                self.signal = False
                break


def new_connections(server_socket):
    global total_connections

    while True:
        sock, address = server_socket.accept()
        print(f"New connection: {address}")

        client = Client(sock, address, total_connections)
        connections.append(client)
        client.start()

        total_connections += 1


def main():
    host = input("Host: ")
    port = int(input("Port: "))

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print("Server started...")

    threading.Thread(target=new_connections, args=(server_socket,), daemon=True).start()

    while True:
        pass


main()
