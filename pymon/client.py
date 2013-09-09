# -*- coding: utf-8 -*-
import pymon
import os
from pymon import utils
from pymon import sender
from datetime import datetime


class Client(object):
    """
    Abstraction of a xymon client.
    """

    def __init__(self, column, log=True, tmp=True, native=True):
        """
        Constructor of the Xymon Client.
        """
        self.__analyzeEnvironment(native)
        self.msg = Message(column=column)
        if log:
            self.logFilePath = os.path.join(self.clientLogsPath, self.msg.column, ".log")
            self.logFile = open(self.logFilePath)
        else:
            self.logFile = None
        if tmp:
            self.tmpFilePath = os.path.join(self.tmpPath, self.msg.column, ".tmp")
            self.tmpFile = open(self.tmpFilePath, "w")
        else:
            self.tmpFile = None

    def __repr__(self):
        return u'Pymon [%s](%s)' % (self.servers, self.sender)

    def __loadServers(self):
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

    def __analyzeEnvironment(self, native):
        """
        Look for Xymon Environment variables to know if it's running in a xymon environment or stand alone.
        If it's running in a xymon environment, gets the information from the variables.
        Then creates the sender (native or pymon own sender)
        """
        self.__loadServers()
        if native:
            xymonBinary = utils.getVariableContent('XYMON')
            if not xymonBinary:
                raise ClientMissingInfoError("XYMON")
            else:
                self.sender = sender.NativeSender(xymonBinary)
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
        self.msg.validate()
        if self.logFile:
            self.logFile.close()
        if self.tmpFile:
            self.tmpFile.close()
        self.sender.send(self)


class Message(object):
    GREEN_COLOR = 'green'
    RED_COLOR = 'red'
    YELLOW_COLOR = 'yellow'
    WHITE_COLOR = 'white'

    def __init__(self, text="", type="status", duration="", machine=None, column=None, color=GREEN_COLOR):
        self.text = text
        self.type = type
        self.duration = duration
        self.column = column
        self.color = color
        self.__get_machine(machine)

    def __get_machine(self, machine):
        if not machine:
            env_machine = utils.getVariableContent('MACHINE')
            if not env_machine:
                raise ClientMissingInfoError("MACHINE")
            else:
                self.machine = env_machine
        else:
            self.machine = machine

    def getMessageString(self):
        date = datetime.now().strftime('%c')
        return '%s%s %s.%s %s %s\n%s\n' % (self.type, self.duration, self.machine, self.column, self.color,
                                           date, self.text)

    def __repr__(self):
        return "Message %s.%s %s" % (self.machine, self.column, self.color)

    def validate(self):
        assert self.machine
        assert self.column
        assert self.color


class ClientMissingInfoError(BaseException):
    def __init__(self, missingInfo):
        self.message = u"Missing %s information" % missingInfo