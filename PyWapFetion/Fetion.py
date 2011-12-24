#coding=utf-8
from cookielib import CookieJar
from urllib2 import Request,build_opener,HTTPHandler,HTTPCookieProcessor
from urllib import urlencode
from Errors import *
from re import compile
from Cache import Cache
            
class Fetion(object):
    def __init__(self,mobile,password,status='4',cachefile='Fetion.cache',keepalive=False):
        if cachefile is not None: self.cache = Cache(cachefile)
        else: self.idfinder = compile('touserid=(\d*)')#在有缓存的情况下，创建对象时不载入正则，提高速度。           
            
        self.opener = build_opener(HTTPCookieProcessor(CookieJar()), HTTPHandler)
        self.mobile,self.password,self.status = mobile, password, status
        self._login()
        
        if keepalive:
            from AliveKeeper import AliveKeeper
            self.alivekeeper = AliveKeeper(self.opener)
        
    def logout(self):
        self.open('im/index/logoutsubmit.action')#退出飞信，否则可能会影响正常短信收发
        try:
            del self.idfinder,self.cache,self.alivekeeper,self.opener,self.mobile,self.password,self.status
        except:
            pass

    send2self = lambda self,message,time=None:'成功' in (self.open('im/user/sendMsgToMyselfs.action',{'msg':message}) if time is None else self.open('im/user/sendTimingMsgToMyselfs.action',{'msg':message,'timing':time}))
    sendBYlist = lambda self,mobile,message,sm=False:dict([[x,self.send(x,message,sm)] for x in mobile])
    changeimpresa = lambda self,impresa: impresa in self.open('im/user/editimpresaSubmit.action',{'impresa':impresa})
    addfriend = lambda self,phone,name='xx':'成功' in self.open('im/user/insertfriendsubmit.action',{'nickname':name,'number':phone,'type':'0'})
    send = lambda self,mobile,message,sm=False:self.send2self(message) if mobile == self.mobile else self.sendBYid(self.findid(mobile),message,sm)
    _login = lambda self:'登陆' in self.open('im/login/inputpasssubmit1.action',{'m':self.mobile,'pass':self.password,'loginstatus':self.status}) 
    tweet = lambda self,content:'成功' in self.open('space/microblog/create.action',{'content':content,'checkCode':'','from':'myspace'})
    markread = lambda self,id:' ' in self.open('im/box/deleteMessages.action',{'fromIdUser':id})
    alive = lambda self:'心情' in self.open('im/index/indexcenter.action')
    __del__ = logout

    def sendBYid(self,id,message,sm=False):
        url = ('im/chat/sendMsg.action?touserid=%s' % id) if sm else ('im/chat/sendShortMsg.action?touserid=%s '% id)
        htm = self.open(url,{'msg':message})
        if '对方不是您的好友' in htm: raise FetionNotYourFriend  
        return False if id is None else '成功' in htm

    
    def _getid(self,mobile):
        if not hasattr(self,'idfinder'): self.idfinder = compile('touserid=(\d*)')#如果尚未构建正则表达式对象，则创建
        result = self.idfinder.findall(self.open('im/index/searchOtherInfoList.action',{'searchText':mobile}))       
        return (result[0] if len(result) > 0 else None)              
        
    def findid(self,mobile):
        if hasattr(self,'cache'):
            id = self.cache[mobile]
            if id is not None: return id
            id = self._getid(mobile)#缓存中没有，获取ID并存入。
            self.cache[mobile] = id
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
        
    def open(self,url,data=''):
        html = self.opener.open(Request('http://f.10086.cn/%s' % url,urlencode(data))).read()
        if '登录' in html and '您正在登录中国移动WAP飞信' not in html: raise FetionNotLogin()
        return html
  