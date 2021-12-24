"""
@author: chuanchao.peng
@date: 2021/12/23 15:09
@file trader_spi.py
@desc:
"""
import time

from settings.settings import USERINFO

from trader.trader import TraderSpi
from trader.base import BaseTradeBroker
from ftdc import qry
from strategy.example import StrategyExample
from broker import RedisBrokerConfig


front = "tcp://180.168.146.187:10202"
appinfo = qry.ReqAuthenticateField(
    BrokerID='9999', UserID='195076', AppID='simnow_client_test', AuthCode='0000000000000000'
)
userinfo = qry.ReqUserLoginField(BrokerID='9999', UserID='195076', Password='Asin#940213')
rbc = RedisBrokerConfig(host='10.170.139.12')
contract = 'ni2201'


trader_spi = TraderSpi()
broker = BaseTradeBroker()
se = StrategyExample(userinfo, rbc, contract)

trader_spi.create_trader_api(USERINFO)
trader_spi.register_front(front)
trader_spi.register_broker(broker)
trader_spi.register_spi()
trader_spi.req_authenticate(appinfo)
trader_spi.req_user_login(userinfo)
trader_spi.req_qry_settlement_info()
trader_spi.init()
# for order_info in se.trade():
#     trader_spi.tb.insert_order(order_info)
count = 0
time.sleep(5)
while count < 10:
    print("**********")
    print(trader_spi.tb.get_instrument(contract, 'SHFE'))
    print(trader_spi.tb.get_market_data(contract, 'SHFE'))
    time.sleep(2)
    count += 1
exit(1)
# trader_spi.join()
