from collections import namedtuple

# 用户数据结构 类比CThostFtdcReqUserLoginField
UserLoginField = namedtuple('UserLoginField', ['BrokerID', 'UserID', 'Password'])

# 客户端认证请求，在交易登陆前调用，认证客户端
"""
///客户端认证请求
struct CThostFtdcReqAuthenticateField
{
    ///经纪公司代码
    TThostFtdcBrokerIDType	BrokerID;
    ///用户代码
    TThostFtdcUserIDType	UserID;
    ///用户端产品信息
    TThostFtdcProductInfoType	UserProductInfo;
    ///认证码
    TThostFtdcAuthCodeType	AuthCode;
    ///App代码
    TThostFtdcAppIDType	AppID;
};
"""
ReqAuthenticateField = namedtuple(
    "CThostFtdcReqAuthenticateField", ["BrokerID", "UserID", "UserProductInfo", "AuthCode", "AppID"]
)

# 深度行情
"""
///深度行情
struct CThostFtdcDepthMarketDataField
{
    ///交易日
    TThostFtdcDateType	TradingDay;
    ///合约代码
    TThostFtdcInstrumentIDType	InstrumentID;
    ///交易所代码
    TThostFtdcExchangeIDType	ExchangeID;
    ///合约在交易所的代码
    TThostFtdcExchangeInstIDType	ExchangeInstID;
    ///最新价
    TThostFtdcPriceType	LastPrice;
    ///上次结算价
    TThostFtdcPriceType	PreSettlementPrice;
    ///昨收盘
    TThostFtdcPriceType	PreClosePrice;
    ///昨持仓量
    TThostFtdcLargeVolumeType	PreOpenInterest;
    ///今开盘
    TThostFtdcPriceType	OpenPrice;
    ///最高价
    TThostFtdcPriceType	HighestPrice;
    ///最低价
    TThostFtdcPriceType	LowestPrice;
    ///数量
    TThostFtdcVolumeType	Volume;
    ///成交金额
    TThostFtdcMoneyType	Turnover;
    ///持仓量
    TThostFtdcLargeVolumeType	OpenInterest;
    ///今收盘
    TThostFtdcPriceType	ClosePrice;
    ///本次结算价
    TThostFtdcPriceType	SettlementPrice;
    ///涨停板价
    TThostFtdcPriceType	UpperLimitPrice;
    ///跌停板价
    TThostFtdcPriceType	LowerLimitPrice;
    ///昨虚实度
    TThostFtdcRatioType	PreDelta;
    ///今虚实度
    TThostFtdcRatioType	CurrDelta;
    ///最后修改时间
    TThostFtdcTimeType	UpdateTime;
    ///最后修改毫秒
    TThostFtdcMillisecType	UpdateMillisec;
    ///申买价一
    TThostFtdcPriceType	BidPrice1;
    ///申买量一
    TThostFtdcVolumeType	BidVolume1;
    ///申卖价一
    TThostFtdcPriceType	AskPrice1;
    ///申卖量一
    TThostFtdcVolumeType	AskVolume1;
    ///申买价二
    TThostFtdcPriceType	BidPrice2;
    ///申买量二
    TThostFtdcVolumeType	BidVolume2;
    ///申卖价二
    TThostFtdcPriceType	AskPrice2;
    ///申卖量二
    TThostFtdcVolumeType	AskVolume2;
    ///申买价三
    TThostFtdcPriceType	BidPrice3;
    ///申买量三
    TThostFtdcVolumeType	BidVolume3;
    ///申卖价三
    TThostFtdcPriceType	AskPrice3;
    ///申卖量三
    TThostFtdcVolumeType	AskVolume3;
    ///申买价四
    TThostFtdcPriceType	BidPrice4;
    ///申买量四
    TThostFtdcVolumeType	BidVolume4;
    ///申卖价四
    TThostFtdcPriceType	AskPrice4;
    ///申卖量四
    TThostFtdcVolumeType	AskVolume4;
    ///申买价五
    TThostFtdcPriceType	BidPrice5;
    ///申买量五
    TThostFtdcVolumeType	BidVolume5;
    ///申卖价五
    TThostFtdcPriceType	AskPrice5;
    ///申卖量五
    TThostFtdcVolumeType	AskVolume5;
    ///当日均价
    TThostFtdcPriceType	AveragePrice;
    ///业务日期
    TThostFtdcDateType	ActionDay;
};
"""
DepthMarketDataField = namedtuple(
    "DepthMarketDataField",
    [
        "TradingDay", "InstrumentID", "ExchangeID", "ExchangeInstID", "LastPrice", "PreSettlementPrice",
        "PreClosePrice", "PreOpenInterest", "OpenPrice", "HighestPrice", "LowestPrice", "Volume", "Turnover",
        "OpenInterest", "ClosePrice", "SettlementPrice", "UpperLimitPrice", "LowerLimitPrice", "PreDelta",
        "CurrDelta", "UpdateTime", "UpdateMillisec", "BidPrice1", "BidVolume1", "AskPrice1", "AskVolume1",
        "BidPrice2", "BidVolume2", "AskPrice2", "AskVolume2", "BidPrice3", "BidVolume3", "AskPrice3", "AskVolume3",
        "BidPrice4", "BidVolume4", "AskPrice4", "AskVolume4", "BidPrice5", "BidVolume5", "AskPrice5", "AskVolume5",
        "AveragePrice", "ActionDay"
    ]
)

