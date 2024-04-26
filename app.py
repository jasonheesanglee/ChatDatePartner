import streamlit as st
from PIL import Image
from ChatBot import ChatBot
from datetime import datetime

def sidebar_slider(factor, value):
    return st.sidebar.slider(factor, 0.00, 100.00, value=value)

def send_message(input_text):
    if input_text.lower() in ['exit', 'quit']:
        st.session_state.chat_history.append({'message': 'Ending Chat Session.', 'is_user': False})
        if 'chatbot' in st.session_state:
            del st.session_state['chatbot']
    else:
        if 'chatbot' in st.session_state:
            response = st.session_state['chatbot'].chat(input_text)
            st.session_state.chat_history.append({'message': input_text, 'is_user': True})
            st.session_state.chat_history.append({'message': response, 'is_user': False})


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
domain = st.sidebar.selectbox('연인의 전공을 골라주세요.', ['컴퓨터공학', '기계공학', '경제학', '수학', '호텔경영학'])
gaebang = sidebar_slider('개방성', value=84.40)
seongsil = sidebar_slider('성실성', value=92.91)
woehyang = sidebar_slider('외향성', value=90.43)
chinhwa = sidebar_slider('친화성', value=88.65)
singyung = sidebar_slider('신경성', value=63.48)

apply_button = st.sidebar.button('연인과의 챗 시작하기')

if 'chat_history' not in st.session_state:
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
    with st.form('Chat Form', clear_on_submit=True):
        user_input = st.text_input('메시지를 입력해주세요.:', key='user_input')
    if st.button('Send'):
        if user_input.lower() in ['exit', 'quit']:
            st.write('Ending Chat Session')
            del st.session_state['chatbot']
            del st.session_state.chat_history
        else:
            response = st.session_state['chatbot'].chat(user_input)
            if 'chatbot' in st.session_state:
                st.session_state.chat_history.append({
                    'name': user_name,
                    'text': input_text
                })
                with st.chat_message(user_name):
                    st.write(input_text)
                st.session_state.chat_history.append({
                    'name': partner_name,
                    'text': response
                })
                with st.chat_message(partner_name):
                    st.write(response)
            for msg in st.session_state.chat_history:
            # st.chat_message takes a string and automatically handles the display.
                with st.chat_message('user'):
                    st.write(msg)

            # st.session_state.chat_history += f"{user_name}: {user_input}\n{partner_name}: {response}"
            # st.text_area('Chat', value=st.session_state.chat_history, height=300, disabled=True)




    #
    # # if 'chat_history' not in st.session_state:
    # st.session_state.chat_history = []
    #
    # if user_name and partner_name and apply_button:
    #     current_time = datetime.now().strftime('%Y%m%d%H%M%S')
    #     session_key = f'{user_name}_{partner_name}_{age}_{domain}_{current_time}'
    #     chatbot = ChatBot(user_name=user_name, partner_name=partner_name,
    #                       sex=gender, age=age, domain=domain,
    #                       session_id=session_key,
    #                       gaebang=gaebang, seongsil=seongsil,
    #                       woehyang=woehyang, chinhwa=chinhwa,
    #                       singyung=singyung, log_file_path=None)
    #     st.session_state['chatbot'] = chatbot
    #
    #
    #     with st.form("Chat Form", clear_on_submit=True):
    #         user_input = st.text_input("메시지를 입력해주세요:", key="chat_input")
    #         submit_button = st.form_submit_button("Send")
    #
    #     if submit_button and user_input:
    #         send_message(user_input)
    #
    #     for message in st.session_state.chat_history:
    #         st.chat_message(message['message'], is_user=message['is_user'])

# ------------------------------------------------------------------
#
# import streamlit as st
# from PIL import Image
# from ChatBot import ChatBot
# from datetime import datetime
#
# def sidebar_slider(factor, value):
#     return st.sidebar.slider(factor, 0.00, 100.00, value=value)
#
# def send_message(input_text, user_name, partner_name):
#     if input_text.lower() in ['exit', 'quit']:
#         st.session_state.chat_history.append({
#             'name': user_name,
#             'text': 'Ending Chat Session.'
#         })
#         with st.chat_message(user_name):
#             st.write(input_text)
#         if 'chatbot' in st.session_state:
#             del st.session_state['chatbot']
#     else:
#         if 'chatbot' in st.session_state:
#             response = st.session_state['chatbot'].chat(input_text)
#             st.session_state.chat_history.append({
#                 'name': user_name,
#                 'text': input_text
#             })
#             with st.chat_message(user_name):
#                 st.write(input_text)
#             st.session_state.chat_history.append({
#                 'name': partner_name,
#                 'text': response
#             })
#             with st.chat_message(partner_name):
#                 st.write(response)
#
#
# st.title('Chat Date Partner')
# st.header('개인화된 연인과 대화를 나누어보세요!')
#
# chat_date_img = Image.open('chat_gf.png')
# width, height = chat_date_img.size
# chat_date_img = chat_date_img.resize((width, height))
#
# left_co, cent_co, last_co = st.columns(3)
# with cent_co:
#     st.image(chat_date_img)
#
# st.sidebar.title('내 연인 설정하기')
# user_name = st.sidebar.text_input('이름/닉네임을 입력해주세요')
# partner_name = st.sidebar.text_input('연인의 이름/닉네임을 입력해주세요')
# gender = st.sidebar.selectbox('연인의 성별을 골라주세요.', ['여자', '남자'])
# age = st.sidebar.slider('연인의 나이를 설정해주세요.', 21, 100, value=26)
# domain = st.sidebar.selectbox('연인의 전공을 골라주세요.', ['컴퓨터공학', '기계공학', '경제학', '수학', '호텔경영학'])
# gaebang = sidebar_slider('개방성', value=84.40)
# seongsil = sidebar_slider('성실성', value=92.91)
# woehyang = sidebar_slider('외향성', value=90.43)
# chinhwa = sidebar_slider('친화성', value=88.65)
# singyung = sidebar_slider('신경성', value=63.48)
#
# apply_button = st.sidebar.button('연인과의 챗 시작하기')
#
# # ---------------------------------------------------------------------------------------------------------------------
# # submit_button = None
# # user_input = None
#
# if (apply_button and user_name and partner_name) or ('chatbot' in st.session_state):
#     current_time = datetime.now().strftime('%Y%m%d%H%M%S')
#     session_key = f'{user_name}_{partner_name}_{age}_{domain}_{current_time}'
#     chatbot = ChatBot(user_name=user_name, partner_name=partner_name, sex=gender, age=age, domain=domain,
#                       session_id=session_key, gaebang=gaebang, seongsil=seongsil,
#                       woehyang=woehyang, chinhwa=chinhwa, singyung=singyung, log_file_path=None)
#     st.session_state['chatbot'] = chatbot
#     with st.form("Chat Form", clear_on_submit=True):
#         user_input = st.text_input("메시지를 입력해주세요:", key="chat_input")
#         submit_button = st.form_submit_button("Send")
#
#     if submit_button and user_input:
#         send_message(user_input, user_name, partner_name)
#         # st.write(user_input)
# else:
#     st.warning('연인과의 챗 시작하기 버튼을 눌러주세요.')





# for msg in st.session_state.chat_history:
#     # st.chat_message takes a string and automatically handles the display.
#     with st.chat_message('user'):
#         st.write(msg['text'])
