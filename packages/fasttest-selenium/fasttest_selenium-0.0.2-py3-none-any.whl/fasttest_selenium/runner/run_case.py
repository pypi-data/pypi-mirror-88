from fasttest_selenium.common import Var
from fasttest_selenium.runner.test_case import TestCase
from fasttest_selenium.drivers.driver_base import DriverBase
from fasttest_selenium.runner.case_analysis import CaseAnalysis


class RunCase(TestCase):

    def setUp(self):
        if self.skip:
            self.skipTest('skip')
        if Var.isReset:
            DriverBase.createSession()

    def testCase(self):
        case = CaseAnalysis()
        case.iteration(self.steps)

    def tearDown(self):
        if Var.isReset:
            DriverBase.quit()
