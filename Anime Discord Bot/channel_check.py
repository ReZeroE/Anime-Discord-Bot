import os
import json

class ChannelCheck:
    def __init__(self):
        self.channel_log = "logs\\channel_log.json"

    def channel_is_private(self, channel_id_param):
        channel_data = dict()
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.channel_log), "r") as rf:
            channel_data = json.load(rf)  

        for channel in channel_data['public channels']:
            for channel_id, channel_name in channel.items():
                if int(channel_id) == channel_id_param:
                    return False

        return True
