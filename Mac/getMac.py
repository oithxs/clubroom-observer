from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, StaleElementReferenceException
import os
import time

def get_macaddress():
    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
        command_executor = os.environ["SELENIUM_URL"],
        options = options
    )

    driver.implicitly_wait(5)

    try:
        driver.get(os.environ["TABLE_URL"])

    except WebDriverException:
        driver.close()
        driver.quit()

    else:
        text_box = driver.find_element(by=By.ID, value="pc-login-password")
        button = driver.find_element(By.ID, value="pc-login-btn")
        text_box.send_keys(os.environ["TABLE_PASS"])
        button.click()

        #ポップアップが出たときの処理
        try:
            driver.find_element(by=By.ID, value="confirm-yes").click()
        except StaleElementReferenceException:
            pass
        finally:
            #MACアドレスを取得
            # driver.find_element(By.ID, value="map_wireless").click() # 本番はこっちを使う
            driver.find_element(By.ID, value="map_wire").click()
            time.sleep(2)
            macaddrs = driver.find_elements(by=By.XPATH, value="//*[@id='bodyWireStat']/tr/td[4]")
            macaddrs = [elem.text for elem in macaddrs]

            driver.close()
            driver.quit()
            return macaddrs

if __name__ == "__main__":
    maclist = get_macaddress()
    for elem in maclist:
        print(elem)