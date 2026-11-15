import sys
import os
sys.path.insert(0, os.path.abspath("."))
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pages.legacy_login_page import LegacyLoginPage
from pages.reception_page import ReceptionPage

sys.stdout.reconfigure(encoding='utf-8')

options = Options()
options.add_argument("--headless=new")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-insecure-localhost")
options.add_argument("--disable-web-security")
options.add_argument("--start-maximized")
options.set_capability("acceptInsecureCerts", True)

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

try:
    print("[1] Logging into BayMax...")
    login_page = LegacyLoginPage(driver)
    login_page.login_full_flow("sysadmin", "Ma3an2025", "Ad Doqi")
    print("Logged in successfully!")

    print("[2] Opening Reception Page...")
    rec_page = ReceptionPage(driver).open()
    time.sleep(2)

    # Let's inspect Save Button
    save_btn = rec_page.find(rec_page.BTN_SAVE_PATIENT)
    print(f"Save button initial state: disabled={save_btn.get_attribute('disabled')}, class='{save_btn.get_attribute('class')}'")

    # Let's rapid click the Save button 5 times using JS
    print("\n[3] Spamming Save Button 5 times rapidly...")
    driver.execute_script("""
        window.__click_states = [];
        let btn = arguments[0];
        for(let i=0; i<5; i++) {
            let disabled_before = btn.disabled || btn.hasAttribute('disabled') || btn.classList.contains('disabled');
            btn.click();
            let disabled_after = btn.disabled || btn.hasAttribute('disabled') || btn.classList.contains('disabled');
            window.__click_states.push({click: i+1, disabled_before: disabled_before, disabled_after: disabled_after});
        }
    """, save_btn)

    states = driver.execute_script("return window.__click_states;")
    print("Click states during rapid spam:")
    for s in states:
        print("  ", s)

    time.sleep(1)
    print(f"Save button 1s after spam: disabled={save_btn.get_attribute('disabled')}, class='{save_btn.get_attribute('class')}'")

    toasts = driver.find_elements(By.CSS_SELECTOR, ".toast-item, .toast-stack .msg, [data-test-id='global-toast-stack']")
    print(f"Toasts visible after spam: count={len(toasts)}")
    for t in toasts:
        print(f"  Toast text: '{t.text.strip()}'")

finally:
    driver.quit()
