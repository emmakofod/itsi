#!/usr/bin/python3

from socket import *
server_port = 12001
server_socket = socket(AF_INET,SOCK_STREAM)

while True:
    try:
        server_socket.bind(('', server_port))
        break  # it works - so break
    except OSError:
        new_port = input("The port is already in use, try another one: ")
        server_port = int(new_port)  # Update the variable + convert to int
        # the loop continues, tries again with new port
        

server_socket.listen(1)
print("The server is ready to receive")

while True:
    conn_socket,client_address = server_socket.accept()
    modified_message =conn_socket.recv(2048).decode().upper()
    conn_socket.send(modified_message.encode())
    print("the ip is: ", client_address[0])
    print("connection received from {}, and {} is sent back".format(client_address[1],modified_message))
    conn_socket.close()
server_socket.close()
