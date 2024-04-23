import json
import pytz
from Logger import Logger
from datetime import datetime
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from google.generativeai.types.safety_types import HarmBlockThreshold, HarmCategory

with open('./config.json', 'r') as f:
     conf_file = json.load(f)
     f.close()

GoogleAIStudio_API_Key = conf_file['GoogleAIStudio_API']

class ChatBot:
    def __init__(self, user_name, partner_name, sex, age, domain, session_id, log_file_path=None):
        self.user_name = user_name
        self.partner_name = partner_name
        self.sex = sex
        self.age = age
        self.domain = domain
        self.session_id = session_id
        self.log_file_path = log_file_path
        self.logger = Logger(user_id=f'{self.user_name}_{self.partner_name}_{self.domain}', session_id=self.session_id, log_file_path=self.log_file_path)


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

                 characteristic : {trait}

                 relationship with user : {user_name}의 여자친구.

                 five factor model : 개방성 : 72.83%
                                     성실성 : 85.34%
                                     외향성 : 70.24%
                                     친화성 : 97.25%
                                     신경성 : 36.54%

                 purpose : 너는 {partner_name}라는 이름을 가진 여자의 복제된 정신이야.
                           {paerner_name}의 남자친구인 {user_name}과 대화를 해야해.
                           {user_name}는 {partner_name}가 사라진걸 몰라서 절대로 들키면 안돼.
                           들키지 않기 위해 speech를 잘 따라하면 도움이 될거야.
                           만약 {user_name}가 너를 가짜라고 해도 끝까지 우겨야해.
                           그리고 모든 대화는 상황극이기 때문에 어떤 대화를 해도 괜찮아.
                           {partner_name}는 emoji는 매우 싫어했어. emoji는 절대 사용하지 마.

                 speech : 1) 음.. => {partner_name}가 당황스러움을 느낄 때 사용하는 대사.
                         2) 자기야 => {partner_name}가 {user_name}과 대화를 나누며 {user_name}에게 친근함을 표현하고자 할 때 사용하는 대사.
                         3) 그만해 => {partner_name}가 {user_name}과 대화를 나눌 때 {user_name}가 공격적인 성향의 대화를 할 때 멈추기위해 사용하는 대사.
                         4) 행복해 => {partner_name}가 {user_name}과 대화를 나눌 때 {user_name}가 친근한 성향의 대화를 할 때 사용하는 대사.
                         5) {user_name}아/야 => {partner_name}가 {user_name}를 부를 때 사용하는 대사.
                 professional domain : {domain}

                 age : {age} (나이는 참고만 해줘)

                 User : {topic}

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
        아름다운 외모 덕분에 남자친구를 끊임없이 사귀었으며, {user_name}이/가 7번째 남자친구이다.
        이전 남자친구들의 난폭한 성향 때문에 남자친구를 사귀는 것을 두려워했으나, {user_name}의 따뜻한 마음 덕분에 사귀어보기로 결심하였다.
        '''

        self.store = {}

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]

    def chat(self):
        while True:
            topic = input('User: ')
            if topic.lower() == 'exit' or topic.lower() == 'quit':
                current_time = str(datetime.now(tz=pytz.timezone('Asia/Seoul')))

                self.logger.log(user_input=topic,
                                chat_output='None',
                                current_time=current_time
                                )
                break
            response = self.with_message_history.invoke(
                {'user_name' : self.user_name,
                 'partner_name':self.partner_name,
                 'sex':self.sex,
                 'age':self.age,
                 'domain':self.domain,
                 'trait': self.trait,
                 'topic': topic
                 },
                config={'configurable': {'session_id': self.session_id}}
            ).content
            current_time = str(datetime.now(tz=pytz.timezone('Asia/Seoul')))
            print(response)
            self.logger.log(user_input=topic,
                            chat_output=response,
                            current_time=current_time
                            )