import socket

from client_server_network.server import Server

# device's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5003

s = Server(SERVER_HOST, SERVER_PORT)
s.recvall()
