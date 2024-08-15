from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import os
import time

url = "http://150.89.253.11/"
tplink_passwd = "takakun"

driver = webdriver.Remote(
    command_executor = os.environ["SELENIUM_URL"],
    options = webdriver.ChromeOptions()
)

driver.implicitly_wait(5)

try:
    driver.get(url)

except WebDriverException:
    driver.close()
    driver.quit()

else:
    time.sleep(5)
    driver.close()
    driver.quit()
