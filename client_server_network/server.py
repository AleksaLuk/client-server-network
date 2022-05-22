"""
server
"""

import socket
import sys
import json
from json import JSONDecodeError
import pickle
import logging
import traceback
from .utils import decrypt_message, get_params


logger = logging.getLogger(__name__)
logging.basicConfig(format="SERVER: %(asctime)s %(levelname)s %(message)s",
                    level=logging.INFO,
                    # filemode='a',
                    handlers=[
                        logging.FileHandler("server_history.log"),
                        logging.StreamHandler()
                    ])

BUFFER_SIZE = 4096  # receive 4096 bytes each time
SEPARATOR = "<SEPARATOR>"
HEADERSIZE = 10


class Server(socket.socket):
    def __init__(self, host, port, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host = host
        self.port = port

    def recvall(self):
        # enabling our server to accept connections
        # 5 here is the number of unaccepted connections that
        # the system will allow before refusing new connections
        self.bind((self.host, self.port))
        self.listen(5)
        logger.info(f"[*] Listening as {self.host}:{self.port}")

        # try:
        #     while True:
        # accept connection if there is any
        while True:
            try:
                client_socket, address = self.accept()
            except KeyboardInterrupt:
                logger.info(f"Server {self.host}:{self.port} shutdown.")
                sys.exit()
            # if below code is executed, that means the sender is connected
            logger.info(f"[+] {address} is connected.")
            # receive the file infos
            # receive using client socket, not server socket
            self.receive_message(client_socket, address)

    @staticmethod
    def receive_object(received, metadata):
        if metadata['encrypt']:
            received = decrypt_message(received)
        if metadata['serialisation'].lower() == 'binary':
            data_loaded = pickle.loads(received)
        elif metadata['serialisation'].lower() == 'json':
            data_loaded = json.loads(received)
        else:
            logger.warning("Incorrect serialisation option provided")
        logger.info(f"Received OBJECT: type={type(data_loaded)}\n{data_loaded}")
        return data_loaded

    @staticmethod
    def receive_file(received, metadata):
        if metadata['encrypt']:
            received = decrypt_message(received)
        with open(metadata['filename'], "wb") as f:
            f.write(received)

        logger.info(f"Received FILE\n\n{received}")
        return received

    def receive_message(self, s, address):
        while True:
            full_msg = b''
            new_msg = True
            quit = False
            while True:
                try:
                    msg = s.recv(64)
                    if not msg:
                        quit = True
                        logger.info(f"Client {address} disconnected.")
                        break
                except ConnectionResetError:
                    quit = True
                    logger.info(f"Client {address} disconnected.")
                    break
                if new_msg:
                    # print("new msg len:", msg[:HEADERSIZE])
                    try:
                        msg_params = get_params(msg, HEADERSIZE)
                    except ValueError as v:
                        logger.info(v)
                        continue
                    new_msg = False

                # print(f"full message length: {msg_params['length']}")

                full_msg += msg

                # print(len(full_msg))

                if len(full_msg) - 4 * HEADERSIZE == msg_params["length"]:
                    logger.info(f"Received message from {address}")
                    # print(pickle.loads(full_msg[HEADERSIZE:]))
                    # return full_msg[4 * HEADERSIZE:], msg_params
                    # s.sendall(bytes(f"{len(full_msg[HEADERSIZE:]):<{HEADERSIZE}}", 'utf-8') + bytes(full_msg[HEADERSIZE:]))
                    if not msg_params:
                        continue
                    msg = full_msg[4 * HEADERSIZE:]
                    # received = client_socket.recv(BUFFER_SIZE)
                    # metadata = pickle.loads(received)
                    # print(metadata)
                    print(msg_params)
                    if msg_params['type'] == 'file':
                        send_msg = self.receive_file(msg, msg_params)
                        send_msg = b"File sent successfully: " + bytes(str(send_msg), "utf-8")
                    elif msg_params['type'] == 'object':
                        send_msg = self.receive_object(msg, msg_params)
                        send_msg = b"Object sent successfully: " + bytes(str(send_msg), "utf-8")
                    s.sendall(bytes(f"{len(send_msg):<{HEADERSIZE}}", 'utf-8') + send_msg)
                    new_msg = True
                    full_msg = b""
            if quit:
                break
