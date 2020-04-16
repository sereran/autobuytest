# coding=utf-8
import time
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException

# 크롬 실행
chromeDriver = '/Users/kakao/IdeaProjects/shopping-spec/selenium-driver/chromedriver/mac64/chromedriver'
# chromeDriver = '/Users/dooboo/IdeaProjects/sereran/autobuy/venv/chromedriver80'
driver = webdriver.Chrome(chromeDriver)
timeout = 10

# 로그인 페이지 접근
login_url = 'http://embuy.co.kr/member/login.html'
driver.get(login_url)
driver.implicitly_wait(timeout)

# 수동 로그인
driver.find_element_by_css_selector('div.login > fieldset > label.id > input#member_id').send_keys(sys.argv[1])
driver.find_element_by_css_selector('div.login > fieldset > label.password > input#member_passwd').send_keys(sys.argv[2])
driver.find_element_by_css_selector('div.login > fieldset > a > img[alt="로그인"]').click()

driver.implicitly_wait(timeout)
time.sleep(2)

# 대상
product_no = '1418'
product_url = 'http://www.embuy.co.kr/product/detail.html?product_no=' + product_no
driver.get(product_url)

# 에러페이지 존재 여부
def exist_warn():
    try:
        driver.implicitly_wait(0)
        warn = driver.find_elements_by_xpath('/html/body[@id="warn"]')
        return len(warn) > 0
    except Exception:
        return False

# warn 페이지 있으면 refresh
try:
    while exist_warn():
        print('에러페이지 존재')
        driver.refresh()
finally:
    print('에러페이지 발견 안되서 넘어감')
    driver.implicitly_wait(timeout)


# 상품상세 진입
count = 0

# 첫 번째 페이지 로딩 - '구매하기' 버튼 노출 떄까지 기다림
first_page_present = EC.presence_of_element_located((By.ID, 'totalProducts'))
WebDriverWait(driver, timeout).until(first_page_present)

def not_exist_order_button():
    try:
        driver.find_element_by_css_selector('div.btnArea > a.first')
    except NoSuchElementException:
        return True
    return False

while not_exist_order_button() or not driver.find_element_by_css_selector('div.btnArea > a.first').is_displayed():
    driver.refresh()
    while_page_present = EC.presence_of_element_located((By.ID, 'totalProducts'))
    WebDriverWait(driver, timeout).until(while_page_present)
    # sleep & 화면로딩 후 진행
    count += 1


driver.find_element_by_css_selector('div.btnArea > a.first').click()
driver.implicitly_wait(timeout)


# 구매하기 버튼 노출됨 - 무통장입금
print('**** 구매 버튼 활성화 진행 ****')

# 주문서 진입
try:
    try:
        # html = driver.page_source
        pay_method = driver.find_element_by_css_selector('div.payArea > div.payment > div.method > span.ec-base-label > input#addr_paymethod2')
        driver.execute_script("arguments[0].click();", pay_method)
    except UnexpectedAlertPresentException:
        print('alertException 떴다..')
        alert = driver.switch_to.alert
        alert.accept()
        pay_method = driver.find_element_by_css_selector('div.payArea > div.payment > div.method > span.ec-base-label > input#addr_paymethod2')
        driver.execute_script("arguments[0].click();", pay_method)
except UnexpectedAlertPresentException:
    print('alertException 또 떴다..')
    alert = driver.switch_to.alert
    alert.accept()
    pay_method = driver.find_element_by_css_selector('div.payArea > div.payment > div.method > span.ec-base-label > input#addr_paymethod2')
    driver.execute_script("arguments[0].click();", pay_method)


driver.find_element_by_id('pname').send_keys('염세란')

select = Select(driver.find_element_by_id('bankaccount'))
select_target = driver.find_element_by_css_selector('table#payment_input_cash > tbody > tr > td > select#bankaccount > option:nth-child(2)')
select_value = select_target.get_attribute('value')
select.select_by_value(select_value)
print('value : '+ select_value)

select_text = select_target.get_attribute('text')
select.select_by_visible_text(select_text)
print('text : '+ select_text)

agree_btn = driver.find_element_by_id('chk_purchase_agreement0')
driver.execute_script("arguments[0].click();", agree_btn)
payment_btn = driver.find_element_by_id('btn_payment')
driver.execute_script("arguments[0].click();", payment_btn)
