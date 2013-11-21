# -*- coding: utf-8 -*-


class InvalidPath(Exception):
    def __init__(self, path):
        super(InvalidPath, self).__init__()
        self.message = "The path %s is invalid!!" % path


class ClientMissingInfoError(Exception):
    def __init__(self, missingInfo):
        super(ClientMissingInfoError, self).__init__()
        self.message = u"Missing %s information" % missingInfo