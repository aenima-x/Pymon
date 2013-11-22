# -*- coding: utf-8 -*-
import os
import pymon
import utils
import sender
from message import Message
from pymonExceptions import ClientMissingInfoError


class Client(object):
    """
    Abstraction of a xymon client.
    """

    def __init__(self, column, log=False, log_write_mode="a", use_xymon=True, debug=False):
        """
        Constructor of the Xymon Client.
        :param column: str
        :param log: bool
        :param log_write_mode: str
        :param use_xymon: bool
        :param debug: bool
        """
        self.sender = None
        self._analyze_environment(use_xymon)
        self.msg = Message(column=column)
        self.debug = debug
        if log:
            self.log_file_path = os.path.join(self.client_logs_path, self.msg.column + ".log")
            self.log_file = open(self.log_file_path, log_write_mode)
        else:
            self.log_file = None

    def __repr__(self):
        return u'Pymon [%s](%s)' % (self.servers, self.sender)

    def _load_servers(self):
        """
        Read and create the Xymon server(s) from the environment varibales.
        """
        self.servers = []
        xymon_port = utils.get_variable_content(['XYMONDPORT', 'BBPORT'])
        if not xymon_port:
            xymon_port = 1984
        primary_server = utils.get_variable_content(['XYMSRV', 'BBDISP'])
        if primary_server and primary_server != '0.0.0.0':
            self.servers.append(pymon.Server(address=primary_server, port=xymon_port))  # Use one primary server
        else:
            multiple_servers = utils.get_variable_content(['XYMSERVERS','BBDISPLAYS'])
            if multiple_servers:
                for i in filter(None, multiple_servers.split(' ')):
                    if i != '0.0.0.0':
                        self.servers.append(pymon.Server(address=i, port=xymon_port))
        if not self.servers:
            raise ClientMissingInfoError('XYMSERVER(S)')

    def _analyze_environment(self, useXymon):
        """
        Look for Xymon Environment variables to know if it's running in a xymon environment or stand alone.
        If it's running in a xymon environment, gets the information from the variables.
        Then creates the sender (xymon or native)
        :param useXymon: bool
        """
        self._load_servers()
        if useXymon:
            xymon_binary = utils.get_variable_content(['XYMON', 'BB'])
            if not xymon_binary:
                raise ClientMissingInfoError("XYMON")
            else:
                self.sender = sender.XymonSender(xymon_binary)
        else:
            self.sender = sender.PymonSender()
        tmp_path = utils.get_variable_content(['XYMONTMP', 'BBTMP'])
        if not tmp_path:
            raise ClientMissingInfoError('XYMONTMP')
        else:
            self.tmp_path = tmp_path
        client_logs_path = utils.get_variable_content(['XYMONCLIENTLOGS', 'BBCLIENTLOGS'])
        if not client_logs_path:
            raise ClientMissingInfoError('XYMONCLIENTLOGS')
        else:
            self.client_logs_path = client_logs_path
        os_type = utils.get_variable_content('SERVEROSTYPE')
        if not os_type:
            self.os_type = None
        else:
            self.os_type = os_type
        self.xymon_client_home = utils.get_variable_content(['XYMONCLIENTHOME', 'HOBBITCLIENTHOME'])

    def get_temp_file(self, filename, mode="w"):
        """
        If you have set a path for temporary files, it will create one.
        :param filename: str
        :param mode: str
        """
        if self.tmp_path:
            return open(os.path.join(self.tmp_path, filename), mode)
        else:
            return None

    def send(self):
        """
        Send the current message to all the servers.
        """
        self.msg.validate()
        if self.log_file:
            self.log_file.close()
        self.sender.send(self, self.debug)
