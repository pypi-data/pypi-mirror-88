#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import inspect
import unittest
from fasttest_selenium.common import *
from fasttest_selenium.utils import *
from fasttest_selenium.keywords import keywords
from fasttest_selenium.runner.run_case import RunCase
from fasttest_selenium.common.logging import log_init
from fasttest_selenium.drivers.driver_base import DriverBase
from fasttest_selenium.result.test_runner import TestRunner

class Project(object):

    def __init__(self):

        self.__init_project()
        self.__init_config()
        self.__init_logging()
        self.__analytical_testcase_file()
        self.__analytical_common_file()
        self.__init_data()
        self.__init_keywords()
        self.__init_images()
        self.__init_testcase_suite()

    def __init_project(self):

        for path in [path  for path in inspect.stack() if str(path[1]).endswith("runtest.py")]:
            self.__ROOT = os.path.dirname(path[1])
            sys.path.append(self.__ROOT)
            sys.path.append(os.path.join(self.__ROOT, 'Scripts'))
            Var.ROOT = self.__ROOT
            Var.global_var = {} # 全局变量
            Var.extensions_var = {} # 扩展数据变量
            Var.common_var = {} # common临时变量，call执行完后重置

    def __init_config(self):

        self.__config = analytical_file(os.path.join(self.__ROOT, 'config.yaml'))
        for configK, configV in self.__config.items():
             Var[configK] = configV

        if Var.browser.lower() not in ['chrome', 'safari']:
            raise ValueError('browser parameter is illegal!')

        browser_config = None
        if 'desiredcaps' in self.__config.keys():
            desiredcaps = self.__config['desiredcaps'][0]
            if Var.browser.lower() in desiredcaps.keys():
                browser_config = Dict(desiredcaps[Var.browser.lower()][0])
        Var.browser_config = browser_config


    def __init_data(self):

        if os.path.exists(os.path.join(Var.ROOT, 'data.json')):
            with open(os.path.join(Var.ROOT, 'data.json'), 'r', encoding='utf-8') as f:
                dict = Dict(json.load(fp=f))
                if dict:
                    log_info('******************* analytical data *******************')
                for extensionsK, extensionsV in dict.items():
                    log_info(' {}: {}'.format(extensionsK, extensionsV))
                    Var.extensions_var[extensionsK] = extensionsV

    def __init_keywords(self):

        Var.default_keywords_data = keywords.return_keywords()

        if 'keywords' in  Var.extensions_var.keys():
            Var.new_keywords_data = Var.extensions_var['keywords']

    def __init_images(self):

        if Var.extensions_var and Var.extensions_var['images']:
            log_info('******************* analytical images *******************')
            images_dict = {}
            for images in Var.extensions_var['images']:
                images_file = os.path.join(Var.ROOT, 'images/{}'.format(images))
                if os.path.isfile(images_file):
                    images_dict[images] = images_file
                else:
                    raise FileNotFoundError('No such file or directory: {}'.format(images_file))
            Var.extensions_var['images_file'] = images_dict
            log_info(' {}'.format(Var.extensions_var['images_file']))

    def __init_logging(self):

        report_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        report_child = "{}_{}".format(Var.browser, report_time)
        Var.report = os.path.join(Var.ROOT, "Report", report_child)

        if not os.path.exists(Var.report):
            os.makedirs(Var.report)
            os.makedirs(os.path.join(Var.report, 'resource'))
        log_init(Var.report)

    def __analytical_testcase_file(self):

        log_info('******************* analytical config *******************')
        for configK, configV in self.__config.items():
            log_info(' {}: {}'.format(configK, configV))
        log_info('******************* analytical testcase *******************')
        testcase = TestCaseUtils()
        self.__testcase = testcase.testcase_path(Var.ROOT, Var.testcase)
        log_info(' case: {}'.format(len(self.__testcase)))
        if self.__testcase:
            for case in self.__testcase:
                log_info(' {}'.format(case))

    def __analytical_common_file(self):

        log_info('******************* analytical common *******************')
        Var.common_func = Dict()
        common_dir = os.path.join(Var.ROOT, "Common")
        for rt, dirs, files in os.walk(common_dir):
            if rt == common_dir:
                self.__load_common_func(rt, files)
            elif rt.split(os.sep)[-1].lower() == Var.platformName.lower():
                self.__load_common_func(rt, files)

    def __load_common_func(self,rt ,files):

        for f in files:
            if not f.endswith('yaml'):
                continue
            for commonK, commonV in analytical_file(os.path.join(rt, f)).items():
                Var.common_func[commonK] = commonV
                log_info(' {}: {}'.format(commonK, commonV))


    def __init_testcase_suite(self):

        self.__suite = []
        for case_path in self.__testcase:
            testcase = analytical_file(case_path)
            testcase['testcase_path'] = case_path
            Var.testcase = testcase
            subsuite = unittest.TestLoader().loadTestsFromTestCase(RunCase)
            self.__suite.append(subsuite)
            Var.testcase = None

    def start(self):
        if not Var.isReset:
            server = ServerUtils(Var.browser, Var.browser_config, Var.implicitlyWait, Var.maxWindow)
            Var.instance = server.start_server()
            DriverBase.init()

        suite = unittest.TestSuite(tuple(self.__suite))
        runner = TestRunner()
        runner.run(suite)

        if not Var.isReset:
            server.stop_server(Var.instance)
