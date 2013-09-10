# -*- coding: utf-8 -*-
import pymon
import os
import utils
import sender
from datetime import datetime


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


class Message(object):
    """
    The Message class
    """
    GREEN_COLOR = 'green'
    RED_COLOR = 'red'
    YELLOW_COLOR = 'yellow'
    WHITE_COLOR = 'white'

    def __init__(self, text="", msgType="status", duration="", machine=None, column=None, color=GREEN_COLOR):
        """
        Constructor.

        :param text: str
        :param msgType: str
        :param duration: str
        :param machine: str
        :param column: str
        :param color: str
        """
        self.text = text
        self.msgType = msgType
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
        """
        Return the message string to send to xymon.
        """
        date = datetime.now().strftime('%c')
        return '%s%s %s.%s %s %s\n%s\n' % (self.msgType, self.duration, self.machine, self.column, self.color,
                                           date, self.text)

    def __repr__(self):
        return "Message %s.%s %s" % (self.machine, self.column, self.color)

    def validate(self):
        """
        Check if all the content is set.
        """
        assert self.machine
        assert self.column
        assert self.color


class ClientMissingInfoError(BaseException):
    def __init__(self, missingInfo):
        super(ClientMissingInfoError, self).__init__()
        self.message = u"Missing %s information" % missingInfo