import json
import pytz
import cohere
import streamlit as st
from datetime import datetime
from Logger import Logger

try:
    COHERE_API_KEY = st.secrets['COHERE_API_KEY']
except:
    with open('api_key.json') as secrets:
        COHERE_API_KEY = json.load(secrets)['COHERE_API_KEY']
# why

class ChatBot:
    def __init__(self,
                 user_name,
                 partner_name,
                 domain,
                 session_id,
                 prompts,
                 log_file_path=None
                 ):

        self.session_id = session_id
        self.co = cohere.Client(api_key=COHERE_API_KEY)
        self.log_file_path = log_file_path
        self.user_id=f'{user_name}_{partner_name}_{domain}'
        self.logger = Logger(user_id=self.user_id,
                             session_id=session_id,
                             log_file_path=self.log_file_path)
        self.system_message = prompts + "\n지금 날짜와 시간은 {time}이야"

    def get_chat_history(self):
        '''
        Get saved logs from json file.
        :return:
        '''
        history = self.logger.get_log()
        chat_history = []
        if self.user_id in history:
            if self.session_id in history[self.user_id]:
                session_hist = history[self.user_id][self.session_id]
                print(session_hist)
                for user, chatbot, time_log in session_hist:
                    chat_history.append(user)
                    chat_history.append(chatbot)
                    chat_history.append(time_log)
        return chat_history

    def chat(self, user_input):  ## Cohere
        '''
        Chat a user with given input using Cohere Api.
        :param user_input: user chat to chatbot -> str
        :return: chat message
        '''
        current_time = str(datetime.now(tz=pytz.timezone('Asia/Seoul')))
        response = self.co.chat(
            chat_history=self.get_chat_history(),
            preamble=self.system_message.replace('{time}', current_time),
            message=user_input,
            connectors=[{"id": "web-search"}],
        ).text

        self.logger.log(user_input=user_input,
                        chat_output=response,
                        current_time=current_time
                        )
        return response