import re
import os
import json

class ParseCommand:
    def __init__(self):
        self.user_input = "logs\\input_database.json"

    def parse_command(self, command):
        command = command.lower().replace('>', '').strip()

        input_data = dict()
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.user_input), "r") as rf:
            input_data = json.load(rf)        

        # Admin Access ==============================================================================================
        admin_input_data = input_data['admin']

        # purge
        user_purge_list = command.split(' ')
        purge_command = user_purge_list[0]

        for std_command in admin_input_data['purge']:
            if std_command == purge_command:
                return 'A1'

        # Moderator Access ==============================================================================================
        mod_input_data = input_data['moderator']

        # terminate
        for std_command in mod_input_data['terminate']:
            if std_command == command:
                return 'M1'


        # User Access ==============================================================================================

        # U1 Help
        # U2 Anime search
        # U3 Manga search
        # U4 Character search
        # U5 Get Perm
        # U6 Get Status

        user_input_data = input_data['user']
        for std_command in user_input_data['help']:
            if std_command == command:
                return 'U1'


        for std_command in user_input_data['get-anime']:
            if command.find(std_command) != -1:
                return f'U2|{std_command}'



        for std_command in user_input_data['get-perm']:
            if std_command == command:
                return 'U5'

        for std_command in user_input_data['get-status']:
            if std_command == command:
                return 'U6'

        return 'None'
        

if __name__ == '__main__':
    pc = ParseCommand()
    print(pc.parse_command(input("your input: ")))
    