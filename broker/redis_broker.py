"""
@author: chuanchao.peng
@date: 2021-12-08
@desc: 使用redis作为broker
"""

import json

import redis

from broker._broker import Broker


class RedisBrokerConfig(object):
    """配置RedisBroker所需参数"""
    host: str
    port: int
    database: int
    name: str

    def __init__(self, host: str, port: int = 6379, database: int = 0, name: str = 'redis_broker'):
        self.host = host
        self.port = port
        self.database = database
        self.name = name


class RedisBroker(Broker):
    """使用单例模式创建RedisBroker"""

    # 连接池
    _pool: redis.ConnectionPool = None
    _redis: redis.Redis = None

    def __init__(self, config: RedisBrokerConfig):
        self.c = config

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(RedisBroker, cls)
            cls._instance = orig.__new__(cls)
        return cls._instance

    def connect(self):
        if self._pool is None:
            self._pool = redis.ConnectionPool.from_url(f"redis://{self.c.host}:{self.c.port}/{self.c.database}")
            self._redis = redis.Redis(connection_pool=self._pool, decode_responses=True)

    def do(self, data: dict):
        """供publisher调用处理数据，此接口必须实现"""
        self.connect()
        d = data
        row = {
            'date': d['TradingDay'], 'time': d['UpdateTime'], 'instrument_id': d['InstrumentID'],
            'close': d['LastPrice'], 'high': d['HighestPrice'], 'low': d['LowestPrice'],
            'upper': d['UpperLimitPrice'], 'lower': d['LowerLimitPrice']
        }
        self._redis.xadd(self.c.name, row)

    def register(self, name: str, publisher: "Publisher"):
        """注册后调用redis连接"""
        publisher.register(name, self)
        self.connect()


if __name__ == '__main__':
    cfg = RedisBrokerConfig('10.170.139.12')
    rb = RedisBroker(cfg)
    RedisBroker(cfg)
