#coding=utf-8
from cookielib import CookieJar
from urllib2 import Request,build_opener,HTTPHandler,HTTPCookieProcessor
from urllib import urlencode
import base64
from Errors import *
from re import compile
from Cache import Cache
from gzip import GzipFile
try:from cStringIO import StringIO
except:from StringIO import StringIO

idfinder = compile('touserid=(\d*)')
idfinder2 = compile('name="internalid" value="(\d+)"')
userstatus = compile('<a href="/im/user/userinfoByuserid.action\?touserid=\d*&amp;.*?">.*?</a>\[(.*?)\]')
infofinder = compile('<dd>(.*?)</dd>')
avatarfinder = compile('<div class="mybox_info_pic"><a href="#"><img src="(.*?)"')
namefinder = compile('<div class="mybox_info_text"><span>(.*?)</span>')
csrf_token = compile('<postfield name="csrfToken" value="(\w+)"/>')
codekey = compile('name="codekey" value="(.*?)">')

msg_re = {
'id'     : compile('<a href="/im/chat/toinputMsg.action\?touserid=(\d*)&amp;'),
'name'    : compile('<a href="/im/chat/toinputMsg.action\?touserid=[^"]*">([^/]*)</a>:'),
'content' : compile('<a href="/im/chat/toinputMsg.action\?touserid=[^"]*">[^/]*</a>:(.*?)<br/>'),
}
    
group_re = {
'name' : compile('\+\|([^<]*?)</a>'),
'id'   : compile('/im/user/crewManagement.action\?idContactList=(\d*)'),
}

__all__ = ['Fetion']
            
