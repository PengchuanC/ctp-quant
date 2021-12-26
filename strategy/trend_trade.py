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

    @staticmethod
    def macd(data, short: int, long: int, length: int):
        """计算MACD"""
        return MACD(data).macd(short, long, length)

    def trade(self) -> Generator[order.InputOrderField]:
        """生成交易指令"""
        yield order.InputOrderField
