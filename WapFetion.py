#!/usr/bin/env python
#coding=utf-8
__name__ = ''
__author__ = 'whtsky'
__license__ = 'MIT'
__doc__ = '基于PyWapFetion的CLI飞信客户端'
__help__ = '''
------------------------基于PyWapFetion的一个CLI飞信客户端---------------------

        命令不区分大小写中括号里为命令的缩写

        help                  显示本帮助信息
        s 好友 信息           发送短信 参数为飞信号或手机号
        add 好友 你的昵称     添加好友 参数为手机号或飞信号
        cls                   清屏
        exit                  退出飞信
'''


from PyWapFetion import Fetion
from PyWapFetion.Errors import *
from getpass import getpass
from sys import exit
from os import system,name
from thread import start_new_thread


def checkmessage(Fetion):
    while True:
        for x,y,z in Fetion.getmessage():
            printl('%s发来信息：%s' % (y,z))
            Fetion.markread(x)
        
        
clear = lambda :system("clear") if name is "posix" else system("cls")

clear()
def printl(msg,newline=True):
    msg = str(msg)
    if newline:
        try:
            print msg.decode('utf-8')
        except exceptions.UnicodeEncodeError:
            print msg
    else:
        try:
            print msg.decode('utf-8'),
        except exceptions.UnicodeEncodeError:
            print msg,
        
def Check(bool):
    if bool:
        printl('成功')
    else:
        printl('失败。。')
printl('请输入您的手机号：',False)
Phone = raw_input('')
if Phone is '' or Phone.isdigit() is False or len(Phone) is not 11:
    printl('手机号错误。',False)
    exit()
printl('请输入密码：（不回显）',False)
Password = getpass('')
printl('''请选择登录状态：
1:在线
2:忙碌
3:离开
4:隐身
输入其他字符默认为隐身''')
Status = raw_input()
Status = '4' if Status is '' or (Status.isdigit() and 0<int(2)<5) else Stauts
try:
    User = Fetion(Phone,Password,Status)
except:
    printl('用户名或密码错误。')
    exit()
    
clear()
start_new_thread(checkmessage,(User,))
printl(__help__)
       
while True:
    command = raw_input('Fetion>').split()
    if len(command) == 0:
        pass
    elif command[0] == 'help' :
        printl(__help__)
    elif command[0] == 'cls' :
        clear()
    elif command[0] == 'exit':
        del User
        exit()
    elif command[0] == 'add':
        Check(User.addfriend(command[1],command[2]))
    elif command[0] == 's':
        Check(User.send(command[1],' '.join(command[2:])))
    else:
        printl('未知命令')