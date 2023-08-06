"""
@author  : MG
@Time    : 2020/11/24 11:05
@File    : object.py
@contact : mmmaaaggg@163.com
@desc    : 用于创建数据库表结构
"""
import enum
import typing
from collections import defaultdict
from datetime import datetime, date

from peewee import (
    CharField,
    SmallIntegerField,
    DateField,
    DateTimeField,
    DoubleField,
    Model,
    CompositeKey,
)
# Peewee provides an alternate database implementation
# for using the mysql-connector driver.
# The implementation can be found in playhouse.mysql_ext.
from playhouse.mysql_ext import MySQLConnectorDatabase
from vnpy.trader.constant import Offset
from vnpy.trader.setting import get_settings

from quant_vnpy.config import logging

logger = logging.getLogger()


class StrategyStatusEnum(enum.IntEnum):
    Created = 0
    Initialized = 1
    RunPending = 2
    Running = 3
    StopPending = 4
    Stopped = 5


def init_db():
    settings = get_settings("database.")
    keys = {"database", "user", "password", "host", "port"}
    settings = {k: v for k, v in settings.items() if k in keys}
    db = MySQLConnectorDatabase(**settings)
    return db


database = init_db()


class StrategyStatus(Model):
    """
    策略状态信息
    * strategy_name 策略名称
    * status 策略状态
    """
    strategy_name: str = CharField(primary_key=True)
    status: int = SmallIntegerField()
    symbols: str = CharField(max_length=20)
    update_dt = DateTimeField()
    description: str = CharField()

    @staticmethod
    def is_table_exists():
        try:
            is_exists = StrategyStatus.table_exists()
            StrategyStatus._meta.database.close()
            return is_exists
        except:
            return False

    @staticmethod
    def set_status(strategy_name, status: int):
        ret_data = StrategyStatus.update(
            status=status, update_dt=datetime.now()
        ).where(StrategyStatus.strategy_name == strategy_name).execute()
        StrategyStatus._meta.database.close()
        return ret_data

    @staticmethod
    def query_status(strategy_name) -> int:
        ss: StrategyStatus = StrategyStatus.get_or_none(StrategyStatus.strategy_name == strategy_name)
        ss._meta.database.close()
        if ss is None:
            return -1
        else:
            return ss.status

    @staticmethod
    def register_strategy(strategy_name, status: int, symbols: str):
        ret_data = StrategyStatus.insert(
            strategy_name=strategy_name, status=status, symbols=symbols, update_dt=datetime.now()).on_conflict(
            preserve=[StrategyStatus.strategy_name],
            update={StrategyStatus.status: status, StrategyStatus.update_dt: datetime.now()}
        ).execute()
        StrategyStatus._meta.database.close()
        return ret_data

    @staticmethod
    def query_all():
        ret_data = [_ for _ in StrategyStatus.select().execute()]
        StrategyStatus._meta.database.close()
        return ret_data

    class Meta:
        database = database
        legacy_table_names = False
        indexes = ((("strategy_name",), True),)
        table_settings = "ENGINE = MEMORY"


class OrderDataModel(Model):
    """
    策略状态信息
    实际生产环境中 orderid 可以唯一确定
    但是，回测环境下，需要与策略名称，品种进行配合才行
    * strategy_name 策略名称
    """
    strategy_name: str = CharField()
    orderid: str = CharField()
    symbol: str = CharField(max_length=20)
    exchange: str = CharField(max_length=20)
    order_type: str = CharField(max_length=20)
    direction: str = CharField(max_length=8)
    offset: str = CharField(max_length=8)
    price = DoubleField()
    volume = DoubleField()
    status: str = CharField(max_length=20)
    datetime = DateTimeField()

    class Meta:
        database = database
        legacy_table_names = False
        primary_key = CompositeKey('strategy_name', 'orderid', 'symbol')
        # indexes = ((("strategy_name", "symbol"), True),)


