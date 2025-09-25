import requests
class tradeService:
    account_id = ''
    astock_online_api = 'http://8.210.7.57/api/'
    def __init__(self, account_id):
        self.account_id = account_id


    def syncAccount(self, data):
        url = self.astock_online_api + "trade/follow/syncAccount"
        # print(url)
        r = requests.request('POST', url, data=data)
        print(r.text)
