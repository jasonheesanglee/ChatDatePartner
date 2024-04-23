import streamlit as st
from PIL import Image
from ChatBot import ChatBot
from datetime import datetime

current_time = str(datetime.now().time()).replace(':', '')
st.title('Chat Date Partner')
st.header('개인화된 연인과 대화를 나누어보세요!')

chat_date_img = Image.open('chat_gf.png')
st.image(chat_date_img)
st.sidebar.title('내 연인 설정하기')
user_name = st.sidebar.text_input('이름/닉네임을 입력해주세요')
partner_name = st.sidebar.text_input('연인의 이름/닉네임을 입력해주세요')
gender = st.sidebar.selectbox('연인의 성별을 골라주세요.',
                              ['남자', '여자']
                              )
age = st.sidebar.slider('연인의 나이를 설정해주세요.',
                        21, 100,
                        value=26
                        )
domain = st.sidebar.selectbox('연인의 전공을 골라주세요.',
                              ['컴퓨터공학', '기계공학', '경제학', '수학', '호텔경영학']
                              )
gaebang = st.sidebar.slider('개방성',
                        0.00, 100.00,
                        value=50.00
                        )
seongsil = st.sidebar.slider('성실성',
                        0.00, 100.00,
                        value=50.00
                        )
woehyang = st.sidebar.slider('외향성',
                        0.00, 100.00,
                        value=50.00
                        )
chinhwa = st.sidebar.slider('친화성',
                        0.00, 100.00,
                        value=50.00
                        )
singyung = st.sidebar.slider('신경성',
                        0.00, 100.00,
                        value=50.00
                        )

apply_button = st.sidebar.button('연인과의 챗 시작하기')

if 'chat_history' not in st.session_state:
        st.session_state.chat_history = ""

if user_name and partner_name and apply_button:
    session_key = f'{user_name}_{partner_name}_{age}_{domain}_{current_time}'
    chatbot = ChatBot(user_name=user_name, partner_name=partner_name,
                      sex=gender, age=age, domain=domain,
                      session_id=session_key,
                      gaebang=gaebang, seongsil=seongsil,
                      woehyang=woehyang, chinhwa=chinhwa,
                      singyung=singyung, log_file_path=None)
    st.session_state['chatbot'] = chatbot

if 'chatbot' in st.session_state:
    user_input = st.text_input('메시지를 입력해주세요.:', key='user_input')
    if st.button('Send'):
        if user_input.lower() in ['exit', 'quit']:
            st.write('Ending Chat Session')
            del st.session_state['chatbot']
            del st.session_state.chat_history

        else:
            response = st.session_state['chatbot'].chat(user_input)
            st.session_state.chat_history += f"{user_name}: {user_input}\n{partner_name}: {response}\n"
            st.text_area('Chat', value=st.session_state.chat_history, height=300, disabled=True)