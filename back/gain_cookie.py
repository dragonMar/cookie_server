#!/usr/bin/env python
# -.- encoding: utf-8 -.-
"""
@author: DragonMa
@contact: mayexin@cnfanews.com
@desc:
"""
import base64
import json
import logging
import random

import re
import traceback

import requests
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from conf.config import SETTING
from libs.check_pic_api.check_pic_api import CHAO_JI_YING


class GainCookie:

    def __init__(self):
        # self.b = webdriver.Chrome("/Users/mayexin/Downloads/chromedriver")
        self.b = webdriver.Remote(
            command_executor=SETTING['webdriver_server'],
            desired_capabilities=DesiredCapabilities.CHROME
        )
        self.wait = WebDriverWait(self.b, 10)

    def gain_cookie(self, rule):
        try:
            # 获取cookie
            self.b.get(rule['url'])
            # 不需要登录
            if rule['is_login'] == 0:
                time.sleep(4)
                cookie = self.b.get_cookies()
                source = self.b.page_source
            # 需要登录
            else:
                # 提取登录规则
                # content = json.loads(rule['content'])
                cookie, source = self.login(rule['content'])
            # 格式化cookie (list to str)
            cookie = self._cookie_format(cookie)
            # source = source.encode('utf8')
            # with open("success.html", 'w') as f:
            #     f.write(source)
            # print(cookie)
            # print(source)
            # print(type(cookie))
            # time.sleep(10)
            return cookie, source
        except Exception as e:
            traceback.print_exc()
            logging.error(e)
            return "", ""
        finally:
            self.b.quit()

    def login(self, rule):
        # 需要切换登录方式
        if rule['x_switch'] != "":
            switch_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, rule['x_switch'])))
            switch_btn.click()
            time.sleep(1)

        # 获取登录主键位
        user = self.wait.until(EC.presence_of_element_located((By.XPATH, rule['x_user'])))
        pwd = self.wait.until(EC.presence_of_element_located((By.XPATH, rule['x_pwd'])))
        user.send_keys(rule['user'])
        pwd.send_keys(rule['pwd'])
        time.sleep(1)
        btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, rule['x_login'])))
        # 不需要验证码
        if rule['check_type'] == 0:
            pass
        # 需要验证码
        elif rule['check_type'] == 1:
            if len(self.b.find_elements_by_xpath(rule['x_image'])) == 0:
                btn.click()
                time.sleep(1)
                if len(self.b.find_elements_by_xpath(rule['x_image'])) == 0:
                    pass
                else:
                    check_text = self._image_to_text(rule['x_image'], btn)
                    input_check = self.wait.until(EC.presence_of_element_located((By.XPATH, rule['x_check'])))
                    input_check.send_keys(check_text)
            else:
                check_text = self._image_to_text(rule['x_image'], btn)
                if check_text == "success!!!":
                    time.sleep(2)
                    cookie = self.b.get_cookies()
                    source = self.b.page_source
                    return cookie, source
                input_check = self.wait.until(EC.presence_of_element_located((By.XPATH, rule['x_check'])))
                input_check.send_keys(check_text)
        time.sleep(random.randrange(1, 3))

        btn.click()

        time.sleep(4)
        # if len(self.b.find_elements_by_xpath(rule['x_user'])) != 0:
        #     return "", ""
        # else:
        cookie = self.b.get_cookies()
        source = self.b.page_source
        return cookie, source

    def _image_to_text(self, x_image, btn):
        img = self.wait.until(EC.presence_of_element_located((By.XPATH, x_image)))
        i = 0
        img_file = ""
        while i<3:
            try:
                src = img.get_attribute("src")
                if re.search(r"http", src):
                    img_file = requests.get(src).content
                    break
                elif re.search(r"base64", src):
                    s = src.split(",")[-1].replace("%0A", "\n")
                    img_file = base64.b64decode(s)
                    break
                else:
                    btn.click()
                    time.sleep(1)
                i += 1
                img = self.wait.until(EC.presence_of_element_located((By.XPATH, x_image)))
            except TimeoutException:
                # 有些网站 有时需要验证码 有时不需要
                return "success!!!"
        if img_file == "":
            return ""
        with open("test.jpg", "wb") as f:
            f.write(img_file)
        result = self._pic_check_api(img_file)
        # print(result)
        return result

    @staticmethod
    def _pic_check_api(file):
        # result = AIP_OCR.basicGeneral(file)
        # print(result)
        # if len(result[u'words_result']):
        #     text = result[u'words_result'][0][u'words']
        # else:
        #     text = ""
        # return text
        result = CHAO_JI_YING.PostPic(file, 1902)
        if isinstance(result, str):
            result = json.loads(result)
        if result['err_no'] == 0:
            return result['pic_str']
        else:
            return ""

    @staticmethod
    def _cookie_format(cookie_list):
        cookie = [item["name"] + "=" + item["value"] for item in cookie_list]
        cookie_str = '; '.join(item for item in cookie)
        return cookie_str
