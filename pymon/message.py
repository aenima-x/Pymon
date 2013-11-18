# -*- coding: utf-8 -*-
from datetime import datetime
import utils
from pymonExceptions import ClientMissingInfoError


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
            env_machine = utils.get_variable_content('MACHINE')
            if not env_machine:
                raise ClientMissingInfoError("MACHINE")
            else:
                self.machine = env_machine
        else:
            self.machine = machine

    def get_message_string(self):
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