import os
import json
import pytz
import streamlit as st
from langchain_cohere import ChatCohere
from langchain_openai import ChatOpenAI
from datetime import datetime
from Logger import Logger
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
current_time = str(datetime.now(tz=pytz.timezone('Asia/Seoul')))
try:
    config = st.secrets
    os.environ['COHERE_API_KEY'] = config['COHERE_API_KEY']
    os.environ['OPENAI_API_KEY'] = config['OPENAI_API_KEY']

except FileNotFoundError:
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
        self.logger = Logger(
            user_id=user_id,
            session_id=session_id,
            log_file_path=self.log_file_path
            )
        
        self.logger.log(
            user_input=prompts, 
            chat_output=None, 
            current_time=current_time
            )
        
        self.messages = self.logger.get_formatted_log()

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
        return self.logger.get_formatted_log()

    def chat(self, user_input):
        '''
        Chat a user with given input using Cohere Api.
        :param user_input: user chat to chatbot -> str
        :return: chat message
        '''
        current_time = str(datetime.now(tz=pytz.timezone('Asia/Seoul')))
        user_input = HumanMessage(content=user_input)
        self.messages.append(user_input)
        chain = ChatPromptTemplate.from_messages(self.messages) | self.llm

        response = chain.invoke({'time': current_time}).content

        self.messages.append(AIMessage(content=response))

        self.logger.log(user_input=user_input.content,
                        chat_output=response,
                        current_time=current_time
                        )
        return response
    
if __name__ == "__main__":
    user_name = "user"
    partner_name = "partner"
    domain = "domain"
    session_id = "session_id"
    prompts = "Your prompts here"
    log_file_path = None
    mode = "chatgpt"

    chatbot = ChatBot(user_name=user_name, partner_name=partner_name, domain=domain,
                      session_id=session_id, prompts=prompts, log_file_path=log_file_path, mode=mode)
    prompt = "Hello, how are you?"
    response = chatbot.chat(prompt)
    print(response)

