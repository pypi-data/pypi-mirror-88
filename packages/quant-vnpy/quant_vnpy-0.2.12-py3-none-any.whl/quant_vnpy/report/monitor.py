"""
@author  : MG
@Time    : 2020/12/11 8:00
@File    : monitor.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
import logging
from threading import Thread
from typing import Callable, Dict


class StrategyPositionMonitor(Thread):

    def __init__(self):
        super().__init__(daemon=True)
        self.is_running = True
        self.logger = logging.getLogger(self.__class__.__name__)
        self.strategy_get_pos_func_dic = {}
        self.time_period_list = [
            ['9:00', '11:30'],
            ['13:30', '3:00'],
            ['21:00', '23:00']
        ]

    def register_get_pos(self, strategy_name: str, get_positions_func: Callable[[], Dict[str, int]]) -> None:
        """
        注册 get_position 方法
        """
        self.strategy_get_pos_func_dic[strategy_name] = get_positions_func

    def get_next_time(self):
        pass

    def run(self) -> None:
        while self.is_running:
            break


if __name__ == "__main__":
    pass
