import sys
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.legacy_login_page import LegacyLoginPage

sys.stdout.reconfigure(encoding='utf-8')

options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-insecure-localhost')
options.set_capability('acceptInsecureCerts', True)

driver = webdriver.Chrome(options=options)
driver.set_window_size(1440, 1000)

PAGES_TO_INSPECT = [
    ("invoice_details_regular", "فاتورة عادية غير مسجلة", "https://196.218.246.250:4040/patient-accounts/invoice-details?rid=12746"),
    ("package_invoice_details", "باكيدج كمي غير مسجل", "https://196.218.246.250:4040/patient-accounts/package-invoice-details?rid=12747"),
    ("ipd_package_invoice", "باكيدج مالي غير مسجل", "https://196.218.246.250:4040/patient-accounts/ipd-package-invoice?rid=12731"),
    ("invoice_details_registered", "فاتورة مسجلة", "https://196.218.246.250:4040/patient-accounts/invoice-details?rid=12744"),
    ("patient_services", "خدمات المريض الداخلي", "https://196.218.246.250:4040/waiting-list/patient-services?ReservID=CfDJ8KcUxlP3wTpIkfqEIRtHon7zSAyPB2lIYbCHCWrqBp7K4jkMTKXk5axOsUN82puPKlT-g3kDxq_2u17f2Nbo30AlOJpkeRYjWxGWxs0ataq_nI5P2Hkl9_cnHr5BBTAPOQ&AccomID=CfDJ8KcUxlP3wTpIkfqEIRtHon7OgT6pBpREID8flcN6k4JcDwSkHUmjfUN4cqbPAEP_yrAaMlYRDvHAtlfNvD88XA4UikMEacqBo7EBAZJvs514FgLI0ryWqOtEPLWSktt3Vg&typ=1&flag=All")
]

try:
    print("Logging in...")
    login = LegacyLoginPage(driver)
    login.login_full_flow()
    time.sleep(2)

    for key, name, url in PAGES_TO_INSPECT:
        print(f"\n{'='*50}\nInspecting: {name} ({url})\n{'='*50}")
        driver.get(url)
        time.sleep(4)

        driver.save_screenshot(f"scratch/{key}.png")
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Headings
        headings = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5'])]
        print("Headings:", headings[:6])

        # All data-test-ids
        dts = [el.get('data-test-id') for el in soup.find_all(attrs={'data-test-id': True}) if el.get('data-test-id') != 'global-toast-stack']
        unique_dts = list(dict.fromkeys(dts))
        print(f"Total data-test-ids: {len(unique_dts)}")
        print("Sample data-test-ids:", unique_dts[:30])

        # Buttons
        btns = [b.get_text(strip=True) for b in soup.find_all('button') if b.get_text(strip=True)]
        print("Buttons:", btns[:15])

        # Tabs / nav-links
        nav_links = [a.get_text(strip=True) for a in soup.find_all(class_=lambda c: c and ('nav-link' in c or 'tab' in c or 'btn' in c))]
        print("Nav / Tabs:", nav_links[:15])

        # Tables
        tables = soup.find_all("table")
        print(f"Tables: {len(tables)}")
        for idx, tbl in enumerate(tables[:3]):
            headers = [th.get_text(strip=True) for th in tbl.find_all("th")]
            print(f" Table {idx+1} headers: {headers}")

    # Inspect /waiting-list/accomodation-rooms patient cards to see how services button is structured
    print(f"\n{'='*50}\nInspecting /waiting-list/accomodation-rooms cards\n{'='*50}")
    driver.get("https://196.218.246.250:4040/waiting-list/accomodation-rooms")
    time.sleep(4)
    soup_rooms = BeautifulSoup(driver.page_source, "html.parser")
    service_links = soup_rooms.find_all(lambda tag: tag.name in ['a', 'button'] and ('خدمات' in tag.get_text() or 'services' in str(tag.get('href', '')).lower()))
    print(f"Service buttons/links in rooms count: {len(service_links)}")
    for sl in service_links[:5]:
        print(" Service link/button:", sl.name, sl.get('href'), sl.get('data-test-id'), sl.get('class'), sl.get_text(strip=True))

finally:
    driver.quit()
