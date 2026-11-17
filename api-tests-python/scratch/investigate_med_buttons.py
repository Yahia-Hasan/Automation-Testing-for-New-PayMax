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

RESERV_ID = "CfDJ8KcUxlP3wTpIkfqEIRtHon4HnOXKri8R-HuwQbLe0ga8sPk_YDBIi7MkseBrAScp2lyLKLKWd1FdbV1bx5vDnm0EQBpbwWI9QcH-t-umVvqBT7aeI7evEqn6rXp7YK12Xw"
ACCOM_ID = "CfDJ8KcUxlP3wTpIkfqEIRtHon6il3dFRgAMVI2R9iXr9AJ77pgneSuKHembPpKo7Y-WpjJgcXZaxrE0K-9uaDSgCs91FGvLxq1k6a3P6tJrXLC-GEMPIyzikQYqlb2CbLezAg"
BASE_URL = "https://196.218.246.250:4040"

try:
    print("[1] Logging in...")
    login_page = LegacyLoginPage(driver)
    login_page.login_full_flow("sysadmin", "Ma3an2025", "Ad Doqi")
    print("Logged in!")

    # Let's inspect Charge Med
    charge_url = f"{BASE_URL}/waiting-list/charge-patient-med?ReservID={RESERV_ID}&AccomID={ACCOM_ID}&typ=1"
    print(f"\n[2] Navigating to: {charge_url}")
    driver.get(charge_url)
    time.sleep(3)
    driver.save_screenshot("scratch/charge_med_screen.png")
    print(f"Current URL: {driver.current_url}")
    print(f"Page Title: {driver.title}")

    # Inspect all buttons on this page
    buttons = driver.find_elements(By.TAG_NAME, "button")
    print(f"\nTotal buttons found on charge med screen: {len(buttons)}")
    for i, b in enumerate(buttons, 1):
        if b.is_displayed():
            t = b.text.strip().replace('\n', ' ')
            tid = b.get_attribute("data-test-id")
            dis = b.get_attribute("disabled")
            cls = b.get_attribute("class")
            print(f"  [{i:02d}] text='{t}' | test_id='{tid}' | disabled={dis} | class='{cls}'")

    # Let's also check Request Med
    req_url = f"{BASE_URL}/waiting-list/patient-request-med?ReservID={RESERV_ID}&AccomID={ACCOM_ID}&typ=1&flag=All"
    print(f"\n[3] Navigating to: {req_url}")
    driver.get(req_url)
    time.sleep(3)
    driver.save_screenshot("scratch/request_med_screen.png")
    print(f"Current URL: {driver.current_url}")
    
    req_buttons = driver.find_elements(By.TAG_NAME, "button")
    print(f"\nTotal buttons found on request med screen: {len(req_buttons)}")
    for i, b in enumerate(req_buttons, 1):
        if b.is_displayed():
            t = b.text.strip().replace('\n', ' ')
            tid = b.get_attribute("data-test-id")
            dis = b.get_attribute("disabled")
            cls = b.get_attribute("class")
            print(f"  [{i:02d}] text='{t}' | test_id='{tid}' | disabled={dis} | class='{cls}'")

finally:
    driver.quit()
