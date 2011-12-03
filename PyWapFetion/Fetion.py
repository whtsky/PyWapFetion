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
        self.opener = build_opener(HTTPCookieProcessor(CookieJar()), HTTPHandler)
        if cachefile is not None:
            self.cache = Cache(cachefile)
        else:
            self.idfinder = compile('touserid=(\d*)')
            #在有缓存的情况下，创建对象时不载入正则，提高速度。           
            
        self.mobile = mobile
        self.password = password
        self.status = status
        
        self._login()
        
        if keepalive:
            from AliveKeeper import AliveKeeper
            self.alivekeeper = AliveKeeper(self.opener)
                
    def send2self(self,message,time=None):
        '''发送定时短信。格式：年月日小时分钟
        如：2011年11月20日11时14分：201111201144
            2012年11月11日11时11分：201211111111
        注意：时间允许范围：当前时刻向后10分钟-向后1年
        如：当前时间：2011年11月20日 11:17
        有效时间范围是:2011年11月20日11:27分到2012年11月20日11:27分
        '''
        return '成功' in self.open('http://f.10086.cn/im/user/sendMsgToMyselfs.action',{'msg':message}) if time is None else self.open('http://f.10086.cn/im/user/sendTimingMsgToMyselfs.action',{'msg':message,'timing':time})
        
    def send(self,mobile,message,sm=False):
        #SM=Short Message,强制发送短信。
        if type(mobile) != StringType: return tuple([self._send(x,message,sm) for x in mobile])
        return self._send(mobile,message,sm)
    
    def changeimpresa(self,impresa):
        #修改心情后会直接返回主页，所以判断返回的页面中是否存在指定的签名
        return impresa in self.open('http://f.10086.cn/im/user/editimpresaSubmit.action',
                                     {'impresa':impresa})
    
    def addfriend(self,phone,name='xx'):
        return '成功' in self.open('http://f.10086.cn/im/user/insertfriendsubmit.action',
                                    {'nickname':name,'number':phone,'type':'0'})
         
    def logout(self):
        #退出飞信，否则可能会影响正常短信收发
        self.open('http://f.10086.cn/im/index/logoutsubmit.action')
        try:
            del self.idfinder
            self.cache.exit()
            del self.cache
            self.alivekeeper.stop()
            del self.alivekeeper
        finally:
            del self.opener
            del self.mobile
            del self.password
            del self.status
    
    def _send(self,mobile,message,sm):
        #SM=Short Message,强制发送短信。
        if mobile is self.mobile: return self.send2self(message)
        return self.send2id(self.findid(mobile),message,sm)

    def _login(self):
        self.open('http://f.10086.cn/im/login/inputpasssubmit1.action',{'m':self.mobile,
                                                                        'pass':self.password,
                                                                        'loginstatus':self.status}) 
        
    def _getid(self,mobile):
        htm = self.open('http://f.10086.cn/im/index/searchOtherInfoList.action',{'searchText':mobile})
        
        if not hasattr(self,'idfinder'):
            #如果尚未构建正则表达式对象，则创建
            self.idfinder = compile('touserid=(\d*)')
        result = self.idfinder.findall(htm)       
                
        if len(result) > 0: return result[0]
        return None
        
    def findid(self,mobile):
        if hasattr(self,'cache'):
            id = self.cache.get(mobile)
            if id is not None: return id
            #缓存中没有，获取ID并存入。
            id = self._getid(mobile)
            self.cache.put(mobile,id)
            return id
        return self._getid(mobile)
        
    def send2id(self,id,message,sm=False):
        if id is None: return False
        url = 'http://f.10086.cn/im/chat/sendMsg.action?touserid='+id if sm else 'http://f.10086.cn/im/chat/sendShortMsg.action?touserid='+id
        return '成功' in self.open(url,{'msg':message})
    
    def getmessage(self):
        web = self.open('http://f.10086.cn/im/box/alllist.action')
        if not hasattr(self,'fidfinder'):
            self.fidfinder     = compile('<a href="/im/chat/toinputMsg.action\?touserid=(\d*)&amp;')
            self.namefinder    = compile('<a href="/im/chat/toinputMsg.action\?touserid=\d*&amp;box=true&amp;t=\d*">([^/]*)</a>:')
            self.contentfinder = compile('<a href="/im/chat/toinputMsg.action\?touserid=\d*&amp;box=true&amp;t=\d*">[^/]*</a>:(.*?)<br/>')
        fids = self.fidfinder.findall(web)
        return tuple([tuple([fids[i],self.namefinder.findall(web)[i],self.contentfinder.findall(web)[i]]) for i in range(len(fids))])
    
    def markread(self,id):
        self.open('http://f.10086.cn/im/box/deleteMessages.action',{'fromIdUser':id})
    
    def alive(self):
        #10分钟无操作，则WAP飞信会自动退出。若已离线则返回False.
        return '心情' in self.open('http://f.10086.cn/im/index/indexcenter.action')
        
    def open(self,url,data=None):
        html = self.opener.open(Request(url,urlencode(data))).read() if data is not None else self.opener.open(url).read()
        if '登陆' in html: raise FetionNotLogin
        elif '对方不是您的好友' in html: raise FetionNotYourFriend
        return html
        
    def tweet(self,content):
        return '成功' in self.open('http://f.10086.cn/space/microblog/create.action',{'content':content,
                                                                                       'checkCode':'',
                                                                                       'from':'myspace'})
    