"""
Client
"""

from socket import socket
import json
import pickle
from client_server_network.sample_files.sample_data import CAR_DATA
import logging
import tqdm
import os

# Library to report events
logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)


def transfer_object(host, port, serialisation_method, obj):
    """
    Sends a python object to a server.

    :param host: The ip address or hostname of the server - the receiver.
    :param port: Port of the server
    :param serialisation_method: Method used to serialise data (xml, json, binary).
    :param obj: python object to be sent e.g. dictionary.
    :return:
    """

    # create the client socket
    soc = socket()
    logging.info(f"Connecting to HOST: {host} & PORT: {port}")

    soc.connect((host, port))
    logging.info(f"Connected")

    serialised_object = serialise_object(obj, serialisation_method)

    # send object:
    soc.sendall(serialised_object)
    logging.info(f"Serialised object sent to server")

    # close the socket
    soc.close()


def transfer_file(host, port, file_name):
    """
    Sends a file to a server.

    :param host: The ip address or hostname of the server - the receiver.
    :param port: Port of the server
    :param file_name: File to be sent.
    :return:
    """

    separator = "<SEPARATOR>"
    buffer_size = 4096  # send 4096 bytes each time step

    # get the file size
    filesize = os.path.getsize(file_name)

    # create the client socket
    s = socket()

    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")

    # send the file_name and filesize
    s.send(f"{file_name}{separator}{filesize}".encode())

    # start sending the file
    progress = tqdm.tqdm(range(filesize), f"Sending {file_name}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(file_name, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(buffer_size)
            if not bytes_read:
                # file transmitting is done
                break
            # use sendall to assure transmission in
            # busy networks
            s.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))
    s.close()


def serialise_object(obj,serialisation_method):
    # serialisation types
    if serialisation_method == "json":
        # Json serialisation
        logging.info(f"Converting object to json format")
        data = str.encode(json.dumps(obj))
    elif serialisation_method == "binary":
        # Binary serialisation
        logging.info(f"Converting object to binary format")
        data = pickle.dumps(obj, -1)
    else:
        logging.error(f"Incorrect method. Please provide one of json or binary.")
        return
    return data


# transfer_object("0.0.0.0",5002,"json", CAR_DATA)
# transfer_file("0.0.0.0", 5006,
#                "/Users/alex/PycharmProjects/client_server_network/client_server_network/sample_files/file1.txt")