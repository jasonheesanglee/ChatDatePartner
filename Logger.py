import os
import json
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


class Logger:
    def __init__(self, user_id, session_id, log_file_path=None):
        self.user_id = user_id
        self.session_id = session_id
        if not log_file_path:
            if not os.path.exists('./logs'):
                os.mkdir('./logs')
            self.log_file_path = f'./logs/{self.user_id}.json'
        self.log_file_path = log_file_path
        

    def get_log(self) -> dict:
        '''
        Reads the logs file and returns it.
        If the log file doesn't exist or is empty, create the base template and return it.
        :return: history of the chat -> dict
        '''
        base_template =  {self.user_id: {self.session_id:[]}}

        try:
            with open(self.log_file_path, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        except (json.JSONDecodeError, TypeError, FileNotFoundError):
            logs = base_template
        return logs

    def log_message(self, user_input:str, chat_output:str, current_time:str) -> list:
        '''
        Place the chat history in a format per iteration so that Cohere models can recognize it.

        :param user_input: user_input -> string
        :param chat_output: chat_output -> string
        :param current_time: current_time -> string
        :return: list of chat history -> list
        '''
        msg = [
            {"type": "human", "content": user_input},
            {"type": "ai", "content": chat_output},
            {"type": "system", "content": f'Current Time : {current_time}'}
                ]
        return msg

    def log(self, user_input, chat_output, current_time) -> None:
        '''
        Logs the chat history to the logs file.
        
        :param user_input: user_input -> string
        :param chat_output: chat_output -> string
        :param current_time: current_time -> string
        :return: None
        '''
        try:
            logs = self.get_log()
            new_log_entry = self.log_message(user_input, chat_output, current_time)
            if self.user_id in logs:
                if self.session_id in logs[self.user_id]:
                    logs[self.user_id][self.session_id].extend(new_log_entry)
                else:
                    logs[self.user_id][self.session_id] = new_log_entry
            else:
                logs[self.user_id] = {self.session_id: new_log_entry}

            os.makedirs(os.path.dirname(self.log_file_path), exist_ok=True)
            with open(self.log_file_path, 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error logging message: {e}")

if __name__ == "__main__":
    logger = Logger(user_id='temp_user', session_id='temp_session')
    logs = logger.get_log()
    print(logs)
