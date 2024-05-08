import json
import pytz
import cohere
import streamlit as st
from Logger import Logger
from datetime import datetime
from google import generativeai
from han_util_unicode import join_jamos, split_syllables
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory, RunnablePassthrough
from langchain_community.chat_message_histories import ChatMessageHistory
from google.generativeai.types.safety_types import HarmBlockThreshold, HarmCategory

from Prompts import Prompts

try:
    GoogleAIStudio_API_Key = st.secrets['GoogleAIStudio_API']
except:
    with open('api_key.json') as secrets:
        GoogleAIStudio_API_Key = json.load(secrets)['GoogleAIStudio_API']

try:
    COHERE_API_KEY = st.secrets['COHERE_API_KEY']
except:
    with open('api_key.json') as secrets:
        COHERE_API_KEY = json.load(secrets)['COHERE_API_KEY']

class ChatBot:
    def __init__(self, user_name, partner_name,
                 sex, age, domain,
                 session_id,
                 gaebang, seongsil, woehyang, chinhwa, singyung,
                 log_file_path=None):
        self.today = datetime.today().strftime('%Y.%m.%d')
        self.user_name = user_name
        self.partner_name = partner_name
        self.sex = sex
        self.age = age
        self.domain = domain
        self.gaebang = gaebang
        self.seongsil = seongsil
        self.woehyang = woehyang
        self.chinhwa = chinhwa
        self.singyung = singyung

        self.session_id = session_id
        self.log_file_path = log_file_path
        self.logger = Logger(user_id=f'{self.user_name}_{self.partner_name}_{self.domain}',
                             session_id=self.session_id,
                             log_file_path=self.log_file_path)

        self.co = cohere.Client(api_key=COHERE_API_KEY)
        if split_syllables(partner_name)[-1] in ['ㅏ', 'ㅑ', 'ㅓ', 'ㅕ',
                                                 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ',
                                                 'ㅡ', 'ㅣ', 'ㅙ', 'ㅞ',
                                                 'ㅚ', 'ㅟ', 'ㅢ', 'ㅒ',
                                                 'ㅖ']:
            self.p_syl = ['가', '야', '는', '를', '야', '']  # 홍주는
        else:
            self.p_syl = ['이', '아', '이는', '을', '이야', '이']  # 희상이는
        if split_syllables(user_name)[-1] in ['ㅏ', 'ㅑ', 'ㅓ', 'ㅕ',
                                              'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ',
                                              'ㅡ', 'ㅣ', 'ㅙ', 'ㅞ',
                                              'ㅚ', 'ㅟ', 'ㅢ', 'ㅒ',
                                              'ㅖ']:
            self.u_syl = ['가', '야', '는', '를', '야', '']  # 홍주는
        else:
            self.u_syl = ['이', '아', '이는', '을', '이야', '이']  # 희상이는

        system_message = Prompts.get_prompts()
        self.system_message = system_message + "\n지금 날짜와 시간은 {time}이야"

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