class Fetion(object):
    def __init__(self,mobile,password,status='0',cachefile='Fetion.cache',keepalive=False):
        '''登录状态：
        在线：400 隐身：0 忙碌：600 离开：100
        '''
        if cachefile is not None: 
            self.cache = Cache(cachefile)        
            
        self.opener = build_opener(HTTPCookieProcessor(CookieJar()), HTTPHandler)
        self.mobile,self.password = mobile, password
        self.csrf = None
        self._login()
        self.changestatus(status)
        
        if keepalive:
            from AliveKeeper import AliveKeeper
            self.alivekeeper = AliveKeeper(self)

    send2self = lambda self,message,time=None:'成功' in (self.open('im/user/sendMsgToMyselfs.action',{'msg':message}) if time is None else self.open('im/user/sendTimingMsgToMyselfs.action',{'msg':message,'timing':time}))
    sendBYlist = lambda self,mobile,message,sm=False:dict([[x,self.send(x,message,sm)] for x in mobile])
    changeimpresa = lambda self,impresa: impresa in self.open('im/user/editimpresaSubmit.action',{'impresa':impresa})
    addfriend = lambda self,phone,name='xx':'成功' in self.open('im/user/insertfriendsubmit.action',{'nickname':name,'number':phone,'type':'0'})
    send = lambda self,mobile,message,sm=False:self.send2self(message) if mobile == self.mobile else self.sendBYid(self.findid(mobile),message,sm)
    tweet = lambda self,content:'成功' in self.open('space/microblog/create.action',{'content':content,'checkCode':'','from':'myspace'})
    markread = lambda self,id:' ' in self.open('im/box/deleteMessages.action',{'fromIdUser':id})
    alive = lambda self:'心情' in self.open('im/index/indexcenter.action')
    getallusersinfo = lambda self: dict([[x,self.getuserinfo(x)] for x in self.getallusers()])
    getallusersstatus = lambda self: dict([[x,self.getuserstatus(x)] for x in self.getallusers()])
    deletefriend = lambda self,id: '删除好友成功!' in self.open('im/user/deletefriendsubmit.action?touserid=%s' % id)
    addblacklist = lambda self,id: '加入黑名单成功!' in self.open('im/user/Addblacklist.action?touserid=%s' % id)
    relieveblack = lambda self,id: '对不起,操作失败,请重新访问此页面' in self.open('im/blackmanage/relieveBlack.action?touserid=%s' % id)#我也不知道为什么操作成功它提示这个。。
    changestatus = lambda self,status='0': 'success' in [self.open('im5/index/setLoginStatus.action?loginstatus='+status) for x in range(2)][1]
    #状态：在线：400 隐身：0 忙碌：600 离开：100
    __enter__ = lambda self:self
    __exit__ = __del__ = logout = lambda self,*agrs:'退出WAP飞信' in self.opener.open('http://f.10086.cn/im/index/logoutsubmit.action').read()
    
    def _login(self):
        page = self.open('/im5/login/loginHtml5.action')
        captcha = codekey.findall(page)[0]
        data = {
            'm': self.mobile,
            'pass': self.password,
            'checkCode': base64.b64decode(captcha),
            'codekey': captcha,
        }
        return '登录' in self.open('/im5/login/loginHtml5.action', data) 


    def sendBYid(self,id,message,sm=False):
        url = ('im/chat/sendMsg.action?touserid=%s' % id) if sm else ('im/chat/sendShortMsg.action?touserid=%s' % id)
        htm = self.open(url,{'msg':message,'csrfToken':self._getcsrf(id)})      
        if '对方不是您的好友' in htm: raise FetionNotYourFriend  
        return False if id is None else '成功' in htm

    def _getid(self,mobile):
        html = self.open('im/index/searchOtherInfoList.action',{'searchText':mobile})
        try: return idfinder.findall(html)[0]
        except IndexError:
            try:
                return idfinder2.findall(html)[0]
            except:
                return None
        except:
            return None
        
    def findid(self,mobile):
        if hasattr(self,'cache'):
            id = self.cache[mobile]
            if id is None: self.cache[mobile] = id = self._getid(mobile)#缓存中没有，获取ID并存入。
            return id
        return self._getid(mobile)
    
    def getuserinfo(self,id):
        url = 'im5/user/userInfo.action?touserid=%s' % id
        web = [self.open(url) for x in range(2)][1].replace('\n','').replace('\t','').replace('\r','')#不知道为什么，HTML5版的WAP飞信第一次访问总是提示正在加载。。
        infos = infofinder.findall(web)
        avatar = avatarfinder.findall(web)[0]
        if avatar.startswith('/im5'):avatar = 'http://f.10086.cn/' + avatar
        try:return {
                    'avatar'    : avatar,
                    'name'      : namefinder.findall(web)[0],
                    'localname' : infos[1],
                    'fid'       : infos[7],
                    'phone'     : infos[8],
                    'sex'       : infos[2],
                    'birthday'  : infos[3],
                    'city'      : infos[5],
                    'sign'      : infos[4],
                    'blood'     : infos[6],
                    'impresa'   : infos[0],
                    }
        except:return None
            
    def getmessage(self):
        web      = self.open('im/box/alllist.action')
        ids      = msg_re['id'].findall(web)
        names    = msg_re['name'].findall(web)
        contents = msg_re['content'].findall(web)
        return tuple([tuple([ids[i],names[i],contents[i]]) for i in range(len(ids))])
    
    def getgroups(self):
        web   = self.open('im/user/userGroupManagement.action')
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
        try: html = GzipFile(fileobj=StringIO(self.opener.open(Request('http://f.10086.cn/%s' % url,data=urlencode(data),headers={'Accept-encoding':'gzip'})).read())).read()
        except: html = self.opener.open(Request('http://f.10086.cn/%s' % url,data=urlencode(data))).read()
#        if '登录' in html and '您正在登录中国移动WAP飞信' not in html: raise FetionNotLogin
        return html
    
    def getuserstatus(self,id):
        web = self.open('im/chat/toinputMsg.action?touserid=%s' % id)
        try:return userstatus.findall(web)[0]
        except:return '已关闭服务'
   
    
    def _getcsrf(self,id=''):    
        if self.csrf is not None:
            return self.csrf
        url = ('im/chat/toinputMsg.action?touserid=%s&type=all' % id)
        htm = self.open(url)
        try:
            self.csrf = csrf_token.findall(htm)[0]
            return self.csrf
        except IndexError:            
            raise FetionCsrfTokenFail         