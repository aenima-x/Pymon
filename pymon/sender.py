# -*- coding: utf-8 -*-
import os
import socket
import utils
from pymonExceptions import InvalidPath


class Sender(object):
    """
    Sender Base class.
    """
    def __init__(self):
        super(Sender, self).__init__()

    def send(self, client, debug=False):
        raise NotImplementedError


class PymonSender(Sender):
    """
    The native pymon sender.
    """
    def __init__(self):
        super(PymonSender, self).__init__()
        pass

    def __repr__(self):
        return u"PymonSender"

    def send(self, client, debug=False):
        for server in client.servers:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((server.address, server.port))
            s.send(client.msg.getMessageString())
            s.close()


class XymonSender(Sender):
    """
    Xymon sender. This will use the xymon binary.
    """
    def __init__(self, binary=None):
        """
        Constructor.
        :param binary: str
        """
        super(XymonSender, self).__init__()
        if not binary:
            self.binary = utils.getVariableContent('XYMON')
        else:
            self.binary = binary
        if not os.path.isfile(self.binary):
            raise InvalidPath(self.binary)

    def __repr__(self):
        return u"XymonSender (%s)" % self.binary

    def send(self, client, debug=False):
        """
        Executes the xymon binary to send the message to all tge servers in the client.
        :param client: Client
        """
        for server in client.servers:
            commandDict = {'binary': self.binary, 'server': server.getURL(), 'fullMessage': client.msg.getMessageString()}
            command = '%(binary)s %(server)s "%(fullMessage)s"' % commandDict
            if debug:
                print(command)
            os.system(command)

