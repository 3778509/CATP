import time
from CATP.UtilsClass.UtilsMethod import *

class BlogLoginTestcase(object):
    def __init__(self):
        self.flag = True
        self.utils = TestClassMethod()

    def Blog(self,driver):
        while self.flag:
            if driver.current_activity == '.ui.login.ViewPage':  ##引导页##
                driver.swipe(680, 480, 80, 480)  ###从引导页滑动切换到登录前页
                if self.utils.isExistElementByid(driver,"com.codoon.gps:id/viewpage_btn_login"):
                    driver.find_element_by_xpath(
                        "//android.widget.Button[contains(@text,'进入咕咚')]").click()  ###跳转到登录页
                self.flag = False  ##置换登录Action，退出循环判断
            elif driver.current_activity == '.ui.SlideActivity':  ##已登录缓存页##
                self.utils.logout(driver)

                self.flag = True  ##退出之前登录，并没完成登录Action，flag标志不变
            else:  ### 剩下情况则为登录页，这种情况界面不需做任何逻辑处理
                self.flag = False  ##置换登录Action，退出循环判断
        else:  ##登录Action为Falg后，统一执行输入账号密码等后续操作
            #############################################
            ####            Blog登录流程             ####
            #############################################
            driver.find_element_by_id("com.codoon.gps:id/ll_login_weibo").click()
            time.sleep(5)  ###延迟，加载界面
            ele = driver.find_elements_by_xpath("//android.widget.EditText")
            ele[0].send_keys("18328368638")
            ele[1].send_keys("xq1988725")
            driver.find_element_by_name("登录").click()  ###完成登录流程
            ###### 登录过程视网络情况加入延时 #####
            time.sleep(15)
            ####弹框判断###
            while self.utils.isExistElementByid(driver,"com.codoon.gps:id/ads_content"):
                driver.find_element_by_id("com.codoon.gps:id/btn_cancel").click()
            time.sleep(1)
            if self.utils.isExistElementByid(driver,"com.codoon.gps:id/ll_description"):
                driver.find_element_by_id("com.codoon.gps:id/btnOk").click()
            #################### 登录完成后的断言判断 ###################################
            self.utils.LoginCheckSuccess(driver)