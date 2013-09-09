# -*- coding: utf-8 -*-
import re
import os
import subprocess

ipv4pattern = "^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
hostnamePattern = "^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$"
ipv4regex = re.compile(ipv4pattern)
hostnameRegex = re.compile(hostnamePattern)


def ipAddressIsValid(ipAddress):
    """
    Validates IP Address.
    """
    if not ipv4regex.match(ipAddress):
        return False
    else:
        octets = ipAddress.split('.')
        f = lambda x: 256 > int(x) > 0
        validOctets = filter(f, octets)
        return len(octets) == len(validOctets)


def hostnameIsValid(address):
    """
    Validate a hostname
    """
    return bool(hostnameRegex.match(address))


def getVariableContent(variableNames):
        """
        Look if the variable is set and get its content.
        For backward compatibility with Hobbit, it can receive a list or variable names to find the same information.

        Arguments:
        variableNames -- Name or names for the variables to find
        """
        if isinstance(variableNames, list):
            response = None
            for variableName in variableNames:
                response = os.environ.get(variableName)
                if response:
                    break
            return response
        else:
            return os.environ.get(variableNames)


def getCommandOutput(command):
    assert isinstance(command, str)
    output = subprocess.check_output(command.split()).strip('\n')
    return output
