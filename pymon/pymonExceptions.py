# -*- coding: utf-8 -*-


class InvalidAddressError(BaseException):
    def __init__(self, address):
        super(InvalidAddressError, self).__init__()
        self.message = "The address %s is invalid!!" % address


class InvalidPortError(BaseException):
    def __init__(self, port):
        super(InvalidPortError, self).__init__()
        self.message = "The port %s is invalid!!" % port


class InvalidPath(BaseException):
    def __init__(self, path):
        super(InvalidPath, self).__init__()
        self.message = "The path %s is invalid!!" % path


class ClientMissingInfoError(BaseException):
    def __init__(self, missingInfo):
        super(ClientMissingInfoError, self).__init__()
        self.message = u"Missing %s information" % missingInfo