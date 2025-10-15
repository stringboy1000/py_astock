import os, json, sys
from pathlib import Path
class Config2:
    astock_online_api = 'http://8.210.7.57/api/'
    config_path = "runtime\\config\\"
    config_file = config_path + "config.json"
    config = {}
    def __init__(self):
        print(self.config_file)

    def get_config_by_path(self):
        os.makedirs(self.config_path, exist_ok=True)
        if not os.path.exists(self.config_file):
            return self.config
        with open(self.config_file, 'r+') as f:
            self.config = json.load(f)
        return self.config

    def save_data(self, data):
        # cwd = os.getcwd()
        # print(cwd)
        # cwd = Path.cwd()
        # print(cwd)
        file_path = self.config_path + 'config.json'
        print(file_path)
        os.makedirs(self.config_path, exist_ok=True)
        with open(file_path, 'w+') as f:
            json.dump(data, f)