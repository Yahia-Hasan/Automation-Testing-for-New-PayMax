import sys
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.legacy_login_page import LegacyLoginPage

sys.stdout.reconfigure(encoding='utf-8')

options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
options.set_capability('acceptInsecureCerts', True)
driver = webdriver.Chrome(options=options)
try:
    LegacyLoginPage(driver).login_full_flow()
    driver.get('https://196.218.246.250:4040/reception')
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, "[data-test-id='patient-data-search-input']").send_keys('30854')
    time.sleep(2)
    items = driver.find_elements(By.CSS_SELECTOR, '.search-dropdown .search-item')
    if items:
        items[0].click()
        time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for b in soup.find_all(['button', 'a']):
        txt = b.get_text(strip=True)
        if txt and any(k in txt for k in ['حجز', 'دخول', 'عيادات', 'طوارئ', 'إسعاف', 'زيارة', 'أجندة']):
            print('Action item:', txt, b.attrs)
finally:
    driver.quit()
