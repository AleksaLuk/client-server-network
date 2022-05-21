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

