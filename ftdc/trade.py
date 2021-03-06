"""
@author: chuanchao.peng
@date: 2021/12/20 16:57
@file trade.py
@desc:
封装常用下单操作
"""

import thosttraderapi as trader_api

from ftdc import structs, order, datatype, qry


class TradeMethod(object):
    def __init__(self, userinfo: qry.ReqUserLoginField):
        self.userinfo = userinfo

    def _gen_order(self, instrument, exchange, price, volume, direction, offset):
        """
        生成交易指令
        Args:
            instrument: 品种
            exchange: 交易所
            price: 价格
            volume: 数量
            direction: 方向
            offset: 开平标识
        """
        input_order: order.InputOrderField = trader_api.CThostFtdcInputOrderField()
        input_order.BrokerID = self.userinfo.BrokerID
        input_order.UserID = self.userinfo.UserID
        input_order.InvestorID = self.userinfo.UserID
        input_order.OrderRef = "1"
        input_order.OrderPriceType = datatype.OrderPriceType.limit_price  # 价格条件，默认限价
        input_order.ContingentCondition = datatype.ContingentConditionType.immediately
        input_order.TimeCondition = datatype.TimeConditionType.gfd
        input_order.VolumeCondition = datatype.VolumeConditionType.av
        input_order.CombHedgeFlag = datatype.ExClientIDType.hedge
        input_order.MinVolume = 0
        input_order.ForceCloseReason = trader_api.THOST_FTDC_FCC_NotForceClose
        input_order.IsAutoSuspend = 0

        input_order.Direction = direction  # 买或卖
        input_order.InstrumentID = instrument
        input_order.ExchangeID = exchange
        input_order.LimitPrice = price
        input_order.VolumeTotalOriginal = volume
        input_order.CombOffsetFlag = offset  # 开或平
        return input_order

    def buy_open(self, instrument, exchange, price, volume):
        """
        买开，开多
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
        卖开，开空
        """
        return self._gen_order(
            instrument, exchange, price, volume, datatype.DirectionType.sell, datatype.OffsetFlagType.open
        )

    def buy_close(self, instrument, exchange, price, volume):
        """买平，平空"""
        return self._gen_order(
            instrument, exchange, price, volume, datatype.DirectionType.buy, datatype.OffsetFlagType.close
        )

    def sell_close(self, instrument, exchange, price, volume):
        """卖平，平多"""
        return self._gen_order(
            instrument, exchange, price, volume, datatype.DirectionType.sell, datatype.OffsetFlagType.close
        )
