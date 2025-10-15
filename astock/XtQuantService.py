import sys

from PyInstaller.building.splash_templates import position_window
from xtquant.xttype import XtPosition

from astock.BaseService import BaseService
class XtQuantService(BaseService):
    xtAssetField = [
        "account_id", "total_asset", "cash", "frozen_cash", "market_value"
    ]

    xtOrderField = [
        "account_id", "stock_code", "order_id", "order_sysid", "order_time",
        "order_type", "order_volume", "price_type", "price", "traded_volume", "order_status", "status_msg",
        "order_remark"
    ]

    xtTradeField = [
        "account_id", "stock_code", "order_type", "traded_id", "traded_time", "traded_price", "traded_volume",
        "traded_amount", "order_id", "order_sysid", "strategy_name", "order_remark"
    ]

    xtPositionField = [
        "account_id", "stock_code", "volume", "can_use_volume", "open_price", "market_value", "frozen_volume",
        "yesterday_volume", "avg_price"
    ]

    acc = None  # 股票账户对象
    xt_trader = None

    #委托单决策系统
    def __init__(self, xt_trader, acc):
        super(XtQuantService, self).__init__()
        self.xt_trader = xt_trader
        self.acc = acc

    #将迅捷的资金账户对象转为字典类型数据
    def xt_asset_2_data(self, XtAsset):
        data = {}
        for field in self.xtAssetField:
            if hasattr(XtAsset, field):
                data[field] = getattr(XtAsset, field)
        return data

    #将迅捷的资金账户对象转为字典类型数据
    def xt_order_2_data(self, XtOrder):
        data = {}
        for field in self.xtOrderField:
            if hasattr(XtOrder, field):
                data[field] = getattr(XtOrder, field)
        return data

    # 将迅捷的资金账户对象转为字典类型数据
    def xt_position_2_data(self, XtPosition):
        data = {}
        for field in self.xtPositionField:
            if hasattr(XtPosition, field):
                data[field] = getattr(XtPosition, field)
        return data

    # 获取资金账号的对象数据
    def get_xt_asset(self):
        XtAsset = self.xt_trader.query_stock_asset(self.acc)
        return XtAsset

    # 获取委托单列表
    def get_xt_order(self):
        XtOrder = self.xt_trader.query_stock_order(self.acc)
        return XtOrder

    # 判断资金账号是否正确获取
    def check_asset_data(self):
        XtAsset = self.xt_trader.query_stock_asset(self.acc)
        # print(XtAsset)
        return self.check_asset_data_by_asset(XtAsset)

    # 实际判断资金账户
    def check_asset_data_by_asset(self, XtAsset):
        a = 0
        for field in self.xtAssetField:
            if not hasattr(XtAsset, field):
                a += 1

        if a > 1:
            return False

        return True

    # 获取仓位列表
    def get_xt_positions(self):
        positions = self.xt_trader.query_stock_positions(self.acc)
        return positions

    # 获取仓位列表，返回字典类型列表
    def get_positions(self):
        positions = self.get_xt_positions()
        now_positions = []
        for XtPosition in positions:
            position = self.xt_position_2_data(XtPosition)
            now_positions.append(position)
        return now_positions

    # 根据stock code获取仓位
    def get_position_by_stock_code(self, stock_code):
        positions = self.get_xt_positions()
        now_position = None
        for XtPosition in positions:
            position = self.xt_position_2_data(XtPosition)
            # print(position)
            # print(stock_code)
            if position['stock_code'] != stock_code:
                continue
            else:
                # print('---------')
                # print(position)
                now_position = position
        if now_position is None:
            return None
        else:
            return now_position