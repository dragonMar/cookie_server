#!/usr/bin/env python
# -.- encoding: utf-8 -.-
"""
@author: DragonMa
@contact: mayexin@cnfanews.com
@desc:
"""
import logging

import redis

from conf.config import SETTING

pool = redis.ConnectionPool(host=SETTING['redis']['host'], password=SETTING['redis']['pwd'],
                            db=SETTING['redis']['db'])  # 实现一个连接池
r = redis.Redis(connection_pool=pool, decode_responses=True)


def redis_hget(name, key):
    data = ""
    try:
        data = r.hget(name, key)
        if data:
            data = data.decode('utf8')
    except Exception as e:
        logging.error(e)
    finally:
        return data


def redis_hset(name, key, value):
    status = False
    try:
        r.hset(name, key, value)
        status = True
    except Exception as e:
        logging.error(e)
    finally:
        return status
