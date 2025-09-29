import requests
from config import config
class tradeService:
    Config = None
    account_id = ''
    token = ''
    astock_online_api = ''
    def __init__(self):
        self.Config = config.Config()
        self.token = self.Config.account['token']
        self.account_id = self.Config.account['account_id']
        self.astock_online_api = self.Config.astock_online_api

    def genRealData(self, data):
        data["token"] = self.token
        data["account_id"] = self.account_id
        return data

    def syncAccount(self, data):
        url = self.astock_online_api + "trade/follow/syncAccount"
        # print(url)
        data = self.genRealData(data)
        r = requests.request('POST', url, data=data)
        # print(r.text)
        return r.text

    def publicOrder(self, data):
        url = self.astock_online_api + "trade/follow/publicOrder"
        data = self.genRealData(data)
        r = requests.request('POST', url, data=data)
        return r.text

    def publicTrade(self, data):
        url = self.astock_online_api + "trade/follow/publicTrade"
        data = self.genRealData(data)
        r = requests.request('POST', url, data=data)
        return r.text

    def publicPosition(self, data):
        url = self.astock_online_api + "trade/follow/publicPosition"
        data = self.genRealData(data)
        r = requests.request('POST', url, data=data)
        return r.text