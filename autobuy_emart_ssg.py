# coding=utf-8
import time
import sys
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# 크롬 실행
# chromeDriver = '/Users/kakao/IdeaProjects/shopping-spec/selenium-driver/chromedriver/mac64/chromedriver'
chromeDriver = '/Users/dooboo/IdeaProjects/sereran/autobuy/venv/chromedriver80'
driver = webdriver.Chrome(chromeDriver)
timeout = 10

# 로그인 페이지 접근
# 테스트
# itemId = '1000036549208'
# 라이트 코럴
itemId = '1000043512191'
# 동숲
# itemId = '1000042290732'

ssh_login_url = 'https://member.ssg.com/member/login.ssg?retURL=http%3A%2F%2Fshinsegaemall.ssg.com%2Fitem%2FitemView.ssg%3FitemId%3D' + itemId
driver.get(ssh_login_url)
driver.implicitly_wait(timeout)

# 로그인
driver.find_element_by_id('mem_id').send_keys(sys.argv[1])
driver.find_element_by_id('mem_pw').send_keys(sys.argv[2])
driver.find_element_by_class_name('cmem_btn').click()

# 첫 번째 페이지 로딩 - '구매하기' 버튼 노출 떄까지 기다림
first_page_present = EC.presence_of_element_located((By.ID, 'oriCart'))
WebDriverWait(driver, timeout).until(first_page_present)


def not_exist_order_button():
    try:
        driver.find_element_by_id('actionPayment')
    except NoSuchElementException:
        return True
    return False


count = 0
compare_price = 400000
target_price = 300000
while not_exist_order_button() or not driver.find_element_by_id('actionPayment').is_displayed():
    driver.refresh()
    while_page_present = EC.presence_of_element_located((By.ID, 'oriCart'))
    WebDriverWait(driver, timeout).until(while_page_present)
    # sleep & 화면로딩 후 진행
    price_str = driver.find_element_by_id('totalPrc').text
    if price_str is not None:
        price = price_str.replace(",", "").replace("원", "")
        print(str(count) + '. 가격 ' + price + '원 : ' + str(datetime.now()))
        if price_str is not '':
            target_price = int(price)
    else:
        print(str(count) + '. (가격 못구함) : ' + str(datetime.now()))
    count += 1

# 구매하기 버튼 노출됨
print('**** 구매 버튼 활성화 진행 ****')
driver.find_element_by_id('actionPayment').click()
# driver.implicitly_wait(timeout)

# 주문서 진입
time.sleep(5)

# 결제 진행
driver.find_element_by_id('rfdMthdCd_10').click()  # 품절시 환불 방법
agreement_check = driver.find_element_by_id('chkPayAgreeAll1')  # 주문할 상품정보 동의
driver.execute_script("arguments[0].click();", agreement_check)
payment_btn = driver.find_element_by_css_selector('.codr_totalprice_area > .codr_btn_payment')
driver.execute_script("arguments[0].click();", payment_btn)