# 响应信息
"""
struct CThostFtdcRspInfoField
{
    ///错误代码
    TThostFtdcErrorIDType	ErrorID;
    ///错误信息
    TThostFtdcErrorMsgType	ErrorMsg;
};
"""
RspInfoField = namedtuple("CThostFtdcRspInfoField", ["ErrorID", "ErrorMsg"])

# 查询投资者结算结果
"""
///查询投资者结算结果
struct CThostFtdcQrySettlementInfoField
{
    ///经纪公司代码
    TThostFtdcBrokerIDType	BrokerID;
    ///投资者代码
    TThostFtdcInvestorIDType	InvestorID;
    ///交易日
    TThostFtdcDateType	TradingDay;
    ///投资者帐号
    TThostFtdcAccountIDType	AccountID;
    ///币种代码
    TThostFtdcCurrencyIDType	CurrencyID;
};
"""
QrySettlementInfoField = namedtuple(
    "CThostFtdcQrySettlementInfoField", ["BrokerID", "InvestorID", "TradingDay", "AccountID", "CurrencyID"]
)

# 投资者结算结果
"""
///投资者结算结果
struct CThostFtdcSettlementInfoField
{
    ///交易日
    TThostFtdcDateType	TradingDay;
    ///结算编号
    TThostFtdcSettlementIDType	SettlementID;
    ///经纪公司代码
    TThostFtdcBrokerIDType	BrokerID;
    ///投资者代码
    TThostFtdcInvestorIDType	InvestorID;
    ///序号
    TThostFtdcSequenceNoType	SequenceNo;
    ///消息正文
    TThostFtdcContentType	Content;
    ///投资者帐号
    TThostFtdcAccountIDType	AccountID;
    ///币种代码
    TThostFtdcCurrencyIDType	CurrencyID;
    };
"""
SettlementInfoField = namedtuple(
    "CThostFtdcSettlementInfoField",
    ["TradingDay", "SettlementID", "BrokerID", "InvestorID", "SequenceNo", "Content", "AccountID", "CurrencyID"]
)

# 投资者结算结果确认信息
"""
///投资者结算结果确认信息
struct CThostFtdcSettlementInfoConfirmField
{
    ///经纪公司代码
    TThostFtdcBrokerIDType	BrokerID;
    ///投资者代码
    TThostFtdcInvestorIDType	InvestorID;
    ///确认日期
    TThostFtdcDateType	ConfirmDate;
    ///确认时间
    TThostFtdcTimeType	ConfirmTime;
    ///结算编号
    TThostFtdcSettlementIDType	SettlementID;
    ///投资者帐号
    TThostFtdcAccountIDType	AccountID;
    ///币种代码
    TThostFtdcCurrencyIDType	CurrencyID;
};
"""
SettlementInfoConfirmField = namedtuple(
    "CThostFtdcSettlementInfoConfirmField",
    ["BrokerID", "InvestorID", "ConfirmDate", "ConfirmTime", "SettlementID", "AccountID", "CurrencyID"]
)

