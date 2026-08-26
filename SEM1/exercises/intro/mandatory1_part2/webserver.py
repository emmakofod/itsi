#!/usr/bin/python3
from datetime import datetime
from socket import *
host = "localhost"
server_port = 6789
server_socket = socket(AF_INET, SOCK_STREAM)

status_code= 0


while True:
    try:
        server_socket.bind((host, server_port))
        break
    except OSError:
        new_port = server_port + 1

server_socket.listen(1)
print("The server is ready to listen.")

while True:
    conn_socket,client_address = server_socket.accept()
    message =conn_socket.recv(2048).decode()
    print("Connection has be made")
    print("message is: ", message)
    print("the ip is: ", client_address[0])

    try:
        first_line = message.split('\n')[0]
        parts = first_line.split(' ')
        filename = parts[1][1:] 
        print("The browser wants: ", filename)

        if not filename:
            filename = "index.html"

        try: 
            with open(f"./{filename}", "r") as file:
                file_content = file.read()

                response = "HTTP/1.1 200 OK \r\n"
                response += "Content-type: text/html\r\n"
                response += "\r\n" 
                response += file_content
            status_code = 200


        except FileNotFoundError:
            response = "HTTP/1.1 404 Not Found \r\n"
            response += "Content-Type: text/html\r\n"
            response += "\r\n"
            response += "<h1>404 - Not Found</h1>"

            status_code = 404

        
        conn_socket.send(response.encode())

        print("connection received from {}, and {} is sent back".format(client_address[1],response))


        ip = client_address[0]
        timestamp = datetime.now().strftime("[%d/%b/%Y:%H:%M:%S +0000]")
        request_line = first_line.strip()
        response_size = len(response.encode())

        
        log_entry = f'{ip} - - {timestamp} "{request_line}" {status_code} {response_size}'
        with open("server.log", "a") as log_file:
            log_file.write(log_entry + "\n")

    except (IndexError, Exception):

        response = "HTTP/1.1 400 Bad Request\r\n"
        response += "Content-Type: text/html\r\n"
        response += "\r\n"
        response += "<h1>400 - Bad Request</h1>"

        status_code = 400

        timestamp = datetime.now().strftime("[%d/%b/%Y:%H:%M:%S +0000]")
        request_line = first_line.strip()
        response_size = len(response.encode())

        log_entry = f'{ip} - - {timestamp} "{request_line}" {status_code} {response_size}'

        with open("server.log", "a") as log_file:
            log_file.write(log_entry + "\n")

   
    conn_socket.close()
server_socket.close()

