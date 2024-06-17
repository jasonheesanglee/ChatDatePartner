import os
import json
import pytz
import cohere
import streamlit as st
from langchain_cohere import ChatCohere
from langchain_openai import ChatOpenAI
from datetime import datetime
from Logger import Logger
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

try:
    config = st.secrets
except:
    with open('./config.json', 'r') as secrets:
        config = json.load(secrets)
os.environ['COHERE_API_KEY'] = config['COHERE_API_KEY']
os.environ['OPENAI_API_KEY'] = config['OPENAI_API_KEY']

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
        user_id = f'{user_name}_{partner_name}_{domain}'
        self.logger = Logger(user_id=user_id,
                             session_id=session_id,
                             log_file_path=self.log_file_path)
        self.messages = self.logger.get_log()[user_id][session_id] # []

        self.system_message = SystemMessage(content="System : current date and time is {time}")
        self.messages.append(self.system_message)
        self.prompt = ChatPromptTemplate.from_messages(self.messages)

    def _initialize_llm(self) -> None:
        """
        선택된 모드에 따라 언어 모델을 초기화합니다.
        """
        if self.mode == 'cohere':
            model = 'command-r-plus'
            self.llm = ChatCohere(model=model)            
        
        elif self.mode == 'chatgpt': 
            model = 'gpt-4o'
            self.llm = ChatOpenAI(model=model)

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
        user_input = HumanMessage(content=user_input)
        self.propmt.append(user_input)
        chain = self.propmt | self.llm

        if self.mode=='cohere':
            response = chain.invoke({'time':current_time}).content
        elif self.mode=='chatgpt':
            response = chain.invoke({'time':current_time}).content

        self.prompt.append(AIMessage(content=response))

        self.logger.log(user_input=user_input,
                        chat_output=response,
                        current_time=current_time
                        )
        return response
    
