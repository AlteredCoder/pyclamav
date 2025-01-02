import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import datetime
import argparse
from typing import List
from pydantic import BaseModel, Field, model_validator
from lib.config import parse_arg, Config, load_config
import logging
from pathlib import Path
from lib import pyclamd
from lib.scan import Scan
import multiprocessing

class TestPyclamav(unittest.TestCase):

    @patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(config='test_config.json', modified_since='24h', verbose=False, process=5))
    def test_parse_arg(self, mock_args):
        args = parse_arg()
        self.assertEqual(args.config, 'test_config.json')
        self.assertEqual(args.modified_since, '24h')
        self.assertEqual(args.verbose, False)

    def test_config_model(self):
        config_data = {
            "folders": ["/path/to/folder1", "/path/to/folder2"],
            "log_folder": "/var/log/pyclamav",
            "modified_file_since": "24h",
            "verbose": False
        }
        config = Config(**config_data)
        self.assertEqual(config.folders, ["/path/to/folder1", "/path/to/folder2"])
        self.assertEqual(config.log_folder, "/var/log/pyclamav")
        self.assertEqual(config.modified_file_since, "24h")
        self.assertIsInstance(config.modified_file_datetime, datetime.datetime)
        self.assertEqual(config.verbose, False)

    @patch('builtins.open', new_callable=mock_open, read_data='{"folders": ["/path/to/folder1", "/path/to/folder2"], "log_folder": "/var/log/pyclamav/", "modified_file_since": "24h", "nb_process": 5, "verbose": false}')
    @patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(config='test_config.json', modified_since='24h', verbose=False, process=5))
    def test_load_config(self, mock_args, mock_file):
        config = load_config()
        self.assertEqual(config.folders, ["/path/to/folder1", "/path/to/folder2"])
        self.assertEqual(config.log_folder, "/var/log/pyclamav/")
        self.assertEqual(config.modified_file_since, "24h")
        self.assertIsInstance(config.modified_file_datetime, datetime.datetime)
        self.assertEqual(config.verbose, False)

    @patch('lib.pyclamd.ClamdUnixSocket')
    @patch('lib.pyclamd.ClamdNetworkSocket')
    def test_init(self, mock_network_socket, mock_unix_socket):
        mock_unix_socket.return_value.ping.return_value = None
        mock_network_socket.return_value.ping.return_value = None

        logger = logging.getLogger()
        scan = Scan(modified_since=datetime.datetime.now(), logger=logger)

        self.assertIsInstance(scan.logger, logging.Logger)
        self.assertIsInstance(scan.modified_since, datetime.datetime)

    @patch('lib.pyclamd.ClamdUnixSocket')
    @patch('lib.pyclamd.ClamdNetworkSocket')
    def test_init_connection_error(self, mock_network_socket, mock_unix_socket):
        mock_unix_socket.side_effect = pyclamd.ConnectionError
        mock_network_socket.side_effect = pyclamd.ConnectionError

        logger = logging.getLogger()
        with self.assertRaises(ValueError):
            Scan(modified_since=datetime.datetime.now(), logger=logger)

    @patch('lib.pyclamd.ClamdUnixSocket')
    @patch('lib.pyclamd.ClamdNetworkSocket')
    def test_scan_file(self, mock_network_socket, mock_unix_socket):
        mock_unix_socket.return_value.ping.return_value = None
        mock_network_socket.return_value.ping.return_value = None
        mock_unix_socket.return_value.scan_stream.return_value = {
            "stream" : ("FOUND", "EICAR")
        }

        logger = logging.getLogger()
        scan = Scan(modified_since=None, logger=logger)

        file = Path('./tests/data/EICAR')
        self.assertTrue(scan.scan_file(file))

    @patch('lib.pyclamd.ClamdUnixSocket')
    @patch('lib.pyclamd.ClamdNetworkSocket')
    @patch("pathlib.Path.stat")
    def test_scan_file_too_old(self, mock_network_socket, mock_unix_socket, mock_stat):
        mock_unix_socket.return_value.ping.return_value = None
        mock_network_socket.return_value.ping.return_value = None

        fake_stat = MagicMock()
        file_modification_dt = datetime.datetime.now() - datetime.timedelta(days=1)
        fake_stat.mt_time = file_modification_dt.timestamp()

        logger = logging.getLogger()
        scan = Scan(modified_since=datetime.datetime.now() - datetime.timedelta(days=2), logger=logger)

        file = Path('./tests/data/EICAR')
        self.assertFalse(scan.scan_file(file))

    @patch('lib.pyclamd.ClamdUnixSocket')
    @patch('lib.pyclamd.ClamdNetworkSocket')
    def test_scan_folder(self, mock_network_socket, mock_unix_socket):
        mock_unix_socket.return_value.ping.return_value = None
        mock_network_socket.return_value.ping.return_value = None
        mock_unix_socket.return_value.scan_stream.return_value = {
            "stream" : ("FOUND", "EICAR")
        }

        logger = logging.getLogger()
        scan = Scan(modified_since=None, logger=logger)

        results = scan.scan_folder('./tests/data/')

        self.assertEqual(len(results), 1)

if __name__ == '__main__':
    unittest.main()
