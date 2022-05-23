"""
Utility functions that support the operation of the core module.
"""

import hashlib
import logging
import pickle
import json
from Crypto.Cipher import AES


KEY = hashlib.sha256("This is a key123".encode()).digest()
IV = "This is an IV456"


def encrypt_message(message: bytes):
    """
    Encrypts message

    :param message: input string to be encrypted
    :return: encrypted message
    """
    obj = AES.new(KEY, AES.MODE_CFB, IV.encode())
    ciphertext = obj.encrypt(message)
    return ciphertext


def decrypt_message(ciphertext: bytes) -> bytes:
    """
    Decryptes message

    :param ciphertext: encrypted message
    :return: decrypted message
    """

    obj2 = AES.new(KEY, AES.MODE_CFB, IV.encode())
    message = obj2.decrypt(ciphertext)
    return message


def serialise_object(obj: any, serialisation_method: str) -> bytes:
    """
    Serialises python object

    :param obj: e.g. list, dict, class
    :param serialisation_method: json or binary
    :return: serialised data
    """

    if serialisation_method.lower() == "json":
        # Text serialisation
        logging.info("Converting object to json format")
        data = str.encode(json.dumps(obj))
    elif serialisation_method.lower() == "binary":
        # Binary serialisation
        logging.info("Converting object to binary format")
        data = pickle.dumps(obj, -1)
    else:
        logging.error("Incorrect method. Please provide one of json or binary.")
        data = None
    return data


def create_headers(block_size: int, *args):
    """
    Creates metadata block headers for server to understand incoming data

    :param block_size: size of block enclosing parameter (e.g. 10 -> "binary    "
    :param args: metadata variables (size, encryption, serialisation method etc)
    :return: headers
    """

    headers = "".join([f"{arg:<{block_size}}" for arg in args])
    return headers


def get_params(msg: bytes, headersize: int) -> dict:
    """
    Parses metadata from block headers

    :param msg: string containing blocks
    :param headersize: size of blocks
    :return: metadata
    """

    data_type = msg[:headersize]
    encrypt = msg[headersize: 2 * headersize]
    param3 = msg[2 * headersize: 3 * headersize]
    length = msg[3 * headersize: 4 * headersize]

    metadata = {
        "type": data_type.strip().decode(),
        "encrypt": bool(int(encrypt)),
        "length": int(length),
    }

    if metadata["type"] == "object":
        metadata["serialisation"] = param3.strip().decode()
    elif metadata["type"] == "file":
        metadata["filename"] = param3.strip().decode()

    return metadata
