"""
@author: chuanchao.peng
@date: 2021/12/21 15:01
@file database_dispatcher.py
@desc:
数据保存
"""

from disptach import DatabaseDispatcher
from broker import RedisBrokerConfig


if __name__ == '__main__':
    cfg = RedisBrokerConfig('10.170.139.12')
    rd = DatabaseDispatcher(cfg)
    rd.dispatch()
