from astock.TradeService import TradeService
from astock.XtQuantService import XtQuantService
from xtquant import xtconstant
class XtTradeService(XtQuantService):
    # 查询迅捷委托单，并将委托单一一上传到服务器
    def query_and_publish_order(self):
        orders = self.xt_trader.query_stock_orders(self.acc, cancelable_only=False)
        # print(orders)
        # sys.exit()
        for order in orders:
            # print(type(order))
            result = self.publish_order(order)
            print(result)

    # 获取资金账户
    def query_and_publish_account(self):
        XtAsset = self.get_xt_asset()
        return self.sync_account(XtAsset)

    def sync_account(self, XtAsset):
        # data = {
        #     "account_id":XtAsset.account_id, #资金账号
        #     "total_asset": XtAsset.total_asset,  # 总资金
        #     "cash": XtAsset.cash,  # 可用资金
        #     "frozen_cash": XtAsset.frozen_cash,#冻结金额
        #     "market_value": XtAsset.market_value,  # 持仓市值
        # }
        # data = {}
        # for field in self.xtAssetField:
        #     if hasattr(XtAsset, field):
        #         data[field] = getattr(XtAsset, field)
        #print(data)
        data = self.xt_asset_2_data(XtAsset)
        ts = TradeService()
        return ts.sync_account(data)

    def publish_order(self, XtOrder):
        # 处理迅捷数据为可上传数据
        # data = {}
        # for field in self.xtOrderField:
        #     if hasattr(XtOrder, field):
        #         data[field] = getattr(XtOrder, field)
        # print(data)

        # data = {
        #     "account_id":XtOrder.account_id, #账号
        #     "stock_code": XtOrder.stock_code, #证券代码，例如"600000.SH"
        #     "order_id": XtOrder.order_id, #订单编号
        #     "order_sysid": XtOrder.order_sysid, #柜台合同编号
        #     "order_time": XtOrder.order_time, #报单时间
        #     "order_type": XtOrder.order_type, #委托类型买入 - xtconstant.STOCK_BUY 卖出 - xtconstant.STOCK_SELL
        #     "order_volume": XtOrder.order_volume, #委托数量
        #     "price_type": XtOrder.price_type, #报价类型，该字段在返回时为柜台返回类型，
        #     "price": XtOrder.price, #委托价格
        #     "traded_volume": XtOrder.traded_volume, #成交数量
        #     "order_status": XtOrder.order_status, #委托状态
        #     "status_msg": XtOrder.status_msg,
        #     "order_remark": XtOrder.order_remark, #委托备注，最大 24 个英文字符
        # }
        data = self.xt_order_2_data(XtOrder)
        # 如果是废单、撤销单，则不上传
        if data['order_status'] in [xtconstant.ORDER_CANCELED,xtconstant.ORDER_REPORTED_CANCEL, xtconstant.ORDER_JUNK]:
            return False
        # 先判断是买单还是卖单，如果是卖单，则要把账号持仓调出来
        if data['order_type'] == xtconstant.STOCK_SELL:
            # print(data['stock_code'])
            #处理逻辑,持仓
            now_position = self.get_position_by_stock_code(data['stock_code'])
            # print(now_position)
            if now_position is None:
                return False
            data['volume'] = now_position['volume']

        ts = TradeService()
        return ts.publish_order(data)

    def publish_trade(self, XtTrade):
        # data = {
        #     "account_id": XtTrade.account_id, #资金账号
        #     "stock_code": XtTrade.stock_code, #证券代码
        #     "traded_id": XtTrade.traded_id, #成交编号
        #     "traded_time": XtTrade.traded_time, #成交时间
        #     "traded_price": XtTrade.traded_price, #成交均价
        #     "traded_volume": XtTrade.traded_volume, #成交数量
        #     "traded_amount": XtTrade.traded_amount, #成交金额
        #     "order_id": XtTrade.order_id, #订单编号
        #     "order_sysid": XtTrade.order_sysid, #柜台合同编号
        #     "strategy_name": XtTrade.strategy_name, #策略名称
        #     "order_remark": XtTrade.order_remark, #委托备注，最大 24 个英文字符(
        # }
        data = {}
        for field in self.xtTradeField:
            if hasattr(XtTrade, field):
                data[field] = getattr(XtTrade, field)
        # print(data)
        ts = TradeService()
        return ts.publish_trade(data)

    def publish_position(self, XtPosition):
        data = {}
        for field in self.xtPositionField:
            if hasattr(XtPosition, field):
                data[field] = getattr(XtPosition, field)
        print(data)

    # 查询迅捷持仓，并将持仓打包上传到服务器
    def query_and_publish_positions(self):
        positions = self.xt_trader.query_stock_positions(self.acc)
        return self.publish_positions(positions)

    # 发布持仓
    def publish_positions(self, positions):
        new_positions = {}
        print('<<<aaaa>>>')
        new_positions = {"600201.sh": {"stock_code": "600201.sh", "volume": 1000},"002222.sz": {"stock_code": "002222.sz", "volume": 100}}
        # if not positions:
        #     return new_positions
        # for XtPosition in positions:
        #     position = self.xt_position_2_data(XtPosition)
        #     stock_code = position['stock_code']
        #     new_positions[stock_code] = position

        ts = TradeService()
        return ts.publish_positions( {'positions': new_positions} )


