from selenium import webdriver
from selenium.webdriver.common.by import By
import config

options = webdriver.ChromeOptions()
options.add_argument("--force-device-scale-factor=0.5")
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.implicitly_wait(5)

driver.get(config.TPLINK_URL)

#ログイン処理
text_box = driver.find_element(by=By.ID, value="pc-login-password")
button = driver.find_element(By.ID, value="pc-login-btn")
text_box.send_keys(config.TPLINK_PASSWD)
button.click()

#MACアドレスを取得
# driver.find_element(By.ID, value="map_wireless").click()
driver.find_element(By.ID, value="map_wire").click()
macaddr = driver.find_elements(by=By.XPATH, value="//*[@id='bodyWireStat']/tr/td[4]")

for elem in macaddr:
    print(elem.text)

driver.quit()