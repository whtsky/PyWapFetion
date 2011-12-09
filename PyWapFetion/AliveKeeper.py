#coding=utf-8
from threading import Thread
from time import sleep
class AliveKeeper(Thread):
    def __init__(self,Opener,sleeptime=240,Daemon=True,start=True):#默认每480秒登陆一次
        self.Opener = Opener
        Thread.__init__(self, name = 'AliveKeeper')
        self.on = True
        self.sleeptime = sleeptime
        self.setDaemon(Daemon)
        if start: self.start()
            
    def run(self): 
        while self.on and '登陆' is not in self.Opener.open('http://f.10086.cn/im/index/indexcenter.action').read():sleep(self.sleeptime)
            
    stop = lambda self:self.on = False
