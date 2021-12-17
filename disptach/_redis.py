"""
@author：chuanchao.peng
@date: 2021-12-08
@desc:
对redis缓存的行情数据进行处理，转化为分钟(30分钟，日)bar
"""

import time
from concurrent.futures import ThreadPoolExecutor

import arrow
import redis

from broker import RedisBroker, RedisBrokerConfig
from logger.logger import logger
from ftdc.structs import DepthMarketDataField


ThreadExecutor = ThreadPoolExecutor(max_workers=2)


class RedisDispatcher(RedisBroker):

    _redis: redis.Redis

    def __init__(self, config: RedisBrokerConfig):
        super().__init__(config)
        self.c = config
        self.connect()
        self.create_group()

    def create_group(self):
        """查询或创建消费者组"""
        exist_stream = self._redis.exists(self.c.name)
        if not exist_stream:
            logger.warning(f"redis中没有{self.c.name}订阅流，即将退出程序...")
            exit(-1)
        groups = self._redis.xinfo_groups(self.c.name)
        if groups:
            self._redis.xgroup_destroy(self.c.name, self.c.name+'_group')
        self._redis.xgroup_create(self.c.name, self.c.name+'_group', id=0)
        self._redis.xinfo_groups(self.c.name)

    def destroy_stream(self):
        """在进入新的一天前，清除历史数据"""
        now: arrow.Arrow = arrow.now()
        date = now.format('YYYY-MM-DD')
        if arrow.get(f'{date} 20:55:00') < now < arrow.get(f'{date} 21:00:00'):
            print('deleting')
            self._redis.delete(self.c.name)
            print('deleted')

    @staticmethod
    def proc(dataset):
        print(dataset)

    def dispatch(self):
        while True:
            exist_stream = self._redis.exists(self.c.name)
            # stream尚未创建，等待publisher创建stream
            if not exist_stream:
                time.sleep(30)
                continue
            items = self._redis.xreadgroup(
                self.c.name+'_group', 'consumer-1', {self.c.name: '>'}, count=1000
            )
            # stream中没有数据可以订阅
            if not items:
                self.destroy_stream()
                time.sleep(10)
                continue
            stream, records = items[0]
            if not records:
                time.sleep(10)
            ids = []
            dataset = []
            for item in records:
                xid, info = item
                ids.append(xid)
                info = {x.decode(): y.decode() for x, y in info.items()}
                dataset.append(info)
            self._redis.xack(self.c.name, self.c.name+"_group", *ids)
            # TODO 保存数据到数据和计算bar
            ThreadExecutor.submit(self.proc, dataset[0])


if __name__ == '__main__':
    cfg = RedisBrokerConfig('10.170.139.12')
    rd = RedisDispatcher(cfg)
    rd.dispatch()
