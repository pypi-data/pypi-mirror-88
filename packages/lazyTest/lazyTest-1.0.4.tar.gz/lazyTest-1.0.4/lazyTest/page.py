# -*- coding = UTF-8 -*-
# Autohr   : buxiubuzhi
# File     : page.py
# project  : McenterSystem
# time     : 2020/12/3 11:56
# Describe :
# ---------------------------------------
import allure, sys
import inspect

from lazyTest import *


class Page:
    module = "conf"

    def __init__(self, base_driver: browser_Config) -> None:
        self.base_driver = base_driver
        self.data = IniFileOperation.read_Ini()
        self.log = GetLogger(self.data[self.module]['log']).logger
        self.selector = readElementSource(self.data[self.module]['source']).readFileToDict()

    @classmethod
    def getPorjectPath(cls):
        """
        获取项目路径
        """
        return sys.path[0][:sys.path[0].index('\page')]

    @classmethod
    def writeKey(cls, filepath, fileType='yaml'):
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
        writeElementKey(cls.getPorjectPath() + filepath, cls.module, fileType, key)
