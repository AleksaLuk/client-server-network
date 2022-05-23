import logging
import unittest
from unittest import mock
import os
from client_server_network.server import Server

logging.disable(logging.CRITICAL)


class TestServer(unittest.TestCase):
    server = Server("", 5432)

    def tearDown(self):
        """
        Removes side effect log file
        """

        try:
            os.remove("server_history.log")
        except FileNotFoundError:
            pass

    def test_recvall(self):
        pass

    @mock.patch("client_server_network.server.pickle.loads")
    @mock.patch("client_server_network.server.json.loads")
    @mock.patch("client_server_network.server.decrypt_message")
    def test_receive_object(self, mock_decrypt, mock_json, mock_pickle):
        """
        Tests object receiving logic
        """

        mock_decrypt.return_value = "decrypted message"
        mock_json.return_value = "de-jsoned message"
        mock_pickle.return_value = "de-pickled message"
        metadata = {}
        metadata["encrypt"] = True
        metadata["serialisation"] = "Json"

        ret = self.server.receive_object("", metadata)
        mock_json.assert_called_with(mock_decrypt.return_value)
        self.assertEqual(mock_json.return_value, ret)

        metadata["encrypt"] = False
        metadata["serialisation"] = "Binary"

        ret = self.server.receive_object("", metadata)
        mock_pickle.assert_called_with("")
        self.assertEqual(mock_pickle.return_value, ret)

    @mock.patch("client_server_network.server.open")
    @mock.patch("client_server_network.server.decrypt_message")
    def test_receive_file(self, mock_decrypt, mock_open):
        """
        Tests file receiving logic
        """

        mock_decrypt.return_value = "decrypted message"
        metadata = {"filename": "name.txt"}
        metadata["encrypt"] = True
        input_data = "path"

        self.server.receive_file(input_data, metadata)
        mock_decrypt.assert_called_with(input_data)
        mock_open.assert_called_with(metadata["filename"], "wb")
        mock_open.return_value.__enter__.return_value.write.assert_called_with(
            mock_decrypt.return_value
        )
        metadata["encrypt"] = False

        self.server.receive_file(input_data, metadata)
        mock_open.return_value.__enter__.return_value.write.assert_called_with(
            input_data
        )

    def test_receive_message(self):
        pass
