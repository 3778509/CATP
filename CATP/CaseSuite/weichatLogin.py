import time
from CATP.UtilsClass.UtilsMethod import *

class WeichatLoginTestcase(object):
    def __init__(self):
        self.flag = True
        self.utils = TestClassMethod()

    def Weichat(self,driver):
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
        else:
            #############################################
            ####            微信登录流程             ####
            #############################################
            while True:
                driver.find_element_by_id("com.codoon.gps:id/ll_login_weixin").click()
                time.sleep(3)  ###延时，加载界面
                if driver.is_app_installed("com.tencent.mm"):
                    break
                else:
                    assert (self.utils.isExistElementByxpath(driver,"您尚未安装微信,请安装后重试!"))
                    driver.find_element_by_id("com.codoon.gps:id/btnOk").click()
                    driver.install_app("D:/com.tencent.mm.apk")  ##此while循环确保微信已安装
            time.sleep(3)  ###延迟，加载界面
            if self.utils.isExistElementByxpath(driver,"QQ号/微信号/Email", "EditText"):
                driver.find_element_by_xpath(
                    "//android.widget.EditText[contains(@text,'QQ号/微信号/Email')]").send_keys(
                    "18328368638")
                driver.find_element_by_xpath("//android.widget.EditText[contains(@password,'true')]").send_keys(
                    "xq1988725")
                driver.find_element_by_id("com.tencent.mm:id/b5t").click()  ###输入账号密码登录
            if self.utils.isExistElementByxpath(driver,"微信登录"):  ###登录后判断是否为授权页面
                x = driver.get_window_size()['width']
                y = driver.get_window_size()['height']  ###根据手机分辨率确定元素的坐标
                driver.tap([(x / 2 * 0.95, y / 2 * 1.08)], 500)
                # if (x,y) == (480,800):
                #     driver.tap([(230, 450)], 500)                                             ####4.0寸屏幕
                # elif (x,y) == (720,1280):
                #     driver.tap([(350,700)],500)                                           ####HD主流屏
                # elif (x,y) == (1080,1920):
                #     driver.tap([(458, 1050)], 500)                                         ###1080p
                # else:
                #     driver.tap([(x/2*0.95,y/2*1.08)],500)
            ###### 登录过程视网络情况加入延时 #####
            time.sleep(15)
            #######若为新账号，进入完善个人资料页 #################
            if driver.current_activity == '.ui.setting.ImproveUserInfoActivity':
                self.utils.CompleteUserInfo(driver)
            ####弹框判断###
            while self.utils.isExistElementByid(driver,"com.codoon.gps:id/ads_content"):
                driver.find_element_by_id("com.codoon.gps:id/btn_cancel").click()
            time.sleep(1)
            if self.utils.isExistElementByid(driver,"com.codoon.gps:id/ll_description"):
                driver.find_element_by_id("com.codoon.gps:id/btnOk").click()
            ################ 登录完成后的断言判断 ###########################
            self.utils.LoginCheckSuccess(driver)