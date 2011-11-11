#coding=utf-8
from pywebfetion import *
myfetion = Fetion('手机号','密码')

myfetion.send2self('发给自己的东西')
myfetion.findid('输入手机号，返回飞信ID')
myfetion.send2id('飞信ID','消息')
myfetion.send('手机号','消息')

myfetion.logout()
#----------------------------------------------------------------------
send2self('手机号','密码','信息')
sendfetion('手机号','密码','接收方手机号','信息')