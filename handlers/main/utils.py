#!/usr/bin/env python
# -.- encoding: utf-8 -.-
"""
@author: DragonMa
@contact: mayexin@cnfanews.com
@desc:
"""
import json
import logging

from tornado import gen

from common.my_error import NoFindElement, ERROR_LIST, NoData


def requests_helper_asy(func):
    @gen.coroutine
    def wrapper(self, *args, **kwargs):
        data = {'status': -1, 'data': {}, 'msg': ''}
        try:
            data['data'] = yield func(self, *args, **kwargs)
            data['status'] = 0

        except NoFindElement:
            data['msg'] = "超时没找到该元素"
            data['status'] = ERROR_LIST['NO_FIND_ELEMENT']
        except NoData:
            data['msg'] = "数据库无该元素"
            data['status'] = ERROR_LIST['NO_DATA']
        except Exception as e:
            data['msg'] = str(e)
            data['status'] = ERROR_LIST['UNKNOWN']
            logging.error(e)
        finally:
            self.write(gen_response(data))
    return wrapper


def requests_helper(func):
    def wrapper(self, *args, **kwargs):
        data = {'status': -1, 'data': {}, 'msg': ''}
        try:
            data['data'] = func(self, *args, **kwargs)
            data['status'] = 0

        except NoFindElement:
            data['msg'] = "超时没找到该元素"
            data['status'] = ERROR_LIST['NO_FIND_ELEMENT']
        except NoData:
            data['msg'] = "数据库无该元素"
            data['status'] = ERROR_LIST['NO_DATA']
        except Exception as e:
            data['msg'] = str(e)
            data['status'] = ERROR_LIST['UNKNOWN']
            logging.error(e)
        finally:
            self.write(gen_response(data))
    return wrapper


def gen_response(data):
    if isinstance(data, dict):
        r =  json.dumps(data)
    elif isinstance(data, str):
        r = data
    else:
        r = ""
    return r
