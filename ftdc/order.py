"""
@author: chuanchao.peng
@date: 2021-12-17
@desc:
交易相关的数据结构
"""

from collections import namedtuple

# 输入报单
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

# 报单
"""
///报单
struct CThostFtdcOrderField
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
    ///本地报单编号
    TThostFtdcOrderLocalIDType	OrderLocalID;
    ///交易所代码
    TThostFtdcExchangeIDType	ExchangeID;
    ///会员代码
    TThostFtdcParticipantIDType	ParticipantID;
    ///客户代码
    TThostFtdcClientIDType	ClientID;
    ///合约在交易所的代码
    TThostFtdcExchangeInstIDType	ExchangeInstID;
    ///交易所交易员代码
    TThostFtdcTraderIDType	TraderID;
    ///安装编号
    TThostFtdcInstallIDType	InstallID;
    ///报单提交状态
    TThostFtdcOrderSubmitStatusType	OrderSubmitStatus;
    ///报单提示序号
    TThostFtdcSequenceNoType	NotifySequence;
    ///交易日
    TThostFtdcDateType	TradingDay;
    ///结算编号
    TThostFtdcSettlementIDType	SettlementID;
    ///报单编号
    TThostFtdcOrderSysIDType	OrderSysID;
    ///报单来源
    TThostFtdcOrderSourceType	OrderSource;
    ///报单状态
    TThostFtdcOrderStatusType	OrderStatus;
    ///报单类型
    TThostFtdcOrderTypeType	OrderType;
    ///今成交数量
    TThostFtdcVolumeType	VolumeTraded;
    ///剩余数量
    TThostFtdcVolumeType	VolumeTotal;
    ///报单日期
    TThostFtdcDateType	InsertDate;
    ///委托时间
    TThostFtdcTimeType	InsertTime;
    ///激活时间
    TThostFtdcTimeType	ActiveTime;
    ///挂起时间
    TThostFtdcTimeType	SuspendTime;
    ///最后修改时间
    TThostFtdcTimeType	UpdateTime;
    ///撤销时间
    TThostFtdcTimeType	CancelTime;
    ///最后修改交易所交易员代码
    TThostFtdcTraderIDType	ActiveTraderID;
    ///结算会员编号
    TThostFtdcParticipantIDType	ClearingPartID;
    ///序号
    TThostFtdcSequenceNoType	SequenceNo;
    ///前置编号
    TThostFtdcFrontIDType	FrontID;
    ///会话编号
    TThostFtdcSessionIDType	SessionID;
    ///用户端产品信息
    TThostFtdcProductInfoType	UserProductInfo;
    ///状态信息
    TThostFtdcErrorMsgType	StatusMsg;
    ///用户强评标志
    TThostFtdcBoolType	UserForceClose;
    ///操作用户代码
    TThostFtdcUserIDType	ActiveUserID;
    ///经纪公司报单编号
    TThostFtdcSequenceNoType	BrokerOrderSeq;
    ///相关报单
    TThostFtdcOrderSysIDType	RelativeOrderSysID;
    ///郑商所成交数量
    TThostFtdcVolumeType	ZCETotalTradedVolume;
    ///互换单标志
    TThostFtdcBoolType	IsSwapOrder;
    ///营业部编号
    TThostFtdcBranchIDType	BranchID;
    ///投资单元代码
    TThostFtdcInvestUnitIDType	InvestUnitID;
    ///资金账号
    TThostFtdcAccountIDType	AccountID;
    ///币种代码
    TThostFtdcCurrencyIDType	CurrencyID;
    ///IP地址
    TThostFtdcIPAddressType	IPAddress;
    ///Mac地址
    TThostFtdcMacAddressType	MacAddress;
};
"""
OrderField = namedtuple(
    'CThostFtdcOrderField',
    [
        "BrokerID", "InvestorID", "InstrumentID", "OrderRef", "UserID", "OrderPriceType", "Direction", "CombOffsetFlag",
        "CombHedgeFlag", "LimitPrice", "VolumeTotalOriginal", "TimeCondition", "GTDDate", "VolumeCondition",
        "MinVolume", "ContingentCondition", "StopPrice", "ForceCloseReason", "IsAutoSuspend", "BusinessUnit",
        "RequestID", "OrderLocalID", "ExchangeID", "ParticipantID", "ClientID", "ExchangeInstID", "TraderID",
        "InstallID", "OrderSubmitStatus", "NotifySequence", "TradingDay", "SettlementID", "OrderSysID", "OrderSource",
        "OrderStatus", "OrderType", "VolumeTraded", "VolumeTotal", "InsertDate", "InsertTime", "ActiveTime",
        "SuspendTime", "UpdateTime", "CancelTime", "ActiveTraderID", "ClearingPartID", "SequenceNo", "FrontID",
        "SessionID", "UserProductInfo", "StatusMsg", "UserForceClose", "ActiveUserID", "BrokerOrderSeq",
        "RelativeOrderSysID", "ZCETotalTradedVolume", "IsSwapOrder", "BranchID", "InvestUnitID", "AccountID",
        "CurrencyID", "IPAddress", "MacAddress"
    ]
)

