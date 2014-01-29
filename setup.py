#coding=utf-8

import os
import codecs

from setuptools import setup
import PyWapFetion

readme = os.path.join(os.path.dirname(__file__), "README.md")

setup(
    name=PyWapFetion.__name__,
    version=PyWapFetion.__version__,
    packages=['PyWapFetion'],
    keywords='library mobile fetion',
    author=PyWapFetion.__author__,
    author_email='whtsky@gmail.com',

    url=PyWapFetion.__website__,
    description='A simple python lib for WapFetion',
    long_description=codecs.open(readme, encoding='utf8').read(),
    license=PyWapFetion.__license__,
    classifiers=[
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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    zip_safe=False,
)
