import time
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# 크롬 실행
chromeDriver = '/Users/kakao/IdeaProjects/shopping-spec/selenium-driver/chromedriver/mac64/chromedriver'
driver = webdriver.Chrome(chromeDriver)
timeout = 10

# 로그인 페이지 접근
buy_url = 'http://m.coupang.com/vm/products/1384804427?vendorItemId=70413795361'
login_url = 'https://login.coupang.com/login/m/login.pang?rtnUrl='+buy_url
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
print(not driver.find_element_by_class_name('gobuy').is_displayed())

while not driver.find_element_by_class_name('gobuy').is_displayed():
    time.sleep(6)
    driver.refresh()
    while_page_present = EC.presence_of_element_located((By.ID, 'bottomMenu'))
    WebDriverWait(driver, timeout).until(while_page_present)
    time.sleep(4)
    print(not driver.find_element_by_class_name('gobuy').is_displayed())

# 구매하기 버튼 노출됨
driver.find_element_by_class_name('close-banner').click()
driver.find_element_by_class_name('gobuy').click()

# 주문서 진입
driver.implicitly_wait(timeout)
second_page_present = EC.presence_of_element_located((By.ID, 'agreement-of-card-agreements'))
WebDriverWait(driver, timeout).until(second_page_present)

# 결제 진행
driver.find_element_by_id('agreement-of-card-agreements').click()
driver.find_element_by_id('paymentBtn').click()
driver.implicitly_wait(timeout)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
