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
    driver.set_window_size(1440, 1000)
    LegacyLoginPage(driver).login_full_flow()
    driver.get('https://196.218.246.250:4040/reception/patient/30854/admission')
    time.sleep(3)

    tabs = [
        ("rooms", "patient-admission-rooms-tab-btn"),
        ("icu", "patient-admission-icu-tab-btn"),
        ("neonatal", "patient-admission-neonatal-tab-btn"),
        ("surgeries", "patient-admission-surgeries-tab-btn"),
        ("payments", "patient-admission-payments-tab-btn"),
    ]

    for name, tab_id in tabs:
        print(f"\n--- Clicking Tab: {name} ({tab_id}) ---")
        btn = driver.find_element(By.CSS_SELECTOR, f"[data-test-id='{tab_id}']")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(1.5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        dts = [el.get('data-test-id') for el in soup.find_all(attrs={'data-test-id': True}) if el.get('data-test-id') != 'global-toast-stack']
        tab_dts = [d for d in dts if name in d or 'room' in d or 'bed' in d or 'surgery' in d or 'payment' in d]
        print(f"Tab-specific data-test-ids for {name}:", tab_dts[:15])

finally:
    driver.quit()
