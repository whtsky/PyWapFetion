#coding=utf-8
from __future__ import with_statement, absolute_import

__name__ = 'PyWapFetion'
__version__ = '0.9.5'
__author__ = 'whtsky'
__website__ = 'http://github.com/whtsky/PyWapFetion'
__license__ = 'MIT'

from PyWapFetion.Fetion import Fetion


def send2self(mobile, password, message):
    with Fetion(mobile, password) as x:
        x.send2self(message)


def send(mobile, password, to, message):
    with Fetion(mobile, password) as x:
        x.send(to, message)
