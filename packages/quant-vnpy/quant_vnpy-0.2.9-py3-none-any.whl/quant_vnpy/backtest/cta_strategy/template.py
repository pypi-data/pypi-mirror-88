"""
@author  : MG
@Time    : 2020/11/16 10:20
@File    : template.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
from typing import Optional, Dict

import pandas as pd
from ibats_utils.mess import datetime_2_str, date_2_str
from vnpy.app.cta_strategy import TargetPosTemplate as TargetPosTemplateBase
from vnpy.trader.constant import Offset
from vnpy.trader.object import OrderData, BarData, TickData, TradeData

from quant_vnpy.backtest.cta_strategy.run import get_output_file_path
from quant_vnpy.config import logging
from quant_vnpy.db.orm import StrategyStatusEnum, StrategyStatusMonitorThread
from quant_vnpy.report.collector import trade_data_collector, order_data_collector
from quant_vnpy.utils.enhancement import BarGenerator


class TargetPosTemplate(TargetPosTemplateBase):

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        self.logger = logging.getLogger(strategy_name)
        self._orders = []  # 记录所有订单数据
        # 仅用于 on_order 函数记录上一个 order 使用，解决vnpy框架重复发送order的问题
        self._last_order = None
        self._trades = []  # 记录所有成交数据
        self.current_bar: Optional[BarData] = None
        self.bar_count = 0
        self.bg = BarGenerator(self.on_bar)
        self._is_realtime_mode = self.strategy_name is not None and self.strategy_name != self.__class__.__name__
        self._strategy_status = StrategyStatusEnum.Created
        if self._is_realtime_mode:
            self._strategy_status_monitor = StrategyStatusMonitorThread(
                self.strategy_name,
                self._get_strategy_status,
                self._set_strategy_status,
                self.vt_symbol,
            )
            self._lock = self._strategy_status_monitor.lock
        else:
            self._strategy_status_monitor = None
            self._lock = None

    def _get_positions(self) -> Dict[str, int]:
        return {self.vt_symbol: self.pos}

    def _set_strategy_status(self, status: StrategyStatusEnum):
        if self._strategy_status == status:
            return

        if status == StrategyStatusEnum.RunPending and self._strategy_status not in (
                StrategyStatusEnum.Created, StrategyStatusEnum.Running
        ):
            # StrategyStatusEnum.RunPending 状态只从数据库端发起
            if self._lock is not None:
                self._lock.acquire()

            try:
                # 保险起见，为防止出现死循环调用，在 on_start 先把状态调整过来
                self._strategy_status = status
                self.write_log(f"策略 {self.strategy_name}[{self.vt_symbol}] 状态 "
                               f"{self._strategy_status.name} -> {status.name} 被远程启动")
            finally:
                if self._lock is not None:
                    self._lock.release()

            self.on_start()

        elif status == StrategyStatusEnum.StopPending and self._strategy_status == StrategyStatusEnum.Running:
            # StrategyStatusEnum.StopPending 状态只从数据库端发起
            if self._lock is not None:
                self._lock.acquire()

            try:
                # 保险起见，为防止出现死循环调用，在 on_stop 先把状态调整过来
                self._strategy_status = status
                self.write_log(f"策略 {self.strategy_name}[{self.vt_symbol}] 状态 "
                               f"{self._strategy_status.name} -> {status.name} 被远程停止")
            finally:
                if self._lock is not None:
                    self._lock.release()

            self.on_stop()
        else:
            self.write_log(f"策略 {self.strategy_name}{self.vt_symbol} 状态 "
                           f"{self._strategy_status.name} -> {status.name}")
            self._strategy_status = status

    def _get_strategy_status(self) -> StrategyStatusEnum:
        return self._strategy_status

    def on_init(self) -> None:
        super().on_init()
        self.bar_count = 0
        self._set_strategy_status(StrategyStatusEnum.Initialized)
        if self._strategy_status_monitor is not None:
            self._strategy_status_monitor.start()

    def on_start(self) -> None:
        super().on_start()
        self._set_strategy_status(StrategyStatusEnum.Running)
        # 整理持仓信息
        self.write_log(f"策略启动，当前初始持仓： {self.vt_symbol} {self.pos}")
        self.put_event()

    def on_tick(self, tick: TickData):
        super().on_tick()
        # 激活分钟线 on_bar
        self.bg.update_tick(tick)

    def on_bar(self, bar: BarData):
        super().on_bar(bar)
        self.current_bar: BarData = bar
        self.bar_count += 1

    def on_order(self, order: OrderData):
        super().on_order(order)
        # self.write_log(
        #     f"{order.direction.value} {order.offset.value} {order.price:.1f}"
        #     if order.datetime is None else
        #     f"{datetime_2_str(order.datetime)} {order.direction.value} {order.offset.value} {order.price:.1f}"
        # )
        current_pos = int(self.pos)
        order_datetime = order.datetime
        if order.offset == Offset.OPEN:
            self.write_log(
                f"{order.vt_symbol:>11s} {order.direction.value} {order.offset.value:4s} "
                f"{order.price:.1f} {current_pos:+d} {order.volume:+.0f} "
                if order_datetime is None else
                f"{datetime_2_str(order_datetime)} {order.vt_symbol} {order.direction.value} {order.offset.value:4s} "
                f"{order.price:.1f} {current_pos:+d} {order.volume:+.0f}",
                'debug'
            )
        else:
            self.write_log(
                f"{order.vt_symbol:>11s} {order.direction.value} {order.offset.value:4s} "
                f"{order.price:.1f}       {current_pos:+d} {-order.volume:+.0f} "
                if order_datetime is None else
                f"{datetime_2_str(order_datetime)} {order.vt_symbol} {order.direction.value} {order.offset.value:4s} "
                f"{order.price:.1f}       {current_pos:+d} {-order.volume:+.0f}",
                'debug'
            )

        if self._last_order is None or self._last_order.orderid != order.orderid:
            self._orders.append(order)
            if self._is_realtime_mode:
                order_data_collector.put_nowait(self.strategy_name, order)
            self._last_order = order

    def on_trade(self, trade: TradeData):
        super().on_trade(trade)
        self._trades.append(trade)
        if self._is_realtime_mode:
            trade_data_collector.put_nowait(self.strategy_name, trade)

    def on_stop(self):
        super().on_stop()
        self._set_strategy_status(StrategyStatusEnum.Stopped)
        self.put_event()
        if self._is_realtime_mode:
            self.report()

    def report(self):
        date_str = date_2_str(self.current_bar.datetime)
        # 处理 trade
        trade_df = pd.DataFrame([{
            "datetime": _.datetime.replace(tzinfo=None),
            "symbol": _.symbol,
            "direction": _.direction.value,
            "offset": _.offset.value,
            "price": _.price,
            "volume": _.volume,
            "orderid": _.orderid,
            "tradeid": _.tradeid,
        } for _ in self._trades]).set_index("orderid")
        file_path = get_output_file_path(
            "data", f"trade_{date_str}.csv",
            root_folder_name=self.strategy_name,
        )
        trade_df.to_csv(file_path)
        # 处理 Order
        order_df = pd.DataFrame([{
            "datetime": _.datetime.replace(tzinfo=None),
            "symbol": _.symbol,
            "direction": _.direction.value,
            "offset": _.offset.value,
            "price": _.price,
            "volume": _.volume,
            "order_type": _.type.value,
            "orderid": _.orderid,
        } for _ in self._orders]).set_index("orderid")
        file_path = get_output_file_path(
            "data", f"order_{date_str}.csv",
            root_folder_name=self.strategy_name,
        )
        trade_df.to_csv(file_path)
        # 合并 order trade
        order_trade_df = pd.concat(
            [order_df, trade_df],
            keys=['order', 'trade'],
            axis=1, sort=True,
        )

        file_path = get_output_file_path(
            "data", f"order_trade_{date_str}.csv",
            root_folder_name=self.strategy_name,
        )
        order_trade_df.to_csv(file_path)
        order_trade_df['datetime'] = order_trade_df.apply(
            lambda x: x['order']['datetime'] if pd.isna(x['trade']['datetime']) else x['trade']['datetime'],
            axis=1
        )
        order_trade_df.drop([('order', 'datetime'), ('trade', 'datetime')], axis=1, inplace=True)
        order_trade_df = order_trade_df[[
            ('datetime', ''),
            ('order', 'symbol'),
            ('order', 'direction'),
            ('order', 'offset'),
            ('order', 'price'),
            ('order', 'volume'),
            ('order', 'order_type'),
            ('trade', 'price'),
            ('trade', 'volume'),
            ('trade', 'tradeid'),
        ]]
        order_trade_df.sort_values('datetime', inplace=True)
        file_path = get_output_file_path(
            "data", f"order_trade_{date_str}.xlsx",
            root_folder_name=self.strategy_name,
        )
        order_trade_df.to_excel(file_path)
        self.logger.info('截止%s下单情况明细：\n%s', datetime_2_str(self.current_bar.datetime), order_df)

    def write_log(self, msg: str, logger_method='info'):
        msg = f"{self.strategy_name} {msg}"
        super().write_log(msg)
        getattr(self.logger, logger_method)(msg)


if __name__ == "__main__":
    pass
