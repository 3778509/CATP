import time
from CATP.UtilsClass.UtilsMethod import *

class MobileLoginTestcase(object):
    def __init__(self):
        self.flag = True
        self.utils = TestClassMethod()

    def Mobile(self,driver):
        '''
            #打开App时，可能存在有三种界面： 1.引导广告页，往右滑动可点击进入咕咚跳转至登录界面
                                             2.播放登录视频，直接进入登陆界面
                                             3.已登录过账号，打开即为app运动界面
            #flag为登录Action标志：1.True：未完成登录action,一直循环直到登录action完成（未完成登录Action有两种情况：已登录需先退出登录；第三方登录未安装相应apk）
                                   2.False: 完成登录Action，退出循环不再执行登录Action判断,接着执行捕获和断言
            '''
        while self.flag:
            if driver.current_activity == '.ui.login.ViewPage':  ##引导页##
                driver.swipe(680, 480, 80, 480)  ###从引导页滑动切换到登录前页
                time.sleep(0.5)
                if self.utils.isExistElementByid(driver,"com.codoon.gps:id/viewpage_btn_login"):
                    driver.find_element_by_xpath(
                        "//android.widget.Button[contains(@text,'进入咕咚')]").click()  ###跳转到登录页
                self.flag = False  ##置换登录Action，退出循环判断
            elif driver.current_activity == '.ui.SlideActivity':  ##已登录缓存页##
                ####弹框判断###
                while self.utils.isExistElementByid(driver, "com.codoon.gps:id/ads_content"):
                    driver.find_element_by_id("com.codoon.gps:id/btn_cancel").click()
                self.utils.logout(driver)
                self.flag = True  ##退出之前登录，并没完成登录Action，flag标志不变
            else:  ### 剩下情况则为登录页，这种情况界面不需做任何逻辑处理
                self.flag = False  ##置换登录Action，退出循环判断
        else:  ##登录Action为Falg后，统一执行输入账号密码等后续操作
            #############################################
            ####         手机和邮箱登录流程          ####
            #############################################
            driver.find_element_by_id("com.codoon.gps:id/tv_login").click()
            time.sleep(3)  ###延时，加载界面
            driver.find_element_by_id("com.codoon.gps:id/login_text_account").send_keys("583@test.com")
            driver.find_element_by_id("com.codoon.gps:id/login_text_password").send_keys("123456")
            driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'登  录')]").click()

            ###### 登录过程视网络情况加入延时 #####
            time.sleep(15)
            ####弹框判断###
            while self.utils.isExistElementByid(driver,"com.codoon.gps:id/ads_content"):
                driver.find_element_by_id("com.codoon.gps:id/btn_cancel").click()
            time.sleep(1)
            if self.utils.isExistElementByid(driver,"com.codoon.gps:id/ll_description"):
                driver.find_element_by_id("com.codoon.gps:id/btnOk").click()
            ####### 断言检查登录是否成功 ###########
            ###  判断依据是底部的5个tab存在，否则登录失败  ###
            self.utils.LoginCheckSuccess(driver)