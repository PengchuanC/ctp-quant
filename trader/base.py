"""
@author: chuanchao.peng
@date: 2021/12/23 13:41
@file base.py
@desc:
"""

from typing import Callable
from queue import Queue
from threading import Lock
from concurrent.futures import ThreadPoolExecutor

import arrow

from ftdc import rsp, order
from database.models import Notification
from logger.logger import logger


def now():
    return arrow.now().format('YYYY-MM-DD HH:mm:ss')


class BaseTradeBroker(object):

    order_list = Queue()
    notifications = Queue()
    spi = None
    pool = ThreadPoolExecutor(2)
    _monitor = False

    def register_spi(self, spi):
        """挂载交易spi"""
        self.spi = spi

    def on_connected(self):
        """连接成功时调用"""
        self.notifications.put((now(), 'spi-交易服务器连接成功'))
        self.spi.execute_waited()

    def on_disconnect(self, reason: int):
        """连接断开"""
        self.notifications.put((now(), f'spi-交易服务器连接断开,原因：{reason}'))

    def on_authenticate(self, pRspAuthenticateField):
        """处理客户端认证响应"""
        self.spi.execute_waited()

    def on_login(self, pRspUserLogin: rsp.RspUserLoginField):
        """处理登陆响应"""
        self.notifications.put((now(), f'spi-登陆成功,SessionID={pRspUserLogin.SessionID}'))
        # 登陆成功，开始事件循环，处理交易
        if not self._monitor:
            self.pool.submit(self.trade_loop)
            self.pool.submit(self.notify_loop)
            self._monitor = True

    def insert_order(self, order_info: order.InputOrderField):
        """将下单指令下发至待执行队列"""
        self.order_list.put(order_info)

    def on_order(self, p_order: order.OrderField):
        """报单成功"""
        notify = f'\nspi-报单通知\n\tOrderStatus={p_order.OrderStatus}, StatusMsg={p_order.StatusMsg}' \
                 f'\n\tLimitPrice={p_order.LimitPrice}, SettlementID={p_order.SettlementID}'
        self.notifications.put((now, notify))

    def on_order_err(self, p_order: order.InputOrderField):
        """报单失败"""
        pass

    def on_trade(self, trade: order.TraderField):
        """报单成功，成交通知"""
        notify = f'\nspi-成交通知\n\tInstrumentID={trade.InstrumentID}\n\tTradeID={trade.TradeID}' \
                 f'\n\tPrice|Volume|Direction\n\t{trade.Price}|{trade.Volume}|{trade.Direction}' \
                 f'\n\tTradeDate={trade.TradeDate}\n\tTradeTime={trade.TradeTime}'
        self.notifications.put((now, notify))

    def on_investor_position(self, position: rsp.InvestorPositionField):
        """投资者持仓响应"""
        p = position
        print(p.InstrumentID, p.TradingDay, p.PosiDirection, p.Position, p.PositionProfit)

    def on_cancel(self):
        """执行撤单"""
        pass

    def on_monitor(self, callback: Callable):
        """
        查询持仓
        Args:
            callback: 回调函数，处理持仓数据
        """
        pass

    def on_settlement_confirm(self, pSettlementInfoConfirm: rsp.SettlementInfoConfirmField,):
        """请求查询结算信息确认响应"""
        pass

    def trade_loop(self):
        """交易指令监听"""
        while True:
            if self.order_list.empty():
                continue
            order_info = self.order_list.get()
            self.spi.trade(order_info)

    def notify_loop(self):
        """通知监听"""
        lock = Lock()
        notifications = []
        while True:
            if self.notifications.empty():
                if notifications:
                    lock.acquire()
                    Notification.bulk_create(notifications)
                    notifications = []
                    lock.release()
                continue
            date, notify = self.notifications.get()
            notifications.append(Notification(date=date, msg=notify))
            logger.info(notify)

