#coding=utf-8
from setuptools import setup
import PyWapFetion

setup(
name = PyWapFetion.__name__,
version = PyWapFetion.__version__,

packages = ['PyWapFetion'],
keywords = 'library mobile fetion',
author = PyWapFetion.__author__,
author_email = 'whtsky@vip.qq.com',

url = PyWapFetion.__website__,
description = 'A simple python lib for WapFetion',
long_description = '''
PyWapFetion is a SDK of WapFetion for Python.

Fetion is a popular IM made by China Mobile.It can send short message to your friends with no cost.
You can send a short message to your mobile phone with no cost,too.And it supports to send TIMING message.
If you want to send Fetion message quickly and easily,PyWapFetion is your BEST choice.

Get to https://github.com/whtsky/PyWapFetion for more information.

* Cache support
* Auto keep alive support
* Quick Send support:send a message in one line.(See example.py)
* Easy to use
* You can receive your messages!
* Throw Exception smartly
* Get user list and group list easily
* Get a friend's info easily
* NO CAPTCHA during using it
* Supports Python 2.5 - 2.7
* You can use 2to3 to make it support Python 3
* MIT LICENSE

THIS IS A THRID PARTY SDK,USE AT YOUR RISK.
''',
license = PyWapFetion.__license__,
classifiers = [
'Development Status :: 4 - Beta',
'Environment :: Console',
'Intended Audience :: Developers',
'License :: OSI Approved :: MIT License',
'Natural Language :: English',
'Natural Language :: Chinese (Simplified)',
'Operating System :: OS Independent',
'Programming Language :: Python :: 2',
'Programming Language :: Python :: 2.5',
'Programming Language :: Python :: 2.6',
'Programming Language :: Python :: 2.7',
'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
'Topic :: Utilities',
'Topic :: Software Development :: Libraries :: Python Modules',
],
zip_safe = True,
)

