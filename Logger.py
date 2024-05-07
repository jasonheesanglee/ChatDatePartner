import os
import json

class Logger:
    def __init__(self, user_id, session_id, log_file_path=None):
        self.user_id = user_id
        self.session_id = session_id
        self.log_file_path = log_file_path

    def get_log(self):
        if self.log_file_path == None:
            if not os.path.exists('./logs'):
                os.mkdir('./logs')
            self.log_file_path = f'./logs/{self.user_id}.json'
        if os.path.exists(self.log_file_path):
            try:
                with open(self.log_file_path, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except json.JSONDecodeError:
                logs = {}
        else:
            logs = {}
        return logs

    def log(self, user_input, chat_output, current_time):
        logs = self.get_log()
        user_session = logs.setdefault(user_input, {}).setdefault(self.session_id, [])

        if self.user_id in logs.keys():
            if self.session_id in logs[self.user_id]:
                logs[self.user_id][self.session_id].append([
                    {'role':'USER', 'message': user_input},
                    {'role':'CHATBOT', 'message': chat_output},
                    {'role':'SYSTEM','current_time':current_time}
                ])
            else:
                logs[self.user_id].add({self.session_id : [
                    {'role':'USER', 'message': user_input},
                    {'role':'CHATBOT', 'message': chat_output},
                    {'role':'SYSTEM', 'current_time':current_time}
                ]})
        else:
            logs[self.user_id] = {self.session_id : [
                    {'role':'USER', 'message': user_input},
                    {'role':'CHATBOT', 'message': chat_output},
                    {'role':'SYSTEM', 'current_time':current_time}
                ]}

        with open(self.log_file_path, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=4)


