#coding=utf-8
from marshal import dump,load
class Cache(object):
    def __init__(self,path):
        self.path = path
        try:
            f = open(path,'rb')
        except:
            self.dict={}
        else:
            self.dict = load(f)
            f.close()
            del f
            
    __getitem__ = get  = lambda self,k:self.dict.get(k)
    __setitem__        = lambda self,k,id:self.dict.__setitem__(k,id)
    __delitem__ = pop  = lambda self,k:self.dict.pop(k,None)
    __del__     = save = lambda self:dump(self.dict,open(self.path,'wb'))    