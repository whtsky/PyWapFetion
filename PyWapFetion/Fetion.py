#coding=utf-8
from cookielib import CookieJar
from urllib2 import Request,build_opener,HTTPHandler,HTTPCookieProcessor
from urllib import urlencode
from Errors import *
from re import compile
from Cache import Cache

idfinder = compile('touserid=(\d*)')
msg_re = {
'id'     : compile('<a href="/im/chat/toinputMsg.action\?touserid=(\d*)&amp;'),
'name'    : compile('<a href="/im/chat/toinputMsg.action\?touserid=[^"]*">([^/]*)</a>:'),
'content' : compile('<a href="/im/chat/toinputMsg.action\?touserid=[^"]*">[^/]*</a>:(.*?)<br/>'),
}

group_re = {
'name' : compile('\+\|([^<]*?)</a>'),
'id'   : compile('/im/user/crewManagement.action\?idContactList=(\d*)'),
}

info_re = {
'name'    : compile('姓名:([^\[\t]*)'),#第一个值为好友姓名，第二个为备注姓名
'fid'     : compile('飞信号:([^<].*)<br/>'),#飞信ID和飞信号不是同一个数字。。
'phone'   : compile('手机号码:([^<].*)<br/>'),
'age'     : compile('年龄:([^<].*)<br/>'),
'sex'     : compile('性别:([^<].*)<br/>'),
'city'    : compile('城市:([^\[]*)'),
'sign'    : compile('星座:([^\[]*)'),
'blood'   : compile('血型:([^\[]*)'),
'impresa' : compile('心情短语:([^<]*)<br/>'),
}
            
class Fetion(object):
    def __init__(self,mobile,password,status='4',cachefile='Fetion.cache',keepalive=False):
        if cachefile is not None: 
            self.cache = Cache(cachefile)        
            
        self.opener = build_opener(HTTPCookieProcessor(CookieJar()), HTTPHandler)
        self.mobile,self.password,self.status = mobile, password, status
        self._login()
        
        if keepalive:
            from AliveKeeper import AliveKeeper
            self.alivekeeper = AliveKeeper(self)

    send2self = lambda self,message,time=None:'成功' in (self.open('im/user/sendMsgToMyselfs.action',{'msg':message}) if time is None else self.open('im/user/sendTimingMsgToMyselfs.action',{'msg':message,'timing':time}))
    sendBYlist = lambda self,mobile,message,sm=False:dict([[x,self.send(x,message,sm)] for x in mobile])
    changeimpresa = lambda self,impresa: impresa in self.open('im/user/editimpresaSubmit.action',{'impresa':impresa})
    addfriend = lambda self,phone,name='xx':'成功' in self.open('im/user/insertfriendsubmit.action',{'nickname':name,'number':phone,'type':'0'})
    send = lambda self,mobile,message,sm=False:self.send2self(message) if mobile == self.mobile else self.sendBYid(self.findid(mobile),message,sm)
    _login = lambda self:'登陆' in self.open('im/login/inputpasssubmit1.action',{'m':self.mobile,'pass':self.password,'loginstatus':self.status}) 
    tweet = lambda self,content:'成功' in self.open('space/microblog/create.action',{'content':content,'checkCode':'','from':'myspace'})
    markread = lambda self,id:' ' in self.open('im/box/deleteMessages.action',{'fromIdUser':id})
    alive = lambda self:'心情' in self.open('im/index/indexcenter.action')
    getallusersinfo = lambda self: dict([[x,self.getuserinfo(x)] for x in self.getallusers()])
    __del__ = logout = lambda self:'退出WAP飞信' in self.opener.open('http://f.10086.cn/im/index/logoutsubmit.action').read()

    def sendBYid(self,id,message,sm=False):
        url = ('im/chat/sendMsg.action?touserid=%s' % id) if sm else ('im/chat/sendShortMsg.action?touserid=%s '% id)
        htm = self.open(url,{'msg':message})
        if '对方不是您的好友' in htm: raise FetionNotYourFriend  
        return False if id is None else '成功' in htm

    
    def _getid(self,mobile):
        result = idfinder.findall(self.open('im/index/searchOtherInfoList.action',{'searchText':mobile}))       
        return (result[0] if len(result) > 0 else None) 
        
    def findid(self,mobile):
        if hasattr(self,'cache'):
            id = self.cache[mobile]
            if id is not None: return id
            id = self._getid(mobile)#缓存中没有，获取ID并存入。
            self.cache[mobile] = id
            return id
        return self._getid(mobile)
    
    def getuserinfo(self,id):
        web = self.open('im/user/userinfoByuserid.action?touserid=%s' % id)
        assert not('对不起,操作失败' in web),'Wrong ID'
        if '对不起,没有找到你要查找的好友.' in web:return None
        return {
            'name'      : info_re['name'].findall(web)[0],
            'localname' : info_re['name'].findall(web)[1],
            'fid'       : info_re['fid'].findall(web)[0],
            'phone'     : info_re['phone'].findall(web)[0],
            'age'       : info_re['age'].findall(web)[0],
            'sex'       : info_re['sex'].findall(web)[0],
            'city'      : info_re['city'].findall(web)[0],
            'sign'      : info_re['sign'].findall(web)[0],
            'blood'     : info_re['blood'].findall(web)[0],
            'impresa'   : info_re['impresa'].findall(web)[0],
        }
            
    def getmessage(self):
        web = self.open('im/box/alllist.action')
        ids     = msg_re['id'].findall(web)
        names    = msg_re['name'].findall(web)
        contents = msg_re['content'].findall(web)
        return tuple([tuple([ids[i],names[i],contents[i]]) for i in range(len(ids))])
    
    def getgroups(self):
        web = self.open('im/user/userGroupManagement.action')
        names = group_re['name'].findall(web)
        ids   = group_re['id'].findall(web)
        return dict([[names[i],ids[i]] for i in range(len(names))])
        
    def getgroupusers(self,groupid):
        page = 1
        ids = []
        while True:
            web = self.open('im/index/contactlistView.action?idContactList=%s&page=%s' % (groupid,page))
            ids += msg_re['id'].findall(web)
            if '下一页' in web: page += 1
            else: break
        return tuple(set(ids))
        
    def getallusers(self):
        users = []
        [users.extend(self.getgroupusers(v)) for k,v in self.getgroups().items()]
        return tuple(set(users))
           
    def open(self,url,data=''):
        html = self.opener.open(Request('http://f.10086.cn/%s' % url,urlencode(data))).read()
        if '登录' in html and '您正在登录中国移动WAP飞信' not in html: raise FetionNotLogin()
        return html
  
