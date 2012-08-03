#coding=utf-8
from __future__ import with_statement
from marshal import dump, load

__all__ = ['Cache']


class Cache(object):
    def __init__(self, path):
        self.path = path
        try:
            with open(path, 'rb') as f:
                self.dict = load(f)
        except:
            self.dict = {}

    __getitem__ = get = lambda self, k: self.dict.get(k)
    __setitem__ = lambda self, k, id: self.dict.__setitem__(k, id)
    __delitem__ = pop = lambda self, k: self.dict.pop(k, None)
    __del__ = save = lambda self: dump(self.dict, open(self.path, 'wb'))
