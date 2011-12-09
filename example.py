#coding=utf-8
from PyWapFetion import *
#仅作参考，详细了解请参考源码

#快速发送：
send2self('手机号','密码','信息')
send('手机号','密码','接收方手机号','信息')

#----------------------------------------------------------------------
myfetion = Fetion('手机号','密码')

myfetion = Fetion('手机号','密码',keepalive=True)#自动保持状态

myfetion.send2self('发给自己的东西')
myfetion.findid('输入手机号，返回飞信ID')
myfetion.sendBYid('飞信ID','消息')
myfetion.send('手机号','消息',sm=True)#发送飞信信息
myfetion.send('昵称','消息')#你也可以这么干
myfetion.sendBYlist('手机号','消息',sm=True)#通过设定sm=True强制发送短信（sm=ShortMessage）
myfetion.addfriend('手机号','你的昵称（5字以内）')
myfetion.send(['手机号1','手机号2','这就是传说中的群发'],'消息')
#成功返回True，失败返回False

myfetion.getmessage()#返回tuple(tuple(飞信号,昵称,内容)) 格式的信息

myfetion.send2self('这个是发给自己的定时短信',time='201111201120')
'''发送定时短信。格式：年月日小时分钟
如：2011年11月20日11时14分：201111201144
    2012年11月11日11时11分：201211111111
注意：时间允许范围：当前时刻向后10分钟-向后1年
如：当前时间：2011年11月20日 11:17
有效时间范围是:2011年11月20日11:27分到2012年11月20日11:27分
'''

myfetion.changeimpresa('改签名')
myfetion.tweet('发飞语')
myfetion.alive()#保持在线，10分钟以上无操作会被判定为离线
#系统默认保持在线，一般不用手动执行。

myfetion.logout()
#-----------------------------------------------------------------------