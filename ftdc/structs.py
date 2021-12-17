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

# 报单参数
"""
///输入报单
struct CThostFtdcInputOrderField
{
    ///经纪公司代码
    TThostFtdcBrokerIDType	BrokerID;
    ///投资者代码
    TThostFtdcInvestorIDType	InvestorID;
    ///合约代码
    TThostFtdcInstrumentIDType	InstrumentID;
    ///报单引用
    TThostFtdcOrderRefType	OrderRef;
    ///用户代码
    TThostFtdcUserIDType	UserID;
    ///报单价格条件
    TThostFtdcOrderPriceTypeType	OrderPriceType;
    ///买卖方向
    TThostFtdcDirectionType	Direction;
    ///组合开平标志
    TThostFtdcCombOffsetFlagType	CombOffsetFlag;
    ///组合投机套保标志
    TThostFtdcCombHedgeFlagType	CombHedgeFlag;
    ///价格
    TThostFtdcPriceType	LimitPrice;
    ///数量
    TThostFtdcVolumeType	VolumeTotalOriginal;
    ///有效期类型
    TThostFtdcTimeConditionType	TimeCondition;
    ///GTD日期
    TThostFtdcDateType	GTDDate;
    ///成交量类型
    TThostFtdcVolumeConditionType	VolumeCondition;
    ///最小成交量
    TThostFtdcVolumeType	MinVolume;
    ///触发条件
    TThostFtdcContingentConditionType	ContingentCondition;
    ///止损价
    TThostFtdcPriceType	StopPrice;
    ///强平原因
    TThostFtdcForceCloseReasonType	ForceCloseReason;
    ///自动挂起标志
    TThostFtdcBoolType	IsAutoSuspend;
    ///业务单元
    TThostFtdcBusinessUnitType	BusinessUnit;
    ///请求编号
    TThostFtdcRequestIDType	RequestID;
    ///用户强评标志
    TThostFtdcBoolType	UserForceClose;
    ///互换单标志
    TThostFtdcBoolType	IsSwapOrder;
    ///交易所代码
    TThostFtdcExchangeIDType	ExchangeID;
    ///投资单元代码
    TThostFtdcInvestUnitIDType	InvestUnitID;
    ///资金账号
    TThostFtdcAccountIDType	AccountID;
    ///币种代码
    TThostFtdcCurrencyIDType	CurrencyID;
    ///交易编码
    TThostFtdcClientIDType	ClientID;
    ///IP地址
    TThostFtdcIPAddressType	IPAddress;
    ///Mac地址
    TThostFtdcMacAddressType	MacAddress;
};
"""
InputOrderField = namedtuple(
    "CThostFtdcInputOrderField",
    [
        "BrokerID", "InvestorID", "InstrumentID", "OrderRef", "UserID", "OrderPriceType", "Direction", "CombOffsetFlag",
        "CombHedgeFlag", "LimitPrice", "VolumeTotalOriginal", "TimeCondition", "GTDDate", "VolumeCondition",
        "MinVolume", "ContingentCondition", "StopPrice", "ForceCloseReason", "IsAutoSuspend", "BusinessUnit",
        "RequestID", "UserForceClose", "IsSwapOrder", "ExchangeID", "InvestUnitID", "AccountID", "CurrencyID",
        "ClientID", "IPAddress", "MacAddress"
    ]
)
