import time
import sys
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# 크롬 실행
chromeDriver = '/Users/kakao/IdeaProjects/shopping-spec/selenium-driver/chromedriver/mac64/chromedriver'
driver = webdriver.Chrome(chromeDriver)
timeout = 10

# 로그인 페이지 접근
# 테스트
# productId = '10340218'
# 동숲
productId = '10573631'
kakao_login_url = 'https://accounts.kakao.com/login?continue=https%3A%2F%2Fkauth.kakao.com%2Foauth%2Fauthorize' \
                  '%3Fclient_id%3D4624f8fb02481684529f7bf484e29ba7%26redirect_uri%3Dhttps%3A%2F%2Fwww' \
                  '.shinsegaetvshopping.com%2Fmember%2FkakaoLoginCallback%26response_type%3Dcode%26state%3DforwardUrl' \
                  '%257C%252Fdisplay%252Fdetail%252F' + productId + '%252Ctype%257C%252CnonOrderYn%257CN '
driver.get(kakao_login_url)
driver.implicitly_wait(timeout)

# 로그인
driver.find_element_by_id('id_email_2').send_keys(sys.argv[1])
driver.find_element_by_id('id_password_3').send_keys(sys.argv[2])
driver.find_element_by_class_name('btn_confirm').click()

# 첫 번째 페이지 로딩 - '구매하기' 버튼 노출 떄까지 기다림
first_page_present = EC.presence_of_element_located((By.CLASS_NAME, 'direct_options_wrap_0'))
WebDriverWait(driver, timeout).until(first_page_present)
time.sleep(3)


def not_exist_order_button():
    try:
        driver.find_element_by_class_name('button_order')
    except NoSuchElementException:
        return True
    return False


count = 0
compare_price = 400000
target_price = 300000
while not_exist_order_button() or not driver.find_element_by_class_name('button_order').is_displayed():
    driver.refresh()
    while_page_present = EC.presence_of_element_located((By.CLASS_NAME, 'direct_options_wrap_0'))
    WebDriverWait(driver, timeout).until(while_page_present)
    # sleep & 화면로딩 후 진행
    price_str = driver.find_element_by_css_selector('.div-best > ._bestPrice').text
    if price_str is not None:
        price = price_str.replace(",", "").replace("원", "")
        print(str(count) + '. 가격 ' + price + '원 : ' + str(datetime.now()))
        target_price = int(price)
    else:
        print(str(count) + '. (가격 못구함) : ' + str(datetime.now()))
    count += 1

# 구매하기 버튼 노출됨
print('**** 구매 버튼 활성화 진행 ****')
driver.find_element_by_class_name('button_order').click()
driver.implicitly_wait(timeout)

# 주문서 진입
second_page_present = EC.presence_of_element_located((By.CSS_SELECTOR, '.order-save-button > .button-submit'))
WebDriverWait(driver, timeout).until(second_page_present)

# 결제 진행
driver.find_element_by_id('buyAgree2').click()
driver.find_element_by_css_selector('.order-save-button > .button-submit').click()
driver.implicitly_wait(timeout)

# 무통장 입금 선택
driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
driver.implicitly_wait(target_price)
all_term_check = driver.find_element_by_id('all_terms')
driver.execute_script("arguments[0].click();", all_term_check)

iframe_next = EC.presence_of_element_located((By.CSS_SELECTOR, '#footer > .btnNext'))
WebDriverWait(driver, timeout).until(iframe_next)
woori_bank = driver.find_element_by_id('bank4')
driver.execute_script("arguments[0].click();", woori_bank)
next_btn = driver.find_element_by_css_selector('#footer > .btnNext')
driver.execute_script("arguments[0].click();", next_btn)

iframe_complete = EC.presence_of_element_located((By.CSS_SELECTOR, '#footer > .btnComplete'))
WebDriverWait(driver, timeout).until(iframe_complete)
driver.find_element_by_id('ReceiptTypeNo').send_keys('01027476516')
confirm_check = driver.find_element_by_id('cofrm')
driver.execute_script("arguments[0].click();", confirm_check)
complete_btn = driver.find_element_by_css_selector('#footer > .btnComplete')
driver.execute_script("arguments[0].click();", complete_btn)

