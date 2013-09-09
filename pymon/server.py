from pymon.utils import ipAddressIsValid, hostnameIsValid
from pymon.pymonExceptions import InvalidAddressError, InvalidPortError

class Server(object):
    """
    Xymon server Class
    """
    def __init__(self, address=None, port=1984):
        """
        Constructor.

        Keyword arguments:
        address -- Server IP address or Hostname (default None)
        port -- Server port number (default 1984)
        """
        if address:
            self.address = address
        self.__port = port

    def __repr__(self):
        return u"Server: %s(%s)" % (self.address, self.port)

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, address):
        """
        Sets Server IP or Hostname.
        Arguments:
        address -- IP or Hostname
        """
        self.__address = self.__validateAddress(address)

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, port):
        try:
            self.__port = int(port)
        except ValueError:
            raise InvalidPortError(port)

    def __validateAddress(self, address):
        """
        Validate the address given, the address could be an IP (X.X.X.X) or a hostname (foo.com)
        """
        if ipAddressIsValid(address) or hostnameIsValid(address):
            return address.lower()
        else:
            raise InvalidAddressError(address)

    def getURL(self):
        if not self.address or not self.port:
            raise InvalidAddressError
        else:
            return "%s:%s" % (self.address, self.port)