import sys
from selenium import webdriver
from time import sleep
from chat_functions import chat_bot


driver = webdriver.Chrome('./chromedriver')

url = input("paste zoom url:\n")
driver.get(url)

while True:
    chat_bot(driver)

# text = input("Quit?")
# driver.quit()
