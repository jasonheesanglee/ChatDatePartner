import streamlit as st
from PIL import Image
from ChatBot import ChatBot
from datetime import datetime

current_time = str(datetime.now().time()).replace(':', '')
st.title('Chat Date Partner')
st.header('Customize your date partner')

chat_date_img = Image.open('chat_gf.png')
st.image(chat_date_img)
st.sidebar.title('Customize Options')
user_name = st.sidebar.text_input('Enter your name')
partner_name = st.sidebar.text_input('Enter your date partner\'s name')
gender = st.sidebar.selectbox('Choose your date partner\'s gender',
                              ['Male', 'Female']
                              )
age = st.sidebar.slider('Identify your date partner\'s age',
                        21, 100,
                        value=26
                        )
domain = st.sidebar.selectbox('Choose your date partner\'s professional domain',
                              ['Computer Science', 'Engineering', 'Economics', 'Mathematics', 'Hospitality Management']
                              )

apply_button = st.sidebar.button('Start Chatting')

if 'chat_history' not in st.session_state:
        st.session_state.chat_history = ""

if user_name and partner_name and apply_button:
    session_key = f'{user_name}_{partner_name}_{age}_{domain}_{current_time}'
    chatbot = ChatBot(user_name=user_name, partner_name=partner_name, sex=gender, age=age, domain=domain, session_id=session_key, log_file_path=None)
    st.session_state['chatbot'] = chatbot

if 'chatbot' in st.session_state:
    user_input = st.text_input('Type your message:', key='user_input')
    if st.button('Send'):
        if user_input.lower() in ['exit', 'quit']:
            st.write('Ending Chat Session')
            del st.session_state['chatbot']
            del st.session_state.chat_history

        else:
            response = st.session_state['chatbot'].chat(user_input)
            st.session_state.chat_history += f"{user_name}: {user_input}\n{partner_name}: {response}\n"
            st.text_area('Chat', value=st.session_state.chat_history, height=300, disabled=True)