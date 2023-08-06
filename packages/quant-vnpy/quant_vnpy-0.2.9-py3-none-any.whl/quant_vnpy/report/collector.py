"""
@author  : MG
@Time    : 2020/12/9 13:05
@File    : collector.py
@contact : mmmaaaggg@163.com
@desc    : 用户收集策略运行过程中的下单、成交等数据
采用独立线程进行数据采集工作，以避免出现因插入数据造成策略延迟或阻塞，保证策略线程运行平稳
"""
__all__ = ('trade_data_collector', 'order_data_collector')

import logging
from queue import Queue, Empty
from threading import Thread
from typing import List, Callable, Dict

from vnpy.trader.object import TradeData, OrderData

from quant_vnpy.db.orm import database, TradeDataModel, OrderDataModel


class OrderDataCollector(Thread):

    def __init__(self):
        super().__init__(daemon=True)
        self.queue = Queue()
        self.is_running = True
        self.logger = logging.getLogger(self.__class__.__name__)

    def put_nowait(self, strategy_name, trade_data):
        self.queue.put_nowait((strategy_name, trade_data))

    def join_queue(self):
        self.queue.join()

    def run(self) -> None:
        data_list: List[(str, OrderData,)] = []
        while self.is_running:
            try:
                strategy_name, order_data = self.queue.get(timeout=1)
                data_list.append(dict(
                    strategy_name=strategy_name,
                    orderid=order_data.orderid,
                    symbol=order_data.symbol,
                    exchange=order_data.exchange.value,
                    order_type=order_data.type.value,
                    direction=order_data.direction.value,
                    offset=order_data.offset.value,
                    price=order_data.price,
                    volume=order_data.volume,
                    status=order_data.status.value,
                    datetime=order_data.datetime,
                ))
                self.queue.task_done()
            except Empty:
                if len(data_list) == 0:
                    continue
                # 攒够一个list，开始集中插入
                try:
                    with database.atomic():
                        # 每次批量插入100条，分成多次插入
                        OrderDataModel.insert_many(data_list).execute()
                        self.logger.info("插入订单数据 %d 条", len(data_list))
                        data_list = []
                finally:
                    OrderDataModel._meta.database.close()


order_data_collector = OrderDataCollector()
order_data_collector.start()


class TradeDataCollector(Thread):

    def __init__(self):
        super().__init__(daemon=True)
        self.queue = Queue()
        self.is_running = True
        self.logger = logging.getLogger(self.__class__.__name__)

    def put_nowait(self, strategy_name, trade_data):
        self.queue.put_nowait((strategy_name, trade_data))

    def join_queue(self):
        self.queue.join()

    def run(self) -> None:
        data_list: List[(str, TradeData,)] = []
        while self.is_running:
            try:
                strategy_name, trade_data = self.queue.get(timeout=1)
                data_list.append(dict(
                    strategy_name=strategy_name,
                    symbol=trade_data.symbol,
                    exchange=trade_data.exchange.value,
                    orderid=trade_data.orderid,
                    tradeid=trade_data.tradeid,
                    direction=trade_data.direction.value,
                    offset=trade_data.offset.value,
                    price=trade_data.price,
                    volume=trade_data.volume,
                    datetime=trade_data.datetime,
                ))
                self.queue.task_done()
            except Empty:
                if len(data_list) == 0:
                    continue
                # 攒够一个list，开始集中插入
                try:
                    with database.atomic():
                        # 每次批量插入100条，分成多次插入
                        TradeDataModel.insert_many(data_list).execute()
                        self.logger.info("插入交易数据 %d 条", len(data_list))
                        data_list = []
                finally:
                    TradeDataModel._meta.database.close()


trade_data_collector = TradeDataCollector()
trade_data_collector.start()


class StrategyPositionMonitor(Thread):

    def __init__(self):
        super().__init__(daemon=True)
        self.queue = Queue()
        self.is_running = True
        self.logger = logging.getLogger(self.__class__.__name__)
        self.strategy_get_pos_func_dic = {}

    def register_get_pos(self, strategy_name: str, get_positions_func: Callable[[], Dict[str, int]]) -> None:
        """
        注册 get_position 方法
        """
        self.strategy_get_pos_func_dic[strategy_name] = get_positions_func

    def run(self) -> None:
        while self.is_running:
            break
