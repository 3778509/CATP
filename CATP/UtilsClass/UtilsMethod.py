import time,random,base64
from selenium.webdriver.common.by import By

class TestClassMethod(object):
    def __init__(self):
        pass

    '''以name判断元素是否存在，返回值为布尔型'''
    @staticmethod
    def isExistElementByname(self, driver, name):
        try:
            driver.find_element_by_name(name)
            return True
        except:
            return False

    '''以xpath判断元素是否存在，返回值为布尔型
    :context 元素的text内容
    :style 元素的种类，默认为TextView
    :attra 元素的属性，默认为text
    '''
    @staticmethod
    def isExistElementByxpath(driver,context, style='TextView', attra='text'):
        try:
            driver.find_element_by_xpath("//android.widget.%s[contains(@%s,'%s')]" % (style, attra, context))
            return True
        except:
            return False

    '''以id判断元素是否存在，返回值为布尔型'''
    @staticmethod
    def isExistElementByid(driver, id):
        try:
            driver.find_element_by_id(id)
            return True
        except:
            return False

    '''注册流程，完善个人资料'''
    @staticmethod
    def CompleteUserInfo(self, driver):
        driver.find_element_by_id("com.codoon.gps:id/women").click()
        while self.isExistElementByxpath(driver, "下一步", 'Button'):
            driver.find_element_by_id("com.codoon.gps:id/button_nextstep").click()
        else:
            assert self.isExistElementByxpath(driver,"选择爱好，找到兴趣相投的小伙伴！")
            while self.isExistElementByxpath(driver,"上一步", 'Button'):
                driver.find_element_by_id("com.codoon.gps:id/button_prestep").click()
        driver.find_element_by_id("com.codoon.gps:id/man").click()
        #### 选择生日页面
        self.swipeControl(driver, By.ID, value="com.codoon.gps:id/common_wheel_left", heading='UP')
        self.swipeControl(driver, By.ID, value="com.codoon.gps:id/common_wheel_mid", heading='DOWN')
        self.swipeControl(driver, By.ID, value="com.codoon.gps:id/common_wheel_right", heading='UP')
        driver.find_element_by_id("com.codoon.gps:id/button_nextstep").click()
        ####  选择身高页面
        self.swipeControl(driver, By.ID, value='com.codoon.gps:id/image_ruler', heading='DOWN')
        driver.find_element_by_id("com.codoon.gps:id/button_nextstep").click()
        ####  选择体重页面
        self.swipeControl(driver, By.ID, value="com.codoon.gps:id/weightRuler", heading='LEFT')
        driver.find_element_by_id("com.codoon.gps:id/button_nextstep").click()
        ####  选择兴趣
        driver.find_element_by_id("com.codoon.gps:id/interest_gray_img").click()
        driver.find_element_by_id("com.codoon.gps:id/button_nextstep").click()

        '''登录后的元素检查'''
        @staticmethod
        def LoginCheckSuccess(self,driver):
            self.assertNotEqual(driver.page_source.find("运动圈"), -1)
            self.assertNotEqual(driver.page_source.find("发现"), -1)
            self.assertNotEqual(driver.page_source.find("运动"), -1)
            self.assertNotEqual(driver.page_source.find("消息"), -1)
            self.assertNotEqual(driver.page_source.find("我的"), -1)

        '''滑动指定元素
        :by 定位元素的方式
        :value 元素标识，与by结合定位
        :heading 元素滑动的方向（UP/DOWN/LEFT/RIGHT）
        '''
        @staticmethod
        def swipeControl(driver, by, value, heading):
            #### 获取控件开始位置的坐标轴
            start = driver.find_element(by=by, value=value).location
            startX = start.get('x')
            startY = start.get('y')
            ##### 获取控件坐标轴差
            q = driver.find_element(by=by, value=value).size
            x = q.get('width')
            y = q.get('height')
            #### 计算出控件结束坐标
            if startX < 0:
                startX = 0
            endX = x + startX
            endY = y + startY
            #### 计算中间点坐标
            if endX > 1080:
                endX = 1080
            centreX = (endX + startX) / 2
            centreY = (endY + startY) / 2

            #### 定义swipe的方向
            actions = {
                'UP': driver.swipe(centreX, centreY + 200, centreX, centreY - 200, 500),
                'DOWN': driver.swipe(centreX, centreY - 200, centreX, centreY + 200, 500),
                'LEFT': driver.swipe(centreX + 200, centreY, centreX - 200, centreY, 500),
                'RIGHT': driver.swipe(centreX - 200, centreY, centreX + 200, centreY, 500),
            }
            ##### action
            actions.get(heading)

            '''登出App'''
            @classmethod
            def logout():
                driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'我的')]").click()
                self.assertNotEqual(driver.find_element_by_id("com.codoon.gps:id/mine_user_nick").text,
                                    '匿名用户')  ###若出现匿名用户，case则failed结束
                driver.find_element_by_id("com.codoon.gps:id/mine_setting_btn").click()  ###点击设置icon
                time.sleep(0.5)
                for i in range(3):
                    driver.swipe(480, 900, 480, 30)  ###向下滑动两次。为兼容不同分辨率的手机
                driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'退出登录')]").click()
                driver.find_element_by_id("com.codoon.gps:id/btn_p").click()

            @staticmethod
            def hasDialog(self,driver):
                while self.isExistElementByid("com.codoon.gps:id/ads_content"):
                    self.driver.find_element_by_id("com.codoon.gps:id/btn_cancel").click()
                time.sleep(1)
                if self.isExistElementByid("com.codoon.gps:id/ll_description"):
                    self.driver.find_element_by_id("com.codoon.gps:id/btnOk").click()

            @classmethod
            def Before_Login():
                while True:
                    if driver.current_activity == '.ui.login.ViewPage':  ##引导页##
                        driver.swipe(680, 480, 80, 480)  ###从引导页滑动切换到登录前页
                        if self.isExistElementByid("com.codoon.gps:id/viewpage_btn_login"):
                            driver.find_element_by_xpath(
                                "//android.widget.Button[contains(@text,'进入咕咚')]").click()  ###跳转到登录页
                        break  ##置换登录Action，退出循环判断
                    elif driver.current_activity == '.ui.SlideActivity':  ##已登录缓存页##
                        self.logout()  ##退出之前登录，并没完成登录Action，flag标志不变
                    else:  ### 剩下情况则为登录页，这种情况界面不需做任何逻辑处理
                        break  ##置换登录Action，退出循环判断

            @classmethod
            def regedit_action(phone,passwd):
                driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'手机号注册')]").click()
                driver.find_element_by_id("com.codoon.gps:id/textViewCodeName").click()
                driver.keyevent(4)
                driver.find_element_by_id("com.codoon.gps:id/register_txt_account").send_keys(phone)
                driver.find_element_by_id("com.codoon.gps:id/register_txt_password").send_keys(passwd)
                driver.find_element_by_id("com.codoon.gps:id/btn_get_verify_code").click()
                ##确认发送验证码弹框
                if self.isExistElementByid("com.codoon.gps:id/message"):
                    self.driver.find_element_by_id("com.codoon.gps:id/btn_p").click()
                    time.sleep(15)  ##弹出短信发送确认框
                ##读取验证码
                f = self.driver.pull_file("/storage/sdcard0/codoon/regedit/Securitycode.txt")
                self.driver.find_element_by_id("com.codoon.gps:id/et_verify_code").send_keys(
                    bytes.decode(base64.b64decode(f)))
                self.driver.find_element_by_id("com.codoon.gps:id/register_btn_submit").click()
                ##########注册流程上传头像和昵称######
                self.driver.find_element_by_id("com.codoon.gps:id/register_txt_username").send_keys(
                    random.choice(["codoon", "test", "gudong", "leo", "dell"]), random.randint(500, 900))
                time.sleep(2)
                self.driver.find_element_by_id("com.codoon.gps:id/regist_portrait").click()  ####上传头像
                self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'相机拍摄')]").click()
                time.sleep(2)
                if self.isExistElementByxpath('调用摄像头'):
                    self.driver.find_element_by_id("com.huawei.systemmanager:id/btn_allow").click()
                time.sleep(2)
                self.driver.find_element_by_id("com.huawei.camera:id/shutter_button").click()
                time.sleep(2)
                self.driver.find_element_by_id("com.huawei.camera:id/btn_done").click()
                time.sleep(2)
                self.driver.find_element_by_id("com.codoon.gps:id/ok_btn").click()
                time.sleep(2)
                self.driver.find_element_by_id("com.codoon.gps:id/register_btn_submit").click()

            @classmethod
            def Tencent_Login(QQnumber,QQpasswd):
                while True:
                    driver.find_element_by_id("com.codoon.gps:id/ll_login_qq").click()
                    time.sleep(3)  ###延迟，加载界面
                    if driver.is_app_installed("com.tencent.mobileqq"):
                        break
                    else:
                        self.assertTrue(self.isExistElementByname("下载QQ"))  ###未安装QQ,断言是否有弹框提示
                        driver.install_app("D:/com.tencent.mobileqq.apk")
                        driver.keyevent(4)  ### keyevent=4 即 手机返回键
                if self.isExistElementByid("com.tencent.mobileqq:id/account"):
                    driver.find_element_by_id("com.tencent.mobileqq:id/account").send_keys(QQnumber)
                    driver.find_element_by_id("com.tencent.mobileqq:id/password").send_keys(QQpasswd)
                    driver.find_element_by_xpath(
                        "//android.widget.Button[contains(@text,'登 录')]").click()  ###未登录QQ,需输入账号密码
                elif self.isExistElementByxpath("你已对该应用授权"):
                    driver.find_element_by_xpath(
                        "//android.widget.Button[contains(@text,'登录')]").click()  ###已登录QQ,需授权登录
                ###### 登录过程视网络情况加入延时 #####
                time.sleep(15)
                #######若为新账号，进入完善个人资料页 #################
                if driver.current_activity == '.ui.setting.ImproveUserInfoActivity':
                    self.CompleteUserInfo()
                time.sleep(1)
                ####弹框判断###
                while self.isExistElementByid("com.codoon.gps:id/ads_content"):
                    driver.find_element_by_id("com.codoon.gps:id/btn_cancel").click()
                time.sleep(1)
                if self.isExistElementByid("com.codoon.gps:id/ll_description"):
                    driver.find_element_by_id("com.codoon.gps:id/btnOk").click()

            @classmethod
            def Blog_Login(user,passwd):
                #############################################
                ####            Blog登录流程             ####
                #############################################
                self.driver.find_element_by_id("com.codoon.gps:id/ll_login_weibo").click()
                time.sleep(5)  ###延迟，加载界面
                ele = self.driver.find_elements_by_xpath("//android.widget.EditText")
                ele[0].send_keys(user)
                ele[1].send_keys(passwd)
                self.driver.find_element_by_name("登录").click()  ###完成登录流程
                ###### 登录过程视网络情况加入延时 #####
                time.sleep(15)
                ####弹框判断###
                while self.isExistElementByid("com.codoon.gps:id/ads_content"):
                    self.driver.find_element_by_id("com.codoon.gps:id/btn_cancel").click()
                time.sleep(1)
                if self.isExistElementByid("com.codoon.gps:id/ll_description"):
                    self.driver.find_element_by_id("com.codoon.gps:id/btnOk").click()

            @classmethod
            def Weichat(user,passwd):
                #############################################
                ####            微信登录流程             ####
                #############################################
                while True:
                    self.driver.find_element_by_id("com.codoon.gps:id/ll_login_weixin").click()
                    time.sleep(3)  ###延时，加载界面
                    if self.driver.is_app_installed("com.tencent.mm"):
                        break
                    else:
                        assert (self.isExistElementByxpath("您尚未安装微信,请安装后重试!"))
                        self.driver.find_element_by_id("com.codoon.gps:id/btnOk").click()
                        self.driver.install_app("D:/com.tencent.mm.apk")  ##此while循环确保微信已安装
                time.sleep(3)  ###延迟，加载界面
                if self.isExistElementByxpath("QQ号/微信号/Email", "EditText"):
                    self.driver.find_element_by_xpath(
                        "//android.widget.EditText[contains(@text,'QQ号/微信号/Email')]").send_keys(
                       user)
                    self.driver.find_element_by_xpath(
                        "//android.widget.EditText[contains(@password,'true')]").send_keys(
                        passwd)
                    self.driver.find_element_by_id("com.tencent.mm:id/b5t").click()  ###输入账号密码登录
                if self.isExistElementByxpath("微信登录"):  ###登录后判断是否为授权页面
                    x = self.driver.get_window_size()['width']
                    y = self.driver.get_window_size()['height']  ###根据手机分辨率确定元素的坐标
                    self.driver.tap([(x / 2 * 0.95, y / 2 * 1.08)], 500)
                    # if (x,y) == (480,800):
                    #     self.driver.tap([(230, 450)], 500)                                             ####4.0寸屏幕
                    # elif (x,y) == (720,1280):
                    #     self.driver.tap([(350,700)],500)                                           ####HD主流屏
                    # elif (x,y) == (1080,1920):
                    #     self.driver.tap([(458, 1050)], 500)                                         ###1080p
                    # else:
                    #     self.driver.tap([(x/2*0.95,y/2*1.08)],500)
                ###### 登录过程视网络情况加入延时 #####
                time.sleep(15)
                #######若为新账号，进入完善个人资料页 #################
                if self.driver.current_activity == '.ui.setting.ImproveUserInfoActivity':
                    self.CompleteUserInfo()
                ####弹框判断###
                while self.isExistElementByid("com.codoon.gps:id/ads_content"):
                    self.driver.find_element_by_id("com.codoon.gps:id/btn_cancel").click()
                time.sleep(1)
                if self.isExistElementByid("com.codoon.gps:id/ll_description"):
                    self.driver.find_element_by_id("com.codoon.gps:id/btnOk").click()

            @classmethod
            def moblie_login(cls):
                #############################################
                ####         手机和邮箱登录流程          ####
                #############################################
                self.driver.find_element_by_id("com.codoon.gps:id/tv_login").click()
                time.sleep(3)  ###延时，加载界面
                self.driver.find_element_by_id("com.codoon.gps:id/login_text_account").send_keys("583@test.com")
                self.driver.find_element_by_id("com.codoon.gps:id/login_text_password").send_keys("123456")
                self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'登  录')]").click()

                ###### 登录过程视网络情况加入延时 #####
                time.sleep(15)
                ####弹框判断###
                while self.isExistElementByid("com.codoon.gps:id/ads_content"):
                    self.driver.find_element_by_id("com.codoon.gps:id/btn_cancel").click()
                time.sleep(1)
                if self.isExistElementByid("com.codoon.gps:id/ll_description"):
                    self.driver.find_element_by_id("com.codoon.gps:id/btnOk").click()