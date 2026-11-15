import json
import os
import sys
import time
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

PAGES_TO_INSPECT = [
    {
        "name": "patient_rays",
        "title": "أشعة المريض",
        "url": "https://196.218.246.250:4040/waiting-list/patient-rays?ReservID=CfDJ8KcUxlP3wTpIkfqEIRtHon4HnOXKri8R-HuwQbLe0ga8sPk_YDBIi7MkseBrAScp2lyLKLKWd1FdbV1bx5vDnm0EQBpbwWI9QcH-t-umVvqBT7aeI7evEqn6rXp7YK12Xw&AccomID=CfDJ8KcUxlP3wTpIkfqEIRtHon6il3dFRgAMVI2R9iXr9AJ77pgneSuKHembPpKo7Y-WpjJgcXZaxrE0K-9uaDSgCs91FGvLxq1k6a3P6tJrXLC-GEMPIyzikQYqlb2CbLezAg&typ=1"
    },
    {
        "name": "patient_tests",
        "title": "تحاليل المريض",
        "url": "https://196.218.246.250:4040/waiting-list/patient-tests?ReservID=CfDJ8KcUxlP3wTpIkfqEIRtHon4HnOXKri8R-HuwQbLe0ga8sPk_YDBIi7MkseBrAScp2lyLKLKWd1FdbV1bx5vDnm0EQBpbwWI9QcH-t-umVvqBT7aeI7evEqn6rXp7YK12Xw&AccomID=CfDJ8KcUxlP3wTpIkfqEIRtHon6il3dFRgAMVI2R9iXr9AJ77pgneSuKHembPpKo7Y-WpjJgcXZaxrE0K-9uaDSgCs91FGvLxq1k6a3P6tJrXLC-GEMPIyzikQYqlb2CbLezAg&typ=1"
    },
    {
        "name": "charge_patient_med",
        "title": "صرف أدوية المريض",
        "url": "https://196.218.246.250:4040/waiting-list/charge-patient-med?ReservID=CfDJ8KcUxlP3wTpIkfqEIRtHon4HnOXKri8R-HuwQbLe0ga8sPk_YDBIi7MkseBrAScp2lyLKLKWd1FdbV1bx5vDnm0EQBpbwWI9QcH-t-umVvqBT7aeI7evEqn6rXp7YK12Xw&AccomID=CfDJ8KcUxlP3wTpIkfqEIRtHon6il3dFRgAMVI2R9iXr9AJ77pgneSuKHembPpKo7Y-WpjJgcXZaxrE0K-9uaDSgCs91FGvLxq1k6a3P6tJrXLC-GEMPIyzikQYqlb2CbLezAg&typ=1"
    },
    {
        "name": "patient_request_med_all",
        "title": "طلب أدوية ومستلزمات (الكل)",
        "url": "https://196.218.246.250:4040/waiting-list/patient-request-med?ReservID=CfDJ8KcUxlP3wTpIkfqEIRtHon4HnOXKri8R-HuwQbLe0ga8sPk_YDBIi7MkseBrAScp2lyLKLKWd1FdbV1bx5vDnm0EQBpbwWI9QcH-t-umVvqBT7aeI7evEqn6rXp7YK12Xw&AccomID=CfDJ8KcUxlP3wTpIkfqEIRtHon6il3dFRgAMVI2R9iXr9AJ77pgneSuKHembPpKo7Y-WpjJgcXZaxrE0K-9uaDSgCs91FGvLxq1k6a3P6tJrXLC-GEMPIyzikQYqlb2CbLezAg&typ=1&flag=All"
    },
    {
        "name": "patient_request_med_drugs",
        "title": "طلب أدوية فقط",
        "url": "https://196.218.246.250:4040/waiting-list/patient-request-med?ReservID=CfDJ8KcUxlP3wTpIkfqEIRtHon4HnOXKri8R-HuwQbLe0ga8sPk_YDBIi7MkseBrAScp2lyLKLKWd1FdbV1bx5vDnm0EQBpbwWI9QcH-t-umVvqBT7aeI7evEqn6rXp7YK12Xw&AccomID=CfDJ8KcUxlP3wTpIkfqEIRtHon6il3dFRgAMVI2R9iXr9AJ77pgneSuKHembPpKo7Y-WpjJgcXZaxrE0K-9uaDSgCs91FGvLxq1k6a3P6tJrXLC-GEMPIyzikQYqlb2CbLezAg&typ=1&flag=Durgs"
    },
    {
        "name": "patient_return_med_drugs",
        "title": "إرجاع أدوية ومستلزمات",
        "url": "https://196.218.246.250:4040/waiting-list/patient-return-med?ReservID=CfDJ8KcUxlP3wTpIkfqEIRtHon4HnOXKri8R-HuwQbLe0ga8sPk_YDBIi7MkseBrAScp2lyLKLKWd1FdbV1bx5vDnm0EQBpbwWI9QcH-t-umVvqBT7aeI7evEqn6rXp7YK12Xw&AccomID=CfDJ8KcUxlP3wTpIkfqEIRtHon6il3dFRgAMVI2R9iXr9AJ77pgneSuKHembPpKo7Y-WpjJgcXZaxrE0K-9uaDSgCs91FGvLxq1k6a3P6tJrXLC-GEMPIyzikQYqlb2CbLezAg&typ=1&flag=Durgs"
    },
    {
        "name": "patient_blood_drugs",
        "title": "بنك دم المريض",
        "url": "https://196.218.246.250:4040/waiting-list/patient-blood?ReservID=CfDJ8KcUxlP3wTpIkfqEIRtHon4HnOXKri8R-HuwQbLe0ga8sPk_YDBIi7MkseBrAScp2lyLKLKWd1FdbV1bx5vDnm0EQBpbwWI9QcH-t-umVvqBT7aeI7evEqn6rXp7YK12Xw&AccomID=CfDJ8KcUxlP3wTpIkfqEIRtHon6il3dFRgAMVI2R9iXr9AJ77pgneSuKHembPpKo7Y-WpjJgcXZaxrE0K-9uaDSgCs91FGvLxq1k6a3P6tJrXLC-GEMPIyzikQYqlb2CbLezAg&typ=1&flag=Durgs"
    },
    {
        "name": "patient_internal_devices",
        "title": "أجهزة داخلية للمريض",
        "url": "https://196.218.246.250:4040/waiting-list/patient-internal-devices?ReservID=CfDJ8KcUxlP3wTpIkfqEIRtHon4HnOXKri8R-HuwQbLe0ga8sPk_YDBIi7MkseBrAScp2lyLKLKWd1FdbV1bx5vDnm0EQBpbwWI9QcH-t-umVvqBT7aeI7evEqn6rXp7YK12Xw&AccomID=CfDJ8KcUxlP3wTpIkfqEIRtHon6il3dFRgAMVI2R9iXr9AJ77pgneSuKHembPpKo7Y-WpjJgcXZaxrE0K-9uaDSgCs91FGvLxq1k6a3P6tJrXLC-GEMPIyzikQYqlb2CbLezAg&typ=1&flag=Durgs"
    },
    {
        "name": "patient_external_devices",
        "title": "أجهزة خارجية للمريض",
        "url": "https://196.218.246.250:4040/waiting-list/patient-external-devices?ReservID=CfDJ8KcUxlP3wTpIkfqEIRtHon4HnOXKri8R-HuwQbLe0ga8sPk_YDBIi7MkseBrAScp2lyLKLKWd1FdbV1bx5vDnm0EQBpbwWI9QcH-t-umVvqBT7aeI7evEqn6rXp7YK12Xw&AccomID=CfDJ8KcUxlP3wTpIkfqEIRtHon6il3dFRgAMVI2R9iXr9AJ77pgneSuKHembPpKo7Y-WpjJgcXZaxrE0K-9uaDSgCs91FGvLxq1k6a3P6tJrXLC-GEMPIyzikQYqlb2CbLezAg&typ=1&flag=Durgs"
    },
    {
        "name": "patient_diet",
        "title": "نظام غذائي للمريض",
        "url": "https://196.218.246.250:4040/waiting-list/patient-diet?ReservID=CfDJ8KcUxlP3wTpIkfqEIRtHon4HnOXKri8R-HuwQbLe0ga8sPk_YDBIi7MkseBrAScp2lyLKLKWd1FdbV1bx5vDnm0EQBpbwWI9QcH-t-umVvqBT7aeI7evEqn6rXp7YK12Xw&AccomID=CfDJ8KcUxlP3wTpIkfqEIRtHon6il3dFRgAMVI2R9iXr9AJ77pgneSuKHembPpKo7Y-WpjJgcXZaxrE0K-9uaDSgCs91FGvLxq1k6a3P6tJrXLC-GEMPIyzikQYqlb2CbLezAg&typ=1&flag=Durgs"
    }
]

