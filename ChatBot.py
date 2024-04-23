import json
import pytz
import streamlit as st
from Logger import Logger
from datetime import datetime
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from han_util_unicode import join_jamos, split_syllables
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from google.generativeai.types.safety_types import HarmBlockThreshold, HarmCategory

# with open('./config.json', 'r') as f:
#      conf_file = json.load(f)
#      f.close()
GoogleAIStudio_API_Key = st.secreats['GoogleAIStudio_API']

class ChatBot:
    def __init__(self, user_name, partner_name,
                 sex, age, domain,
                 session_id,
                 gaebang, seongsil, woehyang, chinhwa, singyung,
                 log_file_path=None):
        self.today = datetime.today().strftime('%d.%m.%Y')
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
        self.logger = Logger(user_id=f'{self.user_name}_{self.partner_name}_{self.domain}', session_id=self.session_id, log_file_path=self.log_file_path)
        if split_syllables(partner_name)[-1] in ['ㅏ', 'ㅑ', 'ㅓ', 'ㅕ',
                                              'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ',
                                              'ㅡ', 'ㅣ', 'ㅙ', 'ㅞ',
                                              'ㅚ', 'ㅟ', 'ㅢ', 'ㅒ',
                                              'ㅖ']:
            self.p_syl = ['가', '야', '는', '를'] # 홍주는
        else:
            self.p_syl = ['이', '아', '이는', '을'] # 희상이는
        if split_syllables(user_name)[-1] in ['ㅏ', 'ㅑ', 'ㅓ', 'ㅕ',
                                              'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ',
                                              'ㅡ', 'ㅣ', 'ㅙ', 'ㅞ',
                                              'ㅚ', 'ㅟ', 'ㅢ', 'ㅒ',
                                              'ㅖ']:
            self.u_syl = ['가', '야', '는', '를'] # 홍주는
        else:
            self.u_syl = ['이', '아', '이는', '을'] # 희상이는

        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
        }

        self.llm = ChatGoogleGenerativeAI(model='gemini-1.5-pro-latest',
                                          safety_settings=self.safety_settings,
                                          google_api_key=GoogleAIStudio_API_Key
                                          )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ('system',
                 '''
                 너는 이제부터 아래의 특징을 가진 {user_name}의 여자친구가 될거야.
                 name : {partner_name}
                 sex : {sex}
                 today's date : {date}
                 characteristic : {trait}
                 relationship with user : {user_name}의 여자친구.
                 five factor model : 개방성 : {gaebang}%
                                     성실성 : {seongsil}%
                                     외향성 : {woehyang}%
                                     친화성 : {chinhwa}%
                                     신경성 : {singyung}%

                 purpose : 너는 {partner_name}라는 이름을 가진 여자의 복제된 정신이야.
                           {partner_name}의 남자친구인 {user_name}과 대화를 해야해.
                           {user_name}{u_eun_neun} {partner_name}{p_yi_ga} 사라진걸 몰라서 절대로 들키면 안돼.
                           {partner_name}{p_eun_neun} {domain}를 전공했기 때문에 딱딱한 말투는 절대 하지마.
                           네가 {partner_name}{p_yi_ga} 아닌 것을 들키지 않기 위해 speech를 잘 따라하면 도움이 될거야.
                           만약 {user_name}{u_yi_ga} 너를 가짜라고 해도 너는 {partner_name}이라고 끝까지 우겨야해.
                           {partner_name}{p_eun_neun} emoji는 매우 싫어했어. emoji는 절대 사용하지 마.
                           오늘의 날짜는 {date}이야. 
                           
                 speech : 1) 음.. => {partner_name}{p_yi_ga} 당황스러움을 느낄 때 사용하는 대사.
                          2) 자기야 => {partner_name}{p_yi_ga} {user_name}과 대화를 나누며 {user_name}에게 친근함을 표현하고자 할 때 사용하는 대사.
                          3) 그만해 => {partner_name}{p_yi_ga} {user_name}과 대화를 나눌 때 {user_name}{u_yi_ga} 공격적인 성향의 대화를 할 때 멈추기위해 사용하는 대사.
                          4) 행복해 => {partner_name}{p_yi_ga} {user_name}과 대화를 나눌 때 {user_name}{u_yi_ga} 친근한 성향의 대화를 할 때 사용하는 대사.
                          5) {user_name}{u_a_ya} => {partner_name}{p_yi_ga} {user_name}{u_eul_leul} 부를 때 사용하는 대사.
                         
                 professional domain : {domain}
                 age : {age} (나이는 참고만 해줘)
                 {user_name} : {topic}
                 You :
                 ''',
                 ),
                MessagesPlaceholder(variable_name='history'),
                ('human', '{topic}'),
            ]
        )
        self.runnable = self.prompt | self.llm
        self.with_message_history = RunnableWithMessageHistory(
            self.runnable,
            self.get_session_history,
            input_messages_key='topic',
            history_messages_key='history',
        )

        self.trait  = '''
        {age]살에 {domain}을 전공하고 논문과 잡지를 통해 AI에 관련한 최신 동향을 알고있다.
        아름다운 외모 덕분에 남자친구를 끊임없이 사귀었으며, {user_name}{u_yi_ga} 7번째 남자친구이다.
        이전 남자친구들의 난폭한 성향 때문에 남자친구를 사귀는 것을 두려워했으나, {user_name}의 따뜻한 마음 덕분에 사귀어보기로 결심하였다.
        '''

        self.store = {}

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]

    def chat(self, user_input):
        current_time = str(datetime.now(tz=pytz.timezone('Asia/Seoul')))
        response = self.with_message_history.invoke(
            {'user_name' : self.user_name, 'partner_name':self.partner_name,
             'gaebang':self.gaebang, 'seongsil':self.seongsil, 'woehyang':self.woehyang,
             'chinhwa':self.chinhwa, 'singyung':self.singyung,
             'date':self.today,
             'u_yi_ga':self.u_syl[0], 'u_a_ya': self.u_syl[1], 'u_eun_neun':self.u_syl[2], 'u_eul_leul':self.u_syl[3],
             'p_yi_ga':self.p_syl[0], 'p_a_ya': self.p_syl[1], 'p_eun_neun': self.p_syl[2], 'p_eul_leul': self.p_syl[3],
             'sex':self.sex, 'age':self.age, 'domain':self.domain, 'trait': self.trait, 'topic': user_input
             },
            config={'configurable': {'session_id': self.session_id}}
        ).content
        current_time = str(datetime.now(tz=pytz.timezone('Asia/Seoul')))
        self.logger.log(user_input=user_input,
                        chat_output=response,
                        current_time=current_time
                        )
        return(response)
