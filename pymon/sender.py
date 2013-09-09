# -*- coding: utf-8 -*-
import os
import socket
import utils
from pymonExceptions import InvalidPath


class Sender(object):
    def __init__(self):
        super(Sender, self).__init__()

    def send(self, client, server):
        raise NotImplementedError


class PymonSender(Sender):
    def __init__(self):
        super(PymonSender, self).__init__()
        pass

    def __repr__(self, client, server):
        return u"PymonSender"

    def send(self, client):
        for server in client.servers:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.send(client.msg.getMessageString())
            s.close()


class NativeSender(Sender):
    def __init__(self, binary=None):
        super(NativeSender, self).__init__()
        if not binary:
            self.binary = utils.getVariableContent('XYMON')
        else:
            self.binary = binary
        if not os.path.isfile(self.binary):
            raise InvalidPath(self.binary)

    def __repr__(self):
        return u"NativeSender (%s)" % self.binary

    def send(self, client):
        for server in client.servers:
            commandDict = {'binary': self.binary, 'server': server.getURL(), 'fullMessage': client.msg.getMessageString()}
            command = '%(binary)s %(server)s "%(fullMessage)s"' % commandDict
            os.system(command)

