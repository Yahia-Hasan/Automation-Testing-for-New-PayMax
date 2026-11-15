import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pages.legacy_login_page import LegacyLoginPage

options = Options()
options.add_argument("--headless=new")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-web-security")
options.set_capability("acceptInsecureCerts", True)

driver = webdriver.Chrome(options=options)
try:
    login = LegacyLoginPage(driver)
    login.login_full_flow("sysadmin", "Ma3an2025", "Ad Doqi")
    print("[+] Login successful, exploring screens...")

    screens = [
        ("Rooms", "https://196.218.246.250:4040/reception/rooms"),
        ("Inpatients", "https://196.218.246.250:4040/reception/inpatients"),
        ("Emergency", "https://196.218.246.250:4040/emergency/waiting-list"),
        ("Invoices", "https://196.218.246.250:4040/patient-accounts/registered-invoices"),
        ("Doctors", "https://196.218.246.250:4040/info-desk/doctors"),
    ]

    results = {}
    for name, url in screens:
        print(f"[*] Navigating to {name} ({url})...")
        driver.get(url)
        time.sleep(4)
        
        elements = driver.find_elements(By.CSS_SELECTOR, "[data-test-id]")
        test_ids = [el.get_attribute("data-test-id") for el in elements if el.get_attribute("data-test-id")]
        
        inputs = [el.get_attribute("placeholder") or el.get_attribute("name") or el.get_attribute("type") 
                  for el in driver.find_elements(By.TAG_NAME, "input")]
        buttons = [el.text.strip() for el in driver.find_elements(By.TAG_NAME, "button") if el.text.strip()]
        
        results[name] = {
            "url": url,
            "title": driver.title,
            "data_test_ids": list(dict.fromkeys(test_ids)),
            "buttons": buttons[:10],
            "inputs_sample": inputs[:10]
        }
        print(f"  -> Found {len(test_ids)} data-test-ids, {len(buttons)} buttons.")

    with open("screen_inspection.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("[+] Results saved to screen_inspection.json")

finally:
    driver.quit()
