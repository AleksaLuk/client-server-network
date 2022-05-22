"""
Client module
"""

import logging
import socket

import tqdm
import os
from .utils import encrypt_message, serialise_object, create_headers

logger = logging.getLogger(__name__)

logging.basicConfig(format=f"CLIENT: %(asctime)s %(levelname)s - %(message)s",
                    level=logging.INFO,
                    handlers=[
                            logging.FileHandler("client_history.log"),
                            logging.StreamHandler()
                        ]
                    )
BUFFER_SIZE = 4096
HEADERSIZE = 10


class Client(socket.socket):
    """
    Client class to interact and send data to server
    """

    def __init__(self, host: str, port: int, *args, **kwargs):
        """
        :param host: The ip address or hostname of the server - the receiver
        :param port: The port of the server - the receiver
        """

        super().__init__(*args, **kwargs)
        self.host = host
        self.port = port

    def connection(self):
        """
        Connect to server
        """

        self.connect((self.host, self.port))
        logger.info(f"Connected to HOST: {self.host} & PORT: {self.port}")

    def receive_message(self):
        """
        Receive response from the server
        """

        message_header = self.recv(HEADERSIZE)
        # print(message_header.decode())
        message_length = int(message_header.decode('utf-8').strip())
        message = self.recv(message_length)
        logger.info(f"Received message from server: {message}")

    def transfer_object(self, serialisation_method: str, obj: any, encrypt=True):
        """
        Sends a python object to a server.

        :param serialisation_method: Method used to serialise data (xml, json, binary).
        :param obj: python object to be sent e.g. dictionary, list, class (binary only)
        :param encrypt: provide object encryption
        """

        transformed_object = serialise_object(obj, serialisation_method)
        if encrypt:
            transformed_object = encrypt_message(transformed_object)

        metadata = create_headers(HEADERSIZE, "object", encrypt, serialisation_method, len(transformed_object))
        # send object:
        self.sendall(bytes(metadata, "utf-8") + transformed_object)
        logger.info(f"Serialised object sent to server")

        self.receive_message()

    def transfer_file(self, filepath: str, encrypt=True):
        """
        Sends a file to a server.

        :param file_path: Path of file to be sent.
        :param encrypt: choose whether encrypt file contents
        """

        # get the file size
        filesize = os.path.getsize(filepath)
        filename = os.path.basename(filepath)
        metadata = create_headers(HEADERSIZE, "file", encrypt, filename, filesize)

        file_contents = b""

        # start sending the file
        logger.info(f"Transferring {filename} to server...")

        progress = tqdm.tqdm(range(filesize), f"CLIENT: Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filepath, "rb") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                # print("A", bytes_read)
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

        self.sendall(bytes(metadata, "utf-8") + file_contents)
        logger.info(f"{filename} transfer complete")
        self.receive_message()
