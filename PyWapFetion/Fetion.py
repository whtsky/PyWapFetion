#coding=utf-8
import cookielib
import urllib2
from urllib import urlencode
from types import StringType
from time import sleep
from Error import Returner
from re import compile
from marshal import dump,load

#有些主机可能不支持多线程
try:
    from threading import Thread
except:
    _have_thread_ = False
else:
    _have_thread_ = True

#状态保持
if _have_thread_ is True:
    class AliveKeeper(Thread):
        def __init__(self,Fetion,sleeptime=240,Daemon=True,start=True):#默认每480秒登陆一次
            self.Fetion = Fetion
            Thread.__init__(self, name = 'AliveKeeper of' + self.Fetion.mobile)
            self.on = True
            self.sleeptime = sleeptime
            self.setDaemon(Daemon)
            if start:
                self.start()
            
        def run(self):
            while self.on and self.Fetion.alive():
                sleep(self.sleeptime)
            
        def stop(self):
            self.on = False
            return not self.on
    
#缓存
class Cache:
    def __init__(self,path):
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
        try:
            return id is self.dict[phone]
        except:
            return False
        
    def rm(self,phone):
        #从字典中删除ID
        try:
            self.dict.pop[phone]
        except:
            #如字典中没有本ID则返回False
            return False
        return True
        
    def save(self):
        f = open(self.path,'wb')
        #将字典保存到文件
        try:
            dump(self.dict,f)
        except:
            return False
        f.close()
        del f
        return True
        
    def exit(self):
        self.save()
        del self.path
        del self.dict
        
class Fetion:
    def __init__(self,mobile,password,status='4',cachefile='Fetion.cache',keepalive=True):
        #如不使用缓存，则设cachefile=False
        if cachefile:
            self.cache = Cache(cachefile)
        else:
            from re import compile
            self.idfinder = compile('touserid=(\d*)')
            #在有缓存的情况下，创建对象时不载入正则，提高速度。           
            
        self.mobile = mobile
        self.password = password
        self.status = status
        
        self._login()
        
        if _have_thread_ and keepalive:
            self.alivekeeper = AliveKeeper(self)
                
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
            req = urllib2.Request('http://f.10086.cn/im/user/sendTimingMsgToMyselfs.action',data)
        return Returner(self.opener.open(req).read())
        
    def send(self,mobile,message,sm=False):
        #SM=Short Message,强制发送短信。
        if type(mobile) != StringType:
            #构建一个字典并将每一个号码的发送结果存入字典
            results = {}
            return tuple([self._send(x,message,sm) for x in mobile])
        else:
            return self._send(mobile,message,sm)
    
    def changeimpresa(self,impresa):
        data = urlencode({'impresa':impresa})
        req = urllib2.Request('http://f.10086.cn/im/user/editimpresaSubmit.action',data)
        #修改心情后会直接返回主页，所以判断返回的页面中是否存在指定的签名
        return impresa in self.opener.open(req).read()
    
    def addfriend(self,phone,name='xx'):
        data = urlencode({'nickname':name,
                          'number':phone,
                          'type':'0'})
        req = urllib2.Request('http://f.10086.cn/im/user/insertfriendsubmit.action',data)
        return Returner(self.opener.open(req).read())
        
    def logout(self):
        #退出飞信，否则可能会影响正常短信收发
        self.opener.open('http://f.10086.cn/im/index/logoutsubmit.action')
        #这些都是可能不存在的东西，防止异常
        try:
            del self.idfinder
            self.cache.exit()
            del self.cache
            self.alivekeeper.stop()
            del self.alivekeeper
        finally:
            #扫尾工作
            del self.opener
            del self.mobile
            del self.password
            del self.status
    
    def _send(self,mobile,message,sm):
        #SM=Short Message,强制发送短信。
        if mobile is self.mobile:
            #如果传入的手机号是自己的手机号，则调用send2self().
            return self.send2self(message)
        else:    
            return self.send2id(self.findid(mobile),message,sm)

    def _login(self):
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()), urllib2.HTTPHandler)
        #登陆并保存cookies.
        data = urlencode({'m':self.mobile,
                         'pass':self.password,
                         'loginstatus':self.status})
        req = urllib2.Request('http://f.10086.cn/im/login/inputpasssubmit1.action',data)
        self.opener.open(req) 
        
    def _getid(self,mobile):
        data = urlencode({'searchText':mobile})
        req = urllib2.Request('http://f.10086.cn/im/index/searchOtherInfoList.action',data)
        #获得HTML页面
        try:
            htm = self.opener.open(req).read()
        except:
            return False
            #移动的服务器挂了，认命吧。
        
        if not hasattr(self,'idfinder'):
            #如果尚未构建正则表达式对象，则创建
            self.idfinder = compile('touserid=(\d*)')
        #正则匹配飞信ID
        result = self.idfinder.findall(htm)       
                
        #找到返回ID，否则返回False
        if len(result) > 0:
            return result[0]
        return False
        
    def findid(self,mobile):
        if hasattr(self,'cache'):
            #如果开启缓存（默认开启），则查找缓存文件
            id = self.cache.get(mobile)
            if id:
                return id
            else:
                #缓存中没有，获取ID并存入。
                id = self._getid(mobile)
                self.cache.put(mobile,id)
                return id
        return self._getid(mobile)
        
    def send2id(self,id,message,sm=False):
        if id is False:
            return False
        #SM=Short Message,强制发送短信。
        data = urlencode({'msg':message})
        if sm:
            req = urllib2.Request('http://f.10086.cn/im/chat/sendMsg.action?touserid='+id,data)
        else:
            req = urllib2.Request('http://f.10086.cn/im/chat/sendShortMsg.action?touserid='+id,data)
        return Returner(self.opener.open(req).read())
    
    def getmessage(self):
        web = self.opener.open('http://f.10086.cn/im/box/alllist.action').read()
        Returner(web) #确保在登录状态中
        if not hasattr(self,'fidfinder'):
            self.fidfinder     = compile('<a href="/im/chat/toinputMsg.action\?touserid=(\d*)&amp;')
            self.namefinder    = compile('<a href="/im/chat/toinputMsg.action\?touserid=\d*&amp;box=true&amp;t=\d*">([^/]*)</a>:')
            self.contentfinder = compile('<a href="/im/chat/toinputMsg.action\?touserid=\d*&amp;box=true&amp;t=\d*">[^/]*</a>:(.*?)<br/>')
        fids = self.fidfinder.findall(web)
        [self.opener.open(urllib2.Request('http://f.10086.cn/im/box/deleteMessages.action',urlencode({'fromIdUser':x}))) for x in fids]
        return tuple([tuple([fids[i],self.namefinder.findall(web)[i],self.contentfinder.findall(web)[i]]) for i in range(len(fids))])
    
    def alive(self):
        #10分钟无操作，则WAP飞信会自动退出
        #用于保持登录状态。若已离线则返回False.
        return '心情' in self.opener.open('http://f.10086.cn/im/index/indexcenter.action').read()
        
        