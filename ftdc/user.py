"""
@author：chuanchao.peng
@date: 2021-12-07
@desc:
交易所行情数据获取采用sub/pub机制，其中CThostFtdcMdApi类实现注册事件和数据发布，
注册成功后，会调用CThostFtdcMdSpi类的相关回调函数，因此，在实现事件响应时，需要复写
CThostFtdcMdSpi类。
"""

from logger.logger import logger

import thostmduserapi as user_api

from ftdc import structs
from broker import Broker


class MdUserApi(user_api.CThostFtdcMdSpi):
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

    def __init__(self, api: "CThostFtdcMdApi", userinfo: structs.UserLoginField):
        user_api.CThostFtdcMdSpi.__init__(self)
        self._api = api
        self._info = userinfo

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
        logger.info("登陆成功，发出订阅行情请求")
        ret = self._api.SubscribeMarketData(["cu2201".encode('utf-8')], 1)
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
        logger.info(
            f"收到登出请求返回信息，UserID={pUserLogout.UserID},ErrorID={pRspInfo.ErrorID},ErrorMsg={pRspInfo.ErrorMsg}"
        )
        self._api.UnSubscribeMarketData(["cu2201".encode('utf-8')], 1)

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
        pass

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
        # TODO 对数据进行处理，如保存到数据库，推送到其他客户端或传输到redis进行处理
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
        ret = self._api.ReqUserLogin(login_field, 0)
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

    def register(self, name: str, broker: Broker):
        """注册broker，用户处理数据"""
        self._brokers[name] = broker
        logger.info(f"数据处理Broker {name} 挂载成功")