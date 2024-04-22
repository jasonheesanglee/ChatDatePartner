from .ChatBot import ChatBot
from datetime import datetime

current_time = str(datetime.now().time()).replace(':', '')

chatbot = ChatBot(name='오해원', sex='female', age='26', domain='실용음악학과', session_id=current_time, log_file_path=None)

if __name__ == '__main__':
    chatbot.chat()
