"""
Demonstration of server connection.
"""

import socket
import configparser
import os
from client_server_network.server import Server


config = configparser.ConfigParser()
config.read(os.path.dirname(__file__) + "/config.cfg")
# Get config variables if use_config == True
if config["Config"].getboolean("use_config"):
    host = config['LocalServer']['host']
    SERVER_HOST = socket.gethostname() if host.lower() == "localhost" else host
    SERVER_PORT = config['LocalServer'].getint('port')
else:
    # device's IP address
    SERVER_HOST = socket.gethostname()
    SERVER_PORT = 5433

s = Server(SERVER_HOST, SERVER_PORT)
s.recvall()
