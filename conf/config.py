#!/usr/bin/env python
# -.- encoding: utf-8 -.-
"""
@author: DragonMa
@contact: mayexin@cnfanews.com
@desc:
"""
import os

SETTING = {
    'setting': {
        'debug': os.getenv("DEBUG", True),
        'template_path': os.path.join(os.path.dirname(__file__), "templates"),
        'static_path': os.path.join(os.path.dirname(__file__), "static"),
    },
    'mysql': {
        'host': os.getenv('MYSQL_HOST', '127.0.0.1'),
        'port': os.getenv('MYSQL_PORT', '3306'),
        'db': os.getenv('MYSQL_DB', 'test'),
        'user': os.getenv('MYSQL_USER', 'root'),
        'pwd': os.getenv("MYSQL_PWD", '')
    },
    "redis": {
        'host': os.getenv("REDIS_HOST", "127.0.0.1"),
        'db': int(os.getenv("REDIS_DB", 0)),
        'pwd': os.getenv("REDIS_PWD", ""),
    },
    "server_list": {
        "servers": os.getenv("SERVER_LIST", 'http://127.0.0.1:8000')
    },
    "webdriver_server": os.getenv("WEBDRIVER_SERVER", "http://127.0.0.1:4444/wd/hub")
}
