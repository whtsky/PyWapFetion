#coding=utf-8

__name__ = 'PyWapFetion'
__version__ = '0.7'
__author__ = 'whtsky'
__website__ = 'http://github.com/whtsky/PyWapFetion'
__license__ = 'MIT'


from Fetion import Fetion,Cache,AliveKeeper
import Error

def send2self(mobile,password,message):
    x = Fetion(mobile,password,keepalive=False)#不用保持状态，减少内存消耗
    x.send2self(message)
    x.logout()
    del x

def send(mobile,password,to,message):
    x = Fetion(mobile,password,keepalive=False)#不用保持状态，减少内存消耗
    x.send(to,message)
    x.logout()
    del x
    
    