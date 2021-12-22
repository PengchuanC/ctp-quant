"""
@author: chuanchao.peng
@date: 2021/12/22 11:00
@file example.py
@desc:
策略示例，主要展示api调用
模拟一个简单策略：判断当前涨跌幅，如果当前上涨幅度小于2%，则开一个多单，然后半小时后平掉
"""

import arrow

from broker import RedisBrokerConfig
from disptach import MemoryDispatcher
from ftdc.trade import TradeMethod
from ftdc.structs import UserLoginField
from ftdc import datatype


class StrategyExample(object):
    close_time = None

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
            print(quote)
            if self.close_time:
                now = arrow.now()
                if now >= self.close_time:
                    lower = float(quote['lower'])
                    order = self.tm.sell_close(self.contract, 'SHFE', lower, 1)
                    order.CombOffsetFlag = OffsetFlagType.close_today
                    return order
                continue
            upper = float(quote['upper'])  # 涨停价
            chg = float(quote['close']) / float(quote['low']) - 1
            if chg <= 0.02:
                order = self.tm.buy_open(self.contract, 'SHFE', upper, 1)
                now = arrow.now()
                self.close_time = now.shift(minutes=30)
                yield order
