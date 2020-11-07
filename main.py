import cam.camout as cam
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from chat_functions import chat_bot
import threading
from speech_stream_to_text import SpeechStream
from time import sleep

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms



def main():
    # Browser manipulation settings
    # url = input("Paste Zoom URL:\n")
    # driver = webdriver.Chrome('./chromedriver')
    # driver.get(url)    

    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    #Change chrome driver path accordingly
    chrome_driver = './chromedriver'
    driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)
    print(driver.title)

    input('Continue?')

    # Speech to text recognition thread and settings
    keywords = ['Martin', 'Quiz', 'Dragonhack']
    keyword_used = {k: False for k in keywords}
    keywords = [s.lower() for s in keywords]
    speech_to_text = SpeechStream(RATE, CHUNK, keywords)
    speech_to_text_worker = threading.Thread(target=speech_to_text.code_driver)
    speech_to_text_worker.start()

    # Video feed thread
    t = threading.Thread(target=cam.start)
    t.start()

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

        # Chat bot integration
        chat_bot(driver)


if __name__ == '__main__':
    main()