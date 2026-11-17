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

    # Let's inspect the entire navbar to find all dropdowns and items
    soup = BeautifulSoup(driver.page_source, "html.parser")
    nav = soup.find("nav") or soup.find("header") or soup
    
    # Let's look for dropdown buttons / nav items
    items = nav.find_all(["div", "li"], class_=lambda c: c and ("nav-item" in c or "dropdown" in c))
    print("Found nav items:", len(items))

    for item in items:
        btn = item.find("button") or item.find("a")
        btn_text = btn.get_text(strip=True) if btn else "NO_BTN"
        links = item.find_all("a")
        link_info = [(a.get("href"), a.get_text(strip=True)) for a in links if a.get("href")]
        if link_info or "العلاج" in btn_text or "حسابات" in btn_text:
            print(f"Dropdown: '{btn_text}' -> {link_info}")

    # Also search for all <a> tags with text containing العلاج or حسابات
    all_links = soup.find_all("a")
    print("\nTarget links:")
    for a in all_links:
        t = a.get_text(strip=True)
        if any(k in t for k in ["العلاج الطبيعي", "كشوف الحساب", "فواتير المرضى", "حسابات المرضى", "مديونيات", "بنك الفنيين", "دمج"]):
            print(f"Text: '{t}', href: '{a.get('href')}'")

finally:
    driver.quit()
