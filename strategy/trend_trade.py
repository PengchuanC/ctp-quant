"""
trend_trade
~~~~~~~~~~~~~~~~
@author: chuanchao.peng
@date: 2021/12/26
@desc:
"""

from typing import Generator

import arrow

from broker import RedisBrokerConfig
from disptach import MemoryDispatcher
from ftdc.trade import TradeMethod
from ftdc import datatype, qry, order


def market_data(config: RedisBrokerConfig):
    md = MemoryDispatcher(config=config)
    for i in md.dispatch():
        yield i


class MACD(object):
    """计算MACD指标"""

    _ema_data = None

    def __init__(self, data):
        self.d = data

    def _ema(self, count):
        if count == 1:
            return self._ema_data[count - 1]
        return self._ema_data[count - 1] * (2 / (count + 1)) + self.ema(count - 1) * (1 - 2 / (count + 1))

    def ema(self, count):
        """计算ema指标
            args:
                count: 周期长度
        """
        self._ema_data = self.d[-count:]
        return self._ema(count)

    def diff(self, short: int, long: int):
        return self.ema(short) - self.ema(long)

    def dea(self, short: int, long: int, length: int):
        """计算dea
            Args:
                short: 快线周期数
                long: 慢线周期数
                length: 平均线周期数
        """
        ds = []
        for lgh in range(length):
            end = length - lgh
            data = self.d[:end]
            macd = MACD(data)
            diff = macd.diff(short, long)
            ds.append(diff)
        dea = sum(ds) / length
        return dea

    def macd(self, short: int, long: int, length: int):
        return 2 * (self.diff(short, long) - self.dea(short, long, length))


class TrendTradeStrategy(object):
    """cta策略"""
    _data = []

    def __init__(self, dp_config: RedisBrokerConfig, contract: str):
        self.md = market_data(dp_config)
        self.contract = contract

    @staticmethod
    def macd(data, short: int, long: int, length: int):
        """计算MACD"""
        return MACD(data).macd(short, long, length)

    def strategy(self, short: int, long: int, length: int):
        if len(self._data) < long:
            return
        else:
            self._data = self._data[-long:]
        return self.macd(self._data, short, long, length)

    def trade(self, short: int, long: int, length: int):
        """生成交易指令"""
        for quote in self.md:
            if quote['instrument_id'] != self.contract:
                continue
            self._data.append(float(quote['close']))
            macd = self.strategy(short, long, length)
            print("macd", macd)
            if macd:
                yield macd
