"""
@author: chuanchao.peng
@date: 2021/12/20 18:23
@desc:
"""

from peewee import SqliteDatabase

from settings.settings import USERINFO


sqlite_db = SqliteDatabase(USERINFO / 'ctp-quant.db')


# 输出数据库引擎，默认使用sqlite
db = sqlite_db

__all__ =('db',)
