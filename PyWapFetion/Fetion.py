#coding=utf-8

import os
from PyWapFetion.Errors import *
from re import compile
from PyWapFetion.Cache import Cache
from gzip import GzipFile

try:
    from http.cookiejar import MozillaCookieJar
    from urllib.request import Request, build_opener
    from urllib.request import HTTPHandler, HTTPCookieProcessor
    from urllib.parse import urlencode
    from io import StringIO
except ImportError:
    # Python 2
    input = raw_input
    from cookielib import MozillaCookieJar
    from urllib2 import Request, build_opener, HTTPHandler, HTTPCookieProcessor
    from urllib import urlencode

    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO
    IS_PY2 = True
else:
    IS_PY2 = False

idfinder = compile('touserid=(\d*)')
idfinder2 = compile('name="internalid" value="(\d+)"')
csrf_token = compile('<postfield name="csrfToken" value="(\w+)"/>')
codekey = compile('<img src="/im5/systemimage/verifycode(.*?).jpeg"')

__all__ = ['Fetion']


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

        cookiejar = MozillaCookieJar(filename=cookiesfile)
        if not os.path.isfile(cookiesfile):
            open(cookiesfile, 'w').write(MozillaCookieJar.header)

        cookiejar.load(filename=cookiesfile)

        cookie_processor = HTTPCookieProcessor(cookiejar)

        self.opener = build_opener(cookie_processor,
                                   HTTPHandler)
        self.mobile, self.password = mobile, password
        if not self.alive():
            self._login()
            cookiejar.save()

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
                        {'nickname': name, 'number': mobile, 'type': '0'})
        return '成功' in htm

    def alive(self):
        htm = self.open('im/index/indexcenter.action')
        return '心情' in htm or '正在登陆' in htm

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
            matches = codekey.findall(page)
            if matches:
                captcha = matches[0]
                img = self.open('/im5/systemimage/verifycode%s.jpeg' % captcha)
                open('verifycode.jpeg', 'wb').write(img)
                captchacode = input('captchaCode:')
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
        data = urlencode(data)
        if not IS_PY2:
            data = data.encode()

        request = Request('http://f.10086.cn/%s' % url, data=data)
        htm = self.opener.open(request).read()
        try:
            htm = GzipFile(fileobj=StringIO(htm)).read()
        finally:
            if IS_PY2:
                return htm
            else:
                return htm.decode()

    def _getcsrf(self, id=''):
        if hasattr(self, 'csrf'):
            return self.csrf
        url = ('im/chat/toinputMsg.action?touserid=%s&type=all' % id)
        htm = self.open(url)
        try:
            self.csrf = csrf_token.findall(htm)[0]
            return self.csrf
        except IndexError:
            print(htm)
            raise FetionCsrfTokenFail
