import cam.camout as cam
import sys
from selenium import webdriver
from time import sleep
from chat_functions import chat_bot
import threading

t = threading.Thread(target=cam.start)
t.start()

driver = webdriver.Chrome('./chromedriver')

url = input("paste zoom url:\n")
driver.get(url)

if input("ready?"):
    while True:
        chat_bot(driver)

# text = input("Quit?")
# driver.quit()
