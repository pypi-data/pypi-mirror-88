# -*- coding = UTF-8 -*-
# Autohr   : yang
# File     : page.py
# project  : McenterSystem
# time     : 2020/12/3 11:56
# Describe :
# ---------------------------------------
import sys
import inspect

from lazyTest import *


class Page(object):
    module = sys._getframe().f_code.co_name

    filePath = r"/resources/elementSource/"

    suffix = ".yaml"

    logPath = "/result/log/"

    logName = "log.log"

    def getPorjectPath(self):
        ...

    def __init__(self, base_driver: browser_Config) -> None:
        self.base_driver = base_driver
        self.log = GetLogger(self.getPorjectPath() + self.logPath + self.logName).logger
        self.selector = readElementSource(
            self.getPorjectPath() + self.filePath + self.module + self.suffix).readFileToDict()

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
        for i in methods:
            func = getattr(cls, i)
            params = list(inspect.getfullargspec(func))[0]
            if params.count('self') > 0:
                params.remove("self")
            key[i] = params
        writeElementKey(cls.getPorjectPath(cls) + cls.filePath, cls.module, cls.suffix, key)
