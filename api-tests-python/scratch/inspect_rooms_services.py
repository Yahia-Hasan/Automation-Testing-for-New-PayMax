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
driver.set_window_size(1440, 1000)

try:
    LegacyLoginPage(driver).login_full_flow()
    driver.get('https://196.218.246.250:4040/waiting-list/accomodation-rooms')
    time.sleep(4)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Look for any button or icon with tooltip/text related to 'خدمات' or 'service'
    matches = []
    for b in soup.find_all(['button', 'a', 'i', 'span']):
        txt = b.get_text(strip=True)
        title = b.get('title', '')
        dt = b.get('data-test-id', '')
        href = b.get('href', '')
        full_str = f"{txt} {title} {dt} {href}".lower()
        if 'خدمات' in full_str or 'service' in full_str:
            matches.append((b.name, txt, title, dt, href, b.get('class')))

    print(f"Total matching elements: {len(matches)}")
    for m in matches:
        print("Match:", m)

    # Let's also look at all data-test-ids on the accomodation-rooms page
    dts = [el.get('data-test-id') for el in soup.find_all(attrs={'data-test-id': True})]
    print("All data-test-ids on rooms page:", list(dict.fromkeys(dts)))

finally:
    driver.quit()
