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

SCREENS = [
    # Physical Therapy (1 screen)
    ("pt_waiting", "قائمة انتظار العلاج الطبيعي", "https://196.218.246.250:4040/physical-therapy/waiting-list"),
    # Patient Accounts (6 screens)
    ("unregistered_invoices", "كشوف الحساب المفتوحة", "https://196.218.246.250:4040/patient-accounts/unregistered-invoices"),
    ("registered_invoices", "فواتير المرضى", "https://196.218.246.250:4040/patient-accounts/registered-invoices"),
    ("patient_checkups", "حسابات المرضى الداخلي", "https://196.218.246.250:4040/patient-accounts/patient-checkups"),
    ("patient_settlements", "مديونيات المرضى", "https://196.218.246.250:4040/patient-accounts/patient-settlements"),
    ("technician_bank", "بنك الفنيين", "https://196.218.246.250:4040/patient-accounts/technician-bank"),
    ("merge_patients", "دمج بين المرضى", "https://196.218.246.250:4040/patient-accounts/merge-patients")
]

try:
    print("Logging in...")
    login_page = LegacyLoginPage(driver)
    login_page.login_full_flow()
    time.sleep(2)

    for i, (key, name, url) in enumerate(SCREENS):
        print(f"\n==========================================")
        print(f"[{i+1}/7] Inspecting: {name} ({url})")
        print(f"==========================================")
        driver.get(url)
        time.sleep(4)

        driver.save_screenshot(f"scratch/{key}.png")
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Headings
        headings = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3', 'h4'])]
        print("Headings:", headings)

        # data-test-ids
        dts = [el.get('data-test-id') for el in soup.find_all(attrs={'data-test-id': True})]
        print(f"data-test-ids ({len(dts)}):", list(dict.fromkeys(dts)))

        # Inputs and buttons
        inputs = [(inp.get('name') or inp.get('id') or inp.get('placeholder') or inp.get('type')) for inp in soup.find_all('input')][:8]
        buttons = [btn.get_text(strip=True) for btn in soup.find_all('button') if btn.get_text(strip=True)][:8]
        print("Sample inputs:", inputs)
        print("Sample buttons:", buttons)

        # Tables
        tables = soup.find_all("table")
        print(f"Tables count: {len(tables)}")
        for j, t in enumerate(tables):
            headers = [th.get_text(strip=True) for th in t.find_all("th")]
            print(f"  Table {j+1}: headers={headers}, rows={len(t.find_all('tr'))}")

finally:
    driver.quit()
