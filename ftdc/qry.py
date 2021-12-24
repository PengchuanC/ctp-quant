"""
@author: chuanchao.peng
@date: 2021/12/23 13:54
@file qry.py
@desc:
封装api请求结构体，使用dataclass
"""

from dataclasses import dataclass


@dataclass
class ReqUserLoginField(object):
    """用户登录请求"""
    BrokerID: str
    UserID: str
    Password: str
    TradingDay: str = None
    UserProductInfo: str = "python dll"
    InterfaceProductInfo: str = None
    ProtocolInfo: str = None
    MacAddress: str = None
    OneTimePassword: str = None
    ClientIPAddress: str = None
    LoginRemark: str = None
    ClientIPPort: int = None


@dataclass
class ReqAuthenticateField(object):
    """客户端认证请求"""
    BrokerID: str
    UserID: str
    AuthCode: str
    AppID: str
    UserProductInfo: str = "python dll"


@dataclass
class QrySettlementInfoField(object):
    """查询投资者结算结果"""
    BrokerID: str
    InvestorID: str
    AccountID: str
    TradingDay: str
    CurrencyID: str


class QrySettlementInfoConfirmField(QrySettlementInfoField):
    """查询结算信息确认域"""
    pass


@dataclass
class QryInvestorPositionField(object):
    """查询投资者持仓"""
    BrokerID: str
    InvestorID: str
    InstrumentID: str
    ExchangeID: str
    InvestUnitID: str = None


@dataclass
class QryInstrumentField(object):
    """查询合约"""
    InstrumentID: str
    ExchangeID: str
    ExchangeInstID: str = None  # 合约在交易所的代码
    ProductID: str = None  # 产品代码


@dataclass
class QryDepthMarketDataField(object):
    """查询行情"""
    InstrumentID: str
    ExchangeID: str
