import pytz
from PIL import Image
import streamlit as st
from ChatBot import ChatBot
from datetime import datetime

def sidebar_slider(factor, value):
    return st.sidebar.slider(factor, 0.00, 100.00, value=value)
#
# def send_message(input_text):
#     if input_text.lower() in ['exit', 'quit']:
#         st.session_state.chat_history.append({'message': 'Ending Chat Session.', 'is_user': False})
#         if 'chatbot' in st.session_state:
#             del st.session_state['chatbot']
#     else:
#         if 'chatbot' in st.session_state:
#             response = st.session_state['chatbot'].chat(input_text)
#             st.session_state.chat_history.append({'message': input_text, 'is_user': True})
#             st.session_state.chat_history.append({'message': response, 'is_user': False})


st.set_page_config('Chat Date Partner', page_icon='😍')

st.title('Chat Date Partner')
st.header('개인화된 연인과 대화를 나누어보세요!')

chat_date_img = Image.open('chat_gf.png')
width, height = chat_date_img.size
# width, height = int(width/2), int(height/2)
chat_date_img = chat_date_img.resize((width, height))

left_co, cent_co, last_co = st.columns(3)
with cent_co:
    st.image(chat_date_img)

st.sidebar.title('내 연인 설정하기')
user_name = st.sidebar.text_input('이름/닉네임을 입력해주세요')
partner_name = st.sidebar.text_input('연인의 이름/닉네임을 입력해주세요')
gender = st.sidebar.selectbox('연인의 성별을 골라주세요.', ['여자', '남자'])
age = st.sidebar.slider('연인의 나이를 설정해주세요.', 21, 100, value=26)
domain = st.sidebar.selectbox('연인의 전공을 골라주세요.', ['호텔경영학', '컴퓨터공학', '기계공학', '경제학', '수학'])
gaebang = sidebar_slider('개방성', value=84.40)
seongsil = sidebar_slider('성실성', value=92.91)
woehyang = sidebar_slider('외향성', value=90.43)
chinhwa = sidebar_slider('친화성', value=88.65)
singyung = sidebar_slider('신경성', value=63.48)

apply_button = st.sidebar.button('연인과의 챗 시작하기')

if 'chat_history' not in st.session_state or str(st.session_state.chat_history) == True:
    st.session_state.chat_history = []
if user_name and partner_name and apply_button:
    current_time = datetime.now().strftime('%Y%m%d%H%M%S')
    session_key = f'{user_name}_{partner_name}_{age}_{domain}_{current_time}'
    chatbot = ChatBot(user_name=user_name, partner_name=partner_name,
                      sex=gender, age=age, domain=domain,
                      session_id=session_key,
                      gaebang=gaebang, seongsil=seongsil,
                      woehyang=woehyang, chinhwa=chinhwa,
                      singyung=singyung, log_file_path=None)
    st.session_state['chatbot'] = chatbot


if 'chatbot' in st.session_state:
    messages = st.container(height=600)
    st.session_state['chatbot'].initializer()
    if st.session_state.chat_history != []:
        for msg in st.session_state.chat_history:
            messages.chat_message(msg['name']).write(msg['text'])
    if prompt := st.chat_input('메시지를 입력해주세요 : '):
        messages.chat_message(user_name).write(prompt)

        if prompt.lower() in ['exit', 'quit']:
            messages.chat_message('System').write('Ending Chat Session')
            del st.session_state['chatbot']
            del st.session_state.chat_history
        else:
            response = st.session_state['chatbot'].chat(prompt)
            messages.chat_message(partner_name).write(response)
            st.session_state.chat_history.append({
                'name': user_name,
                'text': prompt,
                'text_time' : str(datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime('%Y%m%d%H%M%S')),
            })

            st.session_state.chat_history.append({
                'name': partner_name,
                'text': response,
                'text_time': str(datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime('%Y%m%d%H%M%S')),

            })