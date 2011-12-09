#coding=utf-8
from marshal import dump,load
from hashlib import md5 as GETMD5
md5 = lambda x:GETMD5(x).hexdigest()
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
            
    __getitem__ = get  = lambda self,k:self.dict.get(k) if k.isdigit() else self.dict.get(md5(k))
    __setitem__        = lambda self,k,id:self.dict.__setitem__(k,id) if k.isdigit() else self.dict.__setitem__(md5(k),id)
    __delitem__ = pop  = lambda self,k:self.dict.pop(k,None) if k.isdigit() else self.dict.pop(md5(k),None)
    __del__     = save = lambda self:dump(self.dict,open(self.path,'wb'))    