os.makedirs("screenshots/inpatient_care_inspection", exist_ok=True)

opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--ignore-certificate-errors")
opts.add_argument("--window-size=1920,1080")
opts.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=opts)

# Set session cookies and token
session_data = json.load(open("session.json"))
token = session_data["token"]
cookies = session_data.get("cookies", {})

# Open base page first
driver.get("https://196.218.246.250:4040/home")
time.sleep(2)

# Set localStorage token
driver.execute_script(f"localStorage.setItem('baymax_token', '{token}');")
for k, v in cookies.items():
    try:
        driver.add_cookie({"name": k, "value": v, "domain": "196.218.246.250"})
    except Exception:
        pass

driver.get("https://196.218.246.250:4040/home")
time.sleep(2)

results = []

for idx, page in enumerate(PAGES_TO_INSPECT):
    print(f"\n[{idx+1}/{len(PAGES_TO_INSPECT)}] Inspecting: {page['name']} - {page['title']}")
    driver.get(page["url"])
    time.sleep(3)

    current_url = driver.current_url
    title = driver.title

    # Find elements with data-test-id
    test_ids = [el.get_attribute("data-test-id") for el in driver.find_elements(By.CSS_SELECTOR, "[data-test-id]")]
    # Filter unique non-empty
    test_ids = sorted(list(set(filter(None, test_ids))))

    # Find buttons
    buttons = [b.text.strip() for b in driver.find_elements(By.CSS_SELECTOR, "button, a.btn, input[type='button']") if b.text.strip()]

    # Find tables
    tables_count = len(driver.find_elements(By.TAG_NAME, "table"))

    # Screenshot
    shot_path = f"screenshots/inpatient_care_inspection/{page['name']}.png"
    driver.save_screenshot(shot_path)

    page_data = {
        "index": idx + 1,
        "name": page["name"],
        "title": page["title"],
        "url": page["url"],
        "current_url": current_url,
        "tables_count": tables_count,
        "test_ids": test_ids,
        "sample_buttons": buttons[:10],
        "screenshot": shot_path
    }
    results.append(page_data)
    print(f"  Current URL: {current_url}")
    print(f"  Tables found: {tables_count}")
    print(f"  Test IDs found ({len(test_ids)}): {test_ids[:8]}")
    print(f"  Buttons: {buttons[:5]}")

with open("scratch/inpatient_care_inspection.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

driver.quit()
print("\nInspection complete! Saved to scratch/inpatient_care_inspection.json")
