#coding=utf-8
from marshal import dump,load
class Cache:
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
            
    get  = lambda self,phone:self.dict.get(phone)
    put  = lambda self,phone,id:self.dict.setdefault(phone,id)#将ID存入字典
    save = lambda self:dump(self.dict,open(self.path,'wb'))    
