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
            
    __getitem__ = get        = lambda self,phone:self.dict.get(phone)
    __setitem__ = setdefault = lambda self,phone,id:self.dict.setdefault(phone,id)
    __delitem__ = pop        = lambda self,k:self.dict.pop(k,None)
    __del__     = save       = lambda self:dump(self.dict,open(self.path,'wb'))    
