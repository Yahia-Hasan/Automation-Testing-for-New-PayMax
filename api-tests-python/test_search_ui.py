import time
import sys
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
    LegacyLoginPage(driver).login_full_flow()
    driver.get("https://196.218.246.250:4040/reception")
    time.sleep(3)

    search_input = driver.find_element(By.CSS_SELECTOR, "[data-test-id='patient-data-search-input']")
    search_input.clear()
    search_input.send_keys("30902")
    time.sleep(2)

    dropdown = driver.find_element(By.CLASS_NAME, "search-dropdown")
    print("Search Dropdown HTML:\n", dropdown.get_attribute("outerHTML"))

    # Click the child or item
    children = dropdown.find_elements(By.XPATH, "./*")
    print(f"\nChildren of search-dropdown: {len(children)}")
    for c in children:
        print(f"  Child tag={c.tag_name}, class='{c.get_attribute('class')}', text='{c.text[:40]}'")

    # Click the item using selenium native click
    if children:
        print("Clicking first child natively...")
        children[0].click()
        time.sleep(3)

    name_val = driver.find_element(By.CSS_SELECTOR, "[data-test-id='patient-data-patient-name-input']").get_attribute("value")
    code_val = driver.find_element(By.CSS_SELECTOR, "[data-test-id='patient-data-patient-code-input']").get_attribute("value")
    print(f"Result: Code='{code_val}', Name='{name_val}'")

finally:
    driver.quit()
