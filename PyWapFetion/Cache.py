#coding=utf-8
from marshal import dump,load
class Cache:
    def __init__(self,path):
        self.path = path
        try:
            f = open(path,'rb')
            self.dict = load(f)
            f.close()
            del f
        except:
            self.dict={}
            
    def get(self,phone):
        #从字典中取飞信ID，成功返回ID，失败返回None
        try:
            return self.dict[phone]
        except:
            return None
            
    def put(self,phone,id):
        #将ID存入字典
        self.dict[phone] = id
        try:
            return id is self.dict[phone]
        except:
            return False
        
    def rm(self,phone):
        #从字典中删除ID
        try:
            self.dict.pop[phone]
        except:
            #如字典中没有本ID则返回False
            return False
        return True
        
    def save(self):
        f = open(self.path,'wb')
        #将字典保存到文件
        try:
            dump(self.dict,f)
        except:
            return False
        f.close()
        del f
        return True
        
    def exit(self):
        self.save()
        del self.path
        del self.dict