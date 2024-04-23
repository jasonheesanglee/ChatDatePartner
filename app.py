import streamlit as st
from PIL import Image
from ChatBot import Chatbot

st.title('Chat Date Partner')
st.header('Customize your date partner')

chat_date_img = Image.open('chat_gf.png')
st.image(chat_date_img)
st.sidebar.title('Customize Options')
user_name = st.text_input('Enter your name')
partner_name = st.text_input('Enter your date partner\'s name')
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

apply_button = st.sidebar.button('Apply')

if start_button :
    chatbot = Chatbot(user_name=user_name, parner_name=partner_name, sex=gender, age=age, domain=domain, session_id=f'{user_name}_{partner_name}_{age}_{domain}', log_file_path=None)