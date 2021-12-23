"""
@author: chuanchao.peng
@date: 2021/12/23 14:07
@file trader.py
@desc:
"""

from dataclasses import asdict
from queue import Queue
from threading import Event

import thosttraderapi as trader_api

from ftdc import rsp, qry, order
from trader.base import BaseTradeBroker
from logger.logger import logger


class TraderSpi(trader_api.CThostFtdcTraderSpi):

    queue = Queue()
    event = Event()
    # 交易api
    t_api = None
    # 响应处理
    tb: BaseTradeBroker = None
    auth = None
    user = None

    def register_broker(self, broker: BaseTradeBroker):
        """添加响应应答类"""
        self.tb = broker

    def create_trader_api(self, path: str):
        """创建交易api"""
        self.t_api = trader_api.CThostFtdcTraderApi_CreateFtdcTraderApi(f'{path}/')

    def register_front(self, front_address: str):
        """注册交易接口"""
        self.t_api.RegisterFront(front_address)

    def register_spi(self):
        """注册交易回调Spi"""
        self.t_api.RegisterSpi(self)

    def get_tradingday(self):
        return self.t_api.GetTradingDay()

    def init(self):
        """初始化交易接口和broker"""
        self.t_api.Init()
        self.tb.register_spi(self)

    def join(self):
        self.t_api.Join()

    def execute_waited(self):
        """执行排队中的任务"""
        if not self.queue.empty():
            call, args = self.queue.get()
            call(*args)

    def trade(self, order_info: order.InputOrderField):
        """执行下单指令"""
        # 执行下单前，需等待上一单完成
        self.event.wait()
        self.t_api.ReqOrderInsert(order_info, 0)

    def req_authenticate(self, pReqAuthenticateField: qry.ReqAuthenticateField, nRequestID: int = 0):
        """客户端认证请求"""
        auth_field: qry.ReqAuthenticateField = trader_api.CThostFtdcReqAuthenticateField()
        auth_field.BrokerID = pReqAuthenticateField.BrokerID
        auth_field.UserID = pReqAuthenticateField.UserID
        auth_field.AppID = pReqAuthenticateField.AppID
        auth_field.AuthCode = pReqAuthenticateField.AuthCode
        self.auth = pReqAuthenticateField
        self.queue.put((self.t_api.ReqAuthenticate, (auth_field, nRequestID)))

    def req_user_login(self, pReqUserLoginField: qry.ReqUserLoginField, nRequestID: int = 0):
        """用户登陆"""
        login_field: qry.ReqUserLoginField = trader_api.CThostFtdcReqUserLoginField()
        login_field.BrokerID = pReqUserLoginField.BrokerID
        login_field.UserID = pReqUserLoginField.UserID
        login_field.Password = pReqUserLoginField.Password
        login_field.UserProductInfo = pReqUserLoginField.UserProductInfo
        self.user = pReqUserLoginField
        self.queue.put((self.t_api.ReqUserLogin, (login_field, nRequestID)))

    def req_qry_settlement_info_confirm(self, nRequestID: int = 0):
        """请求查询结算信息确认"""
        info: qry.QrySettlementInfoConfirmField = trader_api.CThostFtdcQrySettlementInfoConfirmField()
        info.BrokerID = self.user.BrokerID
        info.InvestorID = self.user.UserID
        info.AccountID = self.user.UserID
        self.queue.put((self.t_api.ReqQrySettlementInfoConfirm, (info, nRequestID)))

    def qry_investor_position(self, instrument_id: str, exchange_id: str):
        """查询投资者持仓明细"""
        logger.info(f'api-持仓查询,InstrumentID={instrument_id},ExchangeID={exchange_id}')
        field: qry.QryInvestorPositionField = trader_api.CThostFtdcQryInvestorPositionField()
        field.BrokerID = self.user.BrokerID
        field.InvestorID = self.user.UserID
        field.ExchangeID = exchange_id
        field.InstrumentID = instrument_id
        self.t_api.ReqQryInvestorPosition(field, 0)

    def OnFrontConnected(self):
        """当客户端与交易后台建立起通信连接时（还未登录前），该方法被调用。"""
        logger.info(f'spi-交易服务器已连接,即将进行客户端认证')
        self.tb.on_connected()

    def OnFrontDisconnected(self, nReason: int):
        """
        当客户端与交易后台通信连接断开时，该方法被调用。当发生这个情况后，API会自动重新连接，客户端可不做处理。
        :param nReason:
        """
        self.tb.on_disconnect(nReason)

    def OnRspQrySettlementInfoConfirm(
            self, pSettlementInfoConfirm: rsp.SettlementInfoConfirmField,
            pRspInfo: rsp.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """请求查询结算信息确认响应"""
        self.tb.on_settement_confirm(pSettlementInfoConfirm)

    def OnRspUserLogin(
            self, pRspUserLogin: rsp.RspUserLoginField, pRspInfo: rsp.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """登录请求响应"""
        self.tb.on_login(pRspUserLogin)

    def OnRspAuthenticate(
            self,
            pRspAuthenticateField: "CThostFtdcRspAuthenticateField",
            pRspInfo: rsp.RspInfoField,
            nRequestID: int,
            bIsLast: bool
    ):
        """客户端认证响应"""
        if pRspInfo.ErrorID != 0:
            logger.error(f'spi-客户端认证失败,ErrorMsg={pRspInfo.ErrorMsg}')
            return
        self.tb.on_authenticate(pRspAuthenticateField)

    def OnRtnOrder(self, pOrder: order.OrderField):
        """报单通知"""
        self.tb.on_order(pOrder)

    def OnRtnTrade(self, pTrade: order.TraderField):
        """成交通知"""
        self.tb.on_trade(pTrade)

    def OnErrRtnOrderInsert(self, pInputOrder: order.InputOrderField, pRspInfo: rsp.RspInfoField):
        """报单录入错误回报"""
        logger.info(f'spi-报单录入错误,OnErrRtnOrderInsert')
        self.event.set()
        self.tb.on_order_err(pInputOrder)

    def OnRspQryInvestorPosition(
            self, pInvestorPosition: rsp.InvestorPositionField,
            pRspInfo: rsp.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """请求查询投资者持仓响应"""
        self.tb.on_investor_position(pInvestorPosition)
