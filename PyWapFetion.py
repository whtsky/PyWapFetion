#coding=utf-8
import cookielib
import urllib2
from urllib import urlencode
from types import *
__name__ = 'PyWapFetion'
__author__ = 'whtsky'
__website__ = 'https://github.com/whtsky/PyWapFetion'
__license__ = 'MIT'

#缓存
class Cache:
    def __init__(self,path):
        from marshal import load
        self.path = path
        try:
            f = open(path,'rb')
            self.dict = load(f)
            f.close()
            del f
        except:
            self.dict={}
        
    def get(self,phone):
        #从字典中取飞信ID，成功返回ID，失败返回False
        try:
            return self.dict[phone]
        except:
            return False
            
    def put(self,phone,id):
        #将ID存入字典
        self.dict[phone] = id
        
    def rm(self,phone):
        #从字典中删除ID
        try:
            self.dict.pop[phone]
            return True
        except:
            #如字典中没有本ID则返回False
            return False
        
    def save(self):
        #将字典保存到文件
        from marshal import dump
        f = open(self.path,'wb')
        dump(self.dict,f)
        f.close()
        del f
        
    def exit(self):
        self.save()
        del self.path
        del self.dict
        
def send2self(mobile,password,message):
    x = Fetion(mobile,password)
    x.send2self(message)
    x.logout()

def send(mobile,password,mobile2,message):
    x = Fetion(mobile,password)
    x.send(mobile2,message)
    x.logout()

class Fetion:
    def __init__(self,mobile,password,status='4',cachefile='Fetion.cache'):
        #如不使用缓存，则设cachefile=False
        if cachefile:
            self.cache = Cache(cachefile)
        else:
            self.cache = False
        #在有缓存的情况下，创建对象时不载入正则，提高速度。           
        self.idfinder = False
            
        self.mobile = mobile
        self.password = password
        self.status = status
        
        self._login()
        
    def send2self(self,message,time=False):
        #发送给自己
        if time is False:
            data = urlencode({'msg':message})
            req = urllib2.Request('http://f.10086.cn/im/user/sendMsgToMyselfs.action',data)
        else:
            '''发送定时短信。格式：年月日小时分钟
            如：2011年11月20日11时14分：201111201144
                2012年11月11日11时11分：201211111111
            注意：时间允许范围：当前时刻向后10分钟-向后1年
            如：当前时间：2011年11月20日 11:17
            有效时间范围是:2011年11月20日11:27分到2012年11月20日11:27分
            '''
            data = urlencode({'msg':message,
                              'timing':time})
            req = urllib2.Request('http://f.10086.cn//im/user/sendTimingMsgToMyselfs.action',data)
        return '成功' in self.opener.open(req).read()
        
    def send(self,mobile,message):
        if type(mobile) != StringType:
            #构建一个字典并将每一个号码的发送结果存入字典
            results = {}
            for x in mobile:
                #实际的发送操作在_send中
                results[x] = self._send(x,message)
            #返回字典
            return results
        else:
            return self._send(mobile,message)
        
    def addfriend(self,phone,name='xx'):
        data = urlencode({'nickname':name,
                          'number':phone,
                          'type':'0'})
        req = urllib2.Request('http://f.10086.cn/im/user/insertfriendsubmit.action',data)
        return '成功' in self.opener.open(req).read()
        
    def logout(self):
        #退出飞信，否则可能会影响正常短信收发
        self.opener.open('http://f.10086.cn/im/index/logoutsubmit.action')
        #这些都是可能不存在的东西，防止异常
        try:
            del self.idfinder
            self.cache.exit()
            del self.cache
        except:
            pass
        #扫尾工作
        del self.opener
        del self.mobile
        del self.password
        del self.status
    
    def _send(self,mobile,message):
        if mobile is self.mobile:
            #如果传入的手机号是自己的手机号，则调用send2self().
            return self.send2self(message)
        else:    
            return self.send2id(self.findid(mobile),message)

    def _login(self):
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()), urllib2.HTTPHandler)
        #登陆并保存cookies.
        data = urlencode({'m':self.mobile,
                         'pass':self.password,
                         'loginstatus':self.status})
        req = urllib2.Request('http://f.10086.cn/im/login/inputpasssubmit1.action',data)
        self.opener.open(req) 
        
    def _getid(self,mobile):
        #如果尚未构建正则表达式对象，则创建
        if self.idfinder is False:
            from re import compile
            self.idfinder = compile('touserid=(\d*)')
            
        #获得HTML页面
        data = urlencode({'searchText':mobile})
        req = urllib2.Request('http://f.10086.cn/im/index/searchOtherInfoList.action',data)
        htm = self.opener.open(req).read()
        
        #正则匹配飞信ID
        result = self.idfinder.findall(htm)
        
        #找到返回ID，否则返回False
        if len(result) > 0:
            return result[0] 
        return False
        
    def findid(self,mobile):
        if self.cache:
            #如果开启缓存（默认开启），则查找缓存文件
            id = self.cache.get(mobile)
            if id:
                return id
            else:
                #缓存中没有，获取ID并存入。
                id = self._getid(mobile)
                self.cache.put(mobile,id)
                return id
        else:
            return self._getid(mobile)
        
    def send2id(self,id,message):
        data = urlencode({'msg':message})
        req = urllib2.Request('http://f.10086.cn/im/chat/sendMsg.action?touserid='+id,data)
        return '成功' in self.opener.open(req).read()
        
    def alive(self):
        #10分钟无操作，则WAP飞信会自动退出
        #用于保持登录状态。若已离线则返回False.
        return '心情' in self.opener.open('http://f.10086.cn/im/index/indexcenter.action').read()