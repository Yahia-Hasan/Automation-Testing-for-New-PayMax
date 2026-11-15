import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.legacy_login_page import LegacyLoginPage

sys.stdout.reconfigure(encoding='utf-8')

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-insecure-localhost")
options.set_capability("acceptInsecureCerts", True)

driver = webdriver.Chrome(options=options)
driver.set_window_size(1366, 768)

try:
    print("Logging in...")
    login_page = LegacyLoginPage(driver)
    login_page.login_full_flow()
    time.sleep(2)

    # 1. Investigate surgery booking loading
    print("\nNavigating to surgery booking...")
    driver.get("https://196.218.246.250:4040/reception/surgery-booking")
    
    # Wait up to 20 seconds for loading spinner to disappear
    for i in range(20):
        time.sleep(1)
        spinners = driver.find_elements(By.CSS_SELECTOR, ".loading-spinner, .p-progress-spinner, [class*='spinner']")
        visible_spinners = [s for s in spinners if s.is_displayed()]
        if not visible_spinners:
            print(f"Spinner disappeared after {i+1} seconds!")
            break
        print(f"Waiting for spinner... ({i+1}s)")

    time.sleep(2)
    driver.save_screenshot("scratch/surgery_booking_loaded.png")
    with open("scratch/surgery_booking_loaded.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    # 2. Investigate admission discharge report
    print("\nNavigating to admission discharge report...")
    driver.get("https://196.218.246.250:4040/reception/admission-discharge-report")
    time.sleep(3)

    # Click search button
    search_btn = driver.find_element(By.XPATH, "//button[@data-test-id='admission-discharge-report-search-btn']")
    print("Clicking Search / عرض button...")
    search_btn.click()
    time.sleep(5)

    driver.save_screenshot("scratch/admission_discharge_loaded.png")
    with open("scratch/admission_discharge_loaded.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

finally:
    driver.quit()
