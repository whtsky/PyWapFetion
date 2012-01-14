#coding=utf-8

__name__ = 'PyWapFetion'
__version__ = '0.9'
__author__ = 'whtsky'
__website__ = 'http://github.com/whtsky/PyWapFetion'
__license__ = 'MIT'


from Fetion import Fetion

def send2self(mobile,password,message):
    x = Fetion(mobile,password)
    x.send2self(message)
    x.logout()
    del x

def send(mobile,password,to,message):
    x = Fetion(mobile,password)
    x.send(to,message)
    x.logout()
    del x
    