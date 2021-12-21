"""
模拟交易策略，交易策略放入协程，每30秒下一次单
策略中忽略交易信号的产生过程，实盘中需要实现策略
"""

import time
from concurrent.futures import ThreadPoolExecutor

from ftdc import structs, order, datatype, trade
from ftdc.trader import trader_api, TraderSpi
from settings.settings import USERINFO
from logger.logger import logger


userinfo = structs.UserLoginField(BrokerID='9999', UserID='195076', Password='Asin#940213')


def insert_order(trader_spi: TraderSpi):
    # 报单
    try:
        tm = trade.TradeMethod(userinfo)
        input_order = tm.buy_open("ni2201", "SHFE", 144000, 1)
        trader_spi.trade(input_order)
    except Exception as e:
        logger.error(e)


def strategy(trader_spi: TraderSpi):
    count = 0
    while count < 10:
        time.sleep(30)
        trader_spi.qry_investor_position('ni2201', 'SHFE')
        # insert_order(trader_spi)
        count += 1


if __name__ == '__main__':
    pool = ThreadPoolExecutor(max_workers=2)
    appinfo = structs.ReqAuthenticateField(
        BrokerID='9999', UserID='195076', UserProductInfo="", AuthCode="0000000000000000", AppID="simnow_client_test"
    )
    api = trader_api.CThostFtdcTraderApi_CreateFtdcTraderApi(f'{USERINFO}/')
    spi = TraderSpi(api, userinfo, appinfo)
    api.RegisterFront("tcp://180.168.146.187:10202")
    api.RegisterSpi(spi)

    api.Init()
    pool.submit(strategy, spi)
    api.Join()
