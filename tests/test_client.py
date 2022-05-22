import logging
import unittest
import os
from unittest import mock
from client_server_network.client import Client

logging.disable(logging.CRITICAL)


class TestClient(unittest.TestCase):
    client = Client("", 5432)

    def tearDown(self):
        try:
            os.remove("client_history.log")
        except FileNotFoundError:
            pass

    @mock.patch("client_server_network.client.Client.receive_message")
    @mock.patch("client_server_network.client.Client.sendall")
    @mock.patch("client_server_network.client.create_headers")
    @mock.patch("client_server_network.client.encrypt_message")
    @mock.patch("client_server_network.client.serialise_object")
    def test_transfer_object(self, serialise_object, encrypt_message, create_headers, sendall, receive_message):
        serialise_object.return_value = b"[1,2,3,4,5]"
        encrypt_message.return_value = b"encrypted message"
        create_headers.return_value = "metadata  "
        input_obj = [1, 2, 3, 4, 5]
        ser_method = "json"
        encrypt = True
        send_type = "object"

        self.client.transfer_object(ser_method, input_obj, encrypt=encrypt)
        serialise_object.assert_called_with(input_obj, ser_method)
        encrypt_message.assert_called_with(serialise_object.return_value)
        create_headers.assert_called_with(10, send_type, encrypt, ser_method, len(encrypt_message.return_value))
        sendall.assert_called_with(bytes(create_headers.return_value, "utf-8") + encrypt_message.return_value)
        receive_message.assert_called_once()

        encrypt = False
        self.client.transfer_object(ser_method, input_obj, encrypt=encrypt)
        serialise_object.assert_called_with(input_obj, ser_method)

        encrypt_message.assert_called_once()
        create_headers.assert_called_with(10, send_type, encrypt, ser_method, len(serialise_object.return_value))
        sendall.assert_called_with(bytes(create_headers.return_value, "utf-8") + serialise_object.return_value)
        self.assertEqual(receive_message.call_count, 2)

    @mock.patch("client_server_network.client.Client.receive_message")
    @mock.patch("client_server_network.client.Client.sendall")
    @mock.patch("client_server_network.client.create_headers")
    @mock.patch("client_server_network.client.encrypt_message")
    @mock.patch("client_server_network.client.os.path.getsize")
    @mock.patch("client_server_network.client.os.path.basename")
    @mock.patch("client_server_network.client.open")
    @mock.patch("client_server_network.client.bytes")
    def test_transfer_file(self, mock_bytes, mock_open, basename, getsize, encrypt_message, create_headers, sendall, receive_message):
        encrypt = True
        send_type = "file"
        getsize.return_value = 100
        basename.return_value = "file.txt"
        create_headers.return_value = "metadata  "
        file_reads = [b"y", b"abc", b"123", b""]
        mock_open.return_value.__enter__.return_value.read.side_effect = file_reads
        mock_bytes.return_value = b"x"
        encrypt_message.return_value = b"encrypted text"

        self.client.transfer_file("file.txt", encrypt=encrypt)

        mock_open.assert_called_with(basename.return_value, "rb")

        create_headers.assert_called_with(10, send_type, encrypt, basename.return_value, getsize.return_value)
        encrypt_message.assert_called_once_with(b"".join(file_reads))
        sendall.assert_called_once_with(mock_bytes.return_value + encrypt_message.return_value)
        receive_message.assert_called_once()

        encrypt = False
        mock_open.return_value.__enter__.return_value.read.side_effect = file_reads
        self.client.transfer_file("file.txt", encrypt=encrypt)
        sendall.assert_called_with(mock_bytes.return_value + b"".join(file_reads))

    @mock.patch("client_server_network.client.Client.connect")
    def test__connect(self, mock_connect):
        self.client._connect()
        mock_connect.assert_called_once_with((self.client.host, self.client.port))

    def test_receive_message(self):
        pass