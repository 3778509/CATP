import time
from CATP.UtilsClass.UtilsMethod import *

class TencentLoginTestcase(object):
    def __init__(self):
        self.flag = True
        self.utils = TestClassMethod()

    def Tencent(self,driver):
        while self.flag:
            if driver.current_activity == '.ui.login.ViewPage':  ##引导页##
                driver.swipe(680, 480, 80, 480)  ###从引导页滑动切换到登录前页
                if self.utils.isExistElementByid(driver,"com.codoon.gps:id/viewpage_btn_login"):
                    driver.find_element_by_xpath(
                        "//android.widget.Button[contains(@text,'进入咕咚')]").click()  ###跳转到登录页
                self.flag = False  ##置换登录Action，退出循环判断
            elif driver.current_activity == '.ui.SlideActivity':  ##已登录缓存页##
                ####弹框判断###
                while self.utils.isExistElementByid(driver, "com.codoon.gps:id/ads_content"):
                    driver.find_element_by_id("com.codoon.gps:id/btn_cancel").click()
                self.utils.logout(driver)
                time.sleep(3)  ###延迟，加载界面
                self.flag = True  ##退出之前登录，并没完成登录Action，flag标志不变
            else:  ### 剩下情况则为登录页，这种情况界面不需做任何逻辑处理
                self.flag = False  ##置换登录Action，退出循环判断
        else:  ##登录Action为Falg后，统一执行输入账号密码等后续操作
            while True:
                driver.find_element_by_id("com.codoon.gps:id/ll_login_qq").click()
                time.sleep(3)  ###延迟，加载界面
                if driver.is_app_installed("com.tencent.mobileqq"):
                    break
                else:
                    assert (self.utils.isExistElementByxpath(driver, "您尚未安装QQ,请安装后重试!"))
                    driver.find_element_by_id("com.codoon.gps:id/btnOk").click()  ###未安装QQ,断言是否有弹框提示
                    driver.install_app("D:/com.tencent.mobileqq.apk")
            if self.utils.isExistElementByid(driver,"com.tencent.mobileqq:id/account"):
                driver.find_element_by_id("com.tencent.mobileqq:id/account").send_keys("2280638288")
                driver.find_element_by_id("com.tencent.mobileqq:id/password").send_keys("codoon123")
                driver.find_element_by_xpath(
                    "//android.widget.Button[contains(@text,'登 录')]").click()  ###未登录QQ,需输入账号密码
            elif self.utils.isExistElementByxpath(driver,"你已对该应用授权"):
                driver.find_element_by_xpath(
                    "//android.widget.Button[contains(@text,'登录')]").click()  ###已登录QQ,需授权登录
            ###### 登录过程视网络情况加入延时 #####
            time.sleep(15)
            #######若为新账号，进入完善个人资料页 #################
            if driver.current_activity == '.ui.setting.ImproveUserInfoActivity':
                self.utils.CompleteUserInfo(driver)
            time.sleep(1)
            ####弹框判断###
            while self.utils.isExistElementByid(driver,"com.codoon.gps:id/ads_content"):
                driver.find_element_by_id("com.codoon.gps:id/btn_cancel").click()
            time.sleep(1)
            if self.utils.isExistElementByid(driver,"com.codoon.gps:id/ll_description"):
                driver.find_element_by_id("com.codoon.gps:id/btnOk").click()
            ################ 登录完成后的断言判断 ###########################
            self.utils.LoginCheckSuccess(driver)