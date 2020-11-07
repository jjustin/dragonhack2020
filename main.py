import cam.camout as cam
import sys
from selenium import webdriver
from chat_functions import chat_bot
import threading
from speech_stream_to_text import SpeechStream
from time import sleep

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

t = threading.Thread(target=cam.start)
t.start()

def main():
    keywords = ['people', 'efforts', 'election']
    keyword_used = {k: False for k in keywords}
    keywords = [s.lower() for s in keywords]
    speech_to_text = SpeechStream(RATE, CHUNK, keywords)
    speech_to_text_worker = threading.Thread(target=speech_to_text.code_driver)
    speech_to_text_worker.start()

    while True:
        # Keyword recognition for speech to text
        speech_to_text.get_keywords()
        keyword = speech_to_text.get_current_keyword()
        if keyword == 'people' and not keyword_used[keyword]:
            keyword_used[keyword] = True
            print('Totally listening to you!')
        elif keyword == 'efforts' and not keyword_used[keyword]:
            keyword_used[keyword] = True
            print('Hello efforts!')
        elif keyword == 'election' and not keyword_used[keyword]:
            keyword_used[keyword] = True
            print('Hello election')

if __name__ == '__main__':
    main()