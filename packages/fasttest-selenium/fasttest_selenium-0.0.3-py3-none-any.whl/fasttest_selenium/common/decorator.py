#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import cv2
import sys
import time
import traceback
import threading
from macaca.webdriver import WebElement
from fasttest_selenium.common import *

def mach_keywords(func, *args, **kwds):
    def wrapper(*args, **kwds):
        start_time = time.time()
        result = None
        try:
            if args or kwds:
                result = func(*args, **kwds)
            else:
                result = func()
        except Exception as e:
            Var.case_snapshot_index += 1
            Var.exception_flag = False
            snapshot_index = Var.case_snapshot_index
            imagename = "Step_{}.png".format(snapshot_index)
            file = os.path.join(Var.snapshot_dir, imagename)
            action_step = args[1]
            style = args[-1]
            try:
                Var.instance.save_screenshot(file)
            except:
                log_error(' screenshot failed!', False)

            stop_time = time.time()
            duration = str('%.2f' % (stop_time - start_time))

            # call action中某一语句抛出异常，会导致call action状态也是false,需要处理
            result_exception_flag = False
            if Var.exception_flag:
                result_exception_flag = True

            result_step = '{}|:|{}|:|{}s|:|{}|:|{}\n'.format(snapshot_index, result_exception_flag, duration,
                                                             imagename, f'{style}- {action_step}')
            with open(os.path.join(Var.snapshot_dir, 'result.log'), 'a') as f:
                f.write(result_step)

            raise e

        return result
    return wrapper

def executor_keywords(func, *args, **kwds):
    def wrapper(*args, **kwds):
        result = None
        exception_flag = False
        exception = None
        Var.ocrimg = None
        start_time = time.time()
        Var.case_snapshot_index += 1
        Var.exception_flag = False
        snapshot_index = Var.case_snapshot_index
        imagename = "Step_{}.png".format(snapshot_index)
        file = os.path.join(Var.snapshot_dir, imagename)
        action_step = args[-2].step
        action_tag = args[-2].tag
        style = args[-1]
        try:
            if args or kwds:
                result = func(*args, **kwds)
            else:
                result = func()
        except Exception as e:
            exception = e
            exception_flag = True
        finally:
            try:
                if Var.ocrimg is not None:
                    # matchImage，绘制图片
                    cv2.imwrite(file, Var.ocrimg)
                    Var.ocrimg = None
                elif Var.saveScreenshot:
                    # 全局参数
                    Var.instance.save_screenshot(file)
                elif not Var.exception_flag and exception_flag:
                    # call出现异常
                    Var.instance.save_screenshot(file)
            except:
                Var.ocrimg = None
                log_error(' screenshot failed!', False)

            stop_time = time.time()
            duration = str('%.2f' % (stop_time - start_time))
            # 获取变量值后需要替换掉原数据
            if action_tag == 'getVar':
                step_ = action_step.split('=', 1)
                result = f'{result}'.replace("<", "{").replace(">", "}")
                if step_[-1].startswith(' '):
                    action_step = f'{step_[0]}= {result}'
                else:
                    action_step = f'{step_[0]}={result}'
                result = None

            # call action中某一语句抛出异常，会导致call action状态也是false,需要处理
            result_exception_flag = not exception_flag
            if Var.exception_flag:
                result_exception_flag = True

            if result is not None:
                # if while 等需要把结果放在语句后面
                result_step = '{}|:|{}|:|{}s|:|{}|:|{}: --> {}'.format(snapshot_index, result_exception_flag,
                                                                         duration,
                                                                         imagename, f'{style}- {action_step}', result)
            else:
                result_step = '{}|:|{}|:|{}s|:|{}|:|{}'.format(snapshot_index, result_exception_flag, duration,
                                                                 imagename, f'{style}- {action_step}')
            result_step = '{}\n'.format(result_step.replace('\n', ''))
            with open(os.path.join(Var.snapshot_dir, 'result.log'), 'a') as f:
                f.write(result_step)

            if exception_flag:
                raise exception
        return result
    return wrapper