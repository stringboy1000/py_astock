class Config:
    account_id = "00781198"
    astock_online_api = 'http://8.210.7.57/api/'
    xtquant_path = r'D:\迅投极速策略交易系统交易终端 华鑫证券QMT模拟\userdata_mini'
    account = None
    accountList = [
        {
        "account_id": "00781198",
        "token": "zxf",
    },{
        "account_id": "800201",
        "token": "zxf123456",
    }
    ]

    def __init__(self):
        self.account = self.getAccountById(self.account_id)


    def getAccountById(self, account_id):
        for account in self.accountList:
            if account["account_id"] == account_id:
                return account
        return None