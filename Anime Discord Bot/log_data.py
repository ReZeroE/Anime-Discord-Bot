import os
import sys
import json

from datetime import datetime
now = datetime.now()

class LogData:
    def __init__(self):
        self.master_log = "logs\\master_log.json"

    def log_data(self, user_id, username, message, channel_name, channel_id):
        master_log = dict()
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.master_log), "r") as rf:
            master_log = json.load(rf)   

        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        data_list =[username,message,channel_id,channel_name,date_time]

        
        try:
            master_log[str(user_id)].append(data_list)
        except:
            master_log[str(user_id)] = [data_list]

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.master_log), "w") as wf:
            json.dump(master_log, wf, indent=4)   

