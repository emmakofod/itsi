#!/usr/bin/python3

import socket
import threading

connections = []
total_connections = 0

p = 23
g = 5

# NYT: gem hvem der vil connecte til hvem
pending_requests = {}  # {target_id: sender_id}

class Client(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal
    
    def __str__(self):
        return str(self.id) + " " + str(self.address)
    
    def run(self):
        while self.signal:
            try:
                data = self.socket.recv(1024)
            except:
                print("Client " + str(self.address) + " disconnected")
                self.signal = False
                connections.remove(self)
                break

            if not data:
                continue

            message = data.decode("utf-8")
            print(f"ID {self.id}: {message}")

            # NYT: håndter CONNECT
            if message.startswith("CONNECT:"):
                target_id = int(message.split(":")[1])

                pending_requests[target_id] = self.id

                connections[target_id].socket.sendall(
                    f"REQUEST:{self.id}".encode()
                )

            # NYT: håndter ACCEPT
            elif message.startswith("ACCEPT:"):
                sender_id = int(message.split(":")[1])

                # send START_DH til begge
                connections[sender_id].socket.sendall(b"START_DH")
                self.socket.sendall(b"START_DH")

            # NYT: videresend kun KEY og MSG (ikke CONNECT/ACCEPT)
            elif message.startswith("KEY:") or message.startswith("MSG:"):
                for client in connections:
                    if client.id != self.id:
                        client.socket.sendall(data)


def newConnections(socket):
    while True:
        sock, address = socket.accept()

        # SEND PARAMS (som før)
        sock.sendall(f"PARAMS:{p},{g}".encode())

        global total_connections
        client = Client(sock, address, total_connections, "Name", True)
        connections.append(client)
        client.start()

        print("New connection at ID " + str(client))
        total_connections += 1


def main():
    host = input("Host: ")
    port = int(input("Port: "))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)

    newConnectionsThread = threading.Thread(target=newConnections, args=(sock,))
    newConnectionsThread.start()

    # VIGTIGT: holder serveren kørende
    newConnectionsThread.join()


main()
