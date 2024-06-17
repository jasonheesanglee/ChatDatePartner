import json
import pytz
import cohere
import streamlit as st
from langchain_cohere import ChatCohere
from langchain_openai import ChatOpenAI
from datetime import datetime
from Logger import Logger

try:
    config = st.secrets
    # COHERE_API_KEY = st.secrets['COHERE_API_KEY']
    # OPENAI_API_KEY = st.secrets['OPENAI_API_KEY']
except:
    with open('./config.json', 'r') as secrets:
        config = json.load(secrets)
COHERE_API_KEY = config['COHERE_API_KEY']
OPENAI_API_KEY = config['OPENAI_API_KEY']

cfg = {
    'cohere_api_key': COHERE_API_KEY,
    'openai_api_key' : OPENAI_API_KEY,
    'chromadb_dir' : ''
}


class ChatBot:
    def __init__(self,
                 user_name,
                 partner_name,
                 domain,
                 session_id,
                 prompts,
                 log_file_path=None,
                 mode='cohere'
                 ):

        self.session_id = session_id
        self.mode=mode
        self._initialize_llm()

        self.log_file_path = log_file_path
        self.logger = Logger(user_id=f'{user_name}_{partner_name}_{domain}',
                             session_id=session_id,
                             log_file_path=self.log_file_path)
        self.system_message = prompts + "\nSystem : current date and time is {time}"

    def _initialize_llm(self) -> None:
        """
        선택된 모드에 따라 언어 모델을 초기화합니다.
        """
        if self.mode == 'cohere':
            model = 'command-r-plus'
            api_key = cfg['cohere_api_key']
            self.llm = ChatCohere(cohere_api_key=api_key, model=model)            
        
        elif self.mode == 'chatgpt': 
            model = 'gpt-4o'
            api_key = cfg['openai_api_key']
            self.llm = ChatOpenAI(api_key=api_key, model=model)

        else:
            raise KeyError('\'mode\' should be either "chatgpt" or "cohere"')
        

    def get_chat_history(self):
        '''
        Get saved logs from json file.
        :return:
        '''
        history = self.logger.get_log()
        chat_history = []
        if self.session_id in history:
            session_hist = [self.session_id]
            for user, chatbot, _ in session_hist:
                chat_history.append(user)
                chat_history.append(chatbot)
        return chat_history

    def chat(self, user_input):
        '''
        Chat a user with given input using Cohere Api.
        :param user_input: user chat to chatbot -> str
        :return: chat message
        '''
        current_time = str(datetime.now(tz=pytz.timezone('Asia/Seoul')))

        if self.mode=='cohere':
            response = self.llm.chat(
                chat_history=self.get_chat_history(),
                preamble=self.system_message.replace('{time}', current_time),
                message=user_input,
                connectors=[{"id": "web-search"}],
            ).text
        elif self.mode=='chatgpt':
            prompt = '\n'.join(self.get_chat_history()) + user_input
            prompt = prompt + f"\n{self.system_message.replace('{time}', current_time)}"
            response = self.llm.invoke(prompt).content


        self.logger.log(user_input=user_input,
                        chat_output=response,
                        current_time=current_time
                        )
        return response
    
