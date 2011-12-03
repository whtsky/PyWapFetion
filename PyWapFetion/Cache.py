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
            
    def get(self,phone):#从字典中取飞信ID，成功返回ID，失败返回None
        try:
            return self.dict[phone]
        except:
            return None
            
    put = lambda self,phone,id:self.dict[phone] = id#将ID存入字典
        
    def save(self):#将字典保存到文件
        f = open(self.path,'wb')
        dump(self.dict,f)
        f.close()
        del f
        
    def exit(self):
        self.save()
        del self.path,self.dict
