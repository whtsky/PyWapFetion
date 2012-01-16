#coding=utf-8
from __future__ import with_statement #在Python2.5中使用with的话需要这么干
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

myfetion.getmessage()#返回tuple(tuple(飞信ID,昵称,内容)) 格式的信息

info = myfetion.getuserinfo('飞信ID') 
'''获取好友信息，返回值为一个dict。格式：
{
'avatar'    : 头像图片的网址,
'name'      : 姓名,
'localname' : 备注姓名,
'fid'       : 飞信号（飞信号不同于飞信ID）,
'phone'     : 手机号,
'birthday'  : 生日,
'sex'       : 性别,
'city'      : 城市,
'sign'      : 星座,
'blood'     : 血型,
'impresa'   : 心情短语,
}
如果无法找到该好友，返回None.
'''

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

groups=myfetion.getgroups()
'''取得所有好友分组。返回一个dict，格式：
{
分组名:分组id
}
'''
users=myfetion.getgroupusers('1') #取得分组号为1的分组内所有好友的*飞信ID*。返回一个tuple
allusers=myfetion.getallusers() #取得所有好友的*飞信ID*。返回一个tuple
allusersinfo=myfetion.getallusersinfo()
'''取得所有用户信息。返回一个dict，格式：
飞信ID:用户信息（同样为一个dict，格式参考上方getuserinfo()的返回值）
'''

status=myfetion.getuserstatus('ID') #返回一个str，内容为当前用户状态
allstatus=myfetion.getallusersstatus() #返回一个dict，格式{用户ID：用户状态}

myfetion.deletefriend('要删除的好友ID')
myfetion.addblacklist('要拉黑的好友ID')
myfetion.relieveblack('要解除拉黑的好友ID')

myfetion.logout()
#-----------------------------------------------------------------------

with Fetion('手机号','密码') as f:#其实你也可以用with，这样更方便一点
    f.send2self('xxxx')