"""
@author：chuanchao.peng
@date: 2021-12-08
@desc:
对redis缓存的行情数据进行处理，转化为分钟(30分钟，日)bar
"""

from concurrent.futures import ThreadPoolExecutor
from threading import Lock

import arrow
import redis

from broker import RedisBroker, RedisBrokerConfig
from logger.logger import logger
from ftdc.structs import DepthMarketDataField
from database.models import HourlyQuote, DailyQuote


ThreadExecutor = ThreadPoolExecutor(max_workers=3)


class DatabaseDispatcher(RedisBroker):

    _redis: redis.Redis
    _data = {}
    _k_bar = {}
    _last = None

    def __init__(self, config: RedisBrokerConfig):
        super().__init__(config)
        self.c = config
        self.connect()
        self.create_group()
        self.lock = Lock()
        self.k_lock = Lock()

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
            self._redis.delete(self.c.name)
            self._save_k_bar()
            logger.info(f'redis stream {self.c.name}已删除')

    def proc(self, dataset):
        for d in dataset:
            # 将毫秒级数据转化为半小时级
            t = arrow.get(f'{d["date"]} {d["time"]}')
            start, end = t.span("hour")
            mid = end.shift(minutes=-30)
            tick = mid if t <= mid else end
            instrument_id = d['instrument_id']
            exist = self._data.get((tick, instrument_id))
            if not exist:
                self.lock.acquire()
                self._data[(tick, instrument_id)] = {
                    'instrument_id': d['instrument_id'], 'date': d['date'], 'time': d['time'],
                    'open': d['close'], 'high': d['close'], 'low': d['close'], 'close': d['close'],
                }
                self.lock.release()
            else:
                high = max([exist['high'], d['high']])
                low = min([exist['low'], d['low']])
                self.lock.acquire()
                self._data[(tick, instrument_id)] = {
                    **exist, 'date': d['date'], 'time': d['time'], 'close': d['close'], 'high': high, 'low': low
                }
                self.lock.release()
        # print(self._data)

    def _save(self):
        keys = list(self._data.keys())
        max_date = max({x[0] for x in keys})
        need_to_add = [x for x in keys if x[0] < max_date]
        if not need_to_add:
            return
        self.lock.acquire()
        data = {}
        for key in need_to_add:
            data[key] = self._data.pop(key)
        self.lock.release()
        sets = []
        for key, v in data.items():
            dm: arrow.Arrow = key[0]
            dt = dm.format('YYYY-MM-DD')
            tm = dm.format('HH:mm:ss')
            hq = HourlyQuote(
                instrument_id=key[1], date=dt, time=tm, open=v['open'], high=v['high'], low=v['low'], close=v['close']
            )
            sets.append(hq)
        HourlyQuote.bulk_create(sets)

    def k_bar(self, dataset):
        """合成日k线"""
        for d in dataset:
            contract = d['instrument_id']
            if contract not in self._k_bar:
                self._k_bar[contract] = [d]
                continue
            if len(self._k_bar[contract]) < 2:
                self.k_lock.acquire()
                self._k_bar[contract].append(d)
                self.k_lock.release()
                continue
            self.k_lock.acquire()
            self._k_bar[contract][1] = d
            self.k_lock.release()

    def _save_k_bar(self):
        data = []
        for value in self._k_bar.values():
            fst, snd = value
            row = DailyQuote(
                instrument_id=fst['instrument_id'], date=arrow.get(snd['date']).format('YYYY-MM-DD'),
                open=float(fst['close']), high=float(snd['high']), low=float(snd['low']), close=float(snd['close'])
            )
            data.append(row)
        DailyQuote.bulk_create(data)
        self._k_bar = {}

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
                # time.sleep(10)
                continue
            stream, records = items[0]
            if not records:
                # time.sleep(10)
                continue
            ids = []
            dataset = []
            for item in records:
                xid, info = item
                ids.append(xid)
                info = {x.decode(): y.decode() for x, y in info.items()}
                dataset.append(info)
            self._redis.xack(self.c.name, self.c.name+"_group", *ids)
            ThreadExecutor.submit(self.proc, dataset)
            ThreadExecutor.submit(self._save)
            ThreadExecutor.submit(self.k_bar, dataset)
