
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class ConsumeGearLogModel(BaseModel):
    def __init__(self, db_connect_key='db_cloudapp', sub_table=None, db_transaction=None):
        super(ConsumeGearLogModel, self).__init__(ConsumeGearLog, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction

    #方法扩展请继承此类
    
class ConsumeGearLog:

    def __init__(self):
        super(ConsumeGearLog, self).__init__()
        self.id = 0  # id
        self.app_id = ""  # 应用标识
        self.act_id = 0  # 活动标识
        self.open_id = ""  # open_id
        self.consume_gear_id = ""  # 消费挡位id
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.create_day = 0  # 创建天

    @classmethod
    def get_field_list(self):
        return ['id', 'app_id', 'act_id', 'open_id', 'consume_gear_id', 'create_date', 'create_day']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "consume_gear_log_tb"
    