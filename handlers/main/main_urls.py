#!/usr/bin/env python
# -.- encoding: utf-8 -.-
"""
@author: DragonMa
@contact: mayexin@cnfanews.com
@desc:
"""

from handlers.main.main_handler import *

handlers = [
    (r'/gain_cookie_test/$', GainCookieTest),  # FF测试
    (r'/gain_cookie/$', GainCookieRequest),  # 获取cookie
    (r'/get_cookie/$', GetCookie),  # 获取cookie
    (r'/update_all_cookie/$', UpdateAllCookie),  # 更新全部cookie
    (r'/save_conf/$', SaveCookieConf),  # 保存cookie配置
]
