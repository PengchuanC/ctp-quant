"""
@author: chuanchao.peng
@date: 2021/12/23 13:41
@file base.py
@desc:
"""
import time
from typing import Callable
from queue import Queue
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
from threading import Event

import arrow
from loguru import logger

from settings.settings import USERINFO
from ftdc import rsp, order
from database.models import Notification


def now():
    return arrow.now().format('YYYY-MM-DD HH:mm:ss')


class BaseTradeBroker(object):

    order_list = Queue()
    notifications = Queue()
    spi = None
    pool = ThreadPoolExecutor(3)
    event = Event()
    _monitor = False

    # 报单引用编号
    order_ref = 0
    # 缓存数据
    data = {'position': {}}

    def register_spi(self, spi):
        """挂载交易spi"""
        self.spi = spi

    def on_connected(self):
        """连接成功时调用"""
        self.pool.submit(self.notify_loop)
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
        self.spi.execute_waited()

    def insert_order(self, order_info: order.InputOrderField):
        """将下单指令下发至待执行队列"""
        order_info.OrderRef = str(self.order_ref)
        self.order_list.put(order_info)
        self.order_ref += 1

    def on_order(self, p_order: order.OrderField):
        """报单成功"""
        notify = f'\nspi-报单通知\n\tInstrumentID|Status|StatusMsg|LimitPrice|Direction|InsertTime\n\t' \
                 f'{p_order.InstrumentID}|{p_order.OrderStatus}|{p_order.StatusMsg}|{p_order.LimitPrice}|' \
                 f'{p_order.Direction}|{p_order.InsertTime}'
        self.notifications.put((now(), notify))

    def on_order_err(self, p_order: order.InputOrderField, p_info: rsp.RspInfoField):
        """报单失败"""
        self.notifications.put((now(), f'spi-报单录入失败,ErrorMsg={p_info.ErrorMsg}'))

    def on_trade(self, trade: order.TraderField):
        """报单成功，成交通知"""
        notify = f'\nspi-成交通知\n\tInstrumentID={trade.InstrumentID}\n\tTradeID={trade.TradeID}' \
                 f'\n\tPrice|Volume|Direction\n\t{trade.Price}|{trade.Volume}|{trade.Direction}' \
                 f'\n\tTradeDate={trade.TradeDate}\n\tTradeTime={trade.TradeTime}'
        self.notifications.put((now, notify))
        self.spi.qry_investor_position(trade.InstrumentID, trade.ExchangeID)

    def on_investor_position(self, position: rsp.InvestorPositionField):
        """投资者持仓响应"""
        p = position
        self.data['position'][p.InstrumentID] = {
            'instrument_id': p.InstrumentID, 'date': p.TradingDay, 'direction': p.PosiDirection,
            'position': float(p.Position), 'profit': float(p.PositionProfit)
        }
        print(self.data['position'][p.InstrumentID])

    def get_position(self, instrument_id: str):
        """获取持仓"""
        return self.data['position'].get(instrument_id)

    def on_cancel(self):
        """执行撤单"""
        pass

    def on_settlement(self, pSettlementInfo: rsp.SettlementInfoField):
        """投资者结算结果响应"""
        self.notifications.put((now(), 'spi-投资者结算查询成功'))
        self.spi.req_qry_settlement_info_confirm()

    def on_settlement_confirm(self, pSettlementInfoConfirm: rsp.SettlementInfoConfirmField,):
        """请求查询结算信息确认响应"""
        # 结算确认成功，开始事件循环，处理交易
        self.notifications.put((now(), f'spi-交易结算确认成功,开始监听下单指令队列'))
        if not self._monitor:
            self.pool.submit(self.trade_loop)
            self._monitor = True

    def trade_loop(self):
        """交易指令监听"""
        self.notifications.put((now(), '开始监听下单指令队列'))
        while True:
            if self.order_list.empty():
                continue
            order_info = self.order_list.get()
            self.spi.trade(order_info)

    def notify_loop(self):
        """通知监听"""
        self.notifications.put((now(), '开始监听通知队列'))
        notifications = []
        while True:
            try:
                if self.notifications.empty():
                    if len(notifications) > 0:
                        try:
                            # Notification.bulk_create(notifications)
                            notifications = []
                        except Exception as e:
                            logger.exception(e)
                            break
                    continue
                date, notify = self.notifications.get()
                n = Notification(date=date, msg=notify)
                notifications.append(n)
                logger.info(notify)
            except Exception as e:
                logger.exception(e)
                break
