import streamlit as st
from PIL import Image
from ChatBot import ChatBot
from datetime import datetime

def sidebar_slider(factor, value):
    return st.sidebar.slider(factor, 0.00, 100.00,value=value)

current_time = str(datetime.now().time()).replace(':', '')
st.title('Chat Date Partner')
st.header('개인화된 연인과 대화를 나누어보세요!')

chat_date_img = Image.open('chat_gf.png')
width, height = chat_date_img.size
# width, height = int(width/2), int(height/2)
chat_date_img = chat_date_img.resize((width, height))

left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image(chat_date_img, )

st.sidebar.title('내 연인 설정하기')
user_name = st.sidebar.text_input('이름/닉네임을 입력해주세요')
partner_name = st.sidebar.text_input('연인의 이름/닉네임을 입력해주세요')
gender = st.sidebar.selectbox('연인의 성별을 골라주세요.',
                              ['여자', '남자']
                              )
age = st.sidebar.slider('연인의 나이를 설정해주세요.',
                        21, 100,
                        value=26
                        )
domain = st.sidebar.selectbox('연인의 전공을 골라주세요.',
                              ['컴퓨터공학', '기계공학', '경제학', '수학', '호텔경영학']
                              )
gaebang = sidebar_slider('개방성', value=84.40)
seongsil = sidebar_slider('성실성', value=92.91)
woehyang = sidebar_slider('외향성', value=90.43)
chinhwa = sidebar_slider('친화성', value=88.65)
singyung = sidebar_slider('신경성', value=63.48)

apply_button = st.sidebar.button('연인과의 챗 시작하기')

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
def send_message():
    user_input = st.session_state.get('user_input', '').strip()
    if user_input.lower() in ['exit', 'quit']:
        st.session_state.chat_history.append({'message' : 'Ending Chat Session.',
                                              'is_user' : False
                                              })
        del st.session_state['chatbot']
        del st.session_state.chat_history

    else:
        response = st.session_state['chatbot'].chat(user_input)
        st.session_state.chat_history.append({'meesage' : user_input, 'is_user': True})
        st.session_state.chat_history.append({'meesage': response, 'is_user': False})
    st.session_state.user_input = ''

# def clear_input():
#     st.session_state.user_input = ''

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
    user_input = st.text_input('메시지를 입력해주세요.:', key='user_input', on_change=send_message)
    send_button = st.button('Send', on_click=send_message)
    for message in st.session_state.chat_history:
        st.chat_message(**message)

