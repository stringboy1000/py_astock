import os,sys,time,json

from pandas.io.common import file_exists, file_path_to_url


class Config:
    account_id = None
    # account_id = "00783343" #作为投顾账户
    # account_id = "00781198" #跟单客户账户
    # account_id = "00780228"  # 跟单客户账户 冠峰
    astock_online_api = 'http://8.210.7.57/api/'
    xtquant_path = r'D:\迅投极速策略交易系统交易终端 华鑫证券QMT模拟\userdata_mini'
    account = None
    accountList = [
        {
            "account_id": "00781198",
            "token": "zxf",
            "xtquant_path":r"D:\迅投极速策略交易系统交易终端 华鑫证券QMT模拟\userdata_mini"
        },{
            "account_id": "00783343", #lucas资金账户
            "token": "lucas123456",
            "xtquant_path":r"E:\迅投极速策略交易系统交易终端 华鑫证券QMT模拟\userdata_mini"
            # "xtquant_path":r"D:\迅投极速策略交易系统交易终端 华鑫证券QMT模拟\userdata_mini"
        },{
            "account_id": "00780228", #lucas资金账户
            "token": "lgf123456",
             "xtquant_path":r"D:\迅投极速策略交易系统交易终端 华鑫证券QMT模拟\userdata_mini"
        }
    ]
    # log_base_path = "C:\\AppData\\klineljing\\runtime\\log\\"
    runtime_path = "runtime\\"
    log_base_path = runtime_path + "log\\"
    config_base_path = runtime_path + "config\\"
    debug_mode = True

    def __init__(self):
        account = self.get_account_by_file()
        if account is None:
            return account
        self.account_id = account['account_id']
        self.account = account[account['account_id']]
        # self.account = self.GetAccountById(self.account_id)

    # 判断文件是否存在
    def file_exist(self, file_path):
        return os.path.exists(file_path)

    # 判断配置是否加载
    def check_config(self):
        # 判断账户token文件是否被加载
        if self.account_id is None or self.account is None:
            return False
        # 其它配置判断
        return True

    # 从json文件中获取数据
    def load_json_data(self, file_path):
        if not self.file_exist(file_path):
            return None
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_account_by_file(self):
        os.makedirs(self.config_base_path, exist_ok=True)
        file_path = self.config_base_path + 'account.json'
        json_data = self.load_json_data(file_path)
        return json_data

    def get_token(self):
        return self.account["token"]

    def GetAccountById(self, account_id):
        for account in self.accountList:
            if account["account_id"] == account_id:
                return account
        return None