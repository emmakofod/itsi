#!/usr/bin/python3

from socket import *
server_port = 12000
server_socket = socket(AF_INET,SOCK_DGRAM)
server_socket.bind(('',server_port))
print("The server is ready to receive")
while True:
    message,client_address = server_socket.recvfrom(2048)
    modified_message = message.decode().upper()
    server_socket.sendto(modified_message.encode(),client_address)
    print("connection received from {}, {} was recieved and {} is sent back".format(client_address,message.decode(),modified_message))
server_socket.close()
