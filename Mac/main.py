from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import time

url = "https://www.google.com"
keyword = "スクレイピング"

driver = webdriver.Remote(
    command_executor = os.environ["SELENIUM_URL"],
    options = webdriver.ChromeOptions()
)

driver.implicitly_wait(10)

driver.get(url)
driver.find_element(By.NAME, "q").send_keys(keyword + Keys.RETURN)

time.sleep(5)
driver.quit()
