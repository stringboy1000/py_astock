# coding:utf-8
import time, datetime, traceback, sys,requests
from xtquant import xtdata
from xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback
from xtquant.xttype import StockAccount
from xtquant import xtconstant
from userQuant.userQuantTrader import MyXtQuantTraderCallback
from config.config import Config
from astock.xtTradeService import xtTradeService


# 定义一个类 创建类的实例 作为状态的容器
class _a():
    pass


A = _a()
A.bought_list = []
A.hsa = xtdata.get_stock_list_in_sector('沪深A股')

if __name__ == '__main__':
    print("start")
    #读取配置
    mc_config = Config()

    # 指定客户端所在路径, 券商端指定到 userdata_mini文件夹
    # 注意：如果是连接投研端进行交易，文件目录需要指定到f"{安装目录}\userdata"
    #path = r'D:\迅投极速策略交易系统交易终端 华鑫证券QMT模拟\userdata_mini'
    path = mc_config.xtquant_path
    # 生成session id 整数类型 同时运行的策略不能重复
    session_id = int(time.time())
    xt_trader = XtQuantTrader(path, session_id)
    # 开启主动请求接口的专用线程 开启后在on_stock_xxx回调函数里调用XtQuantTrader.query_xxx函数不会卡住回调线程，但是查询和推送的数据在时序上会变得不确定
    # 详见: http://docs.thinktrader.net/vip/pages/ee0e9b/#开启主动请求接口的专用线程
    # xt_trader.set_relaxed_response_order_enabled(True)

    # 创建资金账号为 800068 的证券账号对象 股票账号为STOCK 信用CREDIT 期货FUTURE
    acc = StockAccount(mc_config.account_id, 'STOCK')
    # 创建交易回调类对象，并声明接收回调
    callback = MyXtQuantTraderCallback()
    xt_trader.register_callback(callback)
    # 启动交易线程
    xt_trader.start()
    # 建立交易连接，返回0表示连接成功
    connect_result = xt_trader.connect()
    print('建立交易连接，返回0表示连接成功', connect_result)
    # 对交易回调进行订阅，订阅后可以收到交易主推，返回0表示订阅成功
    subscribe_result = xt_trader.subscribe(acc)
    print('对交易回调进行订阅，订阅后可以收到交易主推，返回0表示订阅成功', subscribe_result)
    #取账号信息
    XtAsset = xt_trader.query_stock_asset(acc)
    # print(XtAsset)
    # sys.exit()
    xtTradeService = xtTradeService()
    result = xtTradeService.syncAccount(XtAsset)
    # sys.exit()

    # for attr in dir(account_info):
    #     print(attr)
    # print('可用资金',account_info.cash)
    # print(account_info.total_asset)

    #sys.exit()

    #取可用资金
    available_cash = XtAsset.m_dCash

    print(acc.account_id, '可用资金', available_cash)
    #查账号持仓
    positions = xt_trader.query_stock_positions(acc)
    print(type(positions) )
    for position in positions:
        print(type(position))
        print(position.stock_code)
        print(position.volume)
    trades = xt_trader.query_stock_trades(acc)
    print(type(trades))
    print(len(trades))
    attrs = ['account_id','stock_code','traded_id','traded_time','traded_price','traded_volume','traded_amount','order_id']
    for trade in trades:
        print(type(trade))
        # print(dir(trade))
        for attr in attrs:
            if hasattr(trade, attr):
                print(getattr(trade, attr))

        # print(trade.traded_time)
        # print( time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(trade.traded_time) ) )
        #取各品种 总持仓 可用持仓
    # position_total_dict = {i.stock_code : i.m_nVolume for i in positions}
    # position_available_dict = {i.stock_code : i.m_nCanUseVolume for i in positions}
    # print(acc.account_id, '持仓字典', position_total_dict)
    # print(acc.account_id, '可用持仓字典', position_available_dict)
    #查询当日委托单
    orders = xt_trader.query_stock_orders(acc, cancelable_only=False)
    for order in orders:
        print(type(order))
