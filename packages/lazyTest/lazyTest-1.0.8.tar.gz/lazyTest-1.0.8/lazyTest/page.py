# -*- coding = UTF-8 -*-
# Autohr   : yang
# File     : page.py
# project  : McenterSystem
# time     : 2020/12/3 11:56
# Describe :
# ---------------------------------------
import allure, sys, os
import inspect

from lazyTest import *


class Page(object):
    filePath = r"/resources/element/"

    suffix = ".yaml"

    logPath = "/result/log/"

    logName = "log.log"

    def getPorjectPath(self): ...

    @classmethod
    def getClassName(cls):
        return cls.__name__

    def __init__(self, base_driver: browser_Config) -> None:
        self.base_driver = base_driver
        self.log = GetLogger(self.getPorjectPath() + self.logPath + self.logName).logger
        self.log.info("元素文件: -> %s" % self.getPorjectPath() + self.filePath + self.getClassName() + self.suffix)
        self.selector = readElementSource(
            self.getPorjectPath() + self.filePath + self.getClassName() + self.suffix).readFileToDict()

    @classmethod
    def writeKey(cls):
        '''
        自动创建yaml资源文件
        :param filepath: 从项目路径下开始指定目录
        :param fileType: 默认yaml文件格式
        :return:
        '''
        key = {}
        methods = list(
            filter(lambda m: not m.startswith("__") and not m.endswith("__") and callable(getattr(cls, m)), dir(cls)))
        methods.pop(methods.index("writeKey"))
        methods.pop(methods.index("getPorjectPath"))
        methods.pop(methods.index("getClassName"))
        for i in methods:
            func = getattr(cls, i)
            doc = func.__doc__
            key[i] = doc
        writeElementKey(cls.getPorjectPath(cls) + cls.filePath, cls.getClassName(), cls.suffix, key)

# if __name__ == '__main__':
#     print(Page.getClassName())
