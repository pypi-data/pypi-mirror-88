"""
@author  : MG
@Time    : 2020/11/16 10:20
@File    : template.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
from datetime import datetime
from typing import List, Dict, Optional

import pandas as pd
from ibats_utils.mess import datetime_2_str
from vnpy.app.portfolio_strategy import StrategyTemplate as StrategyTemplateBase
from vnpy.trader.constant import Direction, Offset
from vnpy.trader.object import BarData, TickData

from quant_vnpy.backtest.cta_strategy.run import get_output_file_path
from quant_vnpy.config import logging
from quant_vnpy.db.orm import StrategyStatusEnum, StrategyStatusMonitorThread
from quant_vnpy.utils.enhancement import BarGenerator


class StrategyTemplate(StrategyTemplateBase):
    # 该标识位默认为0（关闭状态）。为1时开启，程序一旦平仓后则停止后续交易。该标识位用于在切换合约时使用
    stop_if_pos_2_0 = 0

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        self.logger = logging.getLogger(strategy_name)
        self.send_order_list = []
        self.current_bars = None
        self.bar_count = 0
        self._strategy_status = StrategyStatusEnum.Created
        self._strategy_status_monitor = StrategyStatusMonitorThread(
            self.strategy_name,
            self._get_strategy_status,
            self._set_strategy_status,
            self.vt_symbols
        ) if self.strategy_name is not None and self.strategy_name != self.__class__.__name__ else None
        self._lock = self._strategy_status_monitor.lock if self._strategy_status_monitor is not None else None
        self.last_tick_time: Optional[datetime] = None

        def on_bar(bar: BarData):
            """"""
            pass

        self.bgs: Dict[str, BarGenerator] = {}
        for vt_symbol in self.vt_symbols:
            self.bgs[vt_symbol] = BarGenerator(on_bar)

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
                self.write_log(f"策略 {self.strategy_name}{self.vt_symbols} 状态 "
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
                self.write_log(f"策略 {self.strategy_name}{self.vt_symbols} 状态 "
                               f"{self._strategy_status.name} -> {status.name} 被远程停止")
            finally:
                if self._lock is not None:
                    self._lock.release()

            self.on_stop()
        else:
            self.write_log(f"策略 {self.strategy_name}{self.vt_symbols} 状态 "
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
        pos_str = '\n'.join([f"{k}: {v}" for k, v in self.pos.items()])
        self.write_log(f"策略启动，当前初始持仓：\n{pos_str}")
        self.put_event()

    def on_tick(self, tick: TickData) -> None:
        super().on_tick(tick)
        if (
                self.last_tick_time
                and self.last_tick_time.minute != tick.datetime.minute
        ):
            bars = {}
            for vt_symbol, bg in self.bgs.items():
                bars[vt_symbol] = bg.generate()
            self.on_bars(bars)

        bg: BarGenerator = self.bgs[tick.vt_symbol]
        bg.update_tick(tick)
        self.last_tick_time = tick.datetime

    def on_bars(self, bars: Dict[str, BarData]) -> None:
        super().on_bars(bars)
        self.current_bars = bars
        self.bar_count += 1

    def send_order(self,
                   vt_symbol: str,
                   direction: Direction,
                   offset: Offset,
                   price: float,
                   volume: float,
                   lock: bool = False
                   ) -> List[str]:
        current_pos = int(self.get_pos(vt_symbol))
        order_datetime = self.current_bars[vt_symbol].datetime if vt_symbol in self.current_bars else None
        if offset == Offset.OPEN:
            if self.stop_if_pos_2_0:
                addon_str = " 当前策略 stop_if_pos_2_0 开启，所有开仓指令将被忽略"
            else:
                addon_str = ''

            self.write_log(
                f"{vt_symbol:>11s} {direction.value} {offset.value:4s} {price:.1f} "
                f"{current_pos:+d} {volume:+.0f} "
                if order_datetime is None else
                f"{datetime_2_str(order_datetime)} {vt_symbol} {direction.value} {offset.value:4s} {price:.1f} "
                f"{current_pos:+d} {volume:+.0f}{addon_str}",
                'debug'
            )
        else:
            self.write_log(
                f"{vt_symbol:>11s} {direction.value} {offset.value:4s} {price:.1f} "
                f"      {current_pos:+d} {-volume:+.0f} "
                if order_datetime is None else
                f"{datetime_2_str(order_datetime)} {vt_symbol} {direction.value} {offset.value:4s} {price:.1f} "
                f"      {current_pos:+d} {-volume:+.0f}",
                'debug'
            )

        if order_datetime is None:
            order_datetime = datetime.now()

        if self.stop_if_pos_2_0 and offset == Offset.OPEN:
            return []
        else:
            self.send_order_list.append({
                "datetime": order_datetime,
                "vt_symbol": vt_symbol, "direction": direction.value,
                "offset": offset.value, "price": price, "volume": volume
            })
            return super().send_order(vt_symbol, direction, offset, price, volume, lock)

    def on_stop(self):
        super().on_stop()
        order_df = pd.DataFrame(self.send_order_list)
        file_path = get_output_file_path(
            "data", "orders.csv",
            root_folder_name=self.strategy_name,
        )
        order_df.to_csv(file_path)
        self.logger.info('运行期间下单情况明细：\n%s', order_df)
        self._set_strategy_status(StrategyStatusEnum.Stopped)
        # 整理持仓信息
        pos_str = '\n'.join([f"{k}: {v}" for k, v in self.pos.items()])
        self.write_log(f"策略停止，当前初始持仓：\n{pos_str}")
        self.put_event()

    def write_log(self, msg: str, logger_method='info'):
        msg = f"{self.strategy_name} {msg}"
        super().write_log(msg)
        getattr(self.logger, logger_method)(msg)


if __name__ == "__main__":
    pass
