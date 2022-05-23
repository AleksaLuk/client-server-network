"""
Server module
"""

import socket
import sys
import json
import pickle
import logging
from .utils import decrypt_message, get_params


logger = logging.getLogger(__name__)
logging.basicConfig(
    format="SERVER: %(asctime)s %(levelname)s %(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler("server_history.log"), logging.StreamHandler()],
)

BUFFER_SIZE = 4096  # receive 4096 bytes each time
SEPARATOR = "<SEPARATOR>"
HEADERSIZE = 10


class Server(socket.socket):
    """
    Server class to receive data from client
    """

    def __init__(self, host: str, port: int, *args, **kwargs):
        """
        :param host: The ip address or hostname of the server - the receiver
        :param port: The port of the server - the receiver
        """

        super().__init__(*args, **kwargs)
        self.host = host
        self.port = port

    def recvall(self):
        """
        Accept and listen for new client connections
        """

        self.bind((self.host, self.port))
        # number of unaccepted connections before refusing new connections
        self.listen(5)
        logger.info("[*] Listening as {}:{}".format(self.host, self.port))

        while True:
            try:
                client_socket, address = self.accept()
            except KeyboardInterrupt:
                logger.info("Server {}:{} shutdown.".format(self.host, self.port))
                sys.exit()
            logger.info("[+] {} is connected.".format(address))
            # receive using client socket, not server socket
            self.receive_message(client_socket, address)

    @staticmethod
    def receive_object(received: bytes, metadata: dict):
        """
        Transforming incoming data sent from client

        :param received: incoming data to be decyrpted/deserialised
        :param metadata: metadata containing information about incoming data
        :return: loaded data
        """

        if metadata["encrypt"]:
            received = decrypt_message(received)
        if metadata["serialisation"].lower() == "binary":
            data_loaded = pickle.loads(received)
        elif metadata["serialisation"].lower() == "json":
            data_loaded = json.loads(received)
        else:
            logger.warning("Incorrect serialisation option provided")
            raise ValueError("Incorrect serialisation option provided")
        logger.info("Received OBJECT: type={}\n{}".format(type(data_loaded), data_loaded))
        return data_loaded

    @staticmethod
    def receive_file(received: bytes, metadata: dict):
        """
        Transforming incoming data sent from client file

        :param received: incoming data to be decyrpted/deserialised
        :param metadata: metadata containing information about incoming data
        :return: loaded data
        """

        if metadata["encrypt"]:
            received = decrypt_message(received)
        with open(metadata["filename"], "wb") as file:
            file.write(received)

        logger.info("Received FILE\n\n{}".format(received))
        return received

    def receive_message(self, sock: socket.socket, address: str):
        """
        While loop connection for a specific client to receive requests and send back responses

        :param sock: client socket
        :param address: address of client
        """

        while True:
            full_msg = b""
            new_msg = True
            break_connection = False
            while True:
                try:
                    msg = sock.recv(64)
                    if not msg:
                        break_connection = True
                        logger.info("Client {} disconnected.".format(address))
                        break
                except ConnectionResetError:
                    break_connection = True
                    logger.info("Client {} disconnected.".format(address))
                    break
                if new_msg:
                    try:
                        msg_params = get_params(msg, HEADERSIZE)
                    except ValueError as val:
                        logger.info(val)
                        continue
                    new_msg = False

                full_msg += msg

                if len(full_msg) - 4 * HEADERSIZE == msg_params["length"]:
                    logger.info("Received message from {}".format(address))
                    if not msg_params:
                        continue
                    msg = full_msg[4 * HEADERSIZE:]
                    logger.info("Metadata: {}".format(msg_params))
                    if msg_params["type"] == "file":
                        send_msg = self.receive_file(msg, msg_params)
                        send_msg = b"File sent successfully: " + bytes(
                            str(send_msg), "utf-8"
                        )
                    elif msg_params["type"] == "object":
                        try:
                            send_msg = self.receive_object(msg, msg_params)
                            send_msg = b"Object sent successfully: " + bytes(
                                str(send_msg), "utf-8"
                            )
                        except ValueError:
                            continue
                    sock.sendall(
                        bytes(f"{len(send_msg):<{HEADERSIZE}}", "utf-8") + send_msg
                    )
                    new_msg = True
                    full_msg = b""
            if break_connection:
                break
