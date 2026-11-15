import sys
import time
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

try:
    print("Logging in...")
    login_page = LegacyLoginPage(driver)
    login_page.login_full_flow()
    time.sleep(3)

    print("Navigating to home page...")
    driver.get("https://196.218.246.250:4040/home")
    time.sleep(3)

    # Check all links on page
    links = driver.find_elements(By.TAG_NAME, "a")
    print(f"Total <a> tags on home: {len(links)}")
    for a in links:
        href = a.get_attribute("href") or ""
        txt = a.text.strip().replace("\n", " ")
        if txt or "reception" in href or "patient" in href or "admission" in href or "surgery" in href or "operation" in href or "report" in href:
            print(f"  [Link] text: '{txt}' | href: '{href}'")

    # Check dropdown buttons specifically
    dropdown_buttons = driver.find_elements(By.XPATH, "//div[contains(@class, 'nav-dropdown')]//button | //div[contains(@class, 'dropdown')]//button")
    print(f"\nFound {len(dropdown_buttons)} dropdown buttons:")
    for b in dropdown_buttons:
        txt = b.text.strip()
        print(f"  [Dropdown Button] '{txt}'")
        try:
            b.click()
            time.sleep(0.5)
            sub_links = driver.find_elements(By.XPATH, "//div[contains(@class, 'dropdown-menu') or contains(@class, 'menu')]//a")
            for sa in sub_links:
                s_href = sa.get_attribute("href") or ""
                s_txt = sa.text.strip().replace("\n", " ")
                if s_txt or s_href:
                    print(f"     -> SubLink: '{s_txt}' | href: '{s_href}'")
            b.click()
            time.sleep(0.3)
        except Exception as ex:
            print(f"     Error clicking: {ex}")

finally:
    driver.quit()
