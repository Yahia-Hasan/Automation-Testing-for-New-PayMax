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
    login_page = LegacyLoginPage(driver)
    login_page.login_full_flow()

    print("Navigating to https://196.218.246.250:4040/reception ...")
    driver.get("https://196.218.246.250:4040/reception")
    time.sleep(5)
    driver.save_screenshot("reception_screen.png")

    with open("reception_page.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    print("Current URL:", driver.current_url)
    print("Page Title:", driver.title)

    # Inspect inputs
    print("\nInputs found on /reception:")
    for inp in driver.find_elements(By.TAG_NAME, "input"):
        print(f"  id='{inp.get_attribute('id')}', placeholder='{inp.get_attribute('placeholder')}', class='{inp.get_attribute('class')}'")

    # Inspect buttons
    print("\nButtons found on /reception:")
    for btn in driver.find_elements(By.TAG_NAME, "button"):
        print(f"  id='{btn.get_attribute('id')}', text='{btn.text.strip()}', class='{btn.get_attribute('class')}'")

    # Inspect tables or cards
    tables = driver.find_elements(By.TAG_NAME, "table")
    print(f"\nTables found: {len(tables)}")
    for t in tables:
        print(f"  Table class='{t.get_attribute('class')}'")

finally:
    driver.quit()
