from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, StaleElementReferenceException
import os
import time
from my_module import operate_sqlite3 as sql

sql.create_DB()

pre_entering_mac = ["23:FB:32:BD:AD:DA","BC:24:11:32:F4:1E"]

#デバッグ用
#sql.add_user("CC:E1:D5:79:29:24", "佐藤さん")
def get_macaddress():
    global pre_entering_mac
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

            now_entering_mac = [elem.text for elem in macaddrs]
            enter_user = [sql.search_user(mac) for mac in list(set(now_entering_mac) - set(pre_entering_mac)) if sql.search_user(mac) is not None]
            leave_user = [sql.search_user(mac) for mac in list(set(pre_entering_mac) - set(now_entering_mac)) if sql.search_user(mac) is not None]

            enter_txt_url = "enter.txt"
            leave_txt_url = "leave.txt"

            with open(enter_txt_url,"w",encoding="utf-8") as f_E:
                for user in enter_user:
                    f_E.write(user)
                    f_E.write("\r")

            with open(leave_txt_url,"w",encoding="utf-8") as f_L:
                for user in leave_user:
                    f_L.write(user)
                    f_L.write("\r")

            pre_entering_mac = list(now_entering_mac)
            driver.close()
            driver.quit()
            return pre_entering_mac

if __name__ == "__main__":
    maclist = get_macaddress()
    for elem in maclist:
        print(elem)