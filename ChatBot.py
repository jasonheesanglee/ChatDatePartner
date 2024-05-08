import json
import pytz
import cohere
import streamlit as st
from datetime import datetime
from google import generativeai
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory, RunnablePassthrough
from langchain_community.chat_message_histories import ChatMessageHistory
from google.generativeai.types.safety_types import HarmBlockThreshold, HarmCategory
from han_util_unicode import build_josa

from Logger import Logger
from Prompts import Prompts

try:
    COHERE_API_KEY = st.secrets['COHERE_API_KEY']
except:
    with open('api_key.json') as secrets:
        COHERE_API_KEY = json.load(secrets)['COHERE_API_KEY']

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
        self.logger = Logger(user_id=f'{user_name}_{partner_name}_{domain}',
                             session_id=session_id,
                             log_file_path=self.log_file_path)
        self.system_message = prompts + "\n지금 날짜와 시간은 {time}이야"

    def get_chat_history(self):
        history = self.logger.get_log()
        chat_history = []
        if self.session_id in history:
            session_hist = [self.session_id]
            for user, chatbot, _ in session_hist:
                chat_history.append(user)
                chat_history.append(chatbot)
        return chat_history

    def chat(self, user_input):  ## Cohere
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