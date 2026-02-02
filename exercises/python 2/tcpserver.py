#!/usr/bin/python3

from socket import *
server_port = 12001
server_socket = socket(AF_INET,SOCK_STREAM)
server_socket.bind(('',server_port))
server_socket.listen(1)
print("The server is ready to receive")
while True:
    conn_socket,client_address = server_socket.accept()
    modified_message =conn_socket.recv(2048).decode().upper()
    conn_socket.send(modified_message.encode())
    print("connection received from {}, and {} is sent back".format(client_address[1],modified_message))
    conn_socket.close()
server_socket.close()
