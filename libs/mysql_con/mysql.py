#!/usr/bin/env python
# -.- encoding: utf-8 -.-
"""
@author: DragonMa
@contact: mayexin@cnfanews.com
@desc:
"""
from urllib import parse

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, TIMESTAMP
from sqlalchemy.orm import sessionmaker

from conf.config import SETTING

engine = sqlalchemy.create_engine(
    "mysql+pymysql://{}:{}@{}:{}/{}".format(SETTING['mysql']['user'], parse.unquote_plus(SETTING['mysql']['pwd']), SETTING['mysql']['host'],
                                            SETTING['mysql']['port'], SETTING['mysql']['db']), max_overflow=5)

Base = declarative_base()


class CookieConf(Base):
    __tablename__ = "cookie_conf"

    web_id = Column(Integer, primary_key=True)
    url = Column(Text)
    is_login = Column(Integer)
    content = Column(Text)
    status = Column(Integer)
    create_time = Column(TIMESTAMP)
    update_time = Column(TIMESTAMP)


Base.metadata.create_all(engine)

Mysql_Session = sessionmaker(bind=engine)

MYSQL_SESSION = Mysql_Session()
