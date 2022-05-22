import logging
import unittest
from unittest import mock
import os
from client_server_network.server import Server

logging.disable(logging.CRITICAL)


class TestServer(unittest.TestCase):
    server = Server("", 5432)

    def tearDown(self):
        try:
            os.remove("server_history.log")
        except FileNotFoundError:
            pass

    def test_recvall(self):
        pass

    @mock.patch("client_server_network.client.pickle.loads")
    @mock.patch("client_server_network.client.jsons.loads")
    @mock.patch("client_server_network.client.decrypt_message")
    def test_receive_object(self, mock_decrypt, mock_json, mock_pickle):
        mock_decrypt.return_value = "decrypted message"
        mock_json.return_value = "de-jsoned message"
        mock_pickle.return_value = "de-pickled message"



    def test_receive_file(self):
        pass

    def test_receive_message(self):
        pass

