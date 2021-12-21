"""
@author: chuanchao.peng
@date: 2021/12/20 16:57
@file trade.py
@desc:
封装常用下单操作
"""

import thosttraderapi as trader_api

from ftdc import structs, order, datatype


class TradeMethod(object):
    def __init__(self, userinfo: structs.UserLoginField):
        input_order: order.InputOrderField = trader_api.CThostFtdcInputOrderField()
        input_order.BrokerID = userinfo.BrokerID
        input_order.UserID = userinfo.UserID
        input_order.InvestorID = userinfo.UserID
        input_order.OrderPriceType = datatype.OrderPriceType.limit_price
        input_order.ContingentCondition = datatype.ContingentConditionType.immediately
        input_order.TimeCondition = datatype.TimeConditionType.gfd
        input_order.VolumeCondition = datatype.VolumeConditionType.av
        input_order.CombHedgeFlag = datatype.ExClientIDType.hedge
        input_order.MinVolume = 0
        input_order.ForceCloseReason = trader_api.THOST_FTDC_FCC_NotForceClose
        input_order.IsAutoSuspend = 0
        self.order = input_order

    def _gen_order(self, instrument, exchange, price, volume, operation, offset):
        """
        生成交易指令
        Args:
            instrument: 品种
            exchange: 交易所
            price: 价格
            volume: 数量
            operation: 方向
            offset: 开平标识
        """
        _order: order.InputOrderField = self.order
        _order.Direction = operation
        _order.InstrumentID = instrument
        _order.ExchangeID = exchange
        _order.LimitPrice = price
        _order.VolumeTotalOriginal = volume
        _order.CombOffsetFlag = offset
        return _order

    def buy_open(self, instrument, exchange, price, volume):
        """
        开多
        Args:
            instrument: 品种
            exchange: 交易所
            price: 价格
            volume: 数量
        """
        return self._gen_order(
            instrument, exchange, price, volume, datatype.DirectionType.buy, datatype.OffsetFlagType.open
        )

    def sell_open(self, instrument, exchange, price, volume):
        """
        开空
        """
        return self._gen_order(
            instrument, exchange, price, volume, datatype.DirectionType.sell, datatype.OffsetFlagType.open
        )

    def buy_close(self, instrument, exchange, price, volume):
        """平多"""
        return self._gen_order(
            instrument, exchange, price, volume, datatype.DirectionType.buy, datatype.OffsetFlagType.close
        )

    def sell_close(self, instrument, exchange, price, volume):
        """平空"""
        return self._gen_order(
            instrument, exchange, price, volume, datatype.DirectionType.sell, datatype.OffsetFlagType.close
        )