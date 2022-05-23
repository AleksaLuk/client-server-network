"""
Demonstration of client connection.
"""


from client_server_network.client import Client
from client_server_network.interface import UserInterface
import socket

# AWS (User does not need to run own server instance)
SERVER_HOST = "18.135.93.207"  # AWS public IP
SERVER_PORT = 80  # AWS port

# Localhost (User must run main-server.py first)
# SERVER_HOST = socket.gethostname()
# SERVER_PORT = 5433

# Through code
# c = Client(SERVER_HOST, SERVER_PORT)
# c.connection()
# data = dict(zip(range(10), range(10)))
# c.transfer_object("json", data, encrypt=True)

# Through GUI
# ui = UserInterface(SERVER_HOST, SERVER_PORT)
# ui.run()

# Through Config
ui = UserInterface()
ui.run(config_file="config.cfg")
