import sys
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

import time
import os
import pytest
import logging
from typing import Dict, Any, List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.reception_page import ReceptionPage
from pages.clinic_visit_draft_page import ClinicVisitDraftPage
from pages.emergency_case_draft_page import EmergencyCaseDraftPage
from pages.patient_admission_page import PatientAdmissionPage
from pages.physical_therapy_page import PhysicalTherapyWaitingListPage
from pages.invoice_details_page import InvoiceDetailsPage
from pages.nursing_module_page import InpatientMedicalReportsPage

logger = logging.getLogger("BayMaxChaosDestructive")

def safe_str(val: Any) -> str:
    """Safely converts Arabic/Unicode strings for console output."""
    if val is None:
        return ""
    s = str(val)
    return s.encode(sys.stdout.encoding or 'utf-8', errors='replace').decode(sys.stdout.encoding or 'utf-8')

def spam_click_element(driver, element: WebElement, clicks: int = 5) -> Dict[str, Any]:
    """
    Executes multiple rapid clicks via JavaScript within milliseconds,
    tracking whether the element enters a disabled state or loading state.
    """
    script = """
        let btn = arguments[0];
        let clicks = arguments[1];
        let states = [];
        
        for (let i = 0; i < clicks; i++) {
            let disabledBefore = false;
            let isAriaBusyBefore = false;
            try {
                disabledBefore = btn.disabled || btn.hasAttribute('disabled') || btn.classList.contains('disabled');
                isAriaBusyBefore = btn.getAttribute('aria-busy') === 'true';
                btn.click();
            } catch(e) {}
            
            let disabledAfter = false;
            let isAriaBusyAfter = false;
            let classesAfter = '';
            try {
                disabledAfter = btn.disabled || btn.hasAttribute('disabled') || btn.classList.contains('disabled');
                isAriaBusyAfter = btn.getAttribute('aria-busy') === 'true';
                classesAfter = btn.className;
            } catch(e) {}
            
            states.push({
                iteration: i + 1,
                disabled_before: disabledBefore,
                disabled_after: disabledAfter,
                aria_busy: isAriaBusyAfter,
                classes: classesAfter
            });
        }
        let finalDisabled = false;
        try {
            finalDisabled = btn.disabled || btn.hasAttribute('disabled') || btn.classList.contains('disabled') || btn.getAttribute('aria-busy') === 'true';
        } catch(e) {}
        
        return {
            states: states,
            final_disabled: finalDisabled
        };
    """
    try:
        data = driver.execute_script(script, element, clicks)
        return {
            "clicks": clicks,
            "states": data.get("states", []),
            "is_disabled_after_spam": data.get("final_disabled", False),
            "entered_disabled_during_spam": any(s.get("disabled_after") for s in data.get("states", [])),
            "is_stale": False
        }
    except Exception as e:
        return {
            "clicks": clicks,
            "states": [],
            "is_disabled_after_spam": False,
            "entered_disabled_during_spam": False,
            "is_stale": True,
            "error": str(e)
        }

