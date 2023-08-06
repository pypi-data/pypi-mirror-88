#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from selenium import webdriver
from fasttest_selenium.common import *


class ServerUtils(object):

    def __getattr__(self, item):
        try:
            return self.__getattribute__(item)
        except:
            return None

    def __init__(self, browser, browser_config, implicitly_wait, max_window):
        self.browser = browser
        self.instance = None
        self.browser_config = browser_config
        if implicitly_wait is None :
            implicitly_wait = 5
        self.implicitly_wait = implicitly_wait
        if max_window is None:
            max_window = False
        self.max_window = max_window

    def start_server(self):

        try:
            path = None
            if self.browser_config:
                if 'path' in self.browser_config.keys():
                    path = self.browser_config['path']
                    if not os.path.isfile(path):
                        log_error(' No such file : {}'.format(path), False)
                        path = None
            if self.browser.lower() == 'chrome':
                if path:
                    self.instance = webdriver.Chrome(path)
                else:
                    self.instance = webdriver.Chrome()
            elif self.browser.lower() == 'firefox':
                self.instance = webdriver.Firefox()
            elif self.browser.lower() == 'edge':
                self.instance = webdriver.Edge()
            elif self.browser.lower() == 'safari':
                self.instance = webdriver.Safari()
            elif self.browser.lower() == 'ie':
                self.instance = webdriver.Ie()
            elif self.browser.lower() == 'opera':
                self.instance = webdriver.Opera()
            elif self.browser.lower() == 'phantomjs':
                self.instance = webdriver.PhantomJS()

            self.instance.implicitly_wait(self.implicitly_wait)
            if self.max_window:
                self.instance.maximize_window()
            return self.instance
        except Exception as e:
            raise e

    def stop_server(self, instance):

        try:
            instance.quit()
        except Exception as e:
            raise e

