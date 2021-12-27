"""
@author：chuanchao.peng
@date: 2021-12-07
@desc:
交易所行情数据获取采用sub/pub机制，其中CThostFtdcMdApi类实现注册事件和数据发布，
注册成功后，会调用CThostFtdcMdSpi类的相关回调函数，因此，在实现事件响应时，需要复写
CThostFtdcMdSpi类。
"""

from typing import List
from itertools import chain

from logger.logger import logger

import thostmduserapi as user_api

from settings.settings import USERINFO
from settings import configs
from ftdc import structs
from broker import Broker


class MdSPi(user_api.CThostFtdcMdSpi):
    """
    继承交易所CThostFtdcMdSpi，该class主要用于响应行情订阅事件

    Attributes:
        api: 交易所行情订阅api实例 :CThostFtdcMdApi
        userinfo: 用户信息

    Properties:
        OnFrontConnected: 当客户端与交易后台建立起通信连接时（还未登录前），该方法被调用。

        OnFrontDisconnected: 当客户端与交易后台通信连接断开时，该方法被调用。当发生这个情况后，API会自动重新连接，客户端可不做处理。

        OnHeartBeatWarning: 心跳超时警告。当长时间未收到报文时，该方法被调用。

        OnRspUserLogin: 登录请求响应.

        OnRspUserLogout: 登出请求响应.

        OnRspQryMulticastInstrument: 请求查询组播合约响应

        OnRspError: 错误应答

        OnRspSubMarketData: 订阅行情应答

        OnRspUnSubMarketData: 取消订阅行情应答

        OnRspSubForQuoteRsp: 订阅询价应答

        OnRspUnSubForQuoteRsp: 取消订阅询价应答

        OnRtnDepthMarketData: 深度行情通知

        OnRtnForQuoteRsp: 询价通知
    """

    _brokers = {}
    _subscribe = []
    _subscribed = False

    api = None

    def __init__(self):
        user_api.CThostFtdcMdSpi.__init__(self)
        self._info = configs.USER
        self.create_md_api()
        self.register_spi()
        self.register_front()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(MdSPi, cls)
            cls._instance = orig.__new__(cls)
        return cls._instance

    def create_md_api(self):
        """创建行情api"""
        self.api = user_api.CThostFtdcMdApi_CreateFtdcMdApi(f'{USERINFO}/')

    def register_spi(self):
        """注册行情回调服务"""
        self.api.RegisterSpi(self)

    def register_front(self):
        """注册行情前置服务"""
        self.api.RegisterFront(configs.MD_FRONT)

    def init(self):
        self.api.Init()

    def join(self):
        self.api.Join()

    def OnFrontConnected(self):
        """
        当客户端与交易后台建立起通信连接时（还未登录前），该方法被调用
        建立连接后开始登陆
        """
        logger.info('成功与交易所建立连接，即将进行登陆操作')
        self._login()

    def OnFrontDisconnected(self, nReason: int):
        """
        当客户端与交易后台通信连接断开时，该方法被调用。当发生这个情况后，API会自动重新连接，客户端可不做处理
        :param nReason: 错误原因 :
        0x1001 网络读失败
        0x1002 网络写失败
        0x2001 接收心跳超时
        0x2002 发送心跳失败
        0x2003 收到错误报文
        """
        logger.info(f'与交易所断开连接，错误代码 {nReason}')

    def OnHeartBeatWarning(self, nTimeLapse):
        """
        心跳超时警告。当长时间未收到报文时，该方法被调用。
        :param nTimeLapse:
        """
        logger.warning(f"长时间未接收到交易所事件通知，上次接收到报文的时间为 {nTimeLapse}")

    def OnRspUserLogin(
            self,
            pRspUserLogin: "CThostFtdcRspUserLoginField",
            pRspInfo: structs.RspInfoField,
            nRequestID: int,
            bIsLast: bool
    ):
        """
        登录请求响应
        :param pRspUserLogin: 用户登录应答，具体字段查询 ’ThostFtdcUserApiStruct.h‘
        :param pRspInfo: 登陆响应信息，包含登陆后的错误代码和错误信息
        :param nRequestID:
        :param bIsLast:
        :return:
        """
        logger.info(
            f"收到登陆请求返回信息，SessionID={pRspUserLogin.SessionID},ErrorID={pRspInfo.ErrorID},ErrorMsg={pRspInfo.ErrorMsg}"
        )
        if self._subscribed:
            return
        logger.info("登陆成功，发出订阅行情请求")
        to_sub = [x.encode('utf-8') for x in self._subscribe]
        ret = self.api.SubscribeMarketData(to_sub, len(to_sub))
        if ret != 0:
            logger.error("深度行情订阅失败，即将退出系统")
            exit(-1)

    def OnRspUserLogout(
            self,
            pUserLogout: "CThostFtdcUserLogoutField",
            pRspInfo: structs.RspInfoField,
            nRequestID: int,
            bIsLast: bool
    ):
        """
        登出请求响应
        :param pUserLogout: 用户登出请求，包含BrokerID和UserID
        :param pRspInfo: 登陆响应信息，包含登陆后的错误代码和错误信息
        :param nRequestID:
        :param bIsLast:
        :return:
        """
        print('log out')
        logger.info(
            f"收到登出请求返回信息，UserID={pUserLogout.UserID},ErrorID={pRspInfo.ErrorID},ErrorMsg={pRspInfo.ErrorMsg}"
        )
        self.unsubscribe_data()

    def OnRspQryMulticastInstrument(
            self,
            pMulticastInstrument: "CThostFtdcMulticastInstrumentField",
            pRspInfo: "CThostFtdcRspInfoField",
            nRequestID: int,
            bIsLast: bool
    ):
        """
        请求查询组播合约响应
        :param pMulticastInstrument:
        :param pRspInfo:
        :param nRequestID:
        :param bIsLast:
        :return:
        """
        logger.info('OnRspQryMulticastInstrument')

    def OnRspError(self, pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool):
        """
        错误应答, 当事件返回不正确时，调用
        :param pRspInfo:
        :param nRequestID:
        :param bIsLast:
        """
        logger.info(
            f"收到错误应答，UserID={pUserLogout.UserID},ErrorID={pRspInfo.ErrorID},ErrorMsg={pRspInfo.ErrorMsg}"
        )

    def OnRspSubMarketData(
            self,
            pSpecificInstrument: "CThostFtdcSpecificInstrumentField",
            pRspInfo: structs.RspInfoField,
            nRequestID: int,
            bIsLast: bool
    ):
        """
        订阅行情应答
        :param pSpecificInstrument:
        :param pRspInfo:
        :param nRequestID:
        :param bIsLast:
        :return:
        """
        error_id = pRspInfo.ErrorID
        if error_id != 0:
            logger.error(f"行情订阅失败,InstrumentID={pSpecificInstrument.InstrumentID},ErrorMsg={pRspInfo.ErrorMsg}")
            return
        logger.info(f"行情订阅成功,InstrumentID={pSpecificInstrument.InstrumentID}")
        self._subscribed = True

    def OnRspUnSubMarketData(
            self,
            pSpecificInstrument: "CThostFtdcSpecificInstrumentField",
            pRspInfo: structs.RspInfoField,
            nRequestID: int,
            bIsLast: bool
    ):
        """取消订阅行情数据"""
        logger.info("取消订阅")

    def OnRspSubForQuoteRsp(
            self,
            pSpecificInstrument: "CThostFtdcSpecificInstrumentField",
            pRspInfo: structs.RspInfoField,
            nRequestID: int,
            bIsLast: bool
    ):
        """订阅询价应答"""
        logger.info("订阅询价")

    def OnRspUnSubForQuoteRsp(
            self,
            pSpecificInstrument: "CThostFtdcSpecificInstrumentField",
            pRspInfo: structs.RspInfoField,
            nRequestID: int,
            bIsLast: bool
    ):
        """订阅询价应答"""
        logger.info("取消订阅询价")

    def OnRtnDepthMarketData(self, pDepthMarketData: structs.DepthMarketDataField):
        """
        深度行情通知
        :param pDepthMarketData: 本身为CThostFtdcDepthMarketDataField类
        """
        data = {x: getattr(pDepthMarketData, x) for x in structs.DepthMarketDataField._fields}
        self._publish(data)

    def OnRtnForQuoteRsp(self, pForQuoteRsp: "CThostFtdcForQuoteRspField"):
        """
        询价通知
        :param pForQuoteRsp:
        """
        logger.info("询价通知")

    def _login(self):
        """登陆"""
        login_field: "CThostFtdcReqUserLoginField" = user_api.CThostFtdcReqUserLoginField()
        login_field.BrokerID = self._info.BrokerID
        login_field.UserID = self._info.UserID
        login_field.Password = self._info.Password
        login_field.UserProductInfo = "python dll"
        ret = self.api.ReqUserLogin(login_field, 0)
        if ret == 0:
            logger.info("登陆请求发送成功")
        else:
            logger.error("登陆请求发送失败")

    def _publish(self, data):
        """
        处理数据
        """
        for name, broker in self._brokers.items():
            broker.do(data)

    def register_broker(self, name: str, broker: Broker):
        """注册broker，用户处理数据"""
        self._brokers[name] = broker
        logger.info(f"数据处理Broker {name} 挂载成功")

    def set_contracts(self, contracts: List[str]):
        self._subscribe = chain.from_iterable([self._subscribe, contracts])

    def unsubscribe_data(self):
        """主动取消订阅数据"""
        to_unsub = [x.encode('utf-8') for x in self._subscribe]
        self.api.UnSubscribeMarketData(to_unsub, len(to_unsub))

    def logout(self):
        logout_field = user_api.CThostFtdcUserLogoutField()
        logout_field.BrokerId = self._info.BrokerID
        logout_field.UserID = self._info.UserID
        self.api.ReqUserLogout(logout_field, 0)
        logger.info('已发出退出登录请求')
