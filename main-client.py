from client_server_network.client import Client
from client_server_network.interface import UserInterface

# device's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5003

# c = Client(SERVER_HOST, SERVER_PORT)
# c._connect()
# d = dict(zip(range(10), range(10)))
# while True:
#     # c.transfer_object("json", d, encrypt=True)
#     c.transfer_file("/Users/alex/PycharmProjects/client_server_network/client_server_network/sample_files/file1.txt",
#                     encrypt=True)
#     input()

UserInterface(SERVER_HOST, SERVER_PORT)
