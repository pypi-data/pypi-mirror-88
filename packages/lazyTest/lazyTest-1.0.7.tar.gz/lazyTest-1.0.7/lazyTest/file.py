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
            yaml.dump(data, f, Dumper=yaml.RoundTripDumper)


class IniFileOperation(FileOperation):

    @staticmethod
    def read_Ini():
        """读取ini配置文件"""
        Ini_Path = sys.path[-1] + r"\resources\conf\config.ini"
        config = configparser.ConfigParser()
        config.read(Ini_Path)
        return config

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


class Csv_File_Operation(FileOperation):

    def readFileToList(self):
        """读取CSV文件"""
        with open(self.filePath, 'r', encoding='utf8')as fp:
            data_list = [i for i in csv.reader(fp)]
        return data_list
