import unittest
from appium import webdriver

from CATP.CaseSuite.blogLogin import *
from CATP.CaseSuite.moblieLogin import *
from CATP.CaseSuite.phoneRegedit import *
from CATP.CaseSuite.tencentLogin import *
from CATP.CaseSuite.weichatLogin import *

class CodoonAutomatedTestingPlan(unittest.TestCase):

    @classmethod
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['deviceName'] = 'Android Mechine'
        desired_caps['appPackage'] = 'com.codoon.gps'
        desired_caps['appActivity'] = '.ui.login.WelcomeActivity'
        desired_caps['unicodeKeyboard'] = True
        desired_caps['resetKeyboard'] = True
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        time.sleep(10)

    @classmethod
    def tearDown(self):
        self.driver.close_app()
        self.driver.quit()

    def testone(self):
        MobileLoginTestcase().Mobile(self.driver)

    def testtwo(self):
        WeichatLoginTestcase().Weichat(self.driver)

    def testthree(self):
        TencentLoginTestcase().Tencent(self.driver)

    def testfour(self):
        BlogLoginTestcase().Blog(self.driver)

    def testfive(self):
        RegeditLogin().Regedit(self.driver)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(CodoonAutomatedTestingPlan("testone"))
    suite.addTest(CodoonAutomatedTestingPlan("testtwo"))
    suite.addTest(CodoonAutomatedTestingPlan("testthree"))
    suite.addTest(CodoonAutomatedTestingPlan("testfour"))

    runner = unittest.TextTestRunner()
    runner.run(suite)