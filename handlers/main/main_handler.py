#!/usr/bin/env python
# -.- encoding: utf-8 -.-
"""
@author: DragonMa
@contact: mayexin@cnfanews.com
@desc:
"""
import datetime
import json
import logging

import tornado.web
from tornado import gen
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor

from back.gain_cookie import GainCookie
from back.main_task import MainTask
from common.my_error import NoData
from handlers.main.utils import requests_helper, requests_helper_asy
from libs.mysql_con.mysql import MYSQL_SESSION, CookieConf
from libs.redis_con.redis_operation import redis_hget


class GainCookieTest(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(4)

    # 测试
    @requests_helper_asy
    @gen.coroutine
    def post(self):
        rule = json.loads(self.request.body)
        cookie, source = yield self._gain_cookies(rule)
        return {'cookie': cookie, 'page_source': source}

    @run_on_executor
    def _gain_cookies(self, rule):
        gain_cookie = GainCookie()
        return gain_cookie.gain_cookie(rule)


class GetCookie(tornado.web.RequestHandler):
    # 查询cookie值
    @requests_helper
    def post(self):
        web_id = self.get_argument("web_id")
        # cookie = SQLITE_SESSION.query(CookieList).filter(CookieList.id == web_id).first()
        cookie = redis_hget("cookie_list", web_id)
        if cookie:
            return {'cookie': cookie}
        else:
            raise NoData


class GainCookieRequest(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(4)

    # 请求子服务器 进行登录
    @requests_helper_asy
    @gen.coroutine
    def post(self):
        rule = json.loads(self.request.body)
        cookie, source = yield self._gain_cookies(rule)
        return {'cookie': cookie, 'page_source': source}

    @run_on_executor
    def _gain_cookies(self, rule):
        gain_cookie = GainCookie()
        return gain_cookie.gain_cookie(rule)


class UpdateAllCookie(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(4)

    # 请求子服务器 进行登录
    @requests_helper_asy
    @gen.coroutine
    def get(self):
        yield self._update_all()
        return {}

    @run_on_executor
    def _update_all(self):
        logging.info("start load page.")
        main_task = MainTask()
        main_task.run()
        logging.info("load page end.")


class SaveCookieConf(tornado.web.RequestHandler):
    @requests_helper
    def post(self):
        data = json.loads(self.request.body)
        now = datetime.datetime.now()
        if MYSQL_SESSION.query(CookieConf).filter(CookieConf.web_id == data['web_id']).first():
            MYSQL_SESSION.query(CookieConf).filter(CookieConf.web_id == data['web_id']).update(
                {'url': data['url'], 'is_login': data['is_login'], 'content': json.dumps(data['content']),
                 'update_time': now, 'status': data['status']}
            )
        else:
            data['content'] = json.dumps(data['content'])
            data['create_time'] = now
            data['update_time'] = now
            try:
                c = CookieConf(**data)
                MYSQL_SESSION.add(c)
                MYSQL_SESSION.commit()
                return {}
            except Exception as e:
                logging.error(e)
                MYSQL_SESSION.rollback()
                raise e
