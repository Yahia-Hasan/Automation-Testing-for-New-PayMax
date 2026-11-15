import sys
import time
from bs4 import BeautifulSoup
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

SEARCH_ACTIONS = [
    ("accountant_leaving_requests", "طلبات خروج المرضى", "https://196.218.246.250:4040/accountant/leaving-requests", "//button[@data-test-id='accom-leaving-wl-search-btn']"),
    ("emergency_transfers", "طلبات تحويل المرضى من الطوارئ", "https://196.218.246.250:4040/reception/emergency-transfers", "//button[@data-test-id='emergency-transfers-search-btn']"),
    ("leaving_approval_report", "تقرير تأكيد طلبات المغادرة", "https://196.218.246.250:4040/reception/leaving-approval-report", "//button[@data-test-id='leaving-approval-report-search-btn']")
]

try:
    print("Logging in...")
    login_page = LegacyLoginPage(driver)
    login_page.login_full_flow()
    time.sleep(2)

    for key, name, url, btn_xpath in SEARCH_ACTIONS:
        print(f"\n==========================================")
        print(f"Testing Search: {name}")
        print(f"==========================================")
        driver.get(url)
        time.sleep(3)

        btn = driver.find_element(By.XPATH, btn_xpath)
        print(f"Clicking search button: {btn.text.strip()}...")
        btn.click()
        time.sleep(4)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.save_screenshot(f"scratch/{key}_searched.png")

        # Find all data-test-id attributes
        dt_list = [el.get("data-test-id") for el in soup.find_all(attrs={"data-test-id": True})]
        print(f"Total data-test-ids: {len(dt_list)}")
        print(f"data-test-ids sample: {list(dict.fromkeys(dt_list))[:15]}")

        # Check tables and headers
        tables = soup.find_all("table")
        print(f"Tables found: {len(tables)}")
        for i, t in enumerate(tables):
            headers = [th.get_text(strip=True) for th in t.find_all("th")]
            rows = t.find_all("tr")
            print(f"  Table {i+1}: headers={headers}, total rows={len(rows)}")

        # Check any text snippets or alerts
        text_snippets = " ".join(soup.stripped_strings)[:200]
        print(f"Page text preview: {text_snippets}")

finally:
    driver.quit()
