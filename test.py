from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

chromeDriver = '/Users/kakao/IdeaProjects/shopping-spec/selenium-driver/chromedriver/mac64/chromedriver'
driver = webdriver.Chrome(chromeDriver)

driver.get('https://m.coupang.com/vm/products/115737923?vendorItemId=3847165103')
timeout = 10
driver.implicitly_wait(timeout)

# 다른 페이지 접근 대기 필요
first_page_present = EC.presence_of_element_located((By.ID, 'bottomMenu'))
WebDriverWait(driver, timeout).until(first_page_present)
print(not driver.find_element_by_class_name('gobuy').is_displayed())

driver.get('http://m.coupang.com/vm/products/1384804427?vendorItemId=70413795361')
second_page_present = EC.presence_of_element_located((By.ID, 'bottomMenu'))
WebDriverWait(driver, timeout).until(second_page_present)
print(not driver.find_element_by_class_name('gobuy').is_displayed())



