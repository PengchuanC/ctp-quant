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
from strategy.trend_trade import TrendTradeStrategy
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
tts = TrendTradeStrategy(rbc, contract)

trader_spi.create_trader_api(USERINFO)
trader_spi.register_front(front)
trader_spi.register_broker(broker)
trader_spi.register_spi()
trader_spi.req_authenticate(appinfo)
trader_spi.req_user_login(userinfo)
trader_spi.req_qry_settlement_info()
trader_spi.init()

time.sleep(5)
print("**********")
for i in tts.trade(5, 34, 7):
    print(i)
exit(1)
# trader_spi.join()
