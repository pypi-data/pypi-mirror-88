"""
@author  : MG
@Time    : 2020/12/11 8:00
@File    : monitor.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
import datetime
import logging
import time
from threading import Thread, Lock
from typing import Callable, Optional, Dict, Tuple, List

import pandas as pd
from ibats_utils.mess import date_2_str, str_2_datetime, datetime_2_str
from peewee import DatabaseError
from vnpy.trader.constant import Direction, Offset
from vnpy.trader.object import TickData

from quant_vnpy.constants import SYMBOL_SIZE_DIC
from quant_vnpy.db.orm import TradeDataModel, PositionStatusModel, StrategyStatus, \
    StrategyStatusEnum
from quant_vnpy.utils.enhancement import get_instrument_type


class StrategyPositionMonitor(Thread):
    logger = logging.getLogger("StrategyPositionMonitor")

    def __init__(self):
        super().__init__(daemon=True)
        self.is_running = True
        self.strategy_get_pos_func_dic: Dict[str, Callable[[], Dict[str, Tuple[int, TickData]]]] = {}
        # 预留2分钟避免应为延时或者时间不准导致的计算错误
        # 时间范围列表需要保持递增的时间顺序
        self.time_period_list = [
            ['09:02:30', '11:32:30'],
            ['13:32:30', '15:02:30'],
            ['21:02:30', '23:02:30']
        ]
        self.time_period_list = [[datetime.time.fromisoformat(_[0]), datetime.time.fromisoformat(_[1])]
                                 for _ in self.time_period_list]
        self._last_dt = None

    def register_get_pos(self, strategy_name: str,
                         get_pos_and_price: Callable[[], Dict[str, Tuple[int, TickData]]]) -> None:
        """
        注册 get_position 方法
        """
        self.strategy_get_pos_func_dic[strategy_name] = get_pos_and_price

    def get_sleep_seconds(self, minutes=5):
        now_dt = datetime.datetime.now()
        now_time = now_dt.time()
        today_str = date_2_str(datetime.date.today())
        for time_from, time_to in self.time_period_list:
            # 如果当前时间小于起始时间，则直接sleep，直到起始时间
            if now_time < time_from:
                target_dt = str_2_datetime(today_str + time_from.strftime(" %H:%M:%S"))
                delta = target_dt - now_dt
                seconds = delta.total_seconds()
                self._last_dt = target_dt
                break

            if self._last_dt is None:
                # 如果首次执行
                if time_from < now_time < time_to:
                    # 在时间区间内
                    target_dt = now_dt
                    seconds = 0
                    self._last_dt = now_dt
                    break
            elif time_from < self._last_dt.time() < time_to:
                # 如果此前执行过，且上一次执行时间在此区间内
                target_dt: datetime.datetime = max(
                    min(str_2_datetime(today_str + time_to.strftime(" %H:%M:%S")),
                        self._last_dt + datetime.timedelta(minutes=minutes)),
                    now_dt)
                delta = target_dt - now_dt
                seconds = delta.total_seconds()
                self._last_dt = target_dt
                break
        else:
            # 次日第一时间执行
            target_dt = str_2_datetime(
                date_2_str(datetime.date.today() + datetime.timedelta(days=1)) +
                self.time_period_list[0][0].strftime(" %H:%M:%S")
            )
            delta = target_dt - now_dt
            seconds = delta.total_seconds()
            self._last_dt = target_dt

        self.logger.debug("Next pos scan datetime is %s", datetime_2_str(target_dt))
        return seconds

    def refresh_positions(self):
        """更新各个策略的持仓盈亏情况"""
        strategy_symbol_pos_status_dic: Dict[str, Dict[str, PositionStatusModel]] = \
            PositionStatusModel.query_latest_position_status()
        strategy_status_list: List[StrategyStatus] = StrategyStatus.query_all()
        for strategy_status in strategy_status_list:
            strategy_name = strategy_status.strategy_name
            if strategy_name in strategy_symbol_pos_status_dic:
                self.refresh_positions_of_strategy(strategy_name, strategy_symbol_pos_status_dic[strategy_name])
            else:
                self.refresh_positions_of_strategy(strategy_name, None)

    def refresh_positions_of_strategy(
            self, strategy_name: str, symbol_pos_status_dic: Optional[Dict[str, PositionStatusModel]]):
        """按策略计算相关合约的持仓、收益计算"""
        # 获取交易记录
        if symbol_pos_status_dic is None:
            # 如果 symbol_pos_status_dic 空，加载全部策略相关交易记录进行重现计算
            symbol_trade_data_list_dic: Dict[str, List[TradeDataModel]] = \
                TradeDataModel.query_trade_data_by_strategy_since(strategy_name, None)
        else:
            # 获得最新更新时间，获取再次之后的算不交易记录
            max_update_dt = max([_.update_dt for _ in symbol_pos_status_dic.values()])
            symbol_trade_data_list_dic: Dict[str, List[TradeDataModel]] = \
                TradeDataModel.query_trade_data_by_strategy_since(strategy_name, max_update_dt)

        # 将交易记录按照 symbol 进行分类，并分别计算
        symbol_set = set(symbol_trade_data_list_dic.keys())
        if symbol_pos_status_dic is not None:
            symbol_set |= set(symbol_pos_status_dic.keys())
        for symbol in symbol_set:
            pos_status = symbol_pos_status_dic[symbol] \
                if symbol_pos_status_dic is not None and symbol in symbol_pos_status_dic else None
            trade_data_list = symbol_trade_data_list_dic[symbol] if symbol in symbol_trade_data_list_dic else []
            self.refresh_positions_by_trade_date(strategy_name, symbol, pos_status, trade_data_list)

    def refresh_positions_by_trade_date(
            self, strategy_name: str, symbol: str,
            pos_status: Optional[PositionStatusModel], trade_data_list: List[TradeDataModel]
    ):
        """根据交易记录更新相应策略及symbol的持仓状态"""
        instrument_type = get_instrument_type(symbol).upper()
        multiplier = SYMBOL_SIZE_DIC.setdefault(instrument_type, 10)
        self.logger.debug("开始更新 %s %s 持仓状态", strategy_name, symbol)
        if pos_status is not None:
            offset_acc_gl = pos_status.offset_acc_gl
            pos_status_dict = dict(
                tradeid=pos_status.tradeid,
                strategy_name=strategy_name,
                symbol=symbol,
                exchange=pos_status.exchange,
                trade_date=pos_status.trade_date,
                trade_dt=pos_status.trade_dt,
                direction=pos_status.direction,
                avg_price=pos_status.avg_price,
                volume=pos_status.volume,
                holding_gl=pos_status.holding_gl,
                offset_gl=pos_status.offset_gl,
                offset_daily_gl=pos_status.offset_daily_gl,
                offset_acc_gl=offset_acc_gl,
                update_dt=pos_status.update_dt,
            )
        else:
            offset_acc_gl = 0
            pos_status_dict = dict(
                tradeid='',
                strategy_name=strategy_name,
                symbol=symbol,
                volume=0,
                avg_price=0,
                holding_gl=0,
                offset_gl=0,
                offset_daily_gl=0,
                offset_acc_gl=offset_acc_gl,
            )

        pos_status_new_list: List[dict] = []
        holding_trade_data_list: List[TradeDataModel] = []  # 相当于一个先入先出队列，用于处理平仓后的价格信息
        curr_closing_trade_data: Optional[TradeDataModel] = None
        curr_closing_trade_data_vol_left = 0
        offset_daily_gl = 0
        trade_date_last = None
        for trade_data in trade_data_list:
            # 检查是否到新的一个交易日，如果是，则 offset_daily_gl 重置为 0
            if trade_date_last is None or trade_date_last != trade_data.datetime.date():
                offset_daily_gl = 0
                trade_date_last = trade_data.datetime.date()

            if trade_data.offset == Offset.OPEN.value:
                # 开仓，检查方向一致的情况下更数据，方向不一致，warning，同时忽略
                if pos_status_dict['volume'] != 0 and pos_status_dict['direction'] != trade_data.direction:
                    self.logger.warning(
                        "交易记录 %s %s %s %.0f 与当前持仓方向不一致，忽略",
                        trade_data.tradeid, trade_data.direction, trade_data.offset, trade_data.volume)
                    continue
                volume = pos_status_dict['volume']
                volume_new = trade_data.volume + volume
                avg_price = pos_status_dict['avg_price']
                avg_price_new = (trade_data.price * trade_data.volume + avg_price * volume) / volume_new
                # 更新持仓状态信息
                pos_status_new_dict = dict(
                    tradeid=trade_data.tradeid,
                    strategy_name=strategy_name,
                    symbol=symbol,
                    exchange=trade_data.exchange,
                    trade_date=trade_data.datetime.date(),
                    trade_dt=trade_data.datetime,
                    direction=trade_data.direction,
                    avg_price=avg_price_new,
                    volume=volume_new,
                    holding_gl=volume_new * (trade_data.price - avg_price_new) * multiplier,
                    offset_daily_gl=offset_daily_gl,
                    offset_acc_gl=offset_acc_gl,
                    update_dt=datetime.datetime.now(),
                )
                pos_status_new_list.append(pos_status_new_dict)
                holding_trade_data_list.append(trade_data)
            else:
                # 平仓，检查持仓是否0，如果是则 warning，同时忽略
                if pos_status_dict["volume"] == 0:
                    self.logger.warning(
                        "交易记录 %s %s %s %.0f 没有对应的持仓数据，忽略",
                        trade_data.tradeid, trade_data.direction, trade_data.offset, trade_data.volume)
                    continue
                # 平仓，检查方向与持仓是否相反，如果方向一致，warning，同时忽略
                if pos_status_dict['direction'] == trade_data.direction:
                    self.logger.warning(
                        "交易记录 %s %s %s %.0f 与当前持仓方向一致，忽略",
                        trade_data.tradeid, trade_data.direction, trade_data.offset, trade_data.volume)
                    continue
                volume = pos_status_dict['volume']
                volume_new = volume - trade_data.volume
                if volume_new < 0:
                    self.logger.warning(
                        "交易记录 %s %s %s %.0f 超过当前持仓 %.0f 手，忽略",
                        trade_data.tradeid, trade_data.direction, trade_data.offset, trade_data.volume, volume)
                    continue
                # 计算平仓盈亏
                offset_gl = 0
                # 根据先入先出原则处理检查平仓了多少个历史的交易订单
                close_vol = trade_data.volume
                if curr_closing_trade_data_vol_left >= close_vol:
                    curr_closing_trade_data_vol_left -= close_vol
                    offset_gl += close_vol * (
                            trade_data.price - curr_closing_trade_data.price
                    ) * (1 if curr_closing_trade_data.direction == Direction.LONG.value else -1)
                else:
                    if curr_closing_trade_data_vol_left > 0:
                        offset_gl += curr_closing_trade_data_vol_left * (
                                trade_data.price - curr_closing_trade_data.price
                        ) * (1 if curr_closing_trade_data.direction == Direction.LONG.value else -1)
                        close_vol = trade_data.volume - curr_closing_trade_data_vol_left
                    else:
                        close_vol = trade_data.volume

                    for i in range(len(holding_trade_data_list)):
                        # 先入先出，总是从第一个位置去交易数据
                        curr_closing_trade_data = holding_trade_data_list.pop(0)
                        curr_closing_trade_data_vol_left = curr_closing_trade_data.volume
                        if curr_closing_trade_data_vol_left >= close_vol:
                            offset_gl += close_vol * (
                                    trade_data.price - curr_closing_trade_data.price
                            ) * (1 if curr_closing_trade_data.direction == Direction.LONG.value else -1)
                            curr_closing_trade_data_vol_left -= close_vol
                            break
                        else:
                            offset_gl += curr_closing_trade_data_vol_left * (
                                    trade_data.price - curr_closing_trade_data.price
                            ) * (1 if curr_closing_trade_data.direction == Direction.LONG.value else -1)
                            close_vol -= curr_closing_trade_data_vol_left
                    else:
                        if close_vol > 0:
                            offset_gl += close_vol * (
                                    trade_data.price - curr_closing_trade_data.price
                            ) * (1 if curr_closing_trade_data.direction == Direction.LONG.value else -1)
                            self.logger.warning(
                                "交易记录 %s %s %s %.0f 当前持仓 %.0f 手，当前持仓全部订单不足以处理当前平仓，"
                                "这种情况发生，说明当前持仓数据与交易数据的累加数字不一致，请检查数据是否缺失",
                                trade_data.tradeid, trade_data.direction, trade_data.offset, trade_data.volume, volume)

                # 平仓盈亏需要 × 乘数
                offset_gl *= multiplier
                offset_daily_gl += offset_gl
                offset_acc_gl += offset_gl
                # 计算平均价格
                avg_price_new = curr_closing_trade_data_vol_left * curr_closing_trade_data.price + sum([
                    _.price * _.volume for _ in holding_trade_data_list
                ])
                # 计算持仓盈亏
                holding_gl = volume_new * (trade_data.price - avg_price_new) * multiplier
                # 更新持仓状态信息
                pos_status_new_dict = dict(
                    tradeid=trade_data.tradeid,
                    strategy_name=strategy_name,
                    symbol=symbol,
                    exchange=trade_data.exchange,
                    trade_date=trade_data.datetime.date(),
                    trade_dt=trade_data.datetime,
                    direction=trade_data.direction,
                    avg_price=avg_price_new,
                    volume=volume_new,
                    holding_gl=holding_gl,
                    offset_gl=offset_gl,
                    offset_daily_gl=offset_daily_gl,
                    offset_acc_gl=offset_acc_gl,
                    update_dt=datetime.datetime.now(),
                )
                pos_status_new_list.append(pos_status_new_dict)

            # 更新最新的持仓状态
            pos_status_dict = pos_status_new_dict

        # 更新的持仓数据插入数据库
        if len(pos_status_new_list) > 0:
            PositionStatusModel.bulk_replace(pos_status_new_list)

    @staticmethod
    def output_report():
        """输出持仓记录、交易记录"""
        strategy_symbol_pos_status_dic: Dict[str, Dict[str, PositionStatusModel]] = \
            PositionStatusModel.query_latest_position_status()
        # 最新一个交易日
        trade_date = None
        # 持仓列表
        holding_list = []
        for strategy_name, symbol_pos_status_dic in strategy_symbol_pos_status_dic.items():
            for symbol, pos_status in symbol_pos_status_dic.items():
                if trade_date is None:
                    trade_date = pos_status.trade_date
                else:
                    trade_date = max(trade_date, pos_status.trade_date)

                holding_list.append([
                    strategy_name, symbol, pos_status.direction, pos_status.volume,
                    pos_status.holding_gl, pos_status.offset_gl, pos_status.offset_acc_gl
                ])

        if len(holding_list) > 0:
            df = pd.DataFrame(holding_list, columns=['策略名称', '合约', '方向', '手数', '持仓盈亏', '平仓盈亏', '累计平仓盈亏'])
            df.to_csv(f"pos_status_{date_2_str(trade_date)}.csv")
            StrategyPositionMonitor.logger.info("当前持仓：\n%s", df)

        # 前一个交易日
        trade_date_list = TradeDataModel.query_latest_n_trade_date_list(2)
        # 通过记录获取交易日数据，选择上一交易日
        if len(trade_date_list) > 0:
            trade_date_last = trade_date_list[-1]
            update_dt = str_2_datetime(date_2_str(trade_date_last) + " 15:00:00")
            strategy_symbol_trade_data_list_dic: Dict[str, Dict[str, List[TradeDataModel]]] = \
                TradeDataModel.query_trade_data_since(update_dt=update_dt)
            trade_list = []
            for strategy_name, symbol_trade_data_list_dic in strategy_symbol_trade_data_list_dic.items():
                for symbol, trade_data_list in symbol_trade_data_list_dic.items():
                    for trade_data in trade_data_list:
                        trade_list.append([
                            trade_data.strategy_name, trade_data.symbol, trade_data.direction, trade_data.offset,
                            trade_data.volume, trade_data.price, datetime_2_str(trade_data.datetime)
                        ])

            if len(trade_list) > 0:
                df = pd.DataFrame(
                    trade_list,
                    columns=['策略名称', '合约', '方向', '操作', '手数', '价格', '时间']
                )
                df.to_csv(f"trade_list_{date_2_str(trade_date)}.csv")
                StrategyPositionMonitor.logger.info("最近一个交易日交易数据：\n%s", df)

    def refresh_position_and_report(self):
        self.refresh_positions()
        StrategyPositionMonitor.output_report()

    def run(self) -> None:
        while self.is_running:
            time.sleep(self.get_sleep_seconds())
            self.refresh_position_and_report()


def _test_position_status_monitor():
    monitor = StrategyPositionMonitor()
    monitor.refresh_position_and_report()


class StrategyStatusMonitor(Thread):
    def __init__(self, name, get_status_func, set_status_func, symbols):
        super().__init__(name=name)
        self.daemon = True
        self.get_status_func = get_status_func
        self.set_status_func = set_status_func
        self.symbols = symbols
        self.lock = Lock()
        self.logger = logging.getLogger(name)
        self.run_task = StrategyStatus.is_table_exists()
        StrategyStatus._meta.database.close()

    def run(self) -> None:
        if not self.run_task:
            self.logger.warning("%s thread is not running because run_task == false")
        # 首次启动初始化状态
        status_int_curr = self.get_status_func().value
        try:
            StrategyStatus.register_strategy(strategy_name=self.name, status=status_int_curr, symbols=self.symbols)
        except DatabaseError:
            self.logger.exception("register_strategy error")
            return
        # 记录最新状态并开始循环
        status_int_last = status_int_curr
        while self.run_task:
            time.sleep(1)
            try:
                with self.lock:
                    # 获取当前策略最新状态，检查是否与上一个状态存在变化，否则更新
                    status_int_curr = self.get_status_func().value
                    # 检查数据库状态与上一状态是否一致，否则更新当前策略状态
                    status_int_db = StrategyStatus.query_status(self.name)

                if status_int_curr != status_int_last:
                    # 检查是否与上一个状态存在变化，否则更新
                    StrategyStatus.set_status(self.name, status=status_int_curr)
                    status_int_last = status_int_curr
                elif status_int_db != status_int_curr:
                    # 检查数据库状态与上一状态是否一致，否则更新当前策略状态
                    self.set_status_func(StrategyStatusEnum(status_int_db))
                    status_int_last = status_int_db
            except:
                self.logger.exception("%s Monitor Error", self.name)
            finally:
                StrategyStatus._meta.database.close()


def _test_strategy_status_monitor():
    class Stg:
        def __init__(self, name):
            self.name = name
            self.status: StrategyStatusEnum = StrategyStatusEnum.Created
            self.lock: [Lock] = None

        def set_status(self, status: StrategyStatusEnum):
            if self.lock is not None:
                self.lock.acquire()
                print("It's locked")
            try:
                self.status = status
            finally:
                if self.lock is not None:
                    self.lock.release()
                    print("It's released")

        def get_status(self) -> StrategyStatusEnum:
            return self.status

    stg = Stg('test_monitor')
    monitor = StrategyStatusMonitor(stg.name, stg.get_status, stg.set_status, symbols='rb2101.SHFE')
    stg.lock = monitor.lock
    monitor.start()
    time.sleep(2)
    # 初始化状态同步
    assert StrategyStatus.query_status(stg.name) == stg.status.value == StrategyStatusEnum.Stopped.Created
    stg.status = StrategyStatusEnum.Stopped
    time.sleep(2)
    # 修改策略状态，自动同步数据库
    assert StrategyStatus.query_status(stg.name) == stg.status.value == StrategyStatusEnum.Stopped.value
    StrategyStatus.set_status(stg.name, StrategyStatusEnum.Running)
    time.sleep(2)
    # 修改数据库，自动同步当前策略状态
    assert StrategyStatus.query_status(stg.name) == stg.status.value == StrategyStatusEnum.Running
    StrategyStatus._meta.database.close()
    monitor.run_task = False
    monitor.join()


if __name__ == "__main__":
    # _test_strategy_status_monitor()
    _test_position_status_monitor()
    pass
