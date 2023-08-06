# -*- coding = UTF-8 -*-
# Autohr   : yang
# File     : file.py
# project  : Python_project
# time     : 2020/11/16 16:55
# Describe : 资源文件的操作
# ---------------------------------------
import configparser
import csv
import json
import sys
from ruamel import yaml


class FileOperation:
    def __init__(self, filePath):
        self.filePath = filePath

    def readFileToDict(self): ...

    def readFileToList(self): ...


class YamlOperation(FileOperation):

    def readFileToDict(self):
        """读取yaml文件"""
        with open(self.filePath, 'r', encoding='UTF-8')as fp:
            yaml_data = yaml.safe_load(fp)
        return yaml_data

    @staticmethod
    def writeFileToDict(realFile, data):
        """写入yaml文件"""
        with open(realFile, "w", encoding="utf-8") as f:
            yaml.round_trip_dump(data, f, Dumper=yaml.RoundTripDumper, default_flow_style=False)


class IniFileOperation(FileOperation):

    def readFileToDict(self):
        """读取ini文件"""
        config = configparser.ConfigParser()
        config.read(self.filePath)
        return config


class JsonFileOperation(FileOperation):

    def readFileToDict(self):
        """读取json文件"""
        with open(self.filePath, 'r', encoding='utf8')as fp:
            json_data = json.load(fp)
        return json_data

    @staticmethod
    def writeFileToDict(realFile, data):
        """将字典格式数据写入到Json文件"""
        with open(realFile, 'w', encoding='utf8')as fp:
            json.dump(data, fp, ensure_ascii=False)


class Csv_File_Operation(FileOperation):

    def readFileToList(self):
        """读取CSV文件,参数化使用"""
        with open(self.filePath, 'r', encoding='utf8')as fp:
            data_list = [i for i in csv.reader(fp)]
        if len(data_list[0]) == 1:
            data_list.pop(0)  # 去首行
            return [i[0] for i in data_list]
        else:
            data_list.pop(0)  # 去首行

        return data_list
