# -*- coding: utf-8 -*-
import os
import utils
import sender
import pymon
from message import Message
from pymonExceptions import ClientMissingInfoError


class Client(object):
    """
    Abstraction of a xymon client.
    """

    def __init__(self, column, log=True, tmp=True, logMode="a", tmpMode="w", useXymon=True):
        """
        Constructor of the Xymon Client.
        :param column: str
        :param log: bool
        :param tmp: bool
        :param logMode: str
        :param tmpMode: str
        :param useXymon: bool
        """
        self.__analyzeEnvironment(useXymon)
        self.msg = Message(column=column)
        if log:
            self.logFilePath = os.path.join(self.clientLogsPath, self.msg.column + ".log")
            self.logFile = open(self.logFilePath, logMode)
        else:
            self.logFile = None
        if tmp:
            self.tmpFilePath = os.path.join(self.tmpPath, self.msg.column + ".tmp")
            self.tmpFile = open(self.tmpFilePath, tmpMode)
        else:
            self.tmpFile = None

    def __repr__(self):
        return u'Pymon [%s](%s)' % (self.servers, self.sender)

    def __loadServers(self):
        """
        Read and create the Xymon server(s) from the environment varibales.
        """
        self.servers = []
        xymonPort = utils.getVariableContent('XYMONDPORT')
        if not xymonPort:
            xymonPort = 1984
        primaryServer = utils.getVariableContent('XYMSRV')
        if primaryServer and primaryServer != '0.0.0.0':
            self.servers.append(pymon.Server(address=primaryServer, port=xymonPort))  # Use one primary server
        else:
            multipleServers = utils.getVariableContent('XYMSERVERS')
            if multipleServers:
                for i in filter(None, multipleServers.split(' ')):
                    if i != '0.0.0.0':
                        self.servers.append(pymon.Server(address=i, port=xymonPort))
        if not self.servers:
            raise ClientMissingInfoError('XYMSERVER(S)')

    def __analyzeEnvironment(self, useXymon):
        """
        Look for Xymon Environment variables to know if it's running in a xymon environment or stand alone.
        If it's running in a xymon environment, gets the information from the variables.
        Then creates the sender (xymon or native)
        :param useXymon: bool
        """
        self.__loadServers()
        if useXymon:
            xymonBinary = utils.getVariableContent('XYMON')
            if not xymonBinary:
                raise ClientMissingInfoError("XYMON")
            else:
                self.sender = sender.XymonSender(xymonBinary)
        else:
            self.sender = sender.PymonSender()
        tmpPath = utils.getVariableContent('XYMONTMP')
        if not tmpPath:
            raise ClientMissingInfoError('XYMONTMP')
        else:
            self.tmpPath = tmpPath
        clientLogsPath = utils.getVariableContent('XYMONCLIENTLOGS')
        if not clientLogsPath:
            raise ClientMissingInfoError('XYMONCLIENTLOGS')
        else:
            self.clientLogsPath = clientLogsPath
        osType = utils.getVariableContent('SERVEROSTYPE')
        if not osType:
            self.osType = None
        else:
            self.osType = osType
        self.xymonClientHome = utils.getVariableContent('XYMONCLIENTHOME')

    def send(self):
        """
        Send the current message to all the servers.
        """
        self.msg.validate()
        if self.logFile:
            self.logFile.close()
        if self.tmpFile:
            self.tmpFile.close()
        self.sender.send(self)
