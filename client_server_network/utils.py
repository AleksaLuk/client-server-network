"""
Utility functions that support the operation of the core module.
"""

import hashlib
from Crypto.Cipher import AES
import pickle
import json
import logging
# import pyxser as pyx - explain that difficulty getting library (add to report)


key = hashlib.sha256('This is a key123'.encode()).digest()
iv = 'This is an IV456'


def encrypt_message(message):
    obj = AES.new(key, AES.MODE_CFB, iv.encode())
    ciphertext = obj.encrypt(message)
    return ciphertext


def decrypt_message(ciphertext):
    obj2 = AES.new(key, AES.MODE_CFB, iv.encode())
    message = obj2.decrypt(ciphertext)
    return message


def serialise_object(obj, serialisation_method):
    # serialisation types
    if serialisation_method.lower() == "json":
        # Json serialisation
        logging.info(f"Converting object to json format")
        data = str.encode(json.dumps(obj))
    elif serialisation_method.lower() == "binary":
        # Binary serialisation
        logging.info(f"Converting object to binary format")
        data = pickle.dumps(obj, -1)
    else:
        logging.error("Incorrect method. Please provide one of json or binary.")
        return
    return data


def create_headers(block_size, *args):
    headers = "".join([f"{arg:<{block_size}}" for arg in args])
    return headers


def get_params(msg, HEADERSIZE):
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