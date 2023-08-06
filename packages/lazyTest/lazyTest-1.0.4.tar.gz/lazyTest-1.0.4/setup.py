# project  :lazyTest
# -*- coding = UTF-8 -*-
# Autohr   :buxiubuzhi
# File     :setup.py
# time     :2020/12/13  19:50
# Describe :
# ---------------------------------------

from setuptools import setup, find_packages

setup(
    name = "lazyTest",      #这里是pip项目发布的名称
    version = "1.0.4",  #版本号，数值大的会优先被pip
    keywords = ("pip", "lazyTest"),
    description = "自动化测试框架",
    long_description = "一个基于pytest + selenium + allure 的自动化测试框架",

    url = "https://github.com/xingheyang/lazyTest.git",     #项目相关文件地址，一般是github
    author = "buxiubuzhi",
    author_email = "xingheyang_99@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["pytest","selenium","allure-pytest","ruamel.yaml"]          #这个项目需要的第三方库
)