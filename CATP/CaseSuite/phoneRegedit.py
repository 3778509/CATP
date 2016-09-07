import time,random,base64
from CATP.UtilsClass.UtilsMethod import *

class RegeditLogin(object):
    def __init__(self):
        self.flag = True
        self.utils = TestClassMethod()

    def Regedit(self,driver):
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
            driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'手机号注册')]").click()
            driver.find_element_by_id("com.codoon.gps:id/textViewCodeName").click()
            driver.keyevent(4)
            driver.find_element_by_id("com.codoon.gps:id/register_txt_account").send_keys("18328368638")
            driver.find_element_by_id("com.codoon.gps:id/register_txt_password").send_keys("123456")
            driver.find_element_by_id("com.codoon.gps:id/btn_get_verify_code").click()
            ##确认发送验证码弹框
            if self.utils.isExistElementByid(driver,"com.codoon.gps:id/message"):
                driver.find_element_by_id("com.codoon.gps:id/btn_p").click()
                time.sleep(15)  ##弹出短信发送确认框
            ##读取验证码
            f = driver.pull_file("/storage/sdcard0/codoon/regedit/Securitycode.txt")
            driver.find_element_by_id("com.codoon.gps:id/et_verify_code").send_keys(
                bytes.decode(base64.b64decode(f)))
            driver.find_element_by_id("com.codoon.gps:id/register_btn_submit").click()
            ##########注册流程上传头像和昵称######
            driver.find_element_by_id("com.codoon.gps:id/register_txt_username").send_keys(
                random.choice(["codoon", "test", "gudong", "leo", "dell"]), random.randint(500, 900))
            time.sleep(2)
            driver.find_element_by_id("com.codoon.gps:id/regist_portrait").click()  ####上传头像
            driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'相机拍摄')]").click()
            time.sleep(2)
            if self.utils.isExistElementByxpath(driver,'调用摄像头'):
                driver.find_element_by_id("com.huawei.systemmanager:id/btn_allow").click()
            time.sleep(2)
            driver.find_element_by_id("com.huawei.camera:id/shutter_button").click()
            time.sleep(2)
            driver.find_element_by_id("com.huawei.camera:id/btn_done").click()
            time.sleep(2)
            driver.find_element_by_id("com.codoon.gps:id/ok_btn").click()
            time.sleep(2)
            driver.find_element_by_id("com.codoon.gps:id/register_btn_submit").click()
            ########################完善资料流程#####################
            if driver.current_activity == '.ui.setting.ImproveUserInfoActivity':
                self.utils.CompleteUserInfo(driver)
            time.sleep(1)
            ####弹框判断#####
            while self.utils.isExistElementByid(driver,"com.codoon.gps:id/ads_content"):
                driver.find_element_by_id("com.codoon.gps:id/btn_cancel").click()
            time.sleep(1)
            if self.utils.isExistElementByid(driver,"com.codoon.gps:id/ll_description"):
                driver.find_element_by_id("com.codoon.gps:id/btnOk").click()
            ################ 登录完成后的断言判断 ###########################
            self.utils.LoginCheckSuccess(driver)