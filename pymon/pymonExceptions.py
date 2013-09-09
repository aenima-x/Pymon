# -*- coding: utf-8 -*-


class InvalidAddressError(BaseException):
    def __init__(self, address):
        self.message = "The address %s is invalid!!" % address


class InvalidPortError(BaseException):
    def __init__(self, port):
        self.message = "The port %s is invalid!!" % port


class InvalidPath(BaseException):
    def __init__(self, path):
        self.message = "The path %s is invalid!!" % path
