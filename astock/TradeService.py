import sys

import requests
from config import Config
from astock.BaseService import BaseService
class TradeService(BaseService):
    # Config = None
    account_id = ''
    token = ''
    astock_online_api = ''
    def __init__(self):
        super(TradeService, self).__init__()
        # self.Config = config.Config()
        self.token = self.Config.account['token']
        self.account_id = self.Config.account['account_id']
        self.astock_online_api = self.Config.astock_online_api

    def gen_real_data(self, data):
        data["token"] = self.token
        data["account_id"] = self.account_id
        return data

    def sync_account(self, data):
        url = self.astock_online_api + "trade/follow/syncAccount"
        # print(url)
        data = self.gen_real_data(data)
        r = requests.request('POST', url, data=data)
        # print(r.text)
        return self.json_loads(r.text)

    def publish_order(self, data):
        url = self.astock_online_api + "trade/follow/publishOrder"
        data = self.gen_real_data(data)
        # print('-------')
        # print(data)
        # print('-------')
        # r = requests.request('POST', url, data=data)
        r = requests.request('POST', url, data=data)
        # print(r.text)
        return self.json_loads(r.text)

    def publish_trade(self, data):
        url = self.astock_online_api + "trade/follow/publishTrade"
        data = self.gen_real_data(data)
        r = requests.request('POST', url, data=data)
        return self.json_loads(r.text)

    # 发布用户持仓,某个仓位的持仓
    def publish_position(self, data):
        url = self.astock_online_api + "trade/follow/publishPosition"
        data = self.gen_real_data(data)
        r = requests.request('POST', url, data=data)
        return self.json_loads(r.text)

    # 发布用户持仓,账户所有仓位的持仓
    def publish_positions(self, data):
        url = self.astock_online_api + "trade/follow/publishPositions"
        data = self.gen_real_data(data)
        print(data)
        r = requests.request('POST', url, data=data)
        print(r.text)
        sys.exit()
        return self.json_loads(r.text)

    def subscribe_order(self, data):
        url = self.astock_online_api + "trade/follow/subscribeOrder"
        data = self.gen_real_data(data)
        # print(data)
        r = requests.request('POST', url, data=data)
        print(r.text)
        return self.json_loads(r.text)

    def sync_account_follower(self, data):
        url = self.astock_online_api + "trade/follow/syncAccountFollower"
        # print(url)
        data = self.gen_real_data(data)
        r = requests.request('POST', url, data=data)
        # print(r.text)
        return self.json_loads(r.text)