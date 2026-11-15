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
driver.set_window_size(1440, 900)

PAGES = [
    ("inpatient_admission", "الزيارة الداخلي (حجز داخلي)", "https://196.218.246.250:4040/reception/patient/30854/admission"),
    ("clinic_visit_draft", "الزيارة الخارجي (عيادات خارجية)", "https://196.218.246.250:4040/clinic/visits/draft?patientCode=30855&clientId=52&mode=opd"),
    ("emergency_case_draft", "زيارة الطوارئ (إسعاف وطوارئ)", "https://196.218.246.250:4040/emergency/cases/draft?patientCode=30856&clientId=52")
]

try:
    print("Logging in...")
    login_page = LegacyLoginPage(driver)
    login_page.login_full_flow()
    time.sleep(2)

    # 1. First let's inspect /reception after selecting a patient to see the action buttons
    print("\n--- Inspecting /reception with patient 30854 ---")
    driver.get("https://196.218.246.250:4040/reception")
    time.sleep(3)
    
    # Search for patient 30854
    search_inp = driver.find_element(By.CSS_SELECTOR, "[data-test-id='patient-data-search-input']")
    search_inp.send_keys("30854")
    time.sleep(2)
    items = driver.find_elements(By.CSS_SELECTOR, ".search-dropdown .search-item")
    if items:
        items[0].click()
        time.sleep(2)
        print("Selected patient 30854 on reception page!")
    
    driver.save_screenshot("scratch/reception_patient_selected.png")
    soup_rec = BeautifulSoup(driver.page_source, "html.parser")
    
    # Look for buttons on reception page
    btns = [(b.get_text(strip=True), b.get('data-test-id'), b.get('class')) for b in soup_rec.find_all('button') if b.get_text(strip=True)]
    print(f"Buttons on reception page with patient loaded ({len(btns)}):")
    for txt, dt, cls in btns:
        if any(k in txt for k in ["داخلي", "عيادات", "طوارئ", "زيارة", "حجز", "إسعاف"]):
            print(f"  Target Button: '{txt}' -> data-test-id='{dt}', class='{cls}'")

    # 2. Inspect each of the 3 deep visit pages
    for key, name, url in PAGES:
        print(f"\n==========================================")
        print(f"Inspecting: {name} ({url})")
        print(f"==========================================")
        driver.get(url)
        time.sleep(4)

        driver.save_screenshot(f"scratch/{key}.png")
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Headings
        headings = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3', 'h4'])]
        print("Headings:", headings[:5])

        # All data-test-ids
        dts = [el.get('data-test-id') for el in soup.find_all(attrs={'data-test-id': True}) if el.get('data-test-id') != 'global-toast-stack']
        print(f"data-test-ids ({len(dts)}):", list(dict.fromkeys(dts))[:25])

        # Tabs
        tabs = [t.get_text(strip=True) for t in soup.find_all(class_=lambda c: c and ('tab' in c or 'nav-link' in c))]
        print("Tabs/Nav:", tabs[:10])

        # Buttons
        page_btns = [b.get_text(strip=True) for b in soup.find_all('button') if b.get_text(strip=True)]
        print("Buttons:", page_btns[:15])

        # Form Inputs
        inputs = [(inp.get('name') or inp.get('id') or inp.get('data-test-id') or inp.get('placeholder') or inp.get('type')) for inp in soup.find_all('input')][:10]
        print("Inputs:", inputs)

        # Selects
        selects = [s.get('data-test-id') or s.get('name') or s.get('class') for s in soup.find_all('select')][:10]
        print("Selects:", selects)

        # Tables
        tables = soup.find_all("table")
        print(f"Tables count: {len(tables)}")
        for j, t in enumerate(tables):
            headers = [th.get_text(strip=True) for th in t.find_all("th")]
            print(f"  Table {j+1}: headers={headers}, rows={len(t.find_all('tr'))}")

finally:
    driver.quit()
