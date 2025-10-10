class Config:
    # account_id = "00783343" #作为投顾账户
    account_id = "00781198" #跟单客户账户
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
            # "xtquant_path":r"E:\迅投极速策略交易系统交易终端 华鑫证券QMT模拟\userdata_mini"
            "xtquant_path":r"D:\迅投极速策略交易系统交易终端 华鑫证券QMT模拟\userdata_mini"
        }
    ]
    log_base_path = "C:\\AppData\\klineljing\\runtime\\log\\"
    debug_mode = True

    def __init__(self):
        self.account = self.GetAccountById(self.account_id)


    def GetAccountById(self, account_id):
        for account in self.accountList:
            if account["account_id"] == account_id:
                return account
        return None