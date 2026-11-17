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

    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Let's inspect all dropdowns
    items = soup.find_all(["div", "li"], class_=lambda c: c and ("nav-item" in c or "dropdown" in c))
    for item in items:
        btn = item.find("button") or item.find("a")
        btn_text = btn.get_text(strip=True) if btn else "NO_BTN"
        if any(k in btn_text for k in ["الإسعاف", "الطوارئ", "العيادات", "التمريض", "سكرتارية"]):
            links = item.find_all("a")
            link_info = [(a.get("href"), a.get_text(strip=True)) for a in links if a.get("href")]
            print(f"\nDropdown: '{btn_text}' ->")
            for h, t in link_info:
                print(f"  {t} -> {h}")

    # Also find all links matching the text in the 3 images
    all_links = soup.find_all("a")
    print("\nMatching links in page:")
    targets = [
        "المرضى بالطوارئ", "تعديل زيارة بالطوارئ", "تقرير الدخول والخروج بالطوارئ",
        "التقارير الطبية للإسعاف والطوارئ", "تقرير اشغال أسرة الطوارئ", "إلغاء خروج مريض طوارئ",
        "قائمة انتظار العيادات", "تقرير العيادات التفصيلي", "المرضى بالعيادات",
        "تعديل زيارة عيادات", "إلغاء خروج مريض عيادات", "التقارير الطبية للعيادات الخارجية",
        "المرضى بالغرف", "المرضى بالرعاية المركزة", "المرضى بالحضانة",
        "قائمة طلبات الأنظمة الغذائية للمرضي", "قائمة طلبات الأنظمة الغذائية للمرافقين",
        "التقارير الطبية للمرضى الداخلي"
    ]
    for a in all_links:
        t = a.get_text(strip=True)
        for target in targets:
            if target in t:
                print(f"  '{t}' -> {a.get('href')}")

finally:
    driver.quit()
