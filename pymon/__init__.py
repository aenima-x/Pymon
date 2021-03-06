from server import Server
from client import Client

__author__ = 'Nicolas Rebagliati (nicolas.rebagliati@aenima-x.com.ar)'
VERSION = (1, 0, 0, 'final', 0)


def get_version():
    """Returns a PEP 386-compliant version number from VERSION."""
    assert VERSION[3] in ('alpha', 'beta', 'rc', 'final')
    sub = ''
    if VERSION[2]:
        parts = 2
    else:
        parts = 3
    main = '.'.join(str(x) for x in VERSION[:parts])
    if VERSION[3] != 'final':
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'c'}
        sub = mapping[VERSION[3]] + str(VERSION[4])
    return str(main + sub)