import sys
from selenium import webdriver
from time import sleep
from chat_functions import chat_bot
import threading
import camout

videoservice = VideoService()
videoservice.start()
while True:
    print(x)
exit()

driver = webdriver.Chrome('./chromedriver')

url = input("paste zoom url:\n")
driver.get(url)

if input("ready?"):
    while True:
        chat_bot(driver)

# text = input("Quit?")
# driver.quit()
