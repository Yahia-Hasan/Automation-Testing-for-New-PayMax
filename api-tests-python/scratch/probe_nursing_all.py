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

urls = [
    ("Patient Diets List", f"{BASE_URL}/waiting-list/patient-diets-list", "[data-test-id='patient-diets-list-show-btn']"),
    ("Attendant Diets List", f"{BASE_URL}/waiting-list/attendant-diets", "[data-test-id='attendant-diets-refresh-btn']"),
    ("Medical Reports", f"{BASE_URL}/waiting-list/medical-reports", "[data-test-id='medical-reports-show-btn']"),
    ("Patient Diet Order", f"{BASE_URL}/waiting-list/patient-diet?ReservID={RESERV_ID}&AccomID={ACCOM_ID}&typ=1&flag=Durgs", "[data-test-id='patient-diet-save-btn']"),
    ("Patient Rays Order", f"{BASE_URL}/waiting-list/patient-rays?ReservID={RESERV_ID}&AccomID={ACCOM_ID}&typ=1", "[data-test-id='patient-ipd-typed-save-btn']"),
    ("Patient Tests Order", f"{BASE_URL}/waiting-list/patient-tests?ReservID={RESERV_ID}&AccomID={ACCOM_ID}&typ=1", "[data-test-id='patient-ipd-typed-save-btn']"),
    ("Charge Patient Med", f"{BASE_URL}/waiting-list/charge-patient-med?ReservID={RESERV_ID}&AccomID={ACCOM_ID}&typ=1", "[data-test-id='charge-patient-med-save-btn']"),
    ("Request Patient Med", f"{BASE_URL}/waiting-list/patient-request-med?ReservID={RESERV_ID}&AccomID={ACCOM_ID}&typ=1&flag=All", "[data-test-id='patient-request-med-save-btn']"),
    ("Patient Blood Bank", f"{BASE_URL}/waiting-list/patient-blood?ReservID={RESERV_ID}&AccomID={ACCOM_ID}&typ=1&flag=Durgs", "[data-test-id='patient-blood-save-btn']"),
    ("Internal Devices", f"{BASE_URL}/waiting-list/patient-internal-devices?ReservID={RESERV_ID}&AccomID={ACCOM_ID}&typ=1&flag=Durgs", "[data-test-id='patient-internal-devices-save-btn']"),
]

try:
    print("[1] Logging in...")
    login_page = LegacyLoginPage(driver)
    login_page.login_full_flow("sysadmin", "Ma3an2025", "Ad Doqi")
    print("Logged in successfully!\n")

    for name, url, btn_selector in urls:
        driver.get(url)
        time.sleep(1.5)
        elements = driver.find_elements(By.CSS_SELECTOR, btn_selector)
        if elements:
            btn = elements[0]
            is_dis = btn.get_attribute('disabled')
            btn_class = btn.get_attribute('class') or ''
            btn_text = btn.text.strip().replace('\n', ' ')
            print(f"[{name}] Found button '{btn_text}' | disabled={is_dis} | class='{btn_class}'")
            
            # Spam click 5 times
            script = """
                let btn = arguments[0];
                let states = [];
                for(let i=0; i<5; i++) {
                    let b = btn.disabled || btn.hasAttribute('disabled') || btn.classList.contains('disabled');
                    try { btn.click(); } catch(e) {}
                    let a = btn.disabled || btn.hasAttribute('disabled') || btn.classList.contains('disabled');
                    states.push({click: i+1, before: b, after: a});
                }
                return states;
            """
            states = driver.execute_script(script, btn)
            entered_dis = any(s['after'] for s in states)
            toasts = driver.find_elements(By.CSS_SELECTOR, ".toast-item, .toast-stack .msg, .toast-error-http-message")
            toast_count = len(toasts)
            print(f"       Spam results: entered_disabled={entered_dis} | toasts_spawned={toast_count}")
        else:
            print(f"[{name}] Button NOT found with selector: {btn_selector}")

finally:
    driver.quit()
