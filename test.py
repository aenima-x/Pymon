import unittest
import os
import pymon
from pymon import sender
from pymon.pymonExceptions import ClientMissingInfoError


class MockSender(sender.Sender):
    def __init__(self):
        super(MockSender, self).__init__()

    def send(self, client, debug=False):
        return client.machine


class PymonServerTests(unittest.TestCase):

    def test_server_ip_invalid(self):
        s = pymon.Server()
        with self.assertRaises(ValueError):
            s.address = '256.4.2.1'

    def test_server_hostname_invalid(self):
        s = pymon.Server()
        with self.assertRaises(ValueError):
            s.address = 'aaa.'

    def test_server_port_invalid(self):
        s = pymon.Server()
        with self.assertRaises(ValueError):
            s.port = 'aaa'

    def test_server(self):
        self.assertIsInstance(pymon.Server(address="192.168.1.1", port=1984), pymon.Server)

    def test_server_url(self):
        s = pymon.Server(address="192.168.1.1", port=1984)
        self.assertEqual(s.get_URL(), "192.168.1.1:1984")


class PymonClientTests(unittest.TestCase):

    def setUp(self):
        self.servers = pymon.Server(address="192.168.1.1", port=1984)

    def test_client_missing_info(self):
        with self.assertRaises(ClientMissingInfoError):
            c = pymon.Client("column")

    def test_native_client_ok(self):
        os.environ['XYMSRV'] = '192.168.1.1'
        os.environ['XYMSERVERS'] = '192.168.1.1 192.168.1.2'
        os.environ['XYMONDPORT'] = '1984'
        os.environ['XYMONCLIENTLOGS'] = '/tmp/'
        os.environ['XYMONTMP'] = '/tmp/'
        os.environ['XYMON'] = '/bin/ls'
        os.environ['MACHINE'] = 'kenny'
        os.environ['SERVEROSTYPE'] = 'Darwin'
        os.environ['XYMONCLIENTHOME'] = '/home/xymon'
        client = pymon.Client("column")
        self.assertIsInstance(client, pymon.Client)
        #client.sender = MockSender(client)
        #self.assertEqual(client.sender.send(), "kenny")

    def test_native_client_one_server(self):
        os.environ['XYMSRV'] = '127.0.0.1'
        os.environ['XYMSERVERS'] = ''
        os.environ['XYMONDPORT'] = '1984'
        os.environ['XYMONCLIENTLOGS'] = '/tmp/'
        os.environ['XYMONTMP'] = '/tmp/'
        os.environ['XYMON'] = '/bin/ls'
        os.environ['MACHINE'] = 'kenny'
        os.environ['SERVEROSTYPE'] = 'Darwin'
        os.environ['XYMONCLIENTHOME'] = '/home/xymon'
        client = pymon.Client("column")
        self.assertIsInstance(client, pymon.Client)

    def test_native_client_two_servers(self):
        os.environ['XYMSRV'] = '0.0.0.0'
        os.environ['XYMSERVERS'] = '192.168.1.1 192.168.1.2'
        os.environ['XYMONDPORT'] = '1984'
        os.environ['XYMONCLIENTLOGS'] = '/tmp/'
        os.environ['XYMONTMP'] = '/tmp/'
        os.environ['XYMON'] = '/bin/ls'
        os.environ['MACHINE'] = 'kenny'
        os.environ['SERVEROSTYPE'] = 'Darwin'
        os.environ['XYMONCLIENTHOME'] = '/home/xymon'
        client = pymon.Client("column")
        self.assertIsInstance(client, pymon.Client)

    def test_native_client_one_server_hobbit(self):
        os.environ['BB'] = '127.0.0.1'
        os.environ['BBDISPLAYS'] = ''
        os.environ['BBPORT'] = '1984'
        os.environ['BBCLIENTLOGS'] = '/tmp/'
        os.environ['BBTMP'] = '/tmp/'
        os.environ['BB'] = '/bin/ls'
        os.environ['MACHINE'] = 'kenny'
        os.environ['SERVEROSTYPE'] = 'Darwin'
        os.environ['HOBBITCLIENTHOME'] = '/home/xymon'
        client = pymon.Client("column")
        self.assertIsInstance(client, pymon.Client)

def main():
    unittest.main()

if __name__ == '__main__':
    main()