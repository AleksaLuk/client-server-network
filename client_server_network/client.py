"""
Client
"""

import logging
import socket

import tqdm
import os
from .utils import encrypt_message, serialise_object

logger = logging.getLogger(__name__)
logging.basicConfig(format=f"CLIENT: %(asctime)s %(levelname)s - %(message)s",
                    level=logging.INFO,
                    # filename="client_server_history.log",
                    handlers=[
                            logging.FileHandler("client_history.log"),
                            logging.StreamHandler()
                        ]
                    )
BUFFER_SIZE = 4096
HEADERSIZE = 10


class Client(socket.socket):
    def __init__(self, host, port, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host = host
        self.port = port

    def _connect(self):
        self.connect((self.host, self.port))
        logger.info(f"Connected to HOST: {self.host} & PORT: {self.port}")

    def receive_message(self):
        message_header = self.recv(HEADERSIZE)
        # print(message_header.decode())
        message_length = int(message_header.decode('utf-8').strip())
        message = self.recv(message_length)
        logger.info(f"Received message from server: {message}")

    def transfer_object(self, serialisation_method, obj, encrypt=True):
        """
        Sends a python object to a server.

        :param host: The ip address or hostname of the server - the receiver.
        :param port: Port of the server
        :param serialisation_method: Method used to serialise data (xml, json, binary).
        :param obj: python object to be sent e.g. dictionary.
        :return:
        """

        transformed_object = serialise_object(obj, serialisation_method)
        if encrypt:
            transformed_object = encrypt_message(transformed_object)

        send_type = "object"
        message = f"{send_type:<{HEADERSIZE}}"
        message += f"{encrypt:<{HEADERSIZE}}"
        message += f"{serialisation_method:<{HEADERSIZE}}"
        message += f"{len(transformed_object):<{HEADERSIZE}}"

        # send object:
        self.sendall(bytes(message, "utf-8") + transformed_object)
        logger.info(f"Serialised object sent to server")

        self.receive_message()

    def transfer_file(self, filepath, encrypt=True):
        """
        Sends a file to a server.

        :param host: The ip address or hostname of the server - the receiver.
        :param port: Port of the server
        :param file_name: File to be sent.
        :return:
        """

        # get the file size
        filesize = os.path.getsize(filepath)
        filename = os.path.basename(filepath)
        send_type = "file"
        message = f"{send_type:<{HEADERSIZE}}"
        message += f"{encrypt:<{HEADERSIZE}}"
        message += f"{filename:<{HEADERSIZE}}"
        message += f"{filesize:<{HEADERSIZE}}"

        file_contents = b""

        # start sending the file
        logger.info(f"Transferring {filename} to server...")
        progress = tqdm.tqdm(range(filesize), f"CLIENT: Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filepath, "rb") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break
                # use sendall to assure transmission in
                # busy networks
                file_contents += bytes_read
                # update the progress bar
                progress.update(len(bytes_read))
        # self.receive_message()
        if encrypt:
            file_contents = encrypt_message(file_contents)

        self.sendall(bytes(message, "utf-8") + file_contents)
        logger.info(f"{filename} transfer complete")
        self.receive_message()
