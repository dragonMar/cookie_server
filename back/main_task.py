#!/usr/bin/env python
# -.- encoding: utf-8 -.-
"""
@author: DragonMa
@contact: mayexin@cnfanews.com
@desc:
"""
import json
import logging
import requests
import asyncio

from conf.config import SETTING
from libs.mysql_con.mysql import MYSQL_SESSION, CookieConf
from libs.redis_con.redis_operation import redis_hset


class MainTask:
    def __init__(self):
        self.server_list = SETTING['server_list']['servers'].split(";")
        self.cookie_conf = []
        self._find_all_cookie_conf()
        self.err_list = []

    def _find_all_cookie_conf(self):
        conf_list = MYSQL_SESSION.query(CookieConf).filter(CookieConf.status == 0).all()
        for data in conf_list:
            self.cookie_conf.append({
                'web_id': data.web_id,
                'url': data.url,
                'is_login': data.is_login,
                'content': "" if data.content == "" else json.loads(data.content)
            })
        logging.info("tasks num: {}".format(len(self.cookie_conf)))

    async def _gain_cookie(self, url, data):
        result = {}
        try:
            logging.info("url: {} data:{}".format(url, data))
            response = requests.post(url, json=data)
            result = response.json()
        except Exception as e:
            logging.error(e)
        finally:
            return result

    async def pub_tasks(self, url, data_list):
        for data in data_list:
            r = await self._gain_cookie(url, data)
            if r.get('status', -1) == 0:
                redis_hset("cookie_list", data['web_id'], r['data']['cookie'])
            else:
                logging.error("server: {}, data:{} error".format(url, data))
                self.err_list.append(data)

    def run(self):
        conf_len = len(self.cookie_conf)
        server_len = len(self.server_list)
        num = int(conf_len / server_len) + 1
        tasks = []
        for i in range(server_len - 1):
            tasks.append(
                self.pub_tasks(self.server_list[i] + "/gain_cookie/", self.cookie_conf[num * i: num * (i + 1)]))
        tasks.append(self.pub_tasks(self.server_list[-1] + "/gain_cookie/", self.cookie_conf[num * (server_len - 1):]))
        loop = asyncio.new_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
