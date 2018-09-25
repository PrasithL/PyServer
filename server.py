import os
import socket
import config
import helpers
from request import Request
import http_responses as http

HOST = config.HOST
PORT = config.PORT

# create a TCP socket
with socket.socket() as server_sock:
    # tell the kernel to reuse the sockets that are in 'TIME_WAIT' state
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # bind socket to address
    server_sock.bind((HOST, PORT))

    # set number of pending connections apart from the active connection
    # set 0 allow only one connection and refuse any additional connections
    server_sock.listen(0)

    print("listening on %s:%s..." % (HOST, PORT))

    while True:
        client_sock, client_addr = server_sock.accept()
        print(client_addr)
        with client_sock:
            try:
                request = Request.from_socket(client_sock)
                if request.method != "GET":
                    client_sock.sendall(http.METHOD_NOT_ALLOWED_RESPONSE)
                    continue

                helpers.serve_file(client_sock, request.path)
            except Exception as e:
                print("Failed to parse request" + e)
                client_sock.sendall(http.BAD_REQUEST_RESPONSE)