# 投资者持仓
"""
///投资者持仓
struct CThostFtdcInvestorPositionField
{
    ///合约代码
    TThostFtdcInstrumentIDType	InstrumentID;
    ///经纪公司代码
    TThostFtdcBrokerIDType	BrokerID;
    ///投资者代码
    TThostFtdcInvestorIDType	InvestorID;
    ///持仓多空方向
    TThostFtdcPosiDirectionType	PosiDirection;
    ///投机套保标志
    TThostFtdcHedgeFlagType	HedgeFlag;
    ///持仓日期
    TThostFtdcPositionDateType	PositionDate;
    ///上日持仓
    TThostFtdcVolumeType	YdPosition;
    ///今日持仓
    TThostFtdcVolumeType	Position;
    ///多头冻结
    TThostFtdcVolumeType	LongFrozen;
    ///空头冻结
    TThostFtdcVolumeType	ShortFrozen;
    ///开仓冻结金额
    TThostFtdcMoneyType	LongFrozenAmount;
    ///开仓冻结金额
    TThostFtdcMoneyType	ShortFrozenAmount;
    ///开仓量
    TThostFtdcVolumeType	OpenVolume;
    ///平仓量
    TThostFtdcVolumeType	CloseVolume;
    ///开仓金额
    TThostFtdcMoneyType	OpenAmount;
    ///平仓金额
    TThostFtdcMoneyType	CloseAmount;
    ///持仓成本
    TThostFtdcMoneyType	PositionCost;
    ///上次占用的保证金
    TThostFtdcMoneyType	PreMargin;
    ///占用的保证金
    TThostFtdcMoneyType	UseMargin;
    ///冻结的保证金
    TThostFtdcMoneyType	FrozenMargin;
    ///冻结的资金
    TThostFtdcMoneyType	FrozenCash;
    ///冻结的手续费
    TThostFtdcMoneyType	FrozenCommission;
    ///资金差额
    TThostFtdcMoneyType	CashIn;
    ///手续费
    TThostFtdcMoneyType	Commission;
    ///平仓盈亏
    TThostFtdcMoneyType	CloseProfit;
    ///持仓盈亏
    TThostFtdcMoneyType	PositionProfit;
    ///上次结算价
    TThostFtdcPriceType	PreSettlementPrice;
    ///本次结算价
    TThostFtdcPriceType	SettlementPrice;
    ///交易日
    TThostFtdcDateType	TradingDay;
    ///结算编号
    TThostFtdcSettlementIDType	SettlementID;
    ///开仓成本
    TThostFtdcMoneyType	OpenCost;
    ///交易所保证金
    TThostFtdcMoneyType	ExchangeMargin;
    ///组合成交形成的持仓
    TThostFtdcVolumeType	CombPosition;
    ///组合多头冻结
    TThostFtdcVolumeType	CombLongFrozen;
    ///组合空头冻结
    TThostFtdcVolumeType	CombShortFrozen;
    ///逐日盯市平仓盈亏
    TThostFtdcMoneyType	CloseProfitByDate;
    ///逐笔对冲平仓盈亏
    TThostFtdcMoneyType	CloseProfitByTrade;
    ///今日持仓
    TThostFtdcVolumeType	TodayPosition;
    ///保证金率
    TThostFtdcRatioType	MarginRateByMoney;
    ///保证金率(按手数)
    TThostFtdcRatioType	MarginRateByVolume;
    ///执行冻结
    TThostFtdcVolumeType	StrikeFrozen;
    ///执行冻结金额
    TThostFtdcMoneyType	StrikeFrozenAmount;
    ///放弃执行冻结
    TThostFtdcVolumeType	AbandonFrozen;
    ///交易所代码
    TThostFtdcExchangeIDType	ExchangeID;
    ///执行冻结的昨仓
    TThostFtdcVolumeType	YdStrikeFrozen;
    ///投资单元代码
    TThostFtdcInvestUnitIDType	InvestUnitID;
    ///大商所持仓成本差值，只有大商所使用
    TThostFtdcMoneyType	PositionCostOffset;
    ///tas持仓手数
    TThostFtdcVolumeType	TasPosition;
    ///tas持仓成本
    TThostFtdcMoneyType	TasPositionCost;
};
"""
InvestorPositionField = namedtuple(
    "CThostFtdcInvestorPositionField",
    [
        "InstrumentID", "BrokerID", "InvestorID", "PosiDirection", "HedgeFlag", "PositionDate", "YdPosition",
        "Position", "LongFrozen", "ShortFrozen", "LongFrozenAmount", "ShortFrozenAmount", "OpenVolume", "CloseVolume",
        "OpenAmount", "CloseAmount", "PositionCost", "PreMargin", "UseMargin", "FrozenMargin", "FrozenCash",
        "FrozenCommission", "CashIn", "Commission", "CloseProfit", "PositionProfit", "PreSettlementPrice",
        "SettlementPrice", "TradingDay", "SettlementID", "OpenCost", "ExchangeMargin", "CombPosition", "CombLongFrozen",
        "CombShortFrozen", "CloseProfitByDate", "CloseProfitByTrade", "TodayPosition", "MarginRateByMoney",
        "MarginRateByVolume", "StrikeFrozen", "StrikeFrozenAmount", "AbandonFrozen", "ExchangeID", "YdStrikeFrozen",
        "InvestUnitID", "PositionCostOffset", "TasPosition", "TasPositionCost"
    ]
)
