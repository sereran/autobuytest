# coding=utf-8
import time
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# 크롬 실행
chromeDriver = '/Users/kakao/IdeaProjects/shopping-spec/selenium-driver/chromedriver/mac64/chromedriver'
# chromeDriver = '/Users/dooboo/IdeaProjects/sereran/autobuy/venv/chromedriver80'
driver = webdriver.Chrome(chromeDriver)
timeout = 4

# 로그인 페이지 접근
dealUrl = '810158162'
login_url = 'https://login.tmon.co.kr/user/loginform?return_url=http%3A%2F%2Ftmon.co.kr%2Fdeal%2F' + dealUrl
driver.get(login_url)
driver.implicitly_wait(timeout)

# 로그인
driver.find_element_by_id('userid').send_keys(sys.argv[1])
driver.find_element_by_id('pwd').send_keys(sys.argv[2])
driver.find_element_by_class_name('btn_login').click()
time.sleep(1)
# driver.find_element_by_class_name('_closeAllTimeAlert').click()
driver.find_element_by_css_selector('.layer_time_box > ._closeAllTimeAlert').click()

# 첫 번째 페이지 로딩 - '구매하기' 버튼 노출 떄까지 기다림
driver.implicitly_wait(timeout)

try:
    while driver.find_element_by_id('view-error').is_displayed():
        driver.refresh()
        driver.implicitly_wait(timeout)
        time.sleep(1)
        print('에러페이지')
except Exception:
    print('통과')

isEnable = False
try:
    first_page_present = EC.presence_of_element_located((By.CSS_SELECTOR, '.deal_topinfo div[data-name="prchDepSelWrap0"] > button.tit'))
    WebDriverWait(driver, timeout).until(first_page_present)
    driver.find_element_by_css_selector('.deal_topinfo div[data-name="prchDepSelWrap0"] > button.tit').click()
    isEnable = driver.find_element_by_css_selector('.deal_topinfo div[data-name="prchDepSelWrap0"] > .purchase_selector > li > button[data-index="128"]').is_enabled()
except Exception:
    isEnable = False

count = 0
# 동숲
# firstOptionIndex = '128' #동숲
# firstOptionIndex = '58' # 테스
while not isEnable:
    driver.refresh()
    try:
        while driver.find_element_by_id('view-error').is_displayed():
            driver.refresh()
            driver.implicitly_wait(timeout)
            time.sleep(1)
            print('에러페이지')
        while_page_present = EC.presence_of_element_located((By.CSS_SELECTOR, '.deal_topinfo div[data-name="prchDepSelWrap0"] > button.tit'))
        WebDriverWait(driver, timeout).until(while_page_present)
        driver.find_element_by_css_selector('.deal_topinfo div[data-name="prchDepSelWrap0"] > button.tit').click()
        isEnable = driver.find_element_by_css_selector('.deal_topinfo div[data-name="prchDepSelWrap0"] > .purchase_selector > li > button[data-index="128"]').is_enabled()
    except Exception:
        isEnable = False

    # sleep & 화면로딩 후 진행
    print(str(count) + '. ' + str(datetime.now()))
    count += 1

# 구매하기 버튼 노출됨
print('**** 구매 버튼 활성화 진행 ****')
# firstOptionIndex = '128' # 동숲
# secondOptionDealNo = '3312057882'
# firstOptionIndex = '58' # 테스트
# secondOptionDealNo = '2269941786'
driver.find_element_by_css_selector('.deal_topinfo div[data-name="prchDepSelWrap0"] > .purchase_selector > li > button[data-index="128"]').click()
driver.find_element_by_css_selector('.deal_topinfo div[data-name="prchDepSelWrap1"] > .purchase_selector > li[data-optionno="3312057882"] > button[data-dealno="3312057882"]').click()
driver.find_element_by_css_selector('.deal_topinfo > .hasItem .purchase_list_box button[data-type="buyNow"]').click()
driver.implicitly_wait(timeout)

# 주문서 진입
while_page_present = EC.presence_of_element_located((By.CSS_SELECTOR, '.checkout_wrap > .checkout_content > .pay_section > .agree ._terms_total_checkbox'))
WebDriverWait(driver, timeout).until(while_page_present)

# 결제 진행
driver.find_element_by_css_selector('.checkout_wrap > .checkout_content > .pay_section > .agree .checkBoxAll').click()  # 품절시 환불 방법
driver.find_element_by_id('_confirmCheckout').click()

