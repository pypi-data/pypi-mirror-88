# -*- coding = UTF-8 -*-
# Autohr   : yang
# File     : cli.py
# project  : UIAutoProject
# time     : 2020/12/14 16:39
# Describe : 
# ---------------------------------------

import argparse
import os, sys
from lazyTest import __version__, __description__

PY3 = sys.version_info[0] == 3


def main():
    """
    API test: parse command line options and run commands.
    """

    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument(
        '-v', '--version', dest='version', action='store_true',
        help="show version")

    parser.add_argument(
        '--project',
        help="Create an lazyTest automation test project.")

    parser.add_argument(
        '-r',
        help="run test case")

    args = parser.parse_args()

    # 获取版本
    if args.version:
        print("version {}".format(__version__))
        return 0

    # 创建项目
    project_name = args.project
    if project_name:
        create_scaffold(project_name)
        return 0

    # 运行用例
    run_file = args.r
    if run_file:
        if PY3:
            ret = os.system("python -V")
            if ret != 0:
                os.system("python3 -V")
                command = "python3 " + run_file
            else:
                command = "python " + run_file
        else:
            raise NameError("Does not support python2")
        os.system(command)
        return 0


def create_scaffold(project_name):
    """
    create scaffold with specified project name.
    """
    if os.path.isdir(project_name):
        print("{}:Not a directory".format(project_name))
        return

    def create_folder(path):
        print("create dir:{}".format(path))
        os.makedirs(path)

    def create_file(path, file_content=""):
        print("create file:{}".format(path))
        with open(path, 'w', encoding='utf-8') as f:
            f.write(file_content)

    conftest = """
# project  :Python_project
# -*- coding = UTF-8 -*-
# Autohr   : 
# File     : conftest.py
# time     : 
# Describe :
# ---------------------------------------
import os
import sys
import time

import allure
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from lazyTest import *

globals()["driver"] = None
globals()["filepath"] = None


def getPorjectPath():
    '''
    获取项目路径
    '''
    return os.path.dirname(os.path.dirname(__file__))


def pytest_addoption(parser):
    # 添加参数到pytest.ini
    parser.addini('Terminal', help='访问浏览器参数')
    parser.addini('URL',  help='添加 url 访问地址参数')
    parser.addini('filepath', help='添加 截图路径')


@pytest.fixture(scope='session')
def getdriver(pytestconfig):
    Terminal = pytestconfig.getini("Terminal")
    URL = pytestconfig.getini("URL")
    globals()["filepath"] = pytestconfig.getini('filepath')
    driver = browser_Config(Terminal, URL)
    globals()["driver"] = driver.base_driver
    yield driver
    driver.browser_close()


@pytest.fixture(scope="function")
def flush_browser(getdriver):
    yield
    getdriver.flush_browser()
    getdriver.sleep(1)


# 用例出现异常或失败时截图
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport():
<<<<<<< HEAD
=======
    picture_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
    filename = getPorjectPath() + globals()["filepath"] + picture_time + ".png"
>>>>>>> 14ead3f648d6acda6dfa6a24bc2a4be5529989d7
    outcome = yield
    report = outcome.get_result()
    if report.when == 'call':
        xfail = hasattr(report, 'wasxfail')
<<<<<<< HEAD
        if report.failed and not xfail:
            picture_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
            filename = getPorjectPath() + globals()["filepath"] + picture_time + ".png"
=======
        if (report.skipped and xfail) or (report.failed and not xfail):
>>>>>>> 14ead3f648d6acda6dfa6a24bc2a4be5529989d7
            globals()["driver"].save_screenshot(filename)
            with open(filename, "rb") as f:
                file = f.read()
                allure.attach(file, "失败截图", allure.attachment_type.PNG)

    """

    pytest = """
[pytest]
Terminal = Chrome
URL = https://www.baidu.com
filepath = /result/screenshot/
    """

    main = """
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
<<<<<<< HEAD
from lazyTest import ClearTestResult
=======
from lazy import ClearTestResult
>>>>>>> 14ead3f648d6acda6dfa6a24bc2a4be5529989d7


def getPorjectPath():
    '''
    获取项目路径
    '''
    return os.path.dirname(os.path.dirname(__file__))


def clearLogAndReport():
    print("----------清空上次测试结果----------")
    path = getPorjectPath() + "/result"
    ClearTestResult(path)
    time.sleep(2)
    print("----------测试结果清空成功----------")


def runlastFailed():
    print("启动失败用例重跑")
    cmd = "pytest -s --lf " + getPorjectPath() + "/case/  --alluredir " + getPorjectPath() + "/result/report"
    print(os.system(cmd))


def startReport():
    print("-------------启动测试报告--------------")
    startReport = "allure serve " + getPorjectPath() + "/result/report"
    print(os.system(startReport))


def startCase(cases):
    print("------------开始执行测试------------")
    cmd = "pytest -s " + getPorjectPath() + "/case/" + cases + " --alluredir " + getPorjectPath() + "/result/report"
    print(os.system(cmd))


def run(cases=" "):
    '''运行case中所有用例'''
    # clearLogAndReport()
    startCase(cases)
    s = input("请选择要启用的服务:1:启动失败用例重跑;\t2：启动测试报告;")
    if s == "1":
        runlastFailed()
        s = input("是否启动测试报告:y/n")
    if s == "2" or s == "y":
        startReport()


run()
    """

    create_folder(project_name)  # 创建项目目录
    # 创建目录结构
    create_folder(os.path.join(project_name, "page"))
    create_folder(os.path.join(project_name, "service"))
    create_folder(os.path.join(project_name, "case"))
    create_folder(os.path.join(project_name, "main"))
    create_folder(os.path.join(project_name, "result"))
    create_folder(os.path.join(project_name, "result", "log"))
    create_folder(os.path.join(project_name, "result", "report"))
    create_folder(os.path.join(project_name, "result", "screenshot"))
    create_folder(os.path.join(project_name, "resources"))
    create_folder(os.path.join(project_name, "resources", "elementSource"))
    # 创建核心文件
    create_file(os.path.join(project_name, "__init__.py"))
    create_file(os.path.join(project_name, "case", "conftest.py"), conftest)
    create_file(os.path.join(project_name, "pytest.ini"), pytest)
    create_file(os.path.join(project_name, "main", "main.py"), main)


if __name__ == '__main__':
    main()

