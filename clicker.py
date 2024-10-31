import time
import os
import schedule
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException


load_dotenv()


options_chrome = webdriver.ChromeOptions()
options_chrome.add_argument('--headless')
options_chrome.add_argument('--log-level=3')


def raise_my_lots(cookies=None):
    browser = webdriver.Chrome(options=options_chrome)
    browser.implicitly_wait(10)

    def vk_authetification():
        browser.get("https://funpay.com/lots/612/trade")

        browser.find_element(By.CLASS_NAME, "social-vk").click()

        browser.find_element(By.XPATH, "//input[@placeholder='Телефон или почта']").send_keys(os.getenv("VK_PHONE_NUMBER"))

        browser.find_element(By.CSS_SELECTOR, "div.vkc__DefaultSkin__button > button").click()

        browser.find_element(By.XPATH, "//input[@name='password']").send_keys("VK_PASSWORD")

        browser.find_element(By.CSS_SELECTOR, ".vkuiButton__in").click()
        time.sleep(0.5)
        browser.find_element(By.XPATH, "//button[@type='submit']").click()

    try:
        if cookies is None:
            vk_authetification()

        else:
            browser.get("https://funpay.com/lots/612/trade")

            for cookie in cookies:
                browser.add_cookie(cookie)
            browser.refresh()

            browser.find_element(By.XPATH, "//a[@href='https://funpay.com/lots/612/']").click()

            browser.find_element(By.XPATH, "//div[@class='pull-right']/child::*").click()

        browser.find_element(By.CSS_SELECTOR, ".btn.btn-default.btn-block.js-lot-raise").click()
        
        auth_cookies = browser.get_cookies()
        print(browser.find_elements(By.ID, "site-message")[0].text)
        time.sleep(100)
    
    except TimeoutException:
        print("Сайт сейчас недоступен, попробуйте отправить запрос позже")
    
    except NoSuchElementException:
        print("Какой-то из элементов был не найден, возможно структура сайта изменилась или включен VPN")
    
    finally:
        browser.quit()
    
    if cookies is None:
        return auth_cookies


def main():
    cookies = raise_my_lots()

    schedule.every(4).hours.do(lambda: raise_my_lots(cookies))

    while True:
        schedule.run_pending()
        time.sleep(1)


main()
