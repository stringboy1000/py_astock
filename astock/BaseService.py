import json,sys
from config import config

class BaseService:
    Config = None

    def __init__(self):
        self.Config = config.Config()

    def json_loads(self, json_str):
        return json.loads(json_str)

    def is_success(self, result):
        # print(type(result))

        # print(result['state'])

        return result['state'] == 'Success'

    def is_error(self,  result):
        print(type(result))
        # print(result.get('state') != None)
        # sys.exit(1)
        if result.get('state') != None:
            return result['state'] == 'Error'
        if result.get('error_code') != None:
            return result['error_code'] == -1

        return False