# 成交
"""
struct CThostFtdcTradeField
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
    ///交易所代码
    TThostFtdcExchangeIDType	ExchangeID;
    ///成交编号
    TThostFtdcTradeIDType	TradeID;
    ///买卖方向
    TThostFtdcDirectionType	Direction;
    ///报单编号
    TThostFtdcOrderSysIDType	OrderSysID;
    ///会员代码
    TThostFtdcParticipantIDType	ParticipantID;
    ///客户代码
    TThostFtdcClientIDType	ClientID;
    ///交易角色
    TThostFtdcTradingRoleType	TradingRole;
    ///合约在交易所的代码
    TThostFtdcExchangeInstIDType	ExchangeInstID;
    ///开平标志
    TThostFtdcOffsetFlagType	OffsetFlag;
    ///投机套保标志
    TThostFtdcHedgeFlagType	HedgeFlag;
    ///价格
    TThostFtdcPriceType	Price;
    ///数量
    TThostFtdcVolumeType	Volume;
    ///成交时期
    TThostFtdcDateType	TradeDate;
    ///成交时间
    TThostFtdcTimeType	TradeTime;
    ///成交类型
    TThostFtdcTradeTypeType	TradeType;
    ///成交价来源
    TThostFtdcPriceSourceType	PriceSource;
    ///交易所交易员代码
    TThostFtdcTraderIDType	TraderID;
    ///本地报单编号
    TThostFtdcOrderLocalIDType	OrderLocalID;
    ///结算会员编号
    TThostFtdcParticipantIDType	ClearingPartID;
    ///业务单元
    TThostFtdcBusinessUnitType	BusinessUnit;
    ///序号
    TThostFtdcSequenceNoType	SequenceNo;
    ///交易日
    TThostFtdcDateType	TradingDay;
    ///结算编号
    TThostFtdcSettlementIDType	SettlementID;
    ///经纪公司报单编号
    TThostFtdcSequenceNoType	BrokerOrderSeq;
    ///成交来源
    TThostFtdcTradeSourceType	TradeSource;
    ///投资单元代码
    TThostFtdcInvestUnitIDType	InvestUnitID;
};
"""
TraderField = namedtuple(
    "CThostFtdcTradeField",
    [
        "BrokerID", "InvestorID", "InstrumentID", "OrderRef", "UserID", "ExchangeID", "TradeID", "Direction",
        "OrderSysID", "ParticipantID", "ClientID", "TradingRole", "ExchangeInstID", "OffsetFlag", "HedgeFlag", "Price",
        "Volume", "TradeDate", "TradeTime", "TradeType", "PriceSource", "TraderID", "OrderLocalID", "ClearingPartID",
        "BusinessUnit", "SequenceNo", "TradingDay", "SettlementID", "TradeSource", "InvestUnitID"
    ]
)

# 查询组合持仓明细
"""
///查询组合持仓明细
struct CThostFtdcQryInvestorPositionCombineDetailField
{
    ///经纪公司代码
    TThostFtdcBrokerIDType	BrokerID;
    ///投资者代码
    TThostFtdcInvestorIDType	InvestorID;
    ///组合持仓合约编码
    TThostFtdcInstrumentIDType	CombInstrumentID;
    ///交易所代码
    TThostFtdcExchangeIDType	ExchangeID;
    ///投资单元代码
    TThostFtdcInvestUnitIDType	InvestUnitID;
};
"""
InvestorPositionCombineDetailField = namedtuple(
    "CThostFtdcQryInvestorPositionCombineDetailField",
    ["BrokerID", "InvestorID", "CombInstrumentID", "ExchangeID", "InvestUnitID"]
)

# 查询投资者持仓
"""
///查询投资者持仓
struct CThostFtdcQryInvestorPositionField
{
    ///经纪公司代码
    TThostFtdcBrokerIDType	BrokerID;
    ///投资者代码
    TThostFtdcInvestorIDType	InvestorID;
    ///合约代码
    TThostFtdcInstrumentIDType	InstrumentID;
    ///交易所代码
    TThostFtdcExchangeIDType	ExchangeID;
    ///投资单元代码
    TThostFtdcInvestUnitIDType	InvestUnitID;
};
"""
QryInvestorPositionField = namedtuple(
    "CThostFtdcQryInvestorPositionField",
    ["BrokerID", "InvestorID", "InstrumentID", "ExchangeID", "InvestUnitID"]
)
