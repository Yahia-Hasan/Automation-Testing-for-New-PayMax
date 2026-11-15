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
    print("Logging in...")
    LegacyLoginPage(driver).login_full_flow()

    # 1. Test Reception Empty Submission
    print("\n--- Testing 1: Reception Empty Save ---")
    driver.get("https://196.218.246.250:4040/reception")
    time.sleep(3)
    new_btn = driver.find_element(By.CSS_SELECTOR, "[data-test-id='patient-data-new-btn']")
    new_btn.click()
    time.sleep(1)
    save_btn = driver.find_element(By.CSS_SELECTOR, "[data-test-id='patient-data-save-btn']")
    save_btn.click()
    time.sleep(2)

    # Check for toast, validation alerts, or error classes
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    toasts = [t.get_text(strip=True) for t in soup.find_all(class_=lambda c: c and ('toast' in c or 'alert' in c or 'error' in c or 'invalid' in c))]
    print("Feedback after empty save in reception:", toasts[:5])
    invalid_inputs = [inp.get('data-test-id') or inp.get('name') for inp in soup.find_all(class_=lambda c: c and ('ng-invalid' in c or 'is-invalid' in c))]
    print("Invalid inputs in reception form:", invalid_inputs[:10])

    # 2. Test Admission Empty Add Surgery
    print("\n--- Testing 2: Admission Empty Add Surgery ---")
    driver.get("https://196.218.246.250:4040/reception/patient/30854/admission")
    time.sleep(3)
    surg_tab = driver.find_element(By.CSS_SELECTOR, "[data-test-id='patient-admission-surgeries-tab-btn']")
    driver.execute_script("arguments[0].click();", surg_tab)
    time.sleep(1.5)
    add_surg = driver.find_element(By.CSS_SELECTOR, "[data-test-id='patient-admission-add-surgery-btn']")
    driver.execute_script("arguments[0].click();", add_surg)
    time.sleep(1.5)

    soup_adm = BeautifulSoup(driver.page_source, 'html.parser')
    adm_toasts = [t.get_text(strip=True) for t in soup_adm.find_all(class_=lambda c: c and ('toast' in c or 'alert' in c or 'error' in c or 'invalid' in c))]
    print("Feedback after empty add surgery:", adm_toasts[:5])

    # 3. Test Patient Services Negative Quantity & Empty Add
    print("\n--- Testing 3: Patient Services Negative Quantity & Empty Add ---")
    url_svc = "https://196.218.246.250:4040/waiting-list/patient-services?ReservID=CfDJ8KcUxlP3wTpIkfqEIRtHon7zSAyPB2lIYbCHCWrqBp7K4jkMTKXk5axOsUN82puPKlT-g3kDxq_2u17f2Nbo30AlOJpkeRYjWxGWxs0ataq_nI5P2Hkl9_cnHr5BBTAPOQ&AccomID=CfDJ8KcUxlP3wTpIkfqEIRtHon7OgT6pBpREID8flcN6k4JcDwSkHUmjfUN4cqbPAEP_yrAaMlYRDvHAtlfNvD88XA4UikMEacqBo7EBAZJvs514FgLI0ryWqOtEPLWSktt3Vg&typ=1&flag=All"
    driver.get(url_svc)
    time.sleep(3)

    # Empty add click
    add_btn = driver.find_element(By.CSS_SELECTOR, "[data-test-id='patient-services-add-btn']")
    add_btn.click()
    time.sleep(1.5)
    soup_svc = BeautifulSoup(driver.page_source, 'html.parser')
    svc_toasts = [t.get_text(strip=True) for t in soup_svc.find_all(class_=lambda c: c and ('toast' in c or 'alert' in c or 'error' in c or 'invalid' in c))]
    print("Feedback after empty service add:", svc_toasts[:5])

    # Try negative quantity
    qty_inp = driver.find_element(By.CSS_SELECTOR, "[data-test-id='patient-services-quantity-input']")
    qty_inp.clear()
    qty_inp.send_keys("-5")
    time.sleep(0.5)
    print("Quantity input value after setting -5:", qty_inp.get_attribute("value"))
    print("Quantity input validation classes:", qty_inp.get_attribute("class"))

finally:
    driver.quit()
