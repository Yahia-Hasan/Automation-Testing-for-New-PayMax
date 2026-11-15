import sys
import os
sys.path.insert(0, os.path.abspath("."))
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pages.legacy_login_page import LegacyLoginPage

sys.stdout.reconfigure(encoding='utf-8')

os.makedirs("screenshots/verified_pages", exist_ok=True)

options = Options()
options.add_argument("--headless=new")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-insecure-localhost")
options.add_argument("--disable-web-security")
options.add_argument("--start-maximized")
options.set_capability("acceptInsecureCerts", True)

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

def test_button_live(name: str, url: str, btn_selector: str, screenshot_name: str):
    print(f"\n==================================================================")
    print(f"VERIFYING: {name}")
    print(f"URL: {url}")
    driver.get(url)
    time.sleep(3)
    
    elements = driver.find_elements(By.CSS_SELECTOR, btn_selector)
    if not elements:
        print(f"  [NOT FOUND] Button selector '{btn_selector}' was not found on {url}")
        driver.save_screenshot(f"screenshots/verified_pages/{screenshot_name}_not_found.png")
        return None

    btn = elements[0]
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
    time.sleep(0.5)

    initial_text = btn.text.strip().replace('\n', ' ')
    initial_disabled = btn.get_attribute("disabled") is not None
    initial_classes = btn.get_attribute("class") or ""

    print(f"  Initial State: text='{initial_text}' | disabled={initial_disabled} | class='{initial_classes}'")

    # Monitor state during rapid 5 clicks
    script = """
        let btn = arguments[0];
        let states = [];
        for(let i=0; i<5; i++) {
            let b_dis = btn.disabled || btn.hasAttribute('disabled') || btn.classList.contains('disabled');
            let b_txt = btn.innerText.trim();
            try { btn.click(); } catch(e) {}
            let a_dis = btn.disabled || btn.hasAttribute('disabled') || btn.classList.contains('disabled');
            let a_txt = btn.innerText.trim();
            states.push({click: i+1, disabled_before: b_dis, disabled_after: a_dis, text_after: a_txt});
        }
        return states;
    """
    states = driver.execute_script(script, btn)
    time.sleep(1)

    driver.save_screenshot(f"screenshots/verified_pages/{screenshot_name}.png")

    post_text = btn.text.strip().replace('\n', ' ') if btn.is_displayed() else "(hidden/detached)"
    post_disabled = (btn.get_attribute("disabled") is not None) if btn.is_displayed() else False
    
    toasts = driver.find_elements(By.CSS_SELECTOR, ".toast-item, .toast-stack .msg, .toast-error-http-message")
    toast_texts = [t.text.strip().replace('\n', ' ') for t in toasts]

    entered_dis = any(s['disabled_after'] for s in states)
    text_changed = any(s['text_after'] != initial_text for s in states)

    print(f"  Post Spam State: text='{post_text}' | disabled={post_disabled}")
    print(f"  Entered Disabled During Clicks: {entered_dis}")
    print(f"  Text Changed to Loading ('يتم الحفظ'): {text_changed}")
    print(f"  Toasts Spawned: {len(toasts)} -> {toast_texts}")
    print(f"  Saved Screenshot: screenshots/verified_pages/{screenshot_name}.png")

    return {
        "name": name,
        "initial_disabled": initial_disabled,
        "entered_disabled": entered_dis,
        "post_disabled": post_disabled,
        "text_changed": text_changed,
        "toasts_count": len(toasts),
        "screenshot": f"screenshots/verified_pages/{screenshot_name}.png"
    }

