#coding=utf-8
from cookielib import CookieJar
from urllib2 import Request,build_opener,HTTPHandler
from urllib import urlencode
from types import StringType
from Errors import *
from re import compile
from Cache import Cache
            
class Fetion:
    def __init__(self,mobile,password,status='4',cachefile='Fetion.cache',keepalive=True):
        if cachefile is not None: self.cache = Cache(cachefile)
        else: self.idfinder = compile('touserid=(\d*)')
            #在有缓存的情况下，创建对象时不载入正则，提高速度。           
            
        self.opener = build_opener(HTTPCookieProcessor(CookieJar()), HTTPHandler)
        self.mobile,self.password,self.status = mobile, password, status
        
        self._login()
        
        if keepalive:
            from AliveKeeper import AliveKeeper
            self.alivekeeper = AliveKeeper(self.opener)
                
       
    def logout(self):
        #退出飞信，否则可能会影响正常短信收发
        self.open('im/index/logoutsubmit.action')
        try:
            self.cache.exit()
            self.alivekeeper.stop()
            del self.idfinder,self.cache,self.alivekeeper
        finally:
            del self.opener,self.mobile,self.password,self.status

    '''发送定时短信。格式：年月日小时分钟
    如：2011年11月20日11时14分：201111201144
        2012年11月11日11时11分：201211111111
    注意：时间允许范围：当前时刻向后10分钟-向后1年
    如：当前时间：2011年11月20日 11:17
    有效时间范围是:2011年11月20日11:27分到2012年11月20日11:27分
    '''
    send2self = lambda self,message,time=None:'成功' in (self.open('im/user/sendMsgToMyselfs.action',{'msg':message}) if time is None else self.open('im/user/sendTimingMsgToMyselfs.action',{'msg':message,'timing':time}))
    send = lambda self,mobile,message,sm=False:tuple([self._send(x,message,sm) for x in mobile]) if type(mobile) != StringType else self._send(mobile,message,sm)
    changeimpresa = lambda self,impresa: impresa in self.open('im/user/editimpresaSubmit.action',{'impresa':impresa})
    addfriend = lambda self,phone,name='xx':'成功' in self.open('im/user/insertfriendsubmit.action',{'nickname':name,'number':phone,'type':'0'})
    _send = lambda self,mobile,message,sm:self.send2self(message) if mobile is self.mobile else self.send2id(self.findid(mobile),message,sm)
    _login = lambda self:'登陆' in self.open('im/login/inputpasssubmit1.action',{'m':self.mobile,'pass':self.password,'loginstatus':self.status}) 
    tweet = lambda self,content:'成功' in self.open('space/microblog/create.action',{'content':content,'checkCode':'','from':'myspace'})
    send2id = lambda self,id,message,sm=False: False if id is None else '成功' in self.open(('im/chat/sendMsg.action?touserid='+id if sm else 'im/chat/sendShortMsg.action?touserid='+id),{'msg':message})
    markread = lambda self,id:' ' in self.open('im/box/deleteMessages.action',{'fromIdUser':id})
    alive = lambda self:'心情' in self.open('im/index/indexcenter.action')

    
    def _getid(self,mobile):
        if not hasattr(self,'idfinder'): self.idfinder = compile('touserid=(\d*)')#如果尚未构建正则表达式对象，则创建
        result = self.idfinder.findall(self.open('im/index/searchOtherInfoList.action',{'searchText':mobile}))       
        return (result[0] if len(result) > 0 else None)              
        
    def findid(self,mobile):
        if hasattr(self,'cache'):
            id = self.cache.get(mobile)
            if id is not None: return id
            id = self._getid(mobile)#缓存中没有，获取ID并存入。
            self.cache.put(mobile,id)
            return id
        return self._getid(mobile)
    
    def getmessage(self):
        web = self.open('im/box/alllist.action')
        if not hasattr(self,'fidfinder'):
            self.fidfinder     = compile('<a href="/im/chat/toinputMsg.action\?touserid=(\d*)&amp;')
            self.namefinder    = compile('<a href="/im/chat/toinputMsg.action\?touserid=\d*&amp;box=true&amp;t=\d*">([^/]*)</a>:')
            self.contentfinder = compile('<a href="/im/chat/toinputMsg.action\?touserid=\d*&amp;box=true&amp;t=\d*">[^/]*</a>:(.*?)<br/>')
        fids = self.fidfinder.findall(web)
        return tuple([tuple([fids[i],self.namefinder.findall(web)[i],self.contentfinder.findall(web)[i]]) for i in range(len(fids))])
        
    def open(self,url,data=None):
        html = self.opener.open(Request('http://f.10086.cn/%s' % url,urlencode(data))).read() if data is not None else self.opener.open('http://f.10086.cn/%s' % url).read()
        if '登陆' in html: raise FetionNotLogin
        elif '对方不是您的好友' in html: raise FetionNotYourFriend
        return html
    