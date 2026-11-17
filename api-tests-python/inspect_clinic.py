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
    print("Navigating to /clinic/waiting-list ...")
    driver.get("https://196.218.246.250:4040/clinic/waiting-list")
    time.sleep(5)
    driver.save_screenshot("clinic_waiting_screen.png")

    with open("clinic_waiting_page.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    print("Current URL:", driver.current_url)
    print("Page Title:", driver.title)

    # Check for data-test-id
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    test_ids = [el.get("data-test-id") for el in soup.find_all(attrs={"data-test-id": True})]
    print(f"\nFound {len(test_ids)} data-test-ids on /clinic/waiting-list:")
    for tid in test_ids:
        print(f"  {tid}")

finally:
    driver.quit()
