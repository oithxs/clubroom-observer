from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import os
import time
from my_module import operate_sqlite3 as sql

sql.create_DB()

pre_entering_mac = ["23:FB:32:BD:AD:DA","BC:24:11:32:F4:1E"]

#デバッグ用
#sql.add_user("CC:E1:D5:79:29:24", "佐藤さん")

def close_webdriver(driver): # webdriverを終了する
    driver.close()
    driver.quit()

def get_macaddress(driver): # macアドレスを取得する
    #MACアドレスを取得
    global pre_entering_mac
    driver.find_element(By.ID, value="map_wireless").click() # 本番はこっちを使う
    # driver.find_element(By.ID, value="map_wire").click()
    time.sleep(2)
    macaddrs = driver.find_elements(by=By.XPATH, value="//*[@id='bodyWlStat']/tr/td[4]")
    # macaddrs = driver.find_elements(by=By.XPATH, value="//*[@id='bodyWireStat']/tr/td[4]")

    now_entering_mac = [elem.text for elem in macaddrs]
    enter_users = [sql.search_user(mac) for mac in list(set(now_entering_mac) - set(pre_entering_mac)) if sql.search_user(mac) is not None]
    leave_users = [sql.search_user(mac) for mac in list(set(pre_entering_mac) - set(now_entering_mac)) if sql.search_user(mac) is not None]

    enter_txt_url = os.environ["ENTER_TXT_URL"]
    leave_txt_url = os.environ["LEAVE_TXT_URL"]

    with open(enter_txt_url,"w",encoding="utf-8") as f_E:
        for user in enter_users:
            print("追記", user)
            f_E.write(user)
            f_E.write("\r")

    with open(leave_txt_url,"w",encoding="utf-8") as f_L:
        for user in leave_users:
            f_L.write(user)
            f_L.write("\r")

    pre_entering_mac = list(now_entering_mac)
    return pre_entering_mac

def login_router(driver): # TP-Linkのログイン画面の処理
    driver.get(os.environ["TABLE_URL"])
    text_box = driver.find_element(by=By.ID, value="pc-login-password")
    button = driver.find_element(By.ID, value="pc-login-btn")
    text_box.send_keys(os.environ["TABLE_PASS"])
    button.click()

    #ポップアップが出たときの処理
    try:
        driver.find_element(by=By.ID, value="confirm-yes").click()
    except StaleElementReferenceException:
        pass

def execute_webdriver(): # webdriverを起動する
    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
        command_executor = os.environ["SELENIUM_URL"],
        options = options
    )
    driver.implicitly_wait(5)

    return driver

if __name__ == "__main__":

    driver = execute_webdriver()
    try:
        login_router(driver)
    except:
        print("ログインに失敗しました")
    else:
        while True:
            try:
                maclist = get_macaddress(driver)

            except NoSuchElementException:
                try:
                    login_router(driver)
                except:
                    print("ログインに失敗しました")

            except KeyboardInterrupt:
                break
            else:
                for elem in maclist:
                    print(elem)
                print()
                # 本番は58程度に設定
                time.sleep(18)
                driver.refresh()
    finally:
        close_webdriver(driver)