from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import os
import time

url = "http://150.89.253.11/"
tplink_passwd = "takakun"

options = webdriver.ChromeOptions()
# options.add_argument("--force-device-scale-factor=0.5")
driver = webdriver.Remote(
    command_executor = os.environ["SELENIUM_URL"],
    options = options
)

driver.implicitly_wait(5)

try:
    driver.get(url)

except WebDriverException:
    driver.close()
    driver.quit()

else:
    text_box = driver.find_element(by=By.ID, value="pc-login-password")
    button = driver.find_element(By.ID, value="pc-login-btn")
    text_box.send_keys(tplink_passwd)
    button.click()

    #MACアドレスを取得
    # driver.find_element(By.ID, value="map_wireless").click()
    driver.find_element(By.ID, value="map_wire").click()
    macaddr = driver.find_elements(by=By.XPATH, value="//*[@id='bodyWireStat']/tr/td[4]")

    for elem in macaddr:
        print(elem.text)

    time.sleep(3)
    driver.close()
    driver.quit()
