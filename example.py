#coding=utf-8
from PyWapFetion import *
myfetion = Fetion('手机号','密码')

myfetion.send2self('发给自己的东西')
myfetion.findid('输入手机号，返回飞信ID')
myfetion.send2id('飞信ID','消息')
myfetion.send('手机号','消息')
myfetion.addfriend('手机号','你的昵称（5字以内）')
#成功返回True，失败返回False

myfetion.logout()
#----------------------------------------------------------------------
send2self('手机号','密码','信息')
send('手机号','密码','接收方手机号','信息')
