#coding=utf-8
from threading import Thread
from time import sleep

__all__ = ['AliveKeeper']


class AliveKeeper(Thread):
    def __init__(self, fetion, sleeptime=240, Daemon=True, start=True):
        self.fetion = fetion
        super(Thread, self).__init__()
        self.sleeptime = sleeptime
        self.setDaemon(Daemon)
        if start:
            self.start()

    def run(self):
        while '登陆' not in self.fetion.open('im/index/indexcenter.action'):
            sleep(self.sleeptime)
