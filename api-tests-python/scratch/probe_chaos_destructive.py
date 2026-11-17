import sys
import os
sys.path.insert(0, os.path.abspath("."))
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pages.legacy_login_page import LegacyLoginPage
from pages.reception_page import ReceptionPage
from pages.physical_therapy_page import PhysicalTherapyWaitingListPage

sys.stdout.reconfigure(encoding='utf-8')

os.makedirs("screenshots/chaos_testing", exist_ok=True)

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
    print("[1] Logging into BayMax...")
    login_page = LegacyLoginPage(driver)
    login_page.login_full_flow("sysadmin", "Ma3an2025", "Ad Doqi")
    print("Logged in!")

    # -------------------------------------------------------------
    # 1. TEST TIME PARADOX: Future Birth Date (تاريخ ميلاد مستقبلي)
    # -------------------------------------------------------------
    print("\n[2] Testing Future Birth Date in Reception...")
    rec_page = ReceptionPage(driver).open()
    time.sleep(1)
    rec_page.click_new()
    time.sleep(0.5)

    birth_input = driver.find_element(By.CSS_SELECTOR, "[data-test-id='patient-data-birth-date-input']")
    age_years_input = driver.find_element(By.CSS_SELECTOR, "[data-test-id='patient-data-age-years-input']")
    age_months_input = driver.find_element(By.CSS_SELECTOR, "[data-test-id='patient-data-age-months-input']")

    # Try entering future date 2035-05-15
    birth_input.clear()
    birth_input.send_keys("05/15/2035")
    # Trigger change / blur event
    driver.execute_script("arguments[0].dispatchEvent(new Event('input')); arguments[0].dispatchEvent(new Event('change')); arguments[0].dispatchEvent(new Event('blur'));", birth_input)
    time.sleep(1)

    age_years_val = age_years_input.get_attribute("value")
    age_months_val = age_months_input.get_attribute("value")
    birth_val = birth_input.get_attribute("value")
    driver.save_screenshot("screenshots/chaos_testing/01_future_birth_date.png")
    
    print(f"  Birth Date input: '{birth_val}'")
    print(f"  Age Years calculated: '{age_years_val}'")
    print(f"  Age Months calculated: '{age_months_val}'")
    
    # Try ancient date: 01/01/1850
    birth_input.clear()
    birth_input.send_keys("01/01/1850")
    driver.execute_script("arguments[0].dispatchEvent(new Event('input')); arguments[0].dispatchEvent(new Event('change')); arguments[0].dispatchEvent(new Event('blur'));", birth_input)
    time.sleep(1)
    ancient_years = age_years_input.get_attribute("value")
    print(f"  Ancient date (1850) Age Years: '{ancient_years}'")
    driver.save_screenshot("screenshots/chaos_testing/02_ancient_birth_date.png")

    # -------------------------------------------------------------
    # 2. TEST REVERSED DATES: From Date > To Date in Physical Therapy
    # -------------------------------------------------------------
    print("\n[3] Testing Reversed Dates in Physical Therapy Waiting List...")
    pt_page = PhysicalTherapyWaitingListPage(driver).open()
    time.sleep(1)

    from_date_input = driver.find_element(*pt_page.INPUT_FROM_DATE)
    to_date_input = driver.find_element(*pt_page.INPUT_TO_DATE)
    search_btn = driver.find_element(*pt_page.BTN_SEARCH)

    # Set From Date to 2026-12-31, and To Date to 2026-01-01 (Reversed!)
    from_date_input.clear()
    from_date_input.send_keys("12/31/2026")
    to_date_input.clear()
    to_date_input.send_keys("01/01/2026")
    time.sleep(0.5)

    print("  Clicking search with From Date (31/12/2026) > To Date (01/01/2026)...")
    search_btn.click()
    time.sleep(2)
    driver.save_screenshot("screenshots/chaos_testing/03_pt_reversed_dates.png")

    toasts = driver.find_elements(By.CSS_SELECTOR, ".toast-item, .toast-stack .msg, .toast-error-http-message")
    toast_texts = [t.text.strip().replace('\n', ' ') for t in toasts]
    print(f"  Toasts visible after reversed date search: {toast_texts}")

    # Check browser console logs for unhandled errors
    logs = driver.get_log("browser")
    err_logs = [l['message'] for l in logs if l['level'] in ('SEVERE', 'ERROR')]
    print(f"  Browser Console Errors: count={len(err_logs)}")
    if err_logs:
        print(f"  Sample Error: {err_logs[0][:120]}")

    # -------------------------------------------------------------
    # 3. TEST PRICE & READONLY TAMPERING
    # -------------------------------------------------------------
    print("\n[4] Testing Price & Readonly Tampering in Services/Devices...")
    RESERV_ID = "CfDJ8KcUxlP3wTpIkfqEIRtHon4HnOXKri8R-HuwQbLe0ga8sPk_YDBIi7MkseBrAScp2lyLKLKWd1FdbV1bx5vDnm0EQBpbwWI9QcH-t-umVvqBT7aeI7evEqn6rXp7YK12Xw"
    ACCOM_ID = "CfDJ8KcUxlP3wTpIkfqEIRtHon6il3dFRgAMVI2R9iXr9AJ77pgneSuKHembPpKo7Y-WpjJgcXZaxrE0K-9uaDSgCs91FGvLxq1k6a3P6tJrXLC-GEMPIyzikQYqlb2CbLezAg"
    rays_url = f"https://196.218.246.250:4040/waiting-list/patient-rays?ReservID={RESERV_ID}&AccomID={ACCOM_ID}&typ=1"
    driver.get(rays_url)
    time.sleep(2)

    price_inputs = driver.find_elements(By.CSS_SELECTOR, "[data-test-id='patient-ipd-typed-unit-price-input']")
    qty_inputs = driver.find_elements(By.CSS_SELECTOR, "[data-test-id='patient-ipd-typed-quantity-input']")

    if price_inputs:
        p_in = price_inputs[0]
        # Inspect readonly / disabled attributes
        is_ro = p_in.get_attribute("readonly") is not None
        is_dis = p_in.get_attribute("disabled") is not None
        orig_val = p_in.get_attribute("value")
        print(f"  Price Input initial state: value='{orig_val}', readonly={is_ro}, disabled={is_dis}")

        # Tamper: strip readonly/disabled via JS and inject arbitrary negative or penny price
        print("  Tampering with Price Input: removing readonly & injecting 0.01 EGP...")
        driver.execute_script("""
            let inp = arguments[0];
            inp.removeAttribute('readonly');
            inp.removeAttribute('disabled');
            inp.value = '0.01';
            inp.dispatchEvent(new Event('input'));
            inp.dispatchEvent(new Event('change'));
        """, p_in)
        time.sleep(0.5)
        tampered_val = p_in.get_attribute("value")
        print(f"  Tampered Price Value in DOM: '{tampered_val}'")
        driver.save_screenshot("screenshots/chaos_testing/04_tampered_price.png")

        # Also test Quantity injection: extreme negative or astronomical quantity
        if qty_inputs:
            q_in = qty_inputs[0]
            driver.execute_script("""
                let inp = arguments[0];
                inp.value = '-999';
                inp.dispatchEvent(new Event('input'));
                inp.dispatchEvent(new Event('change'));
            """, q_in)
            time.sleep(0.5)
            print(f"  Injected Extreme Negative Quantity: '{q_in.get_attribute('value')}'")
            driver.save_screenshot("screenshots/chaos_testing/05_negative_quantity_injected.png")

finally:
    driver.quit()