class TradeDataModel(Model):
    """
    策略状态信息
    实际生产环境中 tradeid 可以唯一确定
    但是，回测环境下，需要与策略名称，品种进行配合才行
    * strategy_name 策略名称
    """
    strategy_name: str = CharField()
    tradeid: str = CharField()
    symbol: str = CharField(max_length=20)
    exchange: str = CharField(max_length=20)
    orderid: str = CharField()
    direction: str = CharField(max_length=8)
    offset: str = CharField(max_length=8)
    price = DoubleField()
    volume = DoubleField()
    datetime = DateTimeField()

    class Meta:
        database = database
        legacy_table_names = False
        primary_key = CompositeKey('strategy_name', 'tradeid', 'symbol')
        # indexes = ((("strategy_name", "symbol"), True),)

    @staticmethod
    def get_latest_open_trade_data():
        """
        获取各个策略最近的一笔开仓交易单
        """
        sql_str = """select trades.* from trade_data_model trades inner join (
            select strategy_name, max(`datetime`) dt from trade_data_model 
            where offset=%s group by strategy_name) latest
            on trades.strategy_name = latest.strategy_name
            and trades.`datetime` = latest.dt"""
        strategy_symbol_latest_open_trade_data_dic = defaultdict(dict)
        for trade_data in TradeDataModel.raw(sql_str, Offset.OPEN.value).execute():
            strategy_symbol_latest_open_trade_data_dic[trade_data.strategy_name][trade_data.symbol] = trade_data

        TradeDataModel._meta.database.close()
        return strategy_symbol_latest_open_trade_data_dic

    @staticmethod
    def query_latest_n_trade_date_list(latest_n) -> typing.List[date]:
        sql_str = f"select distinct Date(`datetime`) from trade_data_model" \
                  f" order by Date(`datetime`) desc limit {latest_n}"
        trade_date_list = []
        try:
            for trade_date in database.execute_sql(sql_str):
                trade_date_list.append(trade_date[0])
        finally:
            database.close()

        return trade_date_list

    @staticmethod
    def query_trade_data_by_strategy_since(
            strategy_name: str = None, update_dt: datetime = None
    ) -> typing.Dict[str, list]:
        """
        :param strategy_name
        :param update_dt 可以为空，非空情况下，返回大于此（不包含）时间的全部交易数据
        """
        try:
            strategy_symbol_trade_data_list_dic = defaultdict(list)
            if update_dt is None:
                for _ in TradeDataModel.select().where(
                        TradeDataModel.strategy_name == strategy_name
                ).order_by(TradeDataModel.datetime).execute():
                    strategy_symbol_trade_data_list_dic[_.symbol].append(_)
            else:
                for _ in TradeDataModel.select().where(
                        TradeDataModel.strategy_name == strategy_name,
                        TradeDataModel.datetime > update_dt
                ).order_by(TradeDataModel.datetime).execute():
                    strategy_symbol_trade_data_list_dic[_.symbol].append(_)
        finally:
            TradeDataModel._meta.database.close()

        return strategy_symbol_trade_data_list_dic

    @staticmethod
    def query_trade_data_since(
            update_dt: datetime = None
    ) -> typing.Dict[str, typing.Dict[str, list]]:
        """
        :param update_dt 可以为空，非空情况下，返回大于此（不包含）时间的全部交易数据
        """
        try:
            strategy_symbol_trade_data_list_dic = defaultdict(lambda: defaultdict(list))
            if update_dt is None:
                for _ in TradeDataModel.select().order_by(TradeDataModel.datetime).execute():
                    strategy_symbol_trade_data_list_dic[_.strategy_name][_.symbol].append(_)
            else:
                for _ in TradeDataModel.select().where(
                        TradeDataModel.datetime > update_dt
                ).order_by(TradeDataModel.datetime).execute():
                    strategy_symbol_trade_data_list_dic[_.strategy_name][_.symbol].append(_)
        finally:
            TradeDataModel._meta.database.close()

        return strategy_symbol_trade_data_list_dic


