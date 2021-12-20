"""
模拟交易策略，交易策略放入协程，没60秒下一次单
策略中忽略交易信号的产生过程，实盘中需要实现策略
"""

import time
from concurrent.futures import ThreadPoolExecutor

from ftdc import structs, order, datatype
from ftdc.trader import trader_api, TraderSpi
from settings.settings import USERINFO


def insert_order(trader_spi: TraderSpi):
    # 报单
    input_order: order.InputOrderField = trader_api.CThostFtdcInputOrderField()
    input_order.BrokerID = '9999'
    input_order.ExchangeID = "SHFE"
    input_order.InstrumentID = "ni2201"
    input_order.UserID = "195076"
    input_order.InvestorID = "195076"
    input_order.Direction = trader_api.THOST_FTDC_D_Buy
    input_order.LimitPrice = 144000
    input_order.VolumeTotalOriginal = 1
    input_order.OrderPriceType = datatype.OrderPriceType.limit_price
    input_order.ContingentCondition = datatype.ContingentConditionType.immediately
    input_order.TimeCondition = datatype.TimeConditionType.gfd
    input_order.VolumeCondition = datatype.VolumeConditionType.av
    input_order.CombHedgeFlag = datatype.ExClientIDType.hedge
    input_order.CombOffsetFlag = datatype.OffsetFlagType.open
    input_order.MinVolume = 0
    input_order.ForceCloseReason = trader_api.THOST_FTDC_FCC_NotForceClose
    input_order.IsAutoSuspend = 0
    trader_spi.trade(input_order)


def strategy(trader_spi: TraderSpi):

    count = 0
    while count < 10:
        insert_order(trader_spi)
        time.sleep(60)


if __name__ == '__main__':
    pool = ThreadPoolExecutor(max_workers=2)
    appinfo = structs.ReqAuthenticateField(
        BrokerID='9999', UserID='195076', UserProductInfo="", AuthCode="0000000000000000", AppID="simnow_client_test"
    )
    userinfo = structs.UserLoginField(BrokerID='9999', UserID='195076', Password='Asin#940213')
    api = trader_api.CThostFtdcTraderApi_CreateFtdcTraderApi(f'{USERINFO}/')
    spi = TraderSpi(api, userinfo, appinfo)
    api.RegisterFront("tcp://180.168.146.187:10201")
    api.RegisterSpi(spi)

    api.Init()
    time.sleep(10)
    spi.qry_investor_position('ni2201')
    # pool.submit(strategy, spi)
    api.Join()
