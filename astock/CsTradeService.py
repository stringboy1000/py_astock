#客户交易策略类
# 客户端连接投顾获取交易，客户端根据实际行情做策略配置
import json,sys

from astock.BaseService import BaseService
from astock.TradeService import TradeService
class CsTradeService(BaseService):
    DCOS = None #决策对象
    def __init__(self, DCOS):
        super(CsTradeService, self).__init__()
        self.DCOS = DCOS

    def subscribe_order(self):
        # 处理迅捷数据为可上传数据
        data = {}
        res_data = {}
        ts = TradeService()
        result = ts.subscribe_order(data)
        # print(result)
        # sys.exit()
        if (self.is_success(result) == True):
            res_data = result['data']
            # print(res_data)
            if (self.is_error(res_data)):
                return res_data
            for value in res_data.values():
                # print(type(value))
                decisionOrder = json.loads(value) #决策数据
                # print(type(decisionOrder))
                print(decisionOrder)
                self.DCOS.op_decision_order(decisionOrder)

                # print(type(decisionOrder))
                # print(decisionOrder)
        # print(res_data)

    #操作决策单，一个决策单被拆分为买决策、卖决策
    def op_decision_order(self, decisionOrder):
        data = {}
        res_data = {}
        ts = TradeService()