class LatestTickPriceModel(Model):
    """
    策略状态信息
    * symbol 产品名称
    """
    symbol: str = CharField(max_length=20)
    exchange: str = CharField(max_length=20)
    price = DoubleField()
    volume = DoubleField()
    datetime = DateTimeField()

    class Meta:
        database = database
        legacy_table_names = False
        primary_key = CompositeKey('symbol')
        table_settings = "ENGINE = MEMORY"

    @staticmethod
    def query_latest_price(symbol):
        """
        获取各个策略最近的一笔开仓交易单
        """
        data: LatestTickPriceModel = LatestTickPriceModel.get_or_none(LatestTickPriceModel.symbol == symbol)
        LatestTickPriceModel._meta.database.close()
        return data

    @staticmethod
    def query_all_latest_price() -> dict:
        """
        获取各个策略最近的一笔开仓交易单
        """
        symbol_tick_dic: typing.Dict[str, LatestTickPriceModel] = {_.symbol: _ for _ in LatestTickPriceModel.select()}
        LatestTickPriceModel._meta.database.close()
        return symbol_tick_dic


class PositionStatusModel(Model):
    """
    策略持仓信息
    * strategy_name 策略名称
    """
    tradeid: str = CharField()
    strategy_name: str = CharField()
    symbol: str = CharField(max_length=20)
    exchange: str = CharField(max_length=20)
    trade_date = DateField()
    trade_dt = DateTimeField()
    direction: int = SmallIntegerField()
    avg_price = DoubleField()  # 评价持仓成本
    volume = DoubleField()
    holding_gl = DoubleField()  # holding gain and loss 持仓盈亏
    offset_gl = DoubleField()  # offset gain and loss 平仓盈亏
    offset_daily_gl = DoubleField()  # daily offset gain and loss 平仓盈亏
    offset_acc_gl = DoubleField()  # accumulate offset gain and loss 平仓盈亏
    update_dt = DateTimeField()

    class Meta:
        database = database
        legacy_table_names = False
        primary_key = CompositeKey('tradeid', 'strategy_name', 'symbol')

    @staticmethod
    def query_latest_position_status() -> typing.Dict[str, dict]:
        """
        获取各个策略最近的一笔开仓交易单
        """
        sql_str = """select pos.* from position_status_model pos inner join (
            select strategy_name, max(`trade_date`) trade_date from position_status_model 
            group by strategy_name, symbol) latest
            on pos.strategy_name = latest.strategy_name
            and pos.trade_date = latest.trade_date"""
        strategy_symbol_pos_status_dic = defaultdict(dict)
        for pos_status in PositionStatusModel.raw(sql_str).execute():
            strategy_symbol_pos_status_dic[pos_status.strategy_name][pos_status.symbol] = pos_status

        PositionStatusModel._meta.database.close()
        return strategy_symbol_pos_status_dic

    @staticmethod
    def bulk_replace(pos_status_new_list: typing.List[dict]):
        try:
            for pos_status_new_dic in pos_status_new_list:
                with database.atomic():
                    PositionStatusModel.replace(**pos_status_new_dic).execute()

        finally:
            PositionStatusModel._meta.database.close()


def init_models():
    # try:
    #     StrategyStatus.create_table()  # 创建表  # engine='MEMORY'
    # except peewee.OperationalError:
    #     logger.warning("StrategyStatus table already exists!")
    #
    # try:
    #     TradeDataModel.create_table()  # 创建表  # engine='MEMORY'
    # except peewee.OperationalError:
    #     logger.warning("TradeDataModel table already exists!")

    database.connect()
    database.create_tables([StrategyStatus, OrderDataModel, TradeDataModel, LatestTickPriceModel, PositionStatusModel])


def _test_record_strategy_status():
    strategy_name = 'asdf11'
    status = StrategyStatusEnum.Running
    StrategyStatus.register_strategy(strategy_name=strategy_name, status=status.value, symbols='rb2101.SHFE')
    ss: StrategyStatus = StrategyStatus.get_or_none(StrategyStatus.strategy_name == strategy_name)
    assert ss.status == status.value
    assert ss.description == ''
    StrategyStatus.set_status(strategy_name=strategy_name, status=status.value)
    ss: StrategyStatus = StrategyStatus.get_or_none(StrategyStatus.strategy_name == strategy_name)
    print(ss, ss.status)
    ss.status = StrategyStatusEnum.Stopped.value
    ss.update()
    ss._meta.database.close()
    print(ss, ss.status)


if __name__ == "__main__":
    init_models()
    # _test_record_strategy_status()