try:
    print("[1] Logging into BayMax...")
    login_page = LegacyLoginPage(driver)
    login_page.login_full_flow("sysadmin", "Ma3an2025", "Ad Doqi")
    print("Logged in successfully!")

    results = []

    # 1. Reception Save Button
    res1 = test_button_live(
        name="Reception - Save Patient (اضافة)",
        url="https://196.218.246.250:4040/reception",
        btn_selector="[data-test-id='patient-data-save-btn']",
        screenshot_name="01_reception_save_btn"
    )
    if res1: results.append(res1)

    # 2. Reception Upload Document Button
    res2 = test_button_live(
        name="Reception - Upload Document (تحميل)",
        url="https://196.218.246.250:4040/reception",
        btn_selector="[data-test-id='patient-data-upload-document-btn']",
        screenshot_name="02_reception_upload_btn"
    )
    if res2: results.append(res2)

    # 3. OPD Clinic Visit Draft Save Button
    res3 = test_button_live(
        name="OPD Clinics - Draft Visit Save (حفظ كشف عيادة)",
        url="https://196.218.246.250:4040/clinic/visits/draft?patientCode=30855&clientId=52&mode=opd",
        btn_selector="[data-test-id='opd-visit-draft-save-btn']",
        screenshot_name="03_opd_visit_draft_save"
    )
    if res3: results.append(res3)

    # 4. Emergency Case Draft Save Button
    res4 = test_button_live(
        name="Emergency - Case Draft Save (حفظ زيارة طوارئ)",
        url="https://196.218.246.250:4040/emergency/cases/draft?patientCode=30856&clientId=52",
        btn_selector="[data-test-id='emergency-visit-draft-save-btn']",
        screenshot_name="04_emergency_draft_save"
    )
    if res4: results.append(res4)

    # 5. Patient Admission Save Button
    res5 = test_button_live(
        name="Inpatients - Admission Save (حفظ حجز داخلي)",
        url="https://196.218.246.250:4040/reception/patient/30854/admission",
        btn_selector="[data-test-id='patient-admission-save-btn']",
        screenshot_name="05_patient_admission_save"
    )
    if res5: results.append(res5)

    # 6. Patient Admission Add Surgery Button
    res6 = test_button_live(
        name="Inpatients - Admission Add Surgery (إضافة عملية)",
        url="https://196.218.246.250:4040/reception/patient/30854/admission",
        btn_selector="[data-test-id='patient-admission-add-surgery-btn']",
        screenshot_name="06_patient_admission_add_surgery"
    )
    if res6: results.append(res6)

    # 7. Physical Therapy Waiting List Search Button
    res7 = test_button_live(
        name="Physical Therapy - Waiting List Search (بحث علاج طبيعي)",
        url="https://196.218.246.250:4040/physical-therapy/waiting-list",
        btn_selector="[data-test-id='pt-waiting-list-search-btn']",
        screenshot_name="07_pt_waiting_search"
    )
    if res7: results.append(res7)

    # 8. Physical Therapy Export Excel Button
    res8 = test_button_live(
        name="Physical Therapy - Export Excel (تصدير إكسيل)",
        url="https://196.218.246.250:4040/physical-therapy/waiting-list",
        btn_selector="[data-test-id='pt-waiting-list-export-excel-btn']",
        screenshot_name="08_pt_export_excel"
    )
    if res8: results.append(res8)

    # 9. Inpatient Medical Reports Show Button
    res9 = test_button_live(
        name="Inpatient Medical Reports - Show (عرض تقرير طبي)",
        url="https://196.218.246.250:4040/waiting-list/medical-reports",
        btn_selector="[data-test-id='medical-reports-show-btn']",
        screenshot_name="09_medical_reports_show"
    )
    if res9: results.append(res9)

    print("\n\n" + "="*80)
    print("FINAL CONSOLIDATED LIVE VERIFICATION SUMMARY")
    print("="*80)
    for r in results:
        status = "SECURED (Disables)" if (r['entered_disabled'] or r['post_disabled'] or r['text_changed']) else "VULNERABLE (No Disable)"
        print(f"[{status}] {r['name']} | Toasts: {r['toasts_count']} | Screenshot: {r['screenshot']}")

finally:
    driver.quit()
