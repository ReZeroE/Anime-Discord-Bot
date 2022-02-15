import os
import sys
import json

class PermissionIdentifier:
    def __init__(self):
        self.user_log = "logs\\user_log.json"

    def get_permission(self, user_id, username_param):

        if user_id == 833536460006490152:
            return 'C-1'

        user_data = dict()
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.user_log), "r") as rf:
            user_data = json.load(rf)

            for user in user_data['admin']:
                for id, username in user.items():
                    if int(id) == user_id:
                        return 'C0'

            for user in user_data['moderator']:
                for id, username in user.items():
                    if int(id) == user_id:
                        return 'C1'

            for user in user_data['user']:
                for id, username in user.items():
                    if int(id) == user_id:
                        return 'C2'

            user_data['user'].append({user_id: username_param})


        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.user_log), "w") as wf:
            json.dump(user_data, wf, indent=4)
        
        return 'C2 - new'

# if __name__ == "__main__":
#     pi = PermissionIdentifier()
#     print(pi.get_permission(1, 'kevin'))