import socket
import configparser
from client_server_network.server import Server

# Comment out if not using config file
config = configparser.ConfigParser()
config.read("config.cfg")
if config["Config"].getboolean("use_config"):
    host = config['LocalServer']['host']
    SERVER_HOST = socket.gethostname() if host.lower() == "localhost" else host
    SERVER_PORT = config['LocalServer'].getint('port')
else:
    # device's IP address
    SERVER_HOST = socket.gethostname()
    SERVER_PORT = 5432

s = Server(SERVER_HOST, SERVER_PORT)
s.recvall()

