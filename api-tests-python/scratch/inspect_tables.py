import sys
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.legacy_login_page import LegacyLoginPage

sys.stdout.reconfigure(encoding='utf-8')

options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
options.set_capability('acceptInsecureCerts', True)
driver = webdriver.Chrome(options=options)
driver.set_window_size(1440, 1000)

urls = [
    ("12746", "https://196.218.246.250:4040/patient-accounts/invoice-details?rid=12746"),
    ("12747", "https://196.218.246.250:4040/patient-accounts/package-invoice-details?rid=12747"),
    ("12731", "https://196.218.246.250:4040/patient-accounts/ipd-package-invoice?rid=12731"),
    ("12744", "https://196.218.246.250:4040/patient-accounts/invoice-details?rid=12744"),
    ("services", "https://196.218.246.250:4040/waiting-list/patient-services?ReservID=CfDJ8KcUxlP3wTpIkfqEIRtHon7zSAyPB2lIYbCHCWrqBp7K4jkMTKXk5axOsUN82puPKlT-g3kDxq_2u17f2Nbo30AlOJpkeRYjWxGWxs0ataq_nI5P2Hkl9_cnHr5BBTAPOQ&AccomID=CfDJ8KcUxlP3wTpIkfqEIRtHon7OgT6pBpREID8flcN6k4JcDwSkHUmjfUN4cqbPAEP_yrAaMlYRDvHAtlfNvD88XA4UikMEacqBo7EBAZJvs514FgLI0ryWqOtEPLWSktt3Vg&typ=1&flag=All")
]

try:
    LegacyLoginPage(driver).login_full_flow()
    for name, url in urls:
        driver.get(url)
        time.sleep(4)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        tables = soup.find_all('table')
        print(f"\n--- URL: {name} ---")
        print(f"Total tables: {len(tables)}")
        for idx, t in enumerate(tables):
            cls = t.get('class')
            dt = t.get('data-test-id')
            trs = t.find_all('tr')
            body = t.find('tbody')
            body_trs = body.find_all('tr') if body else []
            print(f" Table {idx+1}: class={cls}, data-test-id={dt}, total_tr={len(trs)}, tbody_tr={len(body_trs)}")
            if body_trs:
                print(f"   First row text: {[td.get_text(strip=True) for td in body_trs[0].find_all(['td', 'th'])][:5]}")
finally:
    driver.quit()
