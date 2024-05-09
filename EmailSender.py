import os
import glob
import json
import smtplib
import streamlit as st
from smtplib import SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

try:
    st_key = st.secrets['GMAIL_API_KEY']
    api_key = ''
    for i in range(len(st_key)):
        if i > len(st_key) - 4:
            break
        if i % 4 == 0:
            api_key += (f'{st_key[i:i + 4]} ')
    api_key = api_key.strip()

except:
    with open('api_key.json') as secrets:
        api_key = json.load(secrets)['GMAIL_API_KEY']

class EmailSender:
    def __init__(self):
        pass
    def send(self) -> None:
        '''
        Sends email
        :return: None
        '''
        gmail_user = 'volvstang@gmail.com'
        gmail_pw = api_key

        mail_from = gmail_user
        mail_to = 'volvstang@gmail.com'

        mail_subject = f'chat_logs'
        mail_message_body = f'Check the attachments'

        msg = MIMEMultipart()
        msg['Subject'] = mail_subject
        msg['From'] = mail_from
        msg['To'] = mail_to

        msg.attach(MIMEText(mail_message_body, 'plain'))

        if os.path.exists('./logs'):
            files = glob.glob('./logs/*.json')

            for file in files:
                with open(file, 'r') as f:
                    attach = MIMEApplication(f.read(),_subtype='json')
                    filename = os.path.basename(file)
                    attach.add_header('Content-Disposition','attachment',
                                      filename=filename, encoding='utf-8',
                                      )
                    msg.attach(attach)

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(gmail_user, gmail_pw)
            server.sendmail(mail_from, mail_to, msg.as_string())
            server.close()
        except SMTPException as e:
            pass