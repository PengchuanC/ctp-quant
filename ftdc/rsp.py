"""
@author: chuanchao.peng
@date: 2021/12/23 13:54
@file rsp.py
@desc:
封装api响应结构体
"""

from dataclasses import dataclass


@dataclass
class RspInfoField(object):
    """响应信息"""
    ErrorID: int
    ErrorMsg: str


@dataclass
class RspUserLoginField(object):
    """用户登录应答"""
    TradingDay: str
    LoginTime: str
    BrokerID: int
    UserID: int
    SystemName: str  # 交易系统名称
    FrontID: int  # 前置编号
    SessionID: int  # 会话编号
    MaxOrderRef: str  # 最大报单引用
    SHFETime: str  # 上期所时间
    DCETime: str  # 大商所时间
    CZCETime: str  # 郑商所时间
    FFEXTime: str  # 中金所时间
    INETime: str  # 能源中心时间


@dataclass
class SettlementInfoConfirmField(object):
    """投资者结算结果确认信息"""
    BrokerID: int  # 经纪公司代码
    InvestorID: int  # 投资者代码
    ConfirmDate: str  # 确认日期
    ConfirmTime: str  # 确认时间
    SettlementID: int  # 结算编号
    AccountID: str  # 投资者账号
    CurrencyID: str  # 币种代码


@dataclass
class InvestorPositionField(object):
    """投资者持仓"""
    InstrumentID: str  # 合约代码
    BrokerID: str  # 经纪公司代码
    InvestorID: str  # 投资者代码
    PosiDirection: str  # 持仓多空方向
    HedgeFlag: str  # 投机套保标志
    PositionDate: str  # 持仓日期
    YdPosition: int  # 上日持仓
    Position: int  # 今日持仓
    LongFrozen: int  # 多头冻结
    ShortFrozen: int  # 空头冻结
    LongFrozenAmount: int  # 开仓冻结金额
    ShortFrozenAmount: int  # 开仓冻结金额
    OpenVolume: int  # 开仓量
    CloseVolume: int  # 平仓量
    OpenAmount: int  # 开仓金额
    CloseAmount: int  # 平仓金额
    PositionCost: int  # 持仓成本
    PreMargin: int  # 上次占用的保证金
    UseMargin: int  # 占用的保证金
    FrozenMargin: int  # 冻结的保证金
    FrozenCash: int  # 冻结的资金
    FrozenCommission: int  # 冻结的手续费
    CashIn: int  # 资金差额
    Commission: int  # 手续费
    CloseProfit: int  # 平仓盈亏
    PositionProfit: int  # 持仓盈亏
    PreSettlementPrice: int  # 上次结算价
    SettlementPrice: int  # 本次结算价
    TradingDay: str  # 交易日
    SettlementID: str  # 结算编号
    OpenCost: int  # 开仓成本
    ExchangeMargin: int  # 交易所保证金
    CombPosition: int  # 组合成交形成的持仓
    CombLongFrozen: int  # 组合多头冻结
    CombShortFrozen: int  # 组合空头冻结
    CloseProfitByDate: int  # 逐日盯市平仓盈亏
    CloseProfitByTrade: int  # 逐笔对冲平仓盈亏
    TodayPosition: int  # 今日持仓
    MarginRateByMoney: int  # 保证金率
    MarginRateByVolume: int  # 保证金率(按手数)
    StrikeFrozen: int  # 执行冻结
    StrikeFrozenAmount: int  # 执行冻结金额
    AbandonFrozen: int  # 放弃执行冻结
    ExchangeID: str  # 交易所代码
    YdStrikeFrozen: int  # 执行冻结的昨仓
    InvestUnitID: str  # 投资单元代码
    PositionCostOffset: int  # 大商所持仓成本差值，只有大商所使用
    TasPosition: int  # tas持仓手数
    TasPositionCost: int  # tas持仓成本
