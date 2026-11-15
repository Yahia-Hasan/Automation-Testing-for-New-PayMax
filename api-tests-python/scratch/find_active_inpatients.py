import sys
import os
sys.path.insert(0, os.path.abspath("."))
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pages.legacy_login_page import LegacyLoginPage

sys.stdout.reconfigure(encoding='utf-8')

options = Options()
options.add_argument("--headless=new")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-insecure-localhost")
options.add_argument("--disable-web-security")
options.add_argument("--start-maximized")
options.set_capability("acceptInsecureCerts", True)

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

try:
    print("[1] Logging in...")
    login_page = LegacyLoginPage(driver)
    login_page.login_full_flow("sysadmin", "Ma3an2025", "Ad Doqi")
    print("Logged in!")

    print("[2] Opening /reception/inpatients...")
    driver.get("https://196.218.246.250:4040/reception/inpatients")
    time.sleep(3)
    driver.save_screenshot("scratch/inpatients_list.png")

    rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
    print(f"Total rows found in inpatients table: {len(rows)}")

    for i, r in enumerate(rows[:5], 1):
        links = r.find_elements(By.TAG_NAME, "a")
        link_hrefs = [l.get_attribute("href") for l in links if l.get_attribute("href")]
        buttons = r.find_elements(By.TAG_NAME, "button")
        btn_texts = [b.text.strip() for b in buttons if b.text.strip()]
        print(f"Row {i}: text='{r.text.strip()[:40]}' | links={link_hrefs[:2]} | buttons={btn_texts}")

finally:
    driver.quit()
