# -*- coding: utf-8 -*-
from utils import ip_address_is_valid, hostname_is_valid
from pymonExceptions import InvalidAddressError, InvalidPortError


class Server(object):
    """
    Xymon server Class.
    """
    def __init__(self, address=None, port=1984):
        """
        Constructor.
        :param address: str
        :param port: int
        """
        if address:
            self.address = address
        self.port = port

    def __repr__(self):
        return u"Server: %s(%s)" % (self.address, self.port)

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        """
        Sets Server IP or Hostname.
        :param address: str
        """
        self._address = self._validate_address(address)

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        try:
            self._port = int(port)
        except ValueError:
            raise InvalidPortError(port)

    def _validate_address(self, address):
        """
        Validate the address given, the address could be an IP (X.X.X.X) or a hostname (foo.com).
        :param address: str
        """
        if ip_address_is_valid(address) or hostname_is_valid(address):
            return address.lower()
        else:
            raise InvalidAddressError(address)

    def get_URL(self):
        """
        Return the url (host:port) of the server.
        :rtype : str
        """
        if not self.address or not self.port:
            raise InvalidAddressError(None)
        else:
            return "%s:%s" % (self.address, self.port)