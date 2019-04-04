#!/usr/bin/env python
# -.- encoding: utf-8 -.-
"""
@author: DragonMa
@contact: mayexin@cnfanews.com
@desc:
"""

import json
import logging

import os

import tornado.options
from tornado.httpserver import HTTPServer
from tornado.web import Application
import tornado.ioloop
import tornado.log

from back.main_task import MainTask
from conf.config import SETTING
from handlers.main.main_urls import handlers
from apscheduler.schedulers.tornado import TornadoScheduler


class LogFormatter(tornado.log.LogFormatter):

    def __init__(self):
        super(LogFormatter, self).__init__(
            fmt='%(color)s[%(asctime)s %(filename)s:%(funcName)s:%(lineno)d %(levelname)s]%(end_color)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )


def main():
    tornado.options.define("port", default=8000, help="run on the given port", type=int)
    tornado.options.log_file_prefix = os.path.join(os.path.dirname(__file__), 'logs/tornado_main.log')
    # tornado.options.log_rotate_mode = 'time'  # 轮询模式: time or size
    # tornado.options.log_rotate_when = 'D'  # 单位: S / M / H / D / W0 - W6
    # tornado.options.log_rotate_interval = 7  # 间隔: 7天
    tornado.options.parse_command_line()
    [i.setFormatter(LogFormatter()) for i in logging.getLogger().handlers]
    http_server = HTTPServer(Application(handlers, **SETTING['setting']))
    http_server.listen(tornado.options.options.port)
    logging.info("server :{} start...".format(tornado.options.options.port))
    sched = TornadoScheduler()
    # one process
    sched.add_job(load_page, 'interval', hours=2)
    sched.start()
    http_server.start(1)
    tornado.ioloop.IOLoop.current().start()


def load_page():
    logging.info("start load page.")
    main_task = MainTask()
    main_task.run()
    logging.info("load page end.")


if __name__ == '__main__':
    main()
