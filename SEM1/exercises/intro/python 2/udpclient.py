#!/usr/bin/python3

from socket import *
server_name="localhost"
server_port = 12000
message=input("Please enter your lowercase message: ")
client_socket = socket(AF_INET,SOCK_DGRAM)
client_socket.sendto(message.encode(),(server_name,server_port))
modified_message,server_address = client_socket.recvfrom(2048)
print("From Server: "+modified_message.decode())
client_socket.close()
