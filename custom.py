# coding:utf-8
import time, datetime, traceback, sys,requests
from xtquant import xtdata
from xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback
from xtquant.xttype import StockAccount
from xtquant import xtconstant
from userQuant.userQuantTrader import MyXtQuantTraderCallback
from config.Config import Config
from astock.CsTradeService import CsTradeService
from astock.DecisionOrderService import DecisionOrderService
from astock.XtTradeService import XtTradeService
from astock.TradeService import TradeService
from Common.Function import Function
# 定义一个类 创建类的实例 作为状态的容器
class _a():
    pass


A = _a()
A.bought_list = []
# A.hsa = xtdata.get_stock_list_in_sector('沪深A股')

if __name__ == '__main__':
    print("----------------------- k线棱镜 start -----------------------")
    # 读取配置
    mc_config = Config()
    common_function = Function()

    # 判断配置是否被正确加载
    if not mc_config.check_config():
        print("配置文件不存在或错误")
        common_function.count_down_exit(10)


    # 指定客户端所在路径, 券商端指定到 userdata_mini文件夹
    # 注意：如果是连接投研端进行交易，文件目录需要指定到f"{安装目录}\userdata"
    # path = r'D:\迅投极速策略交易系统交易终端 华鑫证券QMT模拟\userdata_mini'
    path = mc_config.account['xtquant_path']
    print(mc_config.__dict__)

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
    # xtTS = XtTradeService(xt_trader, acc)
    DCOS = DecisionOrderService(xt_trader, acc)
    # 获取资金账户，判断资金账户是否有值
    if not DCOS.check_asset_data_by_asset(XtAsset):
        print('资金账户存在问题,请确认后重新打开')
        common_function.count_down_exit(10)

    # 资金账户判断结束
    print('资金账户同步中...')
    xt_asset_data = DCOS.xt_asset_2_data(XtAsset)
    ts = TradeService()
    result = ts.sync_account_follower(xt_asset_data)
    print(result)
    print('资金账户已同步')
    print('----------------------------------------------------------')
    print('策略执行开始')

    #决策对象

    CSTS = CsTradeService(DCOS)


    #循环获取数据
    # CSTS.subscribe_order()
    # print(result)
    # while True:
    #     print('测试')
    #     time.sleep(1)
    #     continue
    # sys.exit()

    # print(result)
    # sys.exit()

    # for attr in dir(account_info):
    #     print(attr)
    # print('可用资金',account_info.cash)
    # print(account_info.total_asset)

    #sys.exit()

    now_time = datetime.datetime.now().time() #当前时间 08:55:58.102178
    stock_start_time = datetime.time(9, 25, 0)
    stock_end_time = datetime.time(14, 57, 0)
    while True:
        now_time = datetime.datetime.now().time()
        if now_time.__lt__(stock_start_time):
            time.sleep(60)
            continue
        elif now_time.__gt__(stock_start_time) and now_time.__lt__(stock_end_time):
            #盘中，调用接口，并且执行
            # 查询当日委托单
            CSTS.subscribe_order()
            time.sleep(0.5)
            continue
        else:
            print('当天已收盘,系统先休息1小时')
            time.sleep(3600)
            break
