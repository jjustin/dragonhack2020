import sys
from selenium import webdriver
from time import sleep


zoom_url = "https://uni-lj-si.zoom.us/j/91203158907?pwd=L2VDTjJlMDhuUjRtaUxEQ2tBUVQrdz09"
driver = webdriver.Chrome('./chromedriver')

driver.get(zoom_url)
sleep(3)

driver.find_element_by_link_text("Join from Your Browser").click()


# driver.quit()


