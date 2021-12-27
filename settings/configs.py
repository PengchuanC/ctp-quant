"""
@author: chuanchao.peng
@date: 2021/12/27 10:07
@file configs.py
@desc:
"""

from broker.redis_broker import RedisBrokerConfig
from ftdc.qry import ReqUserLoginField, ReqAuthenticateField


# 行情前置
MD_FRONT = "tcp://180.168.146.187:10212"
# 交易前置
TRADE_FRONT = "tcp://180.168.146.187:10202"

# redis配置
REDIS_CONFIG = RedisBrokerConfig(host='10.170.139.12', port=6379, database=0, name='redis_broker')

# 用户信息
USER = ReqUserLoginField(BrokerID='9999', UserID='195076', Password='Asin#940213')

# APP信息
APP = ReqAuthenticateField(
    BrokerID='9999', UserID='195076', AppID='simnow_client_test', AuthCode='0000000000000000'
)
