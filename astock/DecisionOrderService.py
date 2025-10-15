#客户交易策略类
# 客户端连接投顾获取交易，客户端根据实际行情做策略配置
import json, time, datetime
import sys

from astock.BaseService import BaseService
from astock.XtQuantService import XtQuantService
from astock.DecisionLogService import DecisionLogService
from xtquant import xtconstant

class DecisionOrderService(XtQuantService):

    expired_time = 180 #过期时间，180秒
    # STOCK_BUY = 23
    # STOCK_SELL = 24

    def fix_data_decision_order(self, decision_order):
        decision_order['order_type'] = int(decision_order['order_type'])
        decision_order['price'] = float(decision_order['price'])
        decision_order['order_market'] = float(decision_order['order_market'])

        return decision_order


    # 操作决策单，一个决策单被拆分为买决策、卖决策
    def op_decision_order(self, decision_order):
        # print(xtconstant.STOCK_BUY)
        # print(xtconstant.STOCK_SELL)
        # decision_order['order_type'] = int(decision_order['order_type'])
        # print(type(decision_order['order_type']) )
        # print('------------')
        # print(decision_order)
        decision_order = self.fix_data_decision_order(decision_order)
        # print(decision_order)
        # print(type(decision_order['order_market']))
        # print(type(decision_order['price']))
        # sys.exit(0)

        if decision_order['order_type'] == xtconstant.STOCK_BUY:
            return self.op_decision_order_buy(decision_order)
        elif decision_order['order_type'] == xtconstant.STOCK_SELL:
            return self.op_decision_order_sell(decision_order)

    #执行买单决策
    def op_decision_order_buy(self, decision_order):
        #print(decisionOrder)
        # print('buy')
        # sys.exit()
        #先判断是否过期的策略
        if self.check_is_expired(decision_order):
            return decision_order
        #获取用户账户信息
        #print(self.acc)
        # XtAsset = self.xt_trader.query_stock_asset(self.acc)
        # print(XtAsset)

        # 判断是否已经执行过该策略
        dls = DecisionLogService()
        if self.Config.debug_mode:
            print('@debug_mode#check_has_decision_order')
        else:
            if dls.check_has_decision_order(decision_order):
                return decision_order
        # 判断执行结束

        #获取用户下单信息
        custom_decision_order = self.get_custom_decision_order_buy(decision_order)
        # print(json.dumps(custom_decision_order))
        # sys.exit()
        #执行下单
        stock_code = custom_decision_order['stock_code']
        order_volume = custom_decision_order['order_volume']
        price = custom_decision_order['price']
        if not dls.check_has_decision_order(decision_order):
            async_seq = self.xt_trader.order_stock_async(self.acc, stock_code, xtconstant.STOCK_BUY, order_volume, xtconstant.FIX_PRICE, price,
                                             'follow_buy', '买入')
            decision_order['async_seq'] = async_seq
            # decision_order.update(custom_decision_order)
            decision_order['cs_stock_code'] = stock_code
            decision_order['cs_order_volume'] = order_volume
            decision_order['cs_price'] = price
            print(json.dumps(decision_order))
            # sys.exit(0)

            #写入log
            dls.do_decision_order(decision_order)
            #写入log结束

        return decision_order


    # 判断投顾订单是否已经过期，在跟单阶段，默认3分钟有效期，过了3分钟即不再跟单
    def check_is_expired(self, decision_order):
        if (self.Config.debug_mode is True):
            print('@debug_mode#check_is_expired')
            return False
        interval = time.time() - float(decision_order['order_time'])
        # print(interval)
        if interval > self.expired_time:
            return True
        return False

    # 获得客户端的决策订单
    # 根据决策订单、客户的资金账户，获得客户的决策单
    def get_custom_decision_order_buy(self, decision_order):
        custom_decision_order = {
            'stock_code' : '',
            'order_volume' : 0,
            'price' : 0,
        }
        decision_order['price'] = float(decision_order['price'])
        # 获取用户账户信息
        XtAsset = self.get_xt_asset()
        # print(XtAsset)

        order_volume = 0
        xt_asset_data = self.xt_asset_2_data(XtAsset)
        # print(json.dumps(xt_asset_data))
        if xt_asset_data['cash'] / decision_order['price'] < 100:
            #总可用资金不够买100股
            return custom_decision_order
        wish_use_cash = xt_asset_data['cash'] * decision_order['order_market'] / 100 #期望使用金额
        # print(wish_use_cash)
        if wish_use_cash / decision_order['price'] < 100:
            order_volume = 100 #资金小于100股，则买100股
        else:
            order_volume = wish_use_cash / decision_order['price']
            # print(order_volume)
            order_volume = 100 * (order_volume // 100) #获取实际下单的股票数
        # print(order_volume)
        custom_decision_order['stock_code'] = decision_order['stock_code']
        custom_decision_order['order_volume'] = order_volume
        custom_decision_order['price'] = decision_order['price']

        return custom_decision_order

    # 执行卖单决策
    def op_decision_order_sell(self, decision_order):
        # 判断是否已经执行过该策略
        dls = DecisionLogService()
        if dls.check_has_decision_order(decision_order):
            print('已经执行该卖出决策' + decision_order['stock_code'])
            return decision_order
        # 判断执行结束

        #获取账户仓位
        custom_decision_order = self.get_custom_decision_order_sell(decision_order)
        if custom_decision_order['order_volume'] < 100:
            dls.do_decision_order(decision_order)
            return decision_order
        stock_code = custom_decision_order['stock_code']
        order_volume = custom_decision_order['order_volume']
        price = custom_decision_order['price']
        async_seq = self.xt_trader.order_stock_async(self.acc, stock_code, xtconstant.STOCK_SELL, order_volume,
                                                     xtconstant.FIX_PRICE, price,
                                                     'follow_sell', '卖出')

        # 写入log
        if async_seq > 0:
            decision_order['async_seq'] = async_seq
            dls.do_decision_order(decision_order)
        # 写入log结束

    def get_custom_decision_order_sell(self, decision_order):
        custom_decision_order = {
            'stock_code': '',
            'order_volume': 0,
            'price': 0,
        }
        # print(decision_order)
        # sys.exit()
        now_position = None
        positions = self.xt_trader.query_stock_positions(self.acc)
        # print(positions)
        # sys.exit()
        for XtPosition in positions:
            position = self.xt_position_2_data(XtPosition)
            # print('------------')
            # print(position)
            # sys.exit()
            if position['stock_code'] != decision_order['stock_code']:
                continue
            else:
                now_position = position

        if now_position is None:
            return custom_decision_order #客户没持仓
        # print(now_position)
        # sys.exit()
        custom_decision_order['stock_code'] = now_position['stock_code']
        custom_decision_order['price'] = decision_order['price']
        # print(type(decision_order['price']))
        # sys.exit()
        #如果有仓位，则确定需要卖出的股票数
        if decision_order['order_market'] == 100:
            custom_decision_order['order_volume'] = now_position['volume']
        else:
            order_volume = now_position['volume'] * decision_order['order_market'] / 100
            order_volume = 100 * (order_volume // 100)
            if order_volume < 100:
                order_volume = 100
            custom_decision_order['order_volume'] = order_volume
        if custom_decision_order['order_volume'] >  now_position['can_use_volume']:
            custom_decision_order['order_volume'] = now_position['can_use_volume']
        # print(custom_decision_order)
        # sys.exit()
        return custom_decision_order



