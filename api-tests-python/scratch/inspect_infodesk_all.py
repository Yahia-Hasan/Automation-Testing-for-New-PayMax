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

INFODESK_PAGES = [
    ("shift_managers", "بيانات مسؤولين الشيفت", "https://196.218.246.250:4040/info-desk/shift-managers"),
    ("surgery_names", "أسماء العمليات", "https://196.218.246.250:4040/info-desk/surgery-names"),
    ("surgery_prices", "أسعار العمليات", "https://196.218.246.250:4040/info-desk/surgery-prices"),
    ("surgery_agenda", "أجندة العمليات", "https://196.218.246.250:4040/info-desk/surgery-agenda"),
    ("clinic_agenda", "أجندة العيادات", "https://196.218.246.250:4040/info-desk/clinic-agenda"),
    ("phone_book", "دليل الهاتف", "https://196.218.246.250:4040/info-desk/phone-book"),
    ("surgery_waiting", "قائمة انتظار العمليات", "https://196.218.246.250:4040/info-desk/surgeries"),
    ("packages", "استعلام عن الباكيدجات", "https://196.218.246.250:4040/info-desk/packages")
]

try:
    print("Logging in...")
    login_page = LegacyLoginPage(driver)
    login_page.login_full_flow()
    time.sleep(2)

    for key, name, url in INFODESK_PAGES:
        print(f"\n==========================================")
        print(f"Inspecting: {name} ({url})")
        print(f"==========================================")
        driver.get(url)
        time.sleep(4)

        driver.save_screenshot(f"scratch/infodesk_{key}.png")
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Custom component tag
        custom_tags = [tag.name for tag in soup.find_all() if '-' in tag.name and 'info' in tag.name or 'agenda' in tag.name or 'phone' in tag.name or 'surgery' in tag.name or 'package' in tag.name or 'shift' in tag.name]
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
        for i, t in enumerate(tables):
            headers = [th.get_text(strip=True) for th in t.find_all("th")]
            print(f"  Table {i+1}: headers={headers}, rows={len(t.find_all('tr'))}")

finally:
    driver.quit()
