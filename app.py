import pytz
from PIL import Image
import streamlit as st
from Prompts import Prompts
# from EmailSender import EmailSender
from ChatBot import ChatBot
from datetime import datetime
from han_util_unicode import build_josa

# email_sender = EmailSender()

def sidebar_slider(factor, value):
    return st.sidebar.slider(factor, 0.00, 100.00, value=value)

st.set_page_config('Chat Date Partner', page_icon='😍')

st.title('Chat Date Partner')
st.header('개인화된 대화상대와 대화를 나누어보세요!')

chat_date_img = Image.open('chat_gf.png')
width, height = chat_date_img.size
chat_date_img = chat_date_img.resize((width, height))

left_co, cent_co, last_co = st.columns(3)
with cent_co:
    st.image(chat_date_img)

st.sidebar.title('대화상대 설정하기')
user_name = st.sidebar.text_input('본인의 이름/닉네임을 입력해주세요')
partner_name = st.sidebar.text_input('상대방의 이름/닉네임을 입력해주세요')
u_gender = st.sidebar.selectbox('본인의 성별을 골라주세요.', ['여자', '남자'], index=1)
p_gender = st.sidebar.selectbox('상대방의 성별을 골라주세요.', ['여자', '남자'], index=0)
friend_type = st.sidebar.text_input('상대방과의 관계를 입력해주세요.', value='연인')
f_syl = build_josa(friend_type)
age = st.sidebar.slider('상대방의 나이를 설정해주세요.', 21, 100, value=26)
domain = st.sidebar.text_input('상대방의 전공을 입력해주세요.', value='호텔경영학과')
gaebang = sidebar_slider('개방성', value=84.40)
seongsil = sidebar_slider('성실성', value=92.91)
woehyang = sidebar_slider('외향성', value=90.43)
chinhwa = sidebar_slider('친화성', value=88.65)
singyung = sidebar_slider('신경성', value=63.48)

if friend_type:
    apply_button = st.sidebar.button(f'{friend_type}{f_syl[6]}의 챗 시작하기')

if user_name and partner_name and apply_button:
    if 'chatbot' in st.session_state:
        del st.session_state['chatbot']
    if 'chat_history' in st.session_state:
        del st.session_state.chat_history
        # email_sender.send()

if 'chat_history' not in st.session_state or str(st.session_state.chat_history) == True:
    st.session_state.chat_history = []

if user_name and partner_name and apply_button:
    current_time = datetime.now().strftime('%Y%m%d%H%M%S')
    session_id = f'{user_name}_{partner_name}_{age}_{domain}_{current_time}'
    prompts = Prompts(user_name=user_name, partner_name=partner_name,
                      u_gender=u_gender, p_gender=p_gender, friend_type=friend_type,
                      age=age, domain=domain, session_id=session_id,
                      gaebang=gaebang, seongsil=seongsil, woehyang=woehyang, chinhwa=chinhwa, singyung=singyung
                      ).get_prompts()
    chatbot = ChatBot(user_name=user_name, partner_name=partner_name, domain=domain,
                      session_id=session_id, prompts=prompts, log_file_path=None)
    st.session_state['chatbot'] = chatbot


if 'chatbot' in st.session_state:
    messages = st.container(height=800)

    if st.session_state.chat_history != []:
        for msg in st.session_state.chat_history:
            messages.chat_message(msg['name']).write(msg['text'])

    if prompt := st.chat_input('메시지를 입력해주세요 : '):
        messages.chat_message(user_name).write(prompt)

        if prompt.lower() in ['exit', 'quit']:
            messages.chat_message('System').write('Ending Current Chat Session')
            del st.session_state['chatbot']
            del st.session_state.chat_history
            # email_sender.send()

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
