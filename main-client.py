from client_server_network.client import Client
from client_server_network.interface import UserInterface
import socket

# device's IP address
SERVER_HOST = socket.gethostname()
SERVER_PORT = 5003

c = Client(SERVER_HOST, SERVER_PORT)
c._connect()
d = dict(zip(range(10), range(10)))

# class Hello:
#     pass
# d = Hello()

c.transfer_object("json", d, encrypt=True)

while True:
    c.transfer_object("json", d, encrypt=True)
    c.transfer_file("/Users/alex/PycharmProjects/client_server_network/client_server_network/sample_files/file1.txt",
                    encrypt=True)
    input()

# UserInterface(SERVER_HOST, SERVER_PORT)