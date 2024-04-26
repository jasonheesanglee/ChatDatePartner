import os
import json

class Logger:
    def __init__(self, user_id, session_id, log_file_path=None):
        self.user_id = user_id
        self.session_id = session_id
        self.log_file_path = log_file_path


    def log(self, user_input, chat_output, current_time):
        if self.log_file_path == None:
            if not os.path.exists('./logs'):
                os.mkdir('./logs/')
            self.log_file_path = f'./logs/{self.user_id}.json'
            logs = {}
        else:
            with open(self.log_file_path, 'r') as f:
                logs = json.load(f)
        if self.user_id in self.logs.keys():
            if self.session_id in self.logs[self.user_id]:
                logs[self.user_id][self.session_id].append([current_time, user_input, chat_output])
            else:
                logs[self.user_id].add({self.session_id : [[current_time, user_input, chat_output]]})
        else:
            logs[self.user_id] = {self.session_id : [[current_time, user_input, chat_output]]}

        with open(self.log_file_path, 'w') as f:
            json.dump(logs, f)

    def get_log(self):
        if os.path.exists(self.log_file_path):
            with open(self.log_file_path, 'r') as f:
                logs = json.load(f)
            return logs
        else:
            return dict()