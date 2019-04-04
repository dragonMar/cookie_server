#!/usr/bin/env python
# -.- encoding: utf-8 -.-
"""
@author: DragonMa
@contact: mayexin@cnfanews.com
@desc:
"""

from selenium.common.exceptions import TimeoutException


class NoFindElement(TimeoutException):
    pass


class NoData(Exception):
    pass


ERROR_LIST = {
    'UNKNOWN': 4000,  # 未知错误
    'NO_FIND_ELEMENT': 4001,  # 未找到该元素
    'NO_DATA': 4002,    # 数据库无该元素
}
