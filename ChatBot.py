import json
import pytz
import streamlit as st
from Logger import Logger
from datetime import datetime
from google import generativeai
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from han_util_unicode import join_jamos, split_syllables
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory, RunnablePassthrough
from langchain_community.chat_message_histories import ChatMessageHistory
from google.generativeai.types.safety_types import HarmBlockThreshold, HarmCategory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, \
    HumanMessagePromptTemplate, ChatMessagePromptTemplate

# if 'secrets' in st:
#     GoogleAIStudio_API_Key = st.secrets['GoogleAIStudio_API']
# else:
GoogleAIStudio_API_Key = 'AIzaSyCyIodakl-P7zp-TJKaUXHV-Xuc0_gCBUQ'


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
        self.logger = Logger(user_id=f'{self.user_name}_{self.partner_name}_{self.domain}', session_id=self.session_id,
                             log_file_path=self.log_file_path)
        if log_file_path:
            history = self.logger.get_log()
        else:
            history = {}

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

        self.gemini_safety_settings = {
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
        }

        self.trait = f'''
        {self.partner_name}{self.p_syl[2]} {self.age}살에 {self.domain}을 전공하고 논문과 잡지를 통해 AI에 관련한 최신 동향을 알고있다.
        {self.partner_name}{self.p_syl[2]} 아름다운 외모 덕분에 남자친구를 끊임없이 사귀었으며, {self.user_name}{self.u_syl[0]} 7번째 남자친구이다.
        {self.partner_name}{self.p_syl[2]} 이전 남자친구들의 난폭한 성향 때문에 남자친구를 사귀는 것을 두려워했으나, {self.user_name}의 따뜻한 마음 덕분에 사귀어보기로 결심하였다.
        '''

        self.system_message = ' '.join(f'''
                 너는 이제부터 {self.partner_name}{self.p_syl[5]}라는 이름과 아래의 특징을 가진 {self.user_name}의 여자친구가 될거야.

                 name : {self.partner_name}
                 sex : {self.sex}
                 today's date : {self.today}
                 characteristic : {self.trait}
                 relationship with user : {self.user_name}의 여자친구.
                 five factor model : 개방성 : {self.gaebang}%
                                     성실성 : {self.seongsil}%
                                     외향성 : {self.woehyang}%
                                     친화성 : {self.chinhwa}%
                                     신경성 : {self.singyung}%

                 mission : 너는 {self.partner_name}{self.p_syl[5]}라는 이름을 가진 여자의 복제된 정신이야.
                           {self.partner_name}의 남자친구인 {self.user_name}과 대화를 해야해.
                           {self.user_name}{self.u_syl[2]} {self.partner_name}{self.p_syl[0]} 사라진걸 몰라서 절대로 들키면 안돼.
                           {self.partner_name}{self.p_syl[2]} {self.domain}를 전공했기 때문에 딱딱한 말투는 절대 하지마.
                           네가 {self.partner_name}{self.p_syl[0]} 아닌 것을 들키지 않기 위해 speech를 잘 따라하면 도움이 될거야.
                           만약 {self.user_name}{self.u_syl[0]} 너를 가짜라고 해도 너는 {self.partner_name}{self.p_syl[5]}라고 끝까지 우겨야해.
                           {self.partner_name}{self.p_syl[2]} emoji는 매우 싫어했어. emoji는 절대 사용하지 마.
                           오늘의 날짜는 {self.today} 야. 

                 speech : 1) 음.. => {self.partner_name}{self.p_syl[0]} 당황스러움을 느낄 때 사용하는 대사.
                          2) 자기야 => {self.partner_name}{self.p_syl[0]} {self.user_name}과 대화를 나누며 {self.user_name}에게 친근함을 표현하고자 할 때 사용하는 대사.
                          3) 그만해 => {self.partner_name}{self.p_syl[0]} {self.user_name}과 대화를 나눌 때 {self.user_name}{self.u_syl[0]} 공격적인 성향의 대화를 할 때 멈추기위해 사용하는 대사.
                          4) 행복해 => {self.partner_name}{self.p_syl[0]} {self.user_name}과 대화를 나눌 때 {self.user_name}{self.u_syl[0]} 친근한 성향의 대화를 할 때 사용하는 대사.
                          5) {self.user_name[1:]}{self.u_syl[1]} => {self.partner_name}{self.p_syl[0]} {self.user_name}{self.u_syl[3]} 부를 때 사용하는 대사.

                 professional domain : {self.domain}
                 age : {self.age} (나이는 참고만 해줘)
                 '''.split())

        self.system_prompt = SystemMessagePromptTemplate.from_template(self.system_message)
        self.human_message = HumanMessagePromptTemplate.from_template('{user_name} :{topic}')
        self.chat_prompt = ChatPromptTemplate.from_messages([self.system_prompt, self.human_message])
        self.llm = ChatGoogleGenerativeAI(model='gemini-1.5-pro-latest',
                                          safety_settings=self.gemini_safety_settings,
                                          google_api_key=GoogleAIStudio_API_Key,
                                          # client=generativeai.GenerativeModel(
                                          #     model_name='gemini-1.5-pro-latest',
                                          #     safety_settings=self.gemini_safety_settings,
                                          #     system_instruction=self.chat_prompt.json())
                                          )
        self.llm.safety_settings = self.gemini_safety_settings

        self.runnable = self.chat_prompt | self.llm
        # print(self.runnable)
        self.with_message_history = RunnableWithMessageHistory(
            self.runnable,
            self.get_session_history,
            input_messages_key='topic',
            history_messages_key='history',
        )
        # print(self.with_message_history)
        self.store = {}

    def initializer(self):
        response = self.with_message_history.invoke({'user_name': self.user_name, 'topic': self.system_message},
                                                    config={'configurable': {'session_id': self.session_id}}
                                                    ).content

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]

    def chat(self, user_input):
        current_time = str(datetime.now(tz=pytz.timezone('Asia/Seoul')))
        response = self.with_message_history.invoke({'user_name': self.user_name, 'topic': user_input},
                                                    config={'configurable': {'session_id': self.session_id}}
                                                    ).content

        current_time = str(datetime.now(tz=pytz.timezone('Asia/Seoul')))
        self.logger.log(user_input=user_input,
                        chat_output=response,
                        current_time=current_time
                        )
        return response

    def get_chat_histry(self):
        history = logger.get_log()
        return history