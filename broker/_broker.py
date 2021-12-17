"""
@author：chuanchao.peng
@date: 2021-12-08
@desc: 创建数据处理的Broker
"""

import abc


class Broker(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def do(self, *args, **kwargs):
        """回调函数，供publisher调用"""
        pass

    @abc.abstractmethod
    def register(self, name, publisher: "Publisher"):
        """注册到publisher"""
        pass
