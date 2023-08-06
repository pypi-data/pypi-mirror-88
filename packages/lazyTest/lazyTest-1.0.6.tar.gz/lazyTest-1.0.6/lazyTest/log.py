# -*- coding = UTF-8 -*-
# Autohr   : yang
# File     : log.py
# project  : Python_project
# time     : 2020/11/16 16:57
# Describe : 日志的操作
# ---------------------------------------

import logging

import sys


class GetLogger:

    def __init__(self, log_path):
        """
        :param log_path: 日志文件的路径
        """
        self.file_name = log_path
        self.logger = logging.getLogger(__name__)
        logging.Logger.manager.loggerDict.pop(__name__)
        # 设置日志等级
        self.logger.setLevel(logging.INFO)
        # 设置日志的输出格式
        self.formatter = logging.Formatter('%(levelname)s %(asctime)s %(module)s[line:%(lineno)d] -- %(message)s')
        # 创建FileHandler对象，将日志写入到文件,a指追加日志到文件末尾
        self.fh = logging.FileHandler(self.file_name, mode='a', encoding='utf8')
        # 设置文件日志的等级
        self.fh.setLevel(logging.INFO)
        # 设置日志的格式与内容
        self.fh.setFormatter(self.formatter)
        # 添加内容到日志文件
        self.logger.addHandler(self.fh)
        # 创建StreamHandler对象，用于输出日志到控制台
        sh = logging.StreamHandler(sys.stdout)
        # 设置控制台输出的日志等级
        sh.setLevel(logging.INFO)
        # 设置控制台输出日志的内容格式
        sh.setFormatter(self.formatter)
        # 添加内容到控制台
        self.logger.addHandler(sh)


    def close_handle(self):
        self.logger.removeHandler(self.fh)
        self.fh.close()

