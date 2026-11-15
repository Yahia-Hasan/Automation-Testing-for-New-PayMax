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

PAGES = [
    ("accom_leaving", "طلبات خروج المرضى", "https://196.218.246.250:4040/accountant/leaving-requests"),
    ("emergency_transfers", "طلبات تحويل المرضى من الطوارئ", "https://196.218.246.250:4040/reception/emergency-transfers"),
    ("leaving_approval", "تقرير تأكيد طلبات المغادرة", "https://196.218.246.250:4040/reception/leaving-approval-report")
]

try:
    print("Logging in...")
    login_page = LegacyLoginPage(driver)
    login_page.login_full_flow()
    time.sleep(2)

    for key, name, url in PAGES:
        print(f"\n==================== {name} ====================")
        driver.get(url)
        # Wait up to 15s for loading text to disappear
        for i in range(15):
            time.sleep(1)
            src = driver.page_source
            if "جاري تحميل البيانات..." not in src and "loading" not in src.lower():
                print(f"Loading finished after {i+1}s!")
                break
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        dts = [el.get('data-test-id') for el in soup.find_all(attrs={'data-test-id': True})]
        print("Data-test-ids after load:", list(dict.fromkeys(dts)))
        
        tables = soup.find_all("table")
        print(f"Tables count: {len(tables)}")
        for t in tables:
            headers = [th.get_text(strip=True) for th in t.find_all("th")]
            rows = len(t.find_all("tr"))
            print(f"  Table: headers={headers}, rows={rows}")
            
        text = " ".join(soup.stripped_strings)[:300]
        print(f"Text snippet: {text}")

finally:
    driver.quit()