class TestChaosAndDestructiveUI:
    """
    Destructive, Edge-Case, and Concurrency Test Suite for BayMax Hospital ERP:
    1. Rapid Spam Clicking & Double-Submission.
    2. DOM Tampering with Prices & Readonly attributes.
    3. Time Paradox (Future/Ancient Birth Dates & Reversed Date Filters).
    """

    # =========================================================================
    # PART 1: RAPID SPAM CLICKING & DOUBLE-SUBMISSION TESTS
    # =========================================================================

    def test_01_rapid_click_reception_save(self, auth_driver):
        """
        [RAPID CLICK TEST]
        Open Reception and spam click 'اضافة' (Save Patient) 5 times in <50ms.
        Assert that the button should ideally disable, and document toast flooding.
        """
        rec_page = ReceptionPage(auth_driver).open()
        time.sleep(1)
        rec_page.click_new()
        time.sleep(0.5)

        save_btn = rec_page.find(rec_page.BTN_SAVE_PATIENT)
        auth_driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_btn)

        result = spam_click_element(auth_driver, save_btn, clicks=5)
        time.sleep(1)
        rec_page.take_screenshot("01_reception_save_spam", folder="chaos_destructive")

        toasts = auth_driver.find_elements(By.CSS_SELECTOR, ".toast-item, .toast-stack .msg, .toast-error-http-message")
        print("\n" + "="*70)
        print(safe_str("[CHAOS 01: RAPID CLICK - RECEPTION SAVE (اضافة)]"))
        print(f"Disabled After Spam: {result['is_disabled_after_spam']}")
        print(f"Entered Disabled During Spam: {result['entered_disabled_during_spam']}")
        print(f"Toasts Spawned: {len(toasts)}")
        print("="*70)

        # Defect confirmation: button was not disabled and spawned multiple toasts
        assert len(toasts) >= 1, "At least one validation toast must be present."

    def test_02_rapid_click_clinic_draft_visit(self, auth_driver):
        """
        [RAPID CLICK TEST]
        Open Outpatient Draft Visit and spam click 'حفظ وتسجيل الزيارة' 5 times.
        Verify if the button disables to prevent duplicate visit registrations.
        """
        draft_page = ClinicVisitDraftPage(auth_driver).open_for_patient(30855, 52)
        assert draft_page.is_loaded()

        save_btn = draft_page.find(draft_page.BTN_SAVE)
        auth_driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_btn)

        result = spam_click_element(auth_driver, save_btn, clicks=5)
        time.sleep(1)
        draft_page.take_screenshot("02_clinic_draft_save_spam", folder="chaos_destructive")

        toasts = auth_driver.find_elements(By.CSS_SELECTOR, ".toast-item, .toast-stack .msg, .toast-error-http-message")
        print("\n" + "="*70)
        print(safe_str("[CHAOS 02: RAPID CLICK - OPD CLINIC DRAFT SAVE (حفظ وتسجيل الزيارة)]"))
        print(f"Disabled After Spam: {result['is_disabled_after_spam']}")
        print(f"Entered Disabled During Spam: {result['entered_disabled_during_spam']}")
        print(f"Toasts Spawned: {len(toasts)}")
        print("="*70)

        assert len(toasts) >= 1

    def test_03_rapid_click_emergency_case_draft(self, auth_driver):
        """
        [RAPID CLICK TEST]
        Open Emergency Case Draft and spam click 'حفظ وتسجيل الزيارة' 5 times.
        Verify if the button disables or allows repeated submission triggers.
        """
        er_page = EmergencyCaseDraftPage(auth_driver).open_for_patient(30856, 52)
        assert er_page.is_loaded()

        save_btn = er_page.find(er_page.BTN_SAVE)
        auth_driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_btn)

        result = spam_click_element(auth_driver, save_btn, clicks=5)
        time.sleep(1)
        er_page.take_screenshot("03_emergency_draft_save_spam", folder="chaos_destructive")

        toasts = auth_driver.find_elements(By.CSS_SELECTOR, ".toast-item, .toast-stack .msg, .toast-error-http-message")
        print("\n" + "="*70)
        print(safe_str("[CHAOS 03: RAPID CLICK - EMERGENCY CASE DRAFT SAVE (حفظ وتسجيل الزيارة)]"))
        print(f"Disabled After Spam: {result['is_disabled_after_spam']}")
        print(f"Entered Disabled During Spam: {result['entered_disabled_during_spam']}")
        print(f"Toasts Spawned: {len(toasts)}")
        print("="*70)

        assert len(toasts) >= 1

    # =========================================================================
    # PART 2: PRICE & READONLY FIELD TAMPERING TESTS
    # =========================================================================

    def test_04_tampering_readonly_invoice_financial_totals(self, auth_driver):
        """
        [DOM TAMPERING TEST: FINANCIAL TOTALS]
        Open Invoice Details screen (rid=12746).
        Attempt to strip 'readonly'/'disabled' attributes from the patient total inputs
        and inject zero '0.00' or negative amount '-5000.00'.
        Verify whether frontend recalculates or protects the financial integrity.
        """
        inv_page = InvoiceDetailsPage(auth_driver)
        inv_page.open_for_reservation(12746)
        assert inv_page.is_loaded()

        # Find invoice total elements
        total_inputs = auth_driver.find_elements(By.CSS_SELECTOR, "input[data-test-id*='total'], input[data-test-id*='cash'], input[readonly]")
        
        tampered_count = 0
        if total_inputs:
            for inp in total_inputs[:3]:
                orig_val = inp.get_attribute("value") or ""
                is_ro_before = inp.get_attribute("readonly") is not None
                
                # Malicious JS tampering: remove readonly and force value to 0.01 EGP
                auth_driver.execute_script("""
                    let el = arguments[0];
                    el.removeAttribute('readonly');
                    el.removeAttribute('disabled');
                    el.value = '0.01';
                    el.dispatchEvent(new Event('input', {bubbles: true}));
                    el.dispatchEvent(new Event('change', {bubbles: true}));
                """, inp)
                time.sleep(0.3)
                
                new_val = inp.get_attribute("value")
                print(f"[DOM TAMPERING] Input: orig='{orig_val}' -> tampered='{new_val}', was_readonly={is_ro_before}")
                tampered_count += 1

        inv_page.take_screenshot("04_invoice_totals_tampered", folder="chaos_destructive")
        print("\n" + "="*70)
        print(safe_str(f"[CHAOS 04: PRICE & READONLY TAMPERING - Total Inputs Tested: {tampered_count}]"))
        print("="*70)
        assert inv_page.is_loaded()

    def test_05_tampering_negative_and_extreme_quantities(self, auth_driver):
        """
        [BOUNDARY & TAMPERING TEST: NEGATIVE QUANTITIES]
        Open Inpatient Admission (patient 30854).
        Inject extreme negative and astronomical values into numeric fields.
        Assert whether client-side form validation prevents negative numbers.
        """
        adm_page = PatientAdmissionPage(auth_driver).open_for_patient(30854)
        assert adm_page.is_admission_loaded()

        # Check phone / number inputs for negative injection
        phone_input = adm_page.find(adm_page.INPUT_RESPONSIBLE_PHONES)
        phone_input.clear()
        phone_input.send_keys("-999999999")
        time.sleep(0.5)

        val = phone_input.get_attribute("value")
        adm_page.take_screenshot("05_admission_negative_input", folder="chaos_destructive")

        print("\n" + "="*70)
        print(safe_str(f"[CHAOS 05: NEGATIVE INPUT INJECTION - Phone Field: '{val}']"))
        print("="*70)

    # =========================================================================
    # PART 3: TIME PARADOX (FUTURE/ANCIENT DATES & REVERSED FILTERS)
    # =========================================================================

    def test_06_future_birth_date_and_negative_age(self, auth_driver):
        """
        [TIME PARADOX TEST: FUTURE BIRTH DATE]
        Open Reception and click 'جديد'.
        Input a birth date in the future (e.g. 15/05/2035).
        Inspect how the system calculates age and whether it accepts or rejects it.
        """
        rec_page = ReceptionPage(auth_driver).open()
        time.sleep(1)
        rec_page.click_new()
        time.sleep(0.5)

        birth_input = auth_driver.find_element(By.CSS_SELECTOR, "[data-test-id='patient-data-birth-date-input']")
        age_years_input = auth_driver.find_element(By.CSS_SELECTOR, "[data-test-id='patient-data-age-years-input']")
        age_months_input = auth_driver.find_element(By.CSS_SELECTOR, "[data-test-id='patient-data-age-months-input']")

        # Enter future birth date: 2035-05-15
        birth_input.clear()
        birth_input.send_keys("05/15/2035")
        auth_driver.execute_script("arguments[0].dispatchEvent(new Event('input', {bubbles: true})); arguments[0].dispatchEvent(new Event('change', {bubbles: true}));", birth_input)
        time.sleep(1)

        age_years = age_years_input.get_attribute("value") or ""
        age_months = age_months_input.get_attribute("value") or ""
        birth_val = birth_input.get_attribute("value") or ""

        rec_page.take_screenshot("06_future_birth_date", folder="chaos_destructive")

        print("\n" + "="*70)
        print(safe_str("[CHAOS 06: TIME PARADOX - FUTURE BIRTH DATE]"))
        print(f"Injected Birth Date: '{birth_val}'")
        print(f"Calculated Age Years: '{age_years}'")
        print(f"Calculated Age Months: '{age_months}'")
        print("="*70)

        # Defect finding: Future date was accepted without immediate validation error
        is_future_accepted = (birth_val != "")
        print(f"[DEFECT FINDING] Future Birth Date Accepted by Input: {is_future_accepted}")
        assert is_future_accepted

    def test_07_ancient_birth_date_centuries_old(self, auth_driver):
        """
        [BOUNDARY TEST: ANCIENT BIRTH DATE]
        Input birth date 01/01/1850 (176 years old).
        Inspect how system handles upper age boundaries.
        """
        rec_page = ReceptionPage(auth_driver).open()
        time.sleep(0.5)

        birth_input = auth_driver.find_element(By.CSS_SELECTOR, "[data-test-id='patient-data-birth-date-input']")
        age_years_input = auth_driver.find_element(By.CSS_SELECTOR, "[data-test-id='patient-data-age-years-input']")

        birth_input.clear()
        birth_input.send_keys("01/01/1850")
        auth_driver.execute_script("arguments[0].dispatchEvent(new Event('input', {bubbles: true})); arguments[0].dispatchEvent(new Event('change', {bubbles: true}));", birth_input)
        time.sleep(1)

        age_years = age_years_input.get_attribute("value") or ""
        rec_page.take_screenshot("07_ancient_birth_date", folder="chaos_destructive")

        print("\n" + "="*70)
        print(safe_str("[CHAOS 07: TIME PARADOX - ANCIENT BIRTH DATE (1850)]"))
        print(f"Calculated Age Years: '{age_years}'")
        print("="*70)

        assert int(age_years) > 120, "System accepted ancient birth date and calculated age > 120 years."

    def test_08_reversed_date_filters_resilience(self, auth_driver):
        """
        [BOUNDARY & LOGIC TEST: REVERSED DATE FILTERS]
        Open Physical Therapy Waiting List (/physical-therapy/waiting-list).
        Set 'From Date' to 31/12/2026 and 'To Date' to 01/01/2026 (From Date > To Date).
        Click 'استعلام' (Search).
        Assert that the system does not crash or freeze the UI.
        """
        pt_page = PhysicalTherapyWaitingListPage(auth_driver).open()
        time.sleep(1)

        from_date_input = auth_driver.find_element(*pt_page.INPUT_FROM_DATE)
        to_date_input = auth_driver.find_element(*pt_page.INPUT_TO_DATE)
        search_btn = auth_driver.find_element(*pt_page.BTN_SEARCH)

        # Invert dates
        from_date_input.clear()
        from_date_input.send_keys("12/31/2026")
        to_date_input.clear()
        to_date_input.send_keys("01/01/2026")
        time.sleep(0.5)

        # Click search with reversed dates
        search_btn.click()
        time.sleep(2)

        pt_page.take_screenshot("08_reversed_dates_pt_search", folder="chaos_destructive")

        toasts = auth_driver.find_elements(By.CSS_SELECTOR, ".toast-item, .toast-stack .msg, .toast-error-http-message")
        print("\n" + "="*70)
        print(safe_str("[CHAOS 08: REVERSED DATE FILTERS - PHYSICAL THERAPY (From > To)]"))
        print(f"Toasts Spawned: {len(toasts)}")
        print("="*70)

        # System should remain responsive and not crash
        assert pt_page.is_loaded(), "Page must remain responsive and loaded after reversed date query."

    def test_09_reversed_dates_inpatient_medical_reports(self, auth_driver):
        """
        [BOUNDARY & LOGIC TEST: REVERSED DATES IN HEAVY REPORTS]
        Open Inpatient Medical Reports (/waiting-list/medical-reports).
        Set 'From Date' to future year 2027 and 'To Date' to past year 2025.
        Click 'عرض' (Show).
        Verify database resilience and query handling.
        """
        rep_page = InpatientMedicalReportsPage(auth_driver).open()
        time.sleep(1)

        from_input = auth_driver.find_element(*rep_page.INPUT_FROM_DATE)
        to_input = auth_driver.find_element(*rep_page.INPUT_TO_DATE)
        show_btn = auth_driver.find_element(*rep_page.BTN_SHOW)

        from_input.clear()
        from_input.send_keys("01/01/2027")
        to_input.clear()
        to_input.send_keys("01/01/2025")
        time.sleep(0.5)

        show_btn.click()
        time.sleep(2)

        rep_page.take_screenshot("09_reversed_dates_med_reports", folder="chaos_destructive")

        print("\n" + "="*70)
        print(safe_str("[CHAOS 09: REVERSED DATES IN MEDICAL REPORTS (2027 > 2025)]"))
        print(f"Page is loaded: {rep_page.is_loaded()}")
        print("="*70)

        assert rep_page.is_loaded(), "Reports screen must remain functional and not crash on inverted dates."
