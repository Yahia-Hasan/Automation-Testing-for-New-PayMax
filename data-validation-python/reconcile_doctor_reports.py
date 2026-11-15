import time
import json
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.driver_factory import create_driver
from utils.auth import login_and_navigate_to_home

def set_date_inputs(driver, d_from, d_to):
    d_inps = driver.find_elements(By.CSS_SELECTOR, "input[type='date']")
    if len(d_inps) >= 2:
        driver.execute_script("""
            arguments[0].value = arguments[2];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            arguments[1].value = arguments[3];
            arguments[1].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[1].dispatchEvent(new Event('change', { bubbles: true }));
        """, d_inps[0], d_inps[1], d_from, d_to)
        time.sleep(0.5)

def wait_for_table(driver, max_wait=30):
    start = time.time()
    while time.time() - start < max_wait:
        tables = driver.find_elements(By.CSS_SELECTOR, "table")
        if tables:
            rows = tables[0].find_elements(By.CSS_SELECTOR, "tbody tr")
            if rows and len(rows) > 0:
                time.sleep(1)
                return tables[0]
        no_data = driver.find_elements(By.CSS_SELECTOR, ".empty-message, .no-data, .p-datatable-emptymessage")
        if no_data and no_data[0].is_displayed():
            return None
        time.sleep(1)
    return None

def query_doctor_report(driver, wait, route, name, date_from, date_to):
    print(f"\n---> Testing Doctor Report: {name} ({route}) [{date_from} to {date_to}]")
    res = {
        "name": name,
        "route": route,
        "date_from": date_from,
        "date_to": date_to,
        "rows_count": 0,
        "headers": [],
        "footer_raw": [],
        "sample_row": [],
        "status": "INIT"
    }

    try:
        driver.get(f"https://196.218.246.250:4040{route}")
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "header.top-navbar")))
        
        try:
            wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".filters-loading")))
        except:
            pass
        time.sleep(1)

        set_date_inputs(driver, date_from, date_to)

        btns = driver.find_elements(By.CSS_SELECTOR, "button.btn-query, .filters-card button.btn-primary, button:not(.nav-group-btn)")
        btn = None
        for b in btns:
            if "استعلام" in b.text or "بحث" in b.text:
                btn = b
                break
        if not btn:
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'استعلام')]")))

        btn.click()
        print("Clicked query, waiting for table results...")

        table = wait_for_table(driver, max_wait=25)
        
        if table is None:
            print("No data or timed out.")
            res["status"] = "NO_DATA_OR_TIMEOUT"
            return res

        res["headers"] = [th.text.strip() for th in table.find_elements(By.TAG_NAME, "th") if th.text.strip()]
        rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
        res["rows_count"] = len(rows)
        if rows:
            res["sample_row"] = [td.text.strip() for td in rows[0].find_elements(By.TAG_NAME, "td")]

        footers = table.find_elements(By.CSS_SELECTOR, "tfoot tr")
        if footers:
            res["footer_raw"] = [c.text.strip() for c in footers[0].find_elements(By.CSS_SELECTOR, "th, td")]
            print(f"Headers: {res['headers']}")
            print(f"Rows count: {res['rows_count']}")
            print(f"Footer totals: {res['footer_raw']}")
        else:
            print(f"Headers: {res['headers']}")
            print(f"Rows count: {res['rows_count']} (No explicit tfoot)")
        res["status"] = "SUCCESS"

    except Exception as e:
        print(f"Error querying {name}: {e}")
        res["status"] = f"ERROR: {e}"

    return res

def main():
    driver = create_driver()
    try:
        login_and_navigate_to_home(driver)
        wait = WebDriverWait(driver, 25)
        
        test_date = "2026-10-10"
        
        reports = [
            ("مرتبات الأطباء عن عمليات (داخلي) (Analytical 10)", "/reports/doctor-inpatient-surgery-salaries"),
            ("مرتبات اطباء العيادات (Analytical 11)", "/reports/opd-doctors-specialty-revenue"),
            ("أتعاب الأطباء (عيادات + عمليات) (Analytical 12)", "/reports/doctors-clinics-surgeries-fees"),
            ("اجمالي الايرادات بالتخصص و الطبيب (Analytical 09)", "/reports/doctors-departments-revenue"),
            ("أتعاب مرور الاستشاريين (General 02)", "/reports/doctor-fees-supervisors"),
            ("تسويات الأطباء (General 09)", "/reports/doctors-settlements")
        ]

        results = []
        for name, route in reports:
            r = query_doctor_report(driver, wait, route, name, test_date, test_date)
            results.append(r)

        print("\n================ FINAL DOCTOR RECONCILIATION ================")
        for r in results:
            print(f"{r['name']} --> Rows: {r['rows_count']} | Footer: {r['footer_raw']} | Status: {r['status']}")

        out_path = Path("discovery/patient/doctor_reconciliation_results.json")
        out_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nAll Doctor results saved to {out_path}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()

