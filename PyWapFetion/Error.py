#coding=utf-8
class FetionNotLogin(Exception):
    pass
class FetionNotYourFriend(Exception):
    pass

def Returner(html):
    if '登陆' in html:
        raise FetionNotLogin
    elif '对方不是您的好友' in html:
        raise FetionNotYourFriend
    else:
        return '成功' in html
        
        