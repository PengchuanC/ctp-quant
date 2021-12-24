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
class SettlementInfoField(object):
    """投资者结算结果"""
    TradingDay: str
    SettlementID: str
    BrokerID: str
    InvestorID: str
    SequenceNo: str
    Content: str
    AccountID: str
    CurrencyID: str


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
    PosiDirection: str  # 持仓多空方向 净 1, 多头 2, 空头 3
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


@dataclass
class InstrumentField(object):
    """合约"""
    InstrumentID: str  # 合约代码
    ExchangeID: str  # 交易所代码
    InstrumentName: str  # 合约名称
    ExchangeInstID: str  # 合约在交易所的代码
    ProductID: str  # 产品代码
    ProductClass: str  # 产品类型
    DeliveryYear: int  # 交割年份
    DeliveryMonth: int  # 交割月
    MaxMarketOrderVolume: int  # 市价单最大下单量
    MinMarketOrderVolume: int  # 市价单最小下单量
    MaxLimitOrderVolume: int  # 限价单最大下单量
    MinLimitOrderVolume: int  # 限价单最小下单量
    VolumeMultiple: int  # 合约数量乘数
    PriceTick: float  # 最小变动价位
    CreateDate: str  # 创建日
    OpenDate: str  # 上市日
    ExpireDate: str  # 到期日
    StartDelivDate: str  # 开始交割日
    EndDelivDate: str  # 结束交割日
    InstLifePhase: str  # 合约生命周期状态
    IsTrading: int  # 当前是否交易
    PositionType: str  # 持仓类型
    PositionDateType: str  # 持仓日期类型
    LongMarginRatio: float  # 多头保证金率
    ShortMarginRatio: float  # 空头保证金率
    MaxMarginSideAlgorithm: str  # 是否使用大额单边保证金算法
    UnderlyingInstrID: str  # 基础商品代码
    StrikePrice: float  # 执行价
    OptionsType: str  # 期权类型
    UnderlyingMultiple: float  # 合约基础商品乘数
    CombinationType: str  # 组合类型


@dataclass
class DepthMarketDataField(object):
    """深度行情"""
    TradingDay: str  # 交易日
    InstrumentID: str  # 合约代码
    ExchangeID: str  # 交易所代码
    ExchangeInstID: str  # 合约在交易所的代码
    LastPrice: float  # 最新价
    PreSettlementPrice: float  # 上次结算价
    PreClosePrice: float  # 昨收盘
    PreOpenInterest: int  # 昨持仓量
    OpenPrice: float  # 今开盘
    HighestPrice: float  # 最高价
    LowestPrice: float  # 最低价
    Volume: int  # 数量
    Turnover: float  # 成交金额
    OpenInterest: float  # 持仓量
    ClosePrice: float  # 今收盘
    SettlementPrice: float  # 本次结算价
    UpperLimitPrice: float  # 涨停板价
    LowerLimitPrice: float  # 跌停板价
    PreDelta: float  # 昨虚实度
    CurrDelta: float  # 今虚实度
    UpdateTime: str  # 最后修改时间
    UpdateMillisec: str  # 最后修改毫秒
    BidPrice1: float  # 申买价一
    BidVolume1: int  # 申买量一
    AskPrice1: float  # 申卖价一
    AskVolume1: int  # 申卖量一
    BidPrice2: float  # 申买价二
    BidVolume2: int  # 申买量二
    AskPrice2: float  # 申卖价二
    AskVolume2: int  # 申卖量二
    BidPrice3: float  # 申买价三
    BidVolume3: int  # 申买量三
    AskPrice3: float  # 申卖价三
    AskVolume3: int  # 申卖量三
    BidPrice4: float  # 申买价四
    BidVolume4: int  # 申买量四
    AskPrice4: float  # 申卖价四
    AskVolume4: int  # 申卖量四
    BidPrice5: float  # 申买价五
    BidVolume5: int  # 申买量五
    AskPrice5: float  # 申卖价五
    AskVolume5: int  # 申卖量五
    AveragePrice: float  # 当日均价
    ActionDay: str  # 业务日期
