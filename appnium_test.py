# coding=utf-8
import unittest
from appium import webdriver
from appium.common.exceptions import NoSuchContextException
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException
import desired_capabilities
from basics import *
from time import sleep
import os
import random


class AndroidTests(unittest.TestCase):
    def setUp(self):
        desired_caps = desired_capabilities.get_desired_capabilities('eqxiu-2.2.2.0007.apk')
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def tearDown(self):
        self.driver.quit()

    def test_a_slideshow_page(self):
        # self.skipTest('Tested')
        # 起始页
        activity = self.driver.current_activity
        self.assertEqual('.activity.SplashActivity', activity)
        # 翻轮播图
        self.driver.implicitly_wait(10)
        el_page1 = self.driver.find_element_by_id('cn.knet.eqxiu:id/viewpager')
        self.assertIsNotNone(el_page1)
        self.swipeLeft(200)
        sleep(1)

        el_page2 = self.driver.find_element_by_id('cn.knet.eqxiu:id/viewpager')
        self.assertIsNotNone(el_page2)
        self.swipeLeft(200)
        sleep(1)

        el_page3_btn = self.driver.find_element_by_id('cn.knet.eqxiu:id/stroll')
        self.assertIsNotNone(el_page3_btn)
        el_page3_btn.click()
        login_view_btn = self.driver.find_element_by_id('cn.knet.eqxiu:id/choice_login')
        self.assertIsNotNone(login_view_btn)
        register_view_btn = self.driver.find_element_by_id('cn.knet.eqxiu:id/choice_register')
        self.assertIsNotNone(register_view_btn)

    def test_b_login(self):
        self.driver.implicitly_wait(10)
        try:
            self.driver.find_element_by_id('cn.knet.eqxiu:id/choice_login').click()
        except NoSuchElementException:
            pass
        self.switch_server()
        # 登录
        self.driver.find_element_by_id('cn.knet.eqxiu:id/login_user_name').send_keys(BASIC_USER['username'])
        self.driver.find_element_by_id('cn.knet.eqxiu:id/login_user_pwd').send_keys(BASIC_USER['psw'])
        self.driver.find_element_by_id('cn.knet.eqxiu:id/login_btn').click()
        self.detach_know()
        self.upgrade_check()
        # banner检查
        daimajia_slider_image = self.driver.find_element_by_id('cn.knet.eqxiu:id/daimajia_slider_image')
        self.assertIsNotNone(daimajia_slider_image)

    def test_c_empty_to_create_template_and_delete(self):
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id("cn.knet.eqxiu:id/no_scene_img")
        self.create_template()
        self.go_back()
        self.praise_check()
        self.assertRaises(NoSuchElementException, self.driver.find_element_by_id, "cn.knet.eqxiu:id/no_scene_img")
        self.delete_scene()
        self.driver.find_element_by_id("cn.knet.eqxiu:id/no_scene_img")

    def test_d_create_business_and_delete(self):
        self.create_business()
        self.go_back()
        self.praise_check()
        self.delete_scene()

    def test_e_create_cards_and_delete(self):
        self.create_cards()
        self.save_scene_in_preview()
        self.praise_check()
        self.delete_scene()

    def test_f_create_photo_gallery(self):
        self.create_photo()
        self.save_scene_in_preview()
        self.praise_check()
        self.delete_scene()

    def test_g_create_template_and_set_and_delete(self):
        self.driver.implicitly_wait(10)
        self.create_template()
        self.save_scene_in_edit(SCENE_BASIC_SETTING)
        self.praise_check()
        self.delete_scene()

    def getSize(self):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return (x, y)

    # 向左滑动
    def swipeLeft(self, t):
        l = self.getSize()
        x1 = int(l[0]*0.85)
        y1 = int(l[1]*0.5)
        x2 = int(l[0]*0.15)
        self.driver.swipe(x1, y1, x2, y1, t)

    # 向右滑动
    def swipeRight(self, t):
        l = self.getSize()
        x1 = int(l[0]*0.15)
        y1 = int(l[1]*0.5)
        x2 = int(l[0]*0.85)
        self.driver.swipe(x1, y1, x2, y1, t)

    # 向上滑动
    def swipeUp(self, t):
        l = self.getSize()
        x1 = int(l[0]*0.5)
        y1 = int(l[1]*0.75)
        y2 = int(l[1]*0.25)
        self.driver.swipe(x1, y1, x1, y2, t)

    # 向下滑动
    def swipeDown(self, t):
        l = self.getSize()
        x1 = int(l[0]*0.5)
        y1 = int(l[1]*0.25)
        y2 = int(l[1]*0.75)
        self.driver.swipe(x1, y1, x1, y2, t)

    # 场景分家提示
    def detach_know(self):
        try:
            self.driver.find_element_by_id('cn.knet.eqxiu:id/detach_know').click()
        except NoSuchElementException:
            pass

    # 升级提示
    def upgrade_check(self):
        try:
            self.driver.find_element_by_id('cn.knet.eqxiu:id/no_up_grade').click()
        except NoSuchElementException:
            pass

    # 切换服务器
    def switch_server(self):
        global SERVER_SWITCHED_FLAG
        # 如果是测试环境则切换至测试服
        if TEST_TYPE == "TEST":
            login_logo_btn = self.driver.find_element_by_id('cn.knet.eqxiu:id/login_logo')
            login_logo_btn_x, login_logo_btn_y = login_logo_btn.location.get('x'), login_logo_btn.location.get('y')
            for i in range(12):
                self.driver.tap([(login_logo_btn_x, login_logo_btn_y)])
            self.driver.find_element_by_id('cn.knet.eqxiu:id/switch_server_btn').click()

            self.driver.find_element_by_name('试炼塔').click()
            SERVER_SWITCHED_FLAG = True
            self.driver.find_element_by_id('android:id/button1').click()

        elif TEST_TYPE == "ONLINE" and SERVER_SWITCHED_FLAG:
            login_logo_btn = self.driver.find_element_by_id('cn.knet.eqxiu:id/login_logo')
            login_logo_btn_x, login_logo_btn_y = login_logo_btn.location.get('x'), login_logo_btn.location.get('y')
            for i in range(12):
                self.driver.tap([(login_logo_btn_x, login_logo_btn_y)])
            self.driver.find_element_by_id('cn.knet.eqxiu:id/switch_server_btn').click()

            self.driver.find_element_by_name('完美世界').click()
            SERVER_SWITCHED_FLAG = False
            self.driver.find_element_by_id('android:id/button1').click()

        elif TEST_TYPE == "PRE":
            login_logo_btn = self.driver.find_element_by_id('cn.knet.eqxiu:id/login_logo')
            login_logo_btn_x, login_logo_btn_y = login_logo_btn.location.get('x'), login_logo_btn.location.get('y')
            for i in range(12):
                self.driver.tap([(login_logo_btn_x, login_logo_btn_y)])
            self.driver.find_element_by_id('cn.knet.eqxiu:id/switch_server_btn').click()

            self.driver.find_element_by_name('预发布').click()
            SERVER_SWITCHED_FLAG = True
            self.driver.find_element_by_id('android:id/button1').click()

    # 给个好评提示
    def praise_check(self):
        try:
            self.driver.find_element_by_id('cn.knet.eqxiu:id/to_refuse').click()
        except NoSuchElementException:
            pass

    # 摇一摇提示
    def take_a_shake(self):
        try:
            self.driver.find_element_by_id("cn.knet.eqxiu:id/able_shake_know").click()
        except NoSuchElementException:
            pass

    # 第一次创建场景时引导图提示
    def new_create_message(self):
        try:
            self.driver.find_element_by_id("cn.knet.eqxiu:id/boot_image")
            for i in range(4):
                self.driver.tap([(self.getSize()[0]*0.25, self.getSize()[1]*0.25)])
                sleep(1)
        except NoSuchElementException:
            pass

    # 创建模板场景
    def create_template(self):
        self.driver.find_element_by_id("cn.knet.eqxiu:id/create_btn").click()
        self.driver.find_element_by_id("cn.knet.eqxiu:id/templates").click()
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_name(random.choice(TEMPLATE_TYPE)).click()
        self.driver.find_elements_by_id("cn.knet.eqxiu:id/templates_page")[0].click()
        sleep(1)
        self.driver.implicitly_wait(10)
        self.new_create_message()

    # 创建商务样例
    def create_business(self):
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id("cn.knet.eqxiu:id/create_btn").click()
        self.driver.find_element_by_id("cn.knet.eqxiu:id/business_samples").click()
        self.driver.implicitly_wait(10)
        self.driver.find_elements_by_id("cn.knet.eqxiu:id/tb")[0].click()
        sleep(1)
        self.driver.find_element_by_id("cn.knet.eqxiu:id/use_sample").click()
        self.driver.implicitly_wait(10)
        self.new_create_message()

    # 创建节日贺卡
    def create_cards(self,  ):
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id("cn.knet.eqxiu:id/create_btn").click()
        self.driver.find_element_by_id("cn.knet.eqxiu:id/greeting_cards").click()
        self.driver.find_elements_by_id("cn.knet.eqxiu:id/tb")[0].click()
        self.driver.find_element_by_id("cn.knet.eqxiu:id/rl_create_card").click()
        self.driver.implicitly_wait(10)
        self.take_a_shake()

    # 创建音乐相册
    def create_photo(self):
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id("cn.knet.eqxiu:id/create_btn").click()
        self.driver.find_element_by_id("cn.knet.eqxiu:id/music_albums").click()
        self.driver.find_elements_by_id("cn.knet.eqxiu:id/tb")[0].click()
        self.driver.find_elements_by_id("cn.knet.eqxiu:id/tb")[0].click()
        self.driver.find_element_by_id("cn.knet.eqxiu:id/create_scene").click()
        self.driver.implicitly_wait(10)
        self.take_a_shake()

    # 编辑界面保存场景信息
    def save_scene_in_edit(self, setting=None):
        self.driver.find_element_by_id("cn.knet.eqxiu:id/edit_save").click()
        self.driver.implicitly_wait(10)
        if setting:
            self.set_setting(setting)
        self.driver.find_element_by_id("cn.knet.eqxiu:id/edit_preview_publish").click()
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id("cn.knet.eqxiu:id/home_icon").click()

    # 预览界面保存场景信息
    def save_scene_in_preview(self, setting=None):
        self.driver.implicitly_wait(10)
        if setting:
            self.set_setting(setting)
        self.driver.find_element_by_id("cn.knet.eqxiu:id/photo_preview_publish").click()
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id("cn.knet.eqxiu:id/home_icon").click()

    # 删除首个场景
    def delete_scene(self):
        self.driver.find_elements_by_id("cn.knet.eqxiu:id/more_ops")[0].click()
        self.driver.find_element_by_id("cn.knet.eqxiu:id/sence_delete").click()
        self.driver.find_element_by_id("cn.knet.eqxiu:id/between").click()

    # 退出
    def go_back(self):
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id("cn.knet.eqxiu:id/edit_back").click()

    # 设置
    def set_setting(self, setting):
        self.driver.find_element_by_id("cn.knet.eqxiu:id/edit_preview_music").click()
        for i in setting:
            if i in ["name", "details"]:
                self.driver.find_element_by_id("cn.knet.eqxiu:id/setting_scene_" + i).send_keys(setting[i])
            elif i == "cover":
                self.driver.find_element_by_id("cn.knet.eqxiu:id/setting_scene_cover").click()
                self.set_cover(setting["cover"])
            elif i == "music":
                self.driver.find_element_by_id("cn.knet.eqxiu:id/setting_music_layout").click()
                self.set_music(setting["music"])
            else:  # 翻页方式
                self.driver.find_element_by_id("cn.knet.eqxiu:id/setting_flips_layout").click()
                self.set_flip(setting["flip"])
        self.driver.find_element_by_id("cn.knet.eqxiu:id/setting_scene_ok").click()

    # 设置封面
    def set_cover(self, cover_info):
        self.driver.find_element_by_name(cover_info['type']).click()
        if cover_info.get("preview"):
            self.driver.find_elements_by_id("cn.knet.eqxiu:id/img_preview")[cover_info.get("index", 1)].click()
            self.driver.find_element_by_id("cn.knet.eqxiu:id/rl_select_current_pic").click()
        else:
            self.driver.find_elements_by_id("cn.knet.eqxiu:id/tb")[cover_info.get("index", 1)].click()

    # 设置音乐
    def set_music(self, music_info):
        self.driver.find_elements_by_name(music_info['type'])
        self.driver.find_elements_by_id("cn.knet.eqxiu:id/rl_music")[music_info.get("index", 1)].click()
        self.driver.find_element_by_id("cn.knet.eqxiu:id/tv_save_music").click()

    # 设置翻页方式
    def set_flip(self, flip_info):
        self.driver.find_element_by_name(flip_info).click()

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(AndroidTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
    # suite = unittest.TestSuite()
    # suite.addTest(AndroidTests("test_a_slideshow_page"))
    # suite.addTest(AndroidTests("test_b_login"))
    # unittest.TextTestRunner().run(suite)
