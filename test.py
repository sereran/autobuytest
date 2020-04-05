import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

chromeDriver = '/Users/kakao/IdeaProjects/shopping-spec/selenium-driver/chromedriver80/mac64/chromedriver80'
driver = webdriver.Chrome(chromeDriver)
timeout = 10

driver.get('http://m.coupang.com/vm/products/1384804427?vendorItemId=70413795361')
driver.implicitly_wait(timeout)
second_page_present = EC.presence_of_element_located((By.ID, 'bottomMenu'))
WebDriverWait(driver, timeout).until(second_page_present)
print(not driver.find_element_by_class_name('gobuy').is_displayed())
time.sleep(2)
price_str = driver.find_element_by_css_selector('#product-info > .price > .sales').text
if price_str is not None:
    print(price_str)
    price = price_str.replace(",", "").replace("원", "")
    print(price)
    if int(price) > 800000:
        print('30만원보다 큼')
    else:
        print('30만원보다 작음')
else:
    print(price_str)

print('끝')



