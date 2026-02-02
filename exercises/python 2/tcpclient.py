#!/usr/bin/python3

from socket import *
server_name="localhost"
server_port = 12001
client_socket = socket(AF_INET,SOCK_STREAM)
client_socket.connect((server_name,server_port))
message=input("Please enter your lowercase message: ")
client_socket.send(message.encode())
modified_message = client_socket.recv(2048)
print("From server: ", modified_message.decode())
client_socket.close()
