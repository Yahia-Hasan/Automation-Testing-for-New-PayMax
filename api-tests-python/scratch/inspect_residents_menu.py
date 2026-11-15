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
driver.set_window_size(1366, 768)

try:
    print("Logging in...")
    login_page = LegacyLoginPage(driver)
    login_page.login_full_flow()
    time.sleep(2)

    # Click on المرضى المقيمين dropdown
    dropdown_btn = driver.find_element(By.XPATH, "//div[contains(@class, 'nav-dropdown')]//button[contains(., 'المرضى المقيمين')]")
    print("Clicking dropdown: المرضى المقيمين")
    dropdown_btn.click()
    time.sleep(1)

    parent_dropdown = dropdown_btn.find_element(By.XPATH, "./..")
    sub_links = parent_dropdown.find_elements(By.TAG_NAME, "a")
    print(f"Found {len(sub_links)} links under المرضى المقيمين:")
    menu_items = []
    for a in sub_links:
        href = a.get_attribute("href")
        txt = a.text.strip().replace("\n", " ")
        print(f"   -> Text: '{txt}' | href: '{href}'")
        if href:
            menu_items.append((txt, href))

    dropdown_btn.click()
    time.sleep(0.5)

    # Now visit each menu item and inspect
    for i, (txt, url) in enumerate(menu_items):
        print(f"\n==========================================")
        print(f"[{i+1}/{len(menu_items)}] Inspecting: {txt} ({url})")
        print(f"==========================================")
        driver.get(url)
        time.sleep(4)

        driver.save_screenshot(f"scratch/resident_{i+1}.png")
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Custom tag
        custom_tags = [tag.name for tag in soup.find_all() if '-' in tag.name and ('room' in tag.name or 'icu' in tag.name or 'neonatal' in tag.name or 'attendant' in tag.name or 'inpatient' in tag.name or 'bed' in tag.name or 'accom' in tag.name)]
        print("Component tags:", set(custom_tags))

        # Headings
        headings = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3', 'h4'])]
        print("Headings:", headings)

        # data-test-ids
        dts = [el.get('data-test-id') for el in soup.find_all(attrs={'data-test-id': True})]
        print(f"data-test-ids ({len(dts)}):", list(dict.fromkeys(dts)))

        # Tables
        tables = soup.find_all("table")
        print(f"Tables count: {len(tables)}")
        for j, t in enumerate(tables):
            headers = [th.get_text(strip=True) for th in t.find_all("th")]
            print(f"  Table {j+1}: headers={headers}, rows={len(t.find_all('tr'))}")

finally:
    driver.quit()
