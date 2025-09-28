from astock import tradeService
from config import config
from userQuant.userQuantTrader import MyXtQuantTraderCallback
from astock.xtTradeService import xtTradeService
import requests,sys
xtts = xtTradeService()
print(xtts)
sys.exit()
mc = MyXtQuantTraderCallback()
mc.on_disconnected()
ts = tradeService.tradeService()
data = {"cash":970000}
result = ts.syncAccount(data)
print(result)
# ts.syncAccount({'a':'bb'})

cf = config.Config()
# print(cf.getAccountById("800201s"))
# a = cf.getAccountById("800201s")
# if a is None:
#     print("ass")
print(cf.account["token"])