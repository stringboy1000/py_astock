import time,datetime
from astock.LogService import LogService

class DecisionLogService(LogService):
    def __init__(self):
        super(DecisionLogService, self).__init__()

    def get_filename(self, order_id):
        today = time.strftime("%Y%m%d", time.localtime())
        filename = self.base_path + today + '_' + order_id + '.json'
        return filename
    def check_has_decision_order(self, decision_order):
        order_id = decision_order['order_id']
        filename = self.get_filename(order_id)
        return self.file_exists(filename)

    def do_decision_order(self, decision_order):
        order_id = decision_order['order_id']
        filename = self.get_filename(order_id)
        if self.Config.debug_mode:
            print('@debug_mode#do_decision_order')
            print(filename)
        self.save_log_json(filename, decision_order)