import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.legacy_login_page import LegacyLoginPage

sys.stdout.reconfigure(encoding='utf-8')

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-insecure-localhost")
options.set_capability("acceptInsecureCerts", True)

driver = webdriver.Chrome(options=options)
driver.set_window_size(1366, 768)

PAGES_TO_INSPECT = [
    ("accountant_leaving_requests", "طلبات خروج المرضى", "https://196.218.246.250:4040/accountant/leaving-requests"),
    ("emergency_transfers", "طلبات تحويل المرضى من الطوارئ", "https://196.218.246.250:4040/reception/emergency-transfers"),
    ("leaving_approval_report", "تقرير تأكيد طلبات المغادرة", "https://196.218.246.250:4040/reception/leaving-approval-report")
]

try:
    print("Logging in...")
    login_page = LegacyLoginPage(driver)
    login_page.login_full_flow()
    time.sleep(2)

    for key, name, url in PAGES_TO_INSPECT:
        print(f"\n==========================================")
        print(f"Inspecting: {name} ({url})")
        print(f"==========================================")
        driver.get(url)
        time.sleep(5)

        driver.save_screenshot(f"scratch/{key}_screen.png")
        with open(f"scratch/{key}_page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        print("Current URL:", driver.current_url)
        print("Page Title:", driver.title)

        # Headers
        print("--- Headers ---")
        for h in driver.find_elements(By.XPATH, "//h1 | //h2 | //h3 | //h4"):
            txt = h.text.strip()
            if txt:
                print(f"  [{h.tag_name}] {txt}")

        # Inputs
        print("--- Inputs & Textareas ---")
        for inp in driver.find_elements(By.XPATH, "//input | //textarea"):
            dt = inp.get_attribute("data-test-id") or ""
            typ = inp.get_attribute("type") or ""
            ph = inp.get_attribute("placeholder") or ""
            name_attr = inp.get_attribute("name") or ""
            id_attr = inp.get_attribute("id") or ""
            print(f"  input: id='{id_attr}', data-test-id='{dt}', name='{name_attr}', type='{typ}', placeholder='{ph}'")

        # Selects & ng-select
        print("--- Selects & ng-select ---")
        for s in driver.find_elements(By.TAG_NAME, "select"):
            dt = s.get_attribute("data-test-id") or ""
            name_attr = s.get_attribute("name") or ""
            print(f"  select: name='{name_attr}', data-test-id='{dt}'")
        for ng in driver.find_elements(By.TAG_NAME, "ng-select"):
            dt = ng.get_attribute("data-test-id") or ""
            id_attr = ng.get_attribute("id") or ""
            ph = ng.get_attribute("placeholder") or ""
            print(f"  ng-select: id='{id_attr}', data-test-id='{dt}', placeholder='{ph}'")

        # Buttons
        print("--- Action Buttons ---")
        for btn in driver.find_elements(By.TAG_NAME, "button"):
            dt = btn.get_attribute("data-test-id") or ""
            txt = btn.text.strip().replace("\n", " ")
            btn_id = btn.get_attribute("id") or ""
            if dt:
                print(f"  btn: text='{txt}', data-test-id='{dt}', id='{btn_id}'")

        # Tables
        tables = driver.find_elements(By.TAG_NAME, "table")
        print(f"--- Tables: {len(tables)} ---")
        for i, tbl in enumerate(tables):
            headers = [th.text.strip().replace("\n", " ") for th in tbl.find_elements(By.TAG_NAME, "th") if th.text.strip()]
            rows = tbl.find_elements(By.XPATH, ".//tbody//tr")
            print(f"  Table {i+1}: headers={headers}, rows_count={len(rows)}")

finally:
    driver.quit()
