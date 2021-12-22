"""
@author: chuanchao.peng
@date: 2021/12/22 11:00
@file example.py
@desc:
策略示例，主要展示api调用
"""
import time

from broker import RedisBrokerConfig
from disptach import MemoryDispatcher
from ftdc.trade import TradeMethod
from ftdc.structs import UserLoginField


class StrategyExample(object):
    max_limit = 0

    def __init__(self, user: UserLoginField, redis_config: RedisBrokerConfig, contract_id: str):
        self.contract = contract_id
        self.dispatcher = MemoryDispatcher(redis_config)
        self.tm = TradeMethod(user)

    def query_quote(self):
        """查询行情，注意会进入事件循环"""
        for quote in self.dispatcher.dispatch():
            if self.contract == quote['instrument_id']:
                yield quote

    def trade(self):
        for quote in self.query_quote():
            # 仅允许下2单
            if self.max_limit >= 2:
                break
            # 下单
            upper = float(quote['upper'])  # 涨停价
            order = self.tm.buy_open(self.contract, 'SHFE', upper, 1)
            self.max_limit += 1
            yield order
            time.sleep(60*30)
