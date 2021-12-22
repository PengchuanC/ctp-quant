"""
@author: chuanchao.peng
@date: 2021/12/22 11:23
@file trade_with_example_strategy.py
@desc:
"""

import time
from concurrent.futures import ThreadPoolExecutor

from ftdc import structs, order, datatype, trade
from strategy.example import StrategyExample
from ftdc.trader import trader_api, TraderSpi
from broker import RedisBrokerConfig
from settings.settings import USERINFO
from logger.logger import logger


pool = ThreadPoolExecutor(max_workers=2)
user = structs.UserLoginField(BrokerID='9999', UserID='195076', Password='Asin#940213')
redis_c = RedisBrokerConfig('10.170.139.12')
appinfo = structs.ReqAuthenticateField(
    BrokerID='9999', UserID='195076', UserProductInfo="", AuthCode="0000000000000000", AppID="simnow_client_test"
)
api = trader_api.CThostFtdcTraderApi_CreateFtdcTraderApi(f'{USERINFO}/')
spi = TraderSpi(api, user, appinfo)
example_strategy = StrategyExample(user, redis_c, 'ni2201')
api.RegisterFront("tcp://180.168.146.187:10202")
api.RegisterSpi(spi)
api.Init()

for order in example_strategy.trade():
    # spi.trade(order)
    # logger.info(f'执行报单，合约代码={order.InstrumentID},报价={order.LimitPrice},数量={order.VolumeTotalOriginal}')
    print(order)
