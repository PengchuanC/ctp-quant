"""
@author: chuanchao.peng
@date: 2021/12/20 14:31
@file datatype.py
@desc:
定义数据类型，主要是交易参数
"""
import thosttraderapi as trader_api


class OrderPriceType(object):
    """报单价格条件类型"""
    any_price = trader_api.THOST_FTDC_OPT_AnyPrice  # 任意价
    limit_price = trader_api.THOST_FTDC_OPT_LimitPrice  # 限价
    best_price = trader_api.THOST_FTDC_OPT_BestPrice  # 最优价
    last_price = trader_api.THOST_FTDC_OPT_LastPrice  # 最新价


class OffsetFlagType(object):
    """开平标志类型"""
    open = trader_api.THOST_FTDC_OF_Open  # 开仓
    close = trader_api.THOST_FTDC_OF_Close  # 平仓
    force_close = trader_api.THOST_FTDC_OF_ForceClose  # 强平
    close_today = trader_api.THOST_FTDC_OF_CloseToday  # 平今
    close_yesterday = trader_api.THOST_FTDC_OF_CloseYesterday  # 平昨
    force_off = trader_api.THOST_FTDC_OF_ForceOff  # 强减
    local_force_close = trader_api.THOST_FTDC_OF_LocalForceClose  # 本地强平


class ForceCloseReasonType(object):
    """强平原因类型"""
    not_force_close = trader_api.THOST_FTDC_FCC_NotForceClose  # 非强平
    lack_deposit = trader_api.THOST_FTDC_FCC_LackDeposit  # 资金不足
    client_over_position_limit = trader_api.THOST_FTDC_FCC_ClientOverPositionLimit  # 客户超仓
    member_over_position_limit = trader_api.THOST_FTDC_FCC_MemberOverPositionLimit  # 会员超仓
    not_multiple = trader_api.THOST_FTDC_FCC_NotMultiple  # 持仓非整数倍
    violation = trader_api.THOST_FTDC_FCC_Violation  # 违规
    other = trader_api.THOST_FTDC_FCC_Other  # 其它
    person_deliv = trader_api.THOST_FTDC_FCC_PersonDeliv  # 自然人临近交割


class TimeConditionType(object):
    """有效期类型"""
    ioc = trader_api.THOST_FTDC_TC_IOC  # 立即完成，否则撤销
    gfs = trader_api.THOST_FTDC_TC_GFS  # 本节有效
    gfd = trader_api.THOST_FTDC_TC_GFD  # 当日有效
    gtd = trader_api.THOST_FTDC_TC_GTD  # 指定日期前有效
    gtc = trader_api.THOST_FTDC_TC_GTC  # 撤销前有效
    gfa = trader_api.THOST_FTDC_TC_GFA  # 集合竞价有效


class VolumeConditionType(object):
    """成交量类型"""
    av = trader_api.THOST_FTDC_VC_AV  # 任何数量
    mv = trader_api.THOST_FTDC_VC_MV  # 最小数量
    cv = trader_api.THOST_FTDC_VC_CV  # 全部数量


class ContingentConditionType(object):
    """触发条件类型"""
    immediately = trader_api.THOST_FTDC_CC_Immediately  # 立即
    touch = trader_api.THOST_FTDC_CC_Touch  # 止损
    touch_profit = trader_api.THOST_FTDC_CC_TouchProfit  # 止赢
    parked_order = trader_api.THOST_FTDC_CC_ParkedOrder  # 预埋单


class ExClientIDType(object):
    """交易编码类型"""
    hedge = trader_api.THOST_FTDC_ECIDT_Hedge  # 套保
    arbitrage = trader_api.THOST_FTDC_ECIDT_Arbitrage  # 套利
    speculation = trader_api.THOST_FTDC_ECIDT_Speculation  # 投机
