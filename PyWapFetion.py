#coding=utf-8
import cookielib
import urllib2
from urllib import urlencode
from re import compile
__name__ = 'PyWapFetion'
__author__ = 'whtsky'
__website__ = 'https://github.com/whtsky/PyWapFetion'
#Under MIT LICENSE.

#Cache
class Cache:
    def __init__(self,path):
        from marshal import load
        self.path=path
        try:
            f=open(path,'rb')
            self.dict=load(f)
            f.close()
        except:
            self.dict={}
        
    def get(self,phone):
        try:
            return self.dict[phone]
        except:
            return False
            
    def put(self,phone,id):
        self.dict[phone]=id
        
    def rm(self,phone):
        try:
            self.dict.pop[phone]
            return True
        except:
            return False
        
    def save(self):
        f=open(self.path,'wb')
        from marshal import dump
        dump(self.dict,f)
        f.close()
        
    def exit(self):
        self.save()
        del self.path
        del self.dict
        
def send2self(mobile,password,message):
    myfetion = Fetion(mobile,password)
    myfetion.send2self(message)
    myfetion.logout()

def sendfetion(mobile,password,mobile2,message):
    myfetion = Fetion(mobile,password)
    myfetion.send(mobile2,message)
    myfetion.logout()

class Fetion:
    def __init__(self,mobile,password,status='4',cachefile='Fetion.cache'):
        if cachefile:
            self.cache=Cache(cachefile)
        else:
            self.cache=False
        self.mobile=mobile
        self.password=password
        self.status=status
        self._login()
        self.idfinder = compile('touserid=(\d*)')
        
    def send2self(self,message):
        data = urlencode({'msg':message})
        req = urllib2.Request('http://f.10086.cn/im/user/sendMsgToMyselfs.action',data)
        self.opener.open(req)
        
    def send(self,mobile,message):
        self.send2id(self.findid(mobile),message)
        
    def addfriend(self,phone,name='xx'):
        data = urlencode({'nickname':name,
                          'number':phone,
                          'type':'0'})
        req = urllib2.Request('http://f.10086.cn/im/user/insertfriendsubmit.action',data)
        self.opener.open(req)
        
    def logout(self):
        self.opener.open('http://f.10086.cn/im/index/logoutsubmit.action')
        del self.opener
        del self.mobile
        del self.password
        del self.status
        del self.idfinder
        self.cache.exit()
        del self.cache
        
    def _login(self):
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()), urllib2.HTTPHandler)
        data = urlencode({'m':self.mobile,
                         'pass':self.password,
                         'loginstatus':self.status})
        req = urllib2.Request('http://f.10086.cn/im/login/inputpasssubmit1.action',data)
        self.opener.open(req) 
        
    def _getid(self,mobile):
        data = urlencode({'searchText':mobile})
        req = urllib2.Request('http://f.10086.cn/im/index/searchOtherInfoList.action',data)
        htm = self.opener.open(req).read()
        result = self.idfinder.findall(htm)
        if len(result) > 0:
            return result[0] 
        return False
        
    def findid(self,mobile):
        if self.cache:
            id = self.cache.get(mobile)
            if id:
                return id
            else:
                id = self._getid(mobile)
                self.cache.put(mobile,id)
                return id
        else:
            return self._getid(mobile)
        
    def send2id(self,id,message):
        data = urlencode({'msg':message})
        req = urllib2.Request('http://f.10086.cn/im/chat/sendMsg.action?touserid='+id,data)
        self.opener.open(req)
