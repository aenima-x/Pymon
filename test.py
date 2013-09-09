import unittest
import os
import pymon
from pymon import sender
from pymon.pymonExceptions import InvalidAddressError, InvalidPortError, InvalidPath
from pymon.client import ClientMissingInfoError


class MockSender(sender.Sender):
    def __init__(self, client):
        super(MockSender, self).__init__(client)

    def send(self):
        return self.client.machine


class PymonServerTests(unittest.TestCase):

    def test_server_ip_invalid(self):
        s = pymon.Server()
        with self.assertRaises(InvalidAddressError):
            s.address = '256.4.2.1'

    def test_server_hostname_invalid(self):
        s = pymon.server.Server()
        with self.assertRaises(InvalidAddressError):
            s.address = 'aaa.'

    def test_server_port_invalid(self):
        s = pymon.Server()
        with self.assertRaises(InvalidPortError):
            s.port = 'aaa'

    def test_server(self):
        self.assertIsInstance(pymon.Server(address="192.168.1.1", port=1984), pymon.server.Server)

    def test_server_url(self):
        s = pymon.Server(address="192.168.1.1", port=1984)
        self.assertEqual(s.getURL(), "192.168.1.1:1984")


class PymonClientTests(unittest.TestCase):

    def setUp(self):
        self.servers = pymon.Server(address="192.168.1.1", port=1984)

    def test_client_missing_info(self):
        with self.assertRaises(ClientMissingInfoError):
            c = pymon.Client()

    def test_native_client_invalid_binary(self):
        os.environ['XYMSRV'] = '192.168.1.1'
        os.environ['XYMSERVERS'] = '192.168.1.1 192.168.1.2'
        os.environ['XYMONDPORT'] = '1984'
        os.environ['XYMONCLIENTLOGS'] = '/var/log/xymon'
        os.environ['XYMONTMP'] = '/tmp/xymon'
        os.environ['XYMON'] = '/bin/xymon'
        os.environ['MACHINE'] = 'kenny'
        os.environ['SERVEROSTYPE'] = 'Darwin'
        os.environ['XYMONCLIENTHOME'] = '/home/xymon'
        with self.assertRaises(InvalidPath):
            client = pymon.Client()

    def test_native_client_ok(self):
        os.environ['XYMSRV'] = '192.168.1.1'
        os.environ['XYMSERVERS'] = '192.168.1.1 192.168.1.2'
        os.environ['XYMONDPORT'] = '1984'
        os.environ['XYMONCLIENTLOGS'] = '/var/log/xymon'
        os.environ['XYMONTMP'] = '/tmp/xymon'
        os.environ['XYMON'] = '/bin/ls'
        os.environ['MACHINE'] = 'kenny'
        os.environ['SERVEROSTYPE'] = 'Darwin'
        os.environ['XYMONCLIENTHOME'] = '/home/xymon'
        client = pymon.Client()
        self.assertIsInstance(client, pymon.Client)
        #client.sender = MockSender(client)
        #self.assertEqual(client.sender.send(), "kenny")


def main():
    unittest.main()

if __name__ == '__main__':
    main()