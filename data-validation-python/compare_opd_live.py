import time
import json
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.driver_factory import create_driver
from utils.auth import login_and_navigate_to_home

def set_date_inputs(driver, date_from_str, date_to_str):
    """Safely updates HTML5 date inputs and fires Angular input & change events."""
    date_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='date']")
    if len(date_inputs) >= 2:
        driver.execute_script("""
            var d1 = arguments[0];
            var d2 = arguments[1];
            var v1 = arguments[2];
            var v2 = arguments[3];
            
            d1.value = v1;
            d1.dispatchEvent(new Event('input', { bubbles: true }));
            d1.dispatchEvent(new Event('change', { bubbles: true }));
            
            d2.value = v2;
            d2.dispatchEvent(new Event('input', { bubbles: true }));
            d2.dispatchEvent(new Event('change', { bubbles: true }));
        """, date_inputs[0], date_inputs[1], date_from_str, date_to_str)
        time.sleep(0.5)

def wait_for_report_results(driver, max_wait=30):
    """Waits for table results to appear and spinners to disappear."""
    start_time = time.time()
    while time.time() - start_time < max_wait:
        # Check if table exists with tbody rows
        tables = driver.find_elements(By.CSS_SELECTOR, "table")
        if tables:
            rows = tables[0].find_elements(By.CSS_SELECTOR, "tbody tr")
            if rows and len(rows) > 0:
                # Give Angular an extra half second to compute tfoot totals
                time.sleep(0.8)
                return tables[0]
        # Also check for empty data message like 'لا توجد بيانات'
        no_data = driver.find_elements(By.CSS_SELECTOR, ".empty-message, .no-data, .p-datatable-emptymessage")
        if no_data and no_data[0].is_displayed():
            return None
        time.sleep(1)
    return None

def query_opd_report(driver, wait, route, name, date_from, date_to):
    print(f"\n---> Testing: {name} ({route}) for period [{date_from} to {date_to}]")
    driver.get(f"https://196.218.246.250:4040{route}")
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "header.top-navbar")))
    
    # Wait for dynamic filters loading if present
    try:
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".filters-loading")))
    except:
        pass
    time.sleep(1)

    # Set dates
    set_date_inputs(driver, date_from, date_to)

    # Click Query button
    query_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-query")))
    query_btn.click()
    print("Clicked query, awaiting data rendering...")

    table = wait_for_report_results(driver, max_wait=20)
    
    result = {
        "report": name,
        "route": route,
        "date_from": date_from,
        "date_to": date_to,
        "rows_count": 0,
        "headers": [],
        "footer_raw": [],
        "parsed_totals": {},
        "status": "SUCCESS"
    }

    if table is None:
        print("No table or rows found (possible no data or timeout).")
        result["status"] = "NO_DATA_OR_TIMEOUT"
        return result

    headers = [th.text.strip() for th in table.find_elements(By.TAG_NAME, "th") if th.text.strip()]
    rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
    result["rows_count"] = len(rows)
    result["headers"] = headers

    # Extract footer totals
    footers = table.find_elements(By.CSS_SELECTOR, "tfoot tr")
    if footers:
        footer_cells = [c.text.strip() for c in footers[0].find_elements(By.CSS_SELECTOR, "th, td")]
        result["footer_raw"] = footer_cells
        print(f"Table Headers: {headers}")
        print(f"Rows count: {len(rows)}")
        print(f"Footer totals: {footer_cells}")
    else:
        print(f"Rows count: {len(rows)} (No explicit footer)")

    return result

def main():
    driver = create_driver()
    try:
        login_and_navigate_to_home(driver)
        wait = WebDriverWait(driver, 20)
        
        # Test 1: Today date (2026-11-08)
        target_date = "2026-11-08"
        reports_to_test = [
            ("/reports/opd-sales-report", "مبيعات العيادات اجمالى (Sales 05)"),
            ("/reports/opd-revenue-summary", "إيرادات العيادات الخارجية (Analytical 22)"),
            ("/reports/total-invoice-by-clinic", "اجمالى على مستوى العياده (General 15)"),
            ("/reports/clinics-case-count", "تقرير بعدد حالات العيادات (General 43)"),
            ("/reports/clinic-sales-in-period", "مبيعات العيادات (Sales 02)")
        ]

        all_results = []
        for route, name in reports_to_test:
            res = query_opd_report(driver, wait, route, name, target_date, target_date)
            all_results.append(res)

        # Save reconciliation data to file
        out_file = Path("discovery/patient/opd_reconciliation_results.json")
        out_file.write_text(json.dumps(all_results, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nAll results saved to: {out_file}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()

