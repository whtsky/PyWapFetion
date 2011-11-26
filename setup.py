#coding=utf-8
from setuptools import setup,find_packages
import PyWapFetion

setup(
name = PyWapFetion.__name__,
version = PyWapFetion.__version__,

packages = find_packages(),
keywords = 'library mobile fetion',
author = PyWapFetion.__author__,
author_email = 'whtsky@vip.qq.com',

url = PyWapFetion.__website__,
description = 'A simple python lib for WapFetion',
long_description = '''
Fetion SDK for Python.

PyWapFetion is a useful Fetion Library for Python made by .It's very easy to use.

Go to https://github.com/whtsky/PyWapFetion for more information.

* Cache support
* Auto keep alive support
* NO CAPTCHA during using it
* Supports Python 2.5 - 2.7
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