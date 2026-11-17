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

try:
    LegacyLoginPage(driver).login_full_flow()
    url = "https://196.218.246.250:4040/waiting-list/patient-services?ReservID=CfDJ8KcUxlP3wTpIkfqEIRtHon7zSAyPB2lIYbCHCWrqBp7K4jkMTKXk5axOsUN82puPKlT-g3kDxq_2u17f2Nbo30AlOJpkeRYjWxGWxs0ataq_nI5P2Hkl9_cnHr5BBTAPOQ&AccomID=CfDJ8KcUxlP3wTpIkfqEIRtHon7OgT6pBpREID8flcN6k4JcDwSkHUmjfUN4cqbPAEP_yrAaMlYRDvHAtlfNvD88XA4UikMEacqBo7EBAZJvs514FgLI0ryWqOtEPLWSktt3Vg&typ=1&flag=All"
    driver.get(url)
    time.sleep(3)

    add_btn = driver.find_element(By.CSS_SELECTOR, "[data-test-id='patient-services-add-service-btn']")
    add_btn.click()
    time.sleep(2)

    driver.save_screenshot("scratch/patient_services_add_modal.png")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    dts = [el.get('data-test-id') for el in soup.find_all(attrs={'data-test-id': True})]
    print("All data-test-ids with modal open:", [d for d in dts if d not in ['global-toast-stack']])

    modal_inputs = [(inp.get('data-test-id') or inp.get('name') or inp.get('id') or inp.get('placeholder')) for inp in soup.find_all(['input', 'select', 'textarea'])]
    print("All inputs/selects:", modal_inputs)

    modal_btns = [(b.get('data-test-id'), b.get_text(strip=True)) for b in soup.find_all('button') if b.get_text(strip=True)]
    print("All buttons:", modal_btns)

finally:
    driver.quit()
