import sys
import os
sys.path.insert(0, os.path.abspath("."))
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pages.legacy_login_page import LegacyLoginPage
from pages.nursing_module_page import NursingRoomsPage

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
    print("[1] Logging in...")
    login_page = LegacyLoginPage(driver)
    login_page.login_full_flow("sysadmin", "Ma3an2025", "Ad Doqi")
    print("Logged in successfully!")

    print("[2] Opening Nursing Rooms...")
    page = NursingRoomsPage(driver).open()
    time.sleep(2)

    reload_btn = driver.find_element(By.CSS_SELECTOR, "[data-test-id='nursing-secretary-reload-btn']")
    print(f"Reload button initial state: disabled={reload_btn.get_attribute('disabled')}, class='{reload_btn.get_attribute('class')}'")

    # Spam click reload button 5 times
    print("[3] Spam clicking reload button 5 times...")
    script = """
        let btn = arguments[0];
        let states = [];
        for(let i=0; i<5; i++) {
            let disabledBefore = btn.disabled || btn.hasAttribute('disabled') || btn.classList.contains('disabled');
            btn.click();
            let disabledAfter = btn.disabled || btn.hasAttribute('disabled') || btn.classList.contains('disabled');
            states.push({click: i+1, before: disabledBefore, after: disabledAfter});
        }
        return states;
    """
    states = driver.execute_script(script, reload_btn)
    for s in states:
        print("  ", s)

    time.sleep(1)
    print(f"Reload button 1s after: disabled={reload_btn.get_attribute('disabled')}, class='{reload_btn.get_attribute('class')}'")

    # Let's inspect all buttons on this screen
    buttons = driver.find_elements(By.TAG_NAME, "button")
    print(f"\nTotal visible buttons on Nursing Rooms: {len(buttons)}")
    for b in buttons:
        if b.is_displayed():
            print(f"  text='{b.text.strip()}' | test_id='{b.get_attribute('data-test-id')}' | disabled={b.get_attribute('disabled')}")

finally:
    driver.quit()
