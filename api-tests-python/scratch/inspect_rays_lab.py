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

PAGES_TO_INSPECT = [
    # Rays (3 screens)
    ("rays_waiting", "قائمة انتظار الأشعة", "https://196.218.246.250:4040/rays/waiting-list"),
    ("rays_status", "موقف تنفيذ حالات الأشعة وطباعة الاستيكر", "https://196.218.246.250:4040/rays/status"),
    ("rays_details", "تقرير تفصيلي بالأشعة", "https://196.218.246.250:4040/rays/details"),
    # Lab & Blood Bank (5 screens)
    ("lab_waiting", "قائمة انتظار التحاليل", "https://196.218.246.250:4040/lab/waiting-list"),
    ("lab_blood_waiting", "قائمة انتظار بنك الدم", "https://196.218.246.250:4040/lab/blood-waiting-list"),
    ("lab_details", "تقرير بالتحاليل التفصيلي", "https://196.218.246.250:4040/lab/details"),
    ("lab_blood_status", "استعلام عن بنك الدم", "https://196.218.246.250:4040/lab/blood-bank-status"),
    ("lab_results_inquiry", "استعلام عن نتائج التحاليل", "https://196.218.246.250:4040/lab/results-inquiry")
]

try:
    print("Logging in...")
    login_page = LegacyLoginPage(driver)
    login_page.login_full_flow()
    time.sleep(2)

    for i, (key, name, url) in enumerate(PAGES_TO_INSPECT):
        print(f"\n==========================================")
        print(f"[{i+1}/8] Inspecting: {name} ({url})")
        print(f"==========================================")
        driver.get(url)
        time.sleep(4)

        driver.save_screenshot(f"scratch/{key}.png")
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Check for angular custom tags
        custom_tags = [tag.name for tag in soup.find_all() if '-' in tag.name and ('ray' in tag.name or 'lab' in tag.name or 'blood' in tag.name or 'waiting' in tag.name or 'status' in tag.name or 'detail' in tag.name)]
        print("Component tags:", set(custom_tags))

        # Headings
        headings = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3', 'h4'])]
        print("Headings:", headings)

        # data-test-ids
        dts = [el.get('data-test-id') for el in soup.find_all(attrs={'data-test-id': True})]
        print(f"data-test-ids ({len(dts)}):", list(dict.fromkeys(dts)))

        # Tables
        tables = soup.find_all("table")
        print(f"Tables count: {len(tables)}")
        for j, t in enumerate(tables):
            headers = [th.get_text(strip=True) for th in t.find_all("th")]
            print(f"  Table {j+1}: headers={headers}, rows={len(t.find_all('tr'))}")

finally:
    driver.quit()
