# coding=utf-8
import time
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# 크롬 실행
# chromeDriver = '/Users/kakao/IdeaProjects/shopping-spec/selenium-driver/chromedriver/mac64/chromedriver'
chromeDriver = '/Users/dooboo/IdeaProjects/sereran/autobuy/venv/chromedriver80'
driver = webdriver.Chrome(chromeDriver)
timeout = 10

# 로그인 페이지 접근
vendor_item_id = '70413795361'
buy_url = 'http://m.coupang.com/vm/products/1384804427?vendorItemId=' + vendor_item_id
login_url = 'https://login.coupang.com/login/m/login.pang?rtnUrl=' + buy_url
driver.get(login_url)
driver.implicitly_wait(timeout)

# 로그인
driver.find_element_by_id('login-email-input').send_keys(sys.argv[1])
driver.find_element_by_id('login-password-input').send_keys(sys.argv[2])
driver.find_element_by_class_name('_loginSubmitButton').click()

# 첫 번째 페이지 로딩 - '구매하기' 버튼 노출 떄까지 기다림
first_page_present = EC.presence_of_element_located((By.ID, 'bottomMenu'))
WebDriverWait(driver, timeout).until(first_page_present)
time.sleep(3)

count = 0
compare_price = 400000
target_price = 300000
isEnable = False
try:
    isEnable = driver.find_element_by_class_name('gobuy').is_displayed()
except Exception:
    isEnable = False


while target_price > compare_price or not isEnable:
    try:
        time.sleep(1)
        driver.refresh()
        driver.implicitly_wait(timeout)
        while_page_present = EC.presence_of_element_located((By.ID, 'bottomMenu'))
        WebDriverWait(driver, timeout).until(while_page_present)
        # sleep & 화면로딩 후 진행
        price_str = driver.find_element_by_css_selector('#product-info > .price > .sales').text
        if price_str is not None:
            price = price_str.replace(",", "").replace("원", "")
            print(str(count) + '. 가격 ' + price + '원 : ' + str(datetime.now()))
            target_price = int(price)
        else:
            print(str(count) + '. (가격 못구함) : ' + str(datetime.now()))
        count += 1
        isEnable = driver.find_element_by_class_name('gobuy').is_displayed()
    except Exception:
        print('ㅇㅔ러 발생')
        isEnable = False


# 구매하기 버튼 노출됨
print('**** 구매 버튼 활성화 진행 ****')
driver.find_element_by_class_name('close-banner').click()
driver.find_element_by_class_name('gobuy').click()
driver.implicitly_wait(timeout)

# 주문서 진입
second_page_present = EC.presence_of_element_located((By.ID, 'agreement-of-card-agreements'))
WebDriverWait(driver, timeout).until(second_page_present)

# 결제 진행
driver.find_element_by_id('agreement-of-card-agreements').click()
driver.find_element_by_id('paymentBtn').click()
driver.implicitly_wait(timeout)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
