"""
server
"""

import socket
import tqdm
import os
import json
from json import JSONDecodeError
import pickle
import logging
import traceback
from .utils import decrypt_message


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


def get_params(msg):
    data_type = msg[:HEADERSIZE]
    encrypt = msg[HEADERSIZE: 2 * HEADERSIZE]
    param3 = msg[2 * HEADERSIZE: 3 * HEADERSIZE]
    length = msg[3 * HEADERSIZE: 4 * HEADERSIZE]

    metadata = {"type": data_type.strip().decode(),
                "encrypt": bool(encrypt),
                "length": int(length)}

    if metadata["type"] == 'object':
        metadata["serialisation"] = param3.strip().decode()
    elif metadata["type"] == 'file':
        metadata["filename"] = param3.strip().decode()

    return metadata


class Server(socket.socket):
    def __init__(self, host, port, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host = host
        self.port = port
        self.bind((host, port))

    def recvall(self):
        # enabling our server to accept connections
        # 5 here is the number of unaccepted connections that
        # the system will allow before refusing new connections
        self.listen(5)
        logger.info(f"[*] Listening as {self.host}:{self.port}")

        # try:
        #     while True:
        # accept connection if there is any
        while True:
            client_socket, address = self.accept()
            # if below code is executed, that means the sender is connected
            logger.info(f"[+] {address} is connected.")
            # receive the file infos
            # receive using client socket, not server socket

            self.receive_message(client_socket, address)

            # except EOFError:
            #     logger.warning("Connection opened but no data received")
            # except Exception as e:
            #     traceback.print_exc()
            #     logger.error(repr(e))
            # finally:
            #     client_socket.close()
            #     self.close()
            #     return self

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
        # start receiving the file from the socket
        # and writing to the file stream
        # progress = tqdm.tqdm(range(
        #     metadata['size']), f"SERVER: Receiving {metadata['filename']}", unit="B", unit_scale=True, unit_divisor=1024)
        # with open(metadata['filename'], "wb") as f:
        #     while True:
        #         # read 1024 bytes from the socket (receive)
        #         bytes_read = client_socket.recv(BUFFER_SIZE)
        #         if not bytes_read:
        #             # nothing is received
        #             # file transmitting is done
        #             break
        #         # write to the file the bytes we just received
        #         if metadata['encrypt']:
        #             bytes_read = decrypt_message(bytes_read)
        #
        #         f.write(bytes_read)
        #         # update the progress bar
        #         progress.update(len(bytes_read))

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
                        break
                except ConnectionResetError:
                    quit = True
                    break
                if new_msg:
                    # print("new msg len:", msg[:HEADERSIZE])
                    try:
                        msg_params = get_params(msg)
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
