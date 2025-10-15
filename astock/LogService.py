import json,time,datetime,os,sys
from config import Config
from astock.BaseService import BaseService
class LogService(BaseService):
    base_path = ''
    def __init__(self):
        super(LogService, self).__init__()
        self.base_path = self.Config.log_base_path

    def file_exists(self, filename):
        try:
            with open(filename):
                pass
            return True
        except FileNotFoundError:
            return False

    def save_log_json(self, filename, data):
        # 新建文件夹
        file_path = os.path.dirname(filename)
        os.makedirs(file_path, exist_ok=True)
        with open(filename, 'w+') as f:
            #读取内容
            json.dump(data, f)
    #
    # print ( time.strftime("%Y%m%d", time.localtime() ) )
    # date = time.strftime("%Y%m%d", time.localtime() )
    # filename = '../runtime/' + date + '.json'
    # with open(filename, 'w', encoding='utf-8') as f:
    #     f.write(json.dumps({'ab' : 'tset'}))
    #
    # with open(filename, 'r', encoding='utf-8') as f:
    #     content = json.loads(f.read())
    #     print(content)