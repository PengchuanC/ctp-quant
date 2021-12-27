"""
@author: chuanchao.peng
@date: 2021/12/22 10:49
@file _memory.py
@desc:
"""

from broker import RedisBroker, RedisBrokerConfig
from logger.logger import logger
from ftdc.structs import DepthMarketDataField
from disptach._database import DatabaseDispatcher


class MemoryDispatcher(DatabaseDispatcher):
    def __init__(self, config: RedisBrokerConfig):
        super().__init__(config)
        self.connect()
        self.create_group()

    def create_group(self):
        """查询或创建消费者组"""
        exist_stream = self._redis.exists(self.c.name)
        if not exist_stream:
            logger.warning(f"redis中没有{self.c.name}订阅流，即将退出程序...")
            exit(-1)
        groups = self._redis.xinfo_groups(self.c.name)
        if not groups:
            self._redis.xgroup_create(self.c.name, self.c.name+'_group', id=0)

    def dispatch(self):
        while True:
            exist_stream = self._redis.exists(self.c.name)
            # stream尚未创建，等待publisher创建stream
            if not exist_stream:
                continue
            items = self._redis.xreadgroup(
                self.c.name + '_group', 'consumer-2', {self.c.name: '>'}, count=10
            )
            # stream中没有数据可以订阅
            if not items:
                continue
            stream, records = items[0]
            if not records:
                continue
            ids = []
            for item in records:
                xid, info = item
                ids.append(xid)
                info = {x.decode(): y.decode() for x, y in info.items()}
                yield info
            self._redis.xack(self.c.name, self.c.name + "_group", *ids)

