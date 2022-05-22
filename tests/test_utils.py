import logging
import unittest
import json
import pickle
from ddt import ddt, data
from client_server_network.utils import encrypt_message, decrypt_message, serialise_object, create_headers
from client_server_network.sample_files.sample_data import DATA
logging.disable(logging.CRITICAL)


@ddt
class TestUtils(unittest.TestCase):

    @data(b"test1", b"ABCDEFGHIJKLMN", b"1234567890", b"{1:2, 3:4}",
          b'\x80\x05\x95\r\x00\x00\x00\x00\x00\x00\x00]\x94(K\x01K\x02K\x03K\x04e.',
          *[str.encode(json.dumps(obj)) for obj in DATA],
          *[pickle.dumps(obj) for obj in DATA])
    def test_encryption(self, string):
        encrpted = encrypt_message(string)
        self.assertNotEqual(encrpted, string)

        decryped = decrypt_message(encrpted)
        self.assertEqual(string, decryped)

    @data(*DATA)
    def test_serialisation(self, obj):
        serialised = serialise_object(obj, "binary")
        self.assertIsInstance(serialised, bytes)
        self.assertNotEqual(serialised, obj)

        deserialised = pickle.loads(serialised)
        self.assertEqual(obj, deserialised)

        serialised = serialise_object(obj, "json")
        self.assertIsInstance(serialised, bytes)
        self.assertNotEqual(serialised, obj)

        deserialised = json.loads(serialised)
        self.assertEqual(obj, deserialised)

        self.assertNotEqual(serialise_object(obj, "json"), serialise_object(obj, "binary"))

    def test_create_headers(self):
        header_size = 10
        send_type, encrypt, serialisation_method, obj_length = "file", True, "binary", 23

        message = f"{send_type:<{header_size}}"
        message += f"{encrypt:<{header_size}}"
        message += f"{serialisation_method:<{header_size}}"
        message += f"{obj_length:<{header_size}}"

        self.assertEqual(message, create_headers(header_size, send_type, encrypt, serialisation_method, obj_length))

        message = f"{send_type}      1         {serialisation_method}    {obj_length}        "
        self.assertEqual(message, create_headers(header_size, send_type, encrypt, serialisation_method, obj_length))
