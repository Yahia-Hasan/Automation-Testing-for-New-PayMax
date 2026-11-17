import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

sys.stdout.reconfigure(encoding='utf-8')

options = Options()
options.add_argument("--headless=new")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-insecure-localhost")
options.set_capability("acceptInsecureCerts", True)

driver = webdriver.Chrome(options=options)
driver.set_window_size(1366, 768)

try:
    print("1. Loading login page...")
    driver.get("http://196.218.246.250/sysadmin/login.aspx?macAdd=000000000000")
    time.sleep(2)

    # Click btnWorkspaceHospital
    hosp_btn = driver.find_element(By.ID, "btnWorkspaceHospital")
    driver.execute_script("arguments[0].click();", hosp_btn)
    time.sleep(2)

    # Enter credentials
    user_elem = driver.find_element(By.ID, "txtInvUserName")
    pass_elem = driver.find_element(By.ID, "txtInvPassword")
    login_btn = driver.find_element(By.ID, "btnLogin")

    user_elem.clear()
    user_elem.send_keys("sysadmin")
    pass_elem.clear()
    pass_elem.send_keys("Ma3an2025")

    print("Clicking btnLogin...")
    driver.execute_script("arguments[0].click();", login_btn)
    time.sleep(4)

    print("URL after login:", driver.current_url)

    # 3. Select branch: Ad Doqi via Telerik RadComboBox
    print("Selecting branch 'Ad Doqi'...")
    try:
        # Try Telerik JS API first
        driver.execute_script("""
            var combo = $find('ddlBranches');
            if (combo) {
                var item = combo.findItemByText('Ad Doqi') || combo.get_items().getItem(0);
                if (item) {
                    item.select();
                }
            }
        """)
        print("Selected via Telerik JS API.")
    except Exception as e:
        print("Telerik JS API fallback to UI click:", e)
        arrow = driver.find_element(By.ID, "ddlBranches_Arrow")
        arrow.click()
        time.sleep(1)
        doqi_item = driver.find_element(By.XPATH, "//li[contains(text(), 'Ad Doqi')]")
        doqi_item.click()

    time.sleep(1)
    # Click btnContinue
    continue_btn = driver.find_element(By.ID, "btnContinue")
    print("Clicking btnContinue...")
    driver.execute_script("arguments[0].click();", continue_btn)
    time.sleep(5)

    print("URL after branch continue:", driver.current_url)
    driver.save_screenshot("after_branch_landing.png")

    # 4. Navigate to new system
    new_url = "https://196.218.246.250:4040/home"
    print(f"\nNavigating to new system: {new_url} ...")
    driver.get(new_url)
    time.sleep(6)
    print("New system URL:", driver.current_url)
    driver.save_screenshot("new_system_page.png")

    # Extract all localStorage
    storage = driver.execute_script(
        "let s = {}; for (let i = 0; i < localStorage.length; i++) { s[localStorage.key(i)] = localStorage.getItem(localStorage.key(i)); } return s;"
    )
    print(f"\nLocalStorage Keys ({len(storage)}):", list(storage.keys()))
    for k, v in storage.items():
        val = str(v)
        print(f"  {k} = {val[:120]}...")

    # Extract cookies
    cookies = driver.get_cookies()
    print(f"\nCookies ({len(cookies)}):")
    for c in cookies:
        print(f"  {c['name']} = {c['value'][:60]} (domain={c.get('domain')}, path={c.get('path')})")

finally:
    driver.quit()
