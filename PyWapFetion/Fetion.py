#coding=utf-8
from cookielib import CookieJar as _CookieJar
from urllib2 import Request, build_opener, HTTPHandler, HTTPCookieProcessor
from urllib import urlencode
import base64
from Errors import *
from re import compile
from Cache import Cache
from gzip import GzipFile
from pickle import dump, load
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

idfinder = compile('touserid=(\d*)')
idfinder2 = compile('name="internalid" value="(\d+)"')
csrf_token = compile('<postfield name="csrfToken" value="(\w+)"/>')
codekey = compile('<img src="/im5/systemimage/verifycode(.*?).jpeg" alt="f" />')

__all__ = ['Fetion']


class CookieJar(_CookieJar):
    """http://stackoverflow.com/questions/1023224/how-to-pickle-a-cookiejar"""
    def __getstate__(self):
        state = self.__dict__.copy()
        del state['_cookies_lock']
        return state

    def __setstate__(self, state):
        self.__dict__ = state
        self._cookies_lock = threading.RLock()


class Fetion(object):
    def __init__(self, mobile, password=None, status='0',
        cachefile='Fetion.cache', cookiesfile=''):
        '''登录状态：
        在线：400 隐身：0 忙碌：600 离开：100
        '''
        if cachefile:
            self.cache = Cache(cachefile)

        if not cookiesfile:
            cookiesfile = '%s.cookies' % mobile
            
        try:
            with open(cookiesfile, 'rb') as f:
                cookie_processor = load(f)
        except:
            cookie_processor = HTTPCookieProcessor(CookieJar())
                        
        self.opener = build_opener(cookie_processor,
            HTTPHandler)
        self.mobile, self.password = mobile, password
        if not self.alive():
            self._login()
        dump(cookie_processor, open(cookiesfile, 'wb'))
        self.changestatus(status)

    def send2self(self, message, time=None):
        if time:
            htm = self.open('im/user/sendTimingMsgToMyselfs.action',
                {'msg': message, 'timing': time})
        else:
            htm = self.open('im/user/sendMsgToMyselfs.action',
                {'msg': message})
        return '成功' in htm

    def send(self, mobile, message, sm=False):
        if mobile == self.mobile:
            return self.send2self(message)
        return self.sendBYid(self.findid(mobile), message, sm)

    def addfriend(self, mobile, name='xx'):
        htm = self.open('im/user/insertfriendsubmit.action',
            {'nickname': name, 'number': phone, 'type': '0'})
        return '成功' in htm

    def alive(self):
        return '心情' in self.open('im/index/indexcenter.action')

    def deletefriend(self, id):
        htm = self.open('im/user/deletefriendsubmit.action?touserid=%s' % id)
        return '删除好友成功!' in htm

    def changestatus(self, status='0'):
        url = 'im5/index/setLoginStatus.action?loginstatus=' + status
        for x in range(2):
            htm = self.open(url)
        return 'success' in htm

    def logout(self, *args):
        self.opener.open('http://f.10086.cn/im/index/logoutsubmit.action')

    __enter__ = lambda self: self
    __exit__ = __del__ = logout

    def _login(self):
        htm = ''
        data = {
            'm': self.mobile,
            'pass': self.password,
        }
        while '图形验证码错误' in htm or not htm:
            page = self.open('/im5/login/loginHtml5.action')
            captcha = codekey.findall(page)[0]
            img = self.open('/im5/systemimage/verifycode%s.jpeg' % captcha)
            open('verifycode.jpeg', 'w').write(img)
            captchacode = raw_input('captchaCode:')
            data['captchaCode'] = captchacode
            htm = self.open('/im5/login/loginHtml5.action', data)
        self.alive()
        return '登录' in htm

    def sendBYid(self, id, message, sm=False):
        url = 'im/chat/sendShortMsg.action?touserid=%s' % id
        if sm:
            url = 'im/chat/sendMsg.action?touserid=%s' % id
        htm = self.open(url,
            {'msg': message, 'csrfToken': self._getcsrf(id)})
        if '对方不是您的好友' in htm:
            raise FetionNotYourFriend
        return '成功' in htm

    def _getid(self, mobile):
        htm = self.open('im/index/searchOtherInfoList.action',
            {'searchText': mobile})
        try:
            return idfinder.findall(htm)[0]
        except IndexError:
            try:
                return idfinder2.findall(htm)[0]
            except:
                return None
        except:
            return None

    def findid(self, mobile):
        if hasattr(self, 'cache'):
            id = self.cache[mobile]
            if not id:
                self.cache[mobile] = id = self._getid(mobile)
            return id
        return self._getid(mobile)

    def open(self, url, data=''):
        request = Request('http://f.10086.cn/%s' % url, data=urlencode(data))
        htm = self.opener.open(request).read()
        try:
            htm = GzipFile(fileobj=StringIO(htm)).read()
        finally:
            return htm

    def _getcsrf(self, id=''):
        if hasattr(self, 'csrf'):
            return self.csrf
        url = ('im/chat/toinputMsg.action?touserid=%s&type=all' % id)
        htm = self.open(url)
        try:
            self.csrf = csrf_token.findall(htm)[0]
            return self.csrf
        except IndexError:
            print htm
            raise FetionCsrfTokenFail
