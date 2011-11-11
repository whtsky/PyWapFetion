#coding=utf-8
import cookielib
import urllib2
from urllib import urlencode
from re import compile
class Fetion :
    def __init__(self,mobile,password,status='4'):
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()), urllib2.HTTPHandler)
        data = urlencode({'m':mobile,
                         'pass':password,
                         'loginstatus':status})
        req = urllib2.Request('http://f.10086.cn/im/login/inputpasssubmit1.action',data)
        self.opener.open(req)
        self.idfinder = compile('touserid=(\d*)')
        
    def send2self(self,message):
        data = urlencode({'msg':message})
        req = urllib2.Request('http://f.10086.cn/im/user/sendMsgToMyselfs.action',data)
        self.opener.open(req)
        
    def send(self,mobile,message):
        send2id(findid(mobile),message)
        
    def findid(self,mobile):
        data = urlencode({'searchText':mobile})
        req = urllib2.Request('http://f.10086.cn/im/index/searchOtherInfoList.action',data)
        htm=self.opener.open(req).read()
        result = self.idfinder.findall(htm)
        if len(result) > 0:
            return result[0] 
        return '0'
        
    def send2id(self,id,message):
        data = urlencode({'msg':message})
        req = urllib2.Request('http://f.10086.cn/im/chat/sendMsg.action?touserid='+id,data)
        self.opener.open(req)
        
    def logout(self):
        self.opener.open('http://f.10086.cn/im/index/logoutsubmit.action')
        del self.opener
