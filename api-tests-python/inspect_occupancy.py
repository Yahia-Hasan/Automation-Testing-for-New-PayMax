import time
import sys
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.legacy_login_page import LegacyLoginPage

sys.stdout.reconfigure(encoding='utf-8')

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-insecure-localhost")
options.set_capability("acceptInsecureCerts", True)
options.set_capability("goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"})

driver = webdriver.Chrome(options=options)
driver.set_window_size(1366, 768)

try:
    print("Logging in...")
    login_page = LegacyLoginPage(driver)
    login_page.login_full_flow()

    target_url = "https://196.218.246.250:4040/reception/occupancy-report"
    print(f"Navigating to {target_url} ...")
    driver.get(target_url)
    time.sleep(6)

    driver.save_screenshot("occupancy_report_screen.png")

    with open("occupancy_report_page.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    print("Current URL:", driver.current_url)
    print("Page Title:", driver.title)

    # Inspect headers & titles
    print("\n--- Headers / Titles ---")
    for h in driver.find_elements(By.XPATH, "//h1 | //h2 | //h3 | //h4"):
        txt = h.text.strip()
        if txt:
            print(f"  [{h.tag_name}] {txt}")

    # Inspect inputs
    print("\n--- Inputs ---")
    for inp in driver.find_elements(By.TAG_NAME, "input"):
        dt = inp.get_attribute("data-test-id") or ""
        typ = inp.get_attribute("type") or ""
        ph = inp.get_attribute("placeholder") or ""
        name = inp.get_attribute("name") or ""
        print(f"  input: type='{typ}', name='{name}', data-test-id='{dt}', placeholder='{ph}'")

    # Inspect selects & ng-selects
    print("\n--- Selects & ng-select ---")
    for s in driver.find_elements(By.TAG_NAME, "select"):
        dt = s.get_attribute("data-test-id") or ""
        print(f"  select: name='{s.get_attribute('name')}', data-test-id='{dt}'")
    for ng in driver.find_elements(By.TAG_NAME, "ng-select"):
        dt = ng.get_attribute("data-test-id") or ""
        cls = ng.get_attribute("class") or ""
        print(f"  ng-select: data-test-id='{dt}', class='{cls}'")

    # Inspect buttons
    print("\n--- Buttons ---")
    for btn in driver.find_elements(By.TAG_NAME, "button"):
        dt = btn.get_attribute("data-test-id") or ""
        txt = btn.text.strip()
        cls = btn.get_attribute("class") or ""
        if txt or dt:
            print(f"  btn: text='{txt}', data-test-id='{dt}', class='{cls}'")

    # Inspect tables / cards / tabs
    tables = driver.find_elements(By.TAG_NAME, "table")
    print(f"\nTables found: {len(tables)}")
    for i, t in enumerate(tables):
        print(f"  Table {i+1}: class='{t.get_attribute('class')}'")
        headers = [th.text.strip() for th in t.find_elements(By.TAG_NAME, "th") if th.text.strip()]
        if headers:
            print(f"    Columns: {' | '.join(headers)}")

    # Extract API calls from performance logs
    print("\n--- API Calls Detected ---")
    logs = driver.get_log("performance")
    api_urls = set()
    for entry in logs:
        try:
            msg = json.loads(entry["message"])["message"]
            if msg.get("method") == "Network.requestWillBeSent":
                req_url = msg["params"]["request"]["url"]
                if "/api/" in req_url:
                    api_urls.add((msg["params"]["request"]["method"], req_url))
        except Exception:
            pass

    for method, url in sorted(api_urls):
        print(f"  {method} -> {url}")

finally:
    driver.quit()
