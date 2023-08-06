#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from fasttest_selenium.runner.action_analysis import ActionAnalysis

class CaseAnalysis(object):

    def __init__(self):
        self.action_nalysis = ActionAnalysis()
        self.testcase_steps = []

    def iteration(self, steps, style='', common={}, iterating_var=None):
        '''

        @param steps:
        @param style: 控制结果报告中每句case的缩进
        @param common: call 调用时需要的参数
        @param iterating_var: for 迭代对象
        @return:
        '''
        if isinstance(steps, list):
            for step in steps:
                if isinstance(step, str):
                    self.case_executor(step, style, common, iterating_var)
                    if step.startswith('break'):
                        return 'break'
                elif isinstance(step, dict):
                    result = self.iteration(step, style, common, iterating_var)
                    if result == 'break':
                        return 'break'
        elif isinstance(steps, dict):
            for key, values in steps.items():
                if key.startswith('while'):
                    while self.case_executor(key, style, common, iterating_var):
                        result = self.iteration(values, f'{style}  ', common, iterating_var)
                        if result == 'break':
                            break
                elif key.startswith('if') or key.startswith('elif') or key.startswith('else'):
                    if self.case_executor(key, style, common, iterating_var):
                        result = self.iteration(values, f'{style}  ', common, iterating_var)
                        if result == 'break':
                            return 'break'
                        break # 判断下执行完毕，跳出循环
                elif re.match('for\s+(\$\{\w+\})\s+in\s+(\S+)', key):
                    parms = self.case_executor(key, style, common, iterating_var)
                    for f in parms['value']:
                        iterating_var = {parms['key']: f}
                        result = self.iteration(values, f'{style}  ', common, iterating_var)
                        if result == 'break':
                            break
                else:
                    raise SyntaxError('- {}:'.format(key))

    def case_executor(self, step, style, common, iterating_var):
        result = self.action_nalysis.action_analysis(step, style, common, iterating_var)
        return result