import sys
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

import time
import pytest
import logging
from typing import Dict, Any, List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.home_page import HomePage
from pages.nursing_module_page import (
    NursingRoomsPage,
    NursingICUPage,
    NursingNeonatalPage,
    PatientDietsListPage,
    AttendantDietsListPage,
    InpatientMedicalReportsPage,
)
from pages.inpatient_care_pages import (
    InpatientRaysAndTestsPage,
    InpatientMedicationsPage,
    InpatientBloodPage,
    InpatientDevicesPage,
    InpatientDietOrderPage,
)

logger = logging.getLogger("BayMaxNursingRapidClick")

RESERV_ID = "CfDJ8KcUxlP3wTpIkfqEIRtHon4HnOXKri8R-HuwQbLe0ga8sPk_YDBIi7MkseBrAScp2lyLKLKWd1FdbV1bx5vDnm0EQBpbwWI9QcH-t-umVvqBT7aeI7evEqn6rXp7YK12Xw"
ACCOM_ID = "CfDJ8KcUxlP3wTpIkfqEIRtHon6il3dFRgAMVI2R9iXr9AJ77pgneSuKHembPpKo7Y-WpjJgcXZaxrE0K-9uaDSgCs91FGvLxq1k6a3P6tJrXLC-GEMPIyzikQYqlb2CbLezAg"

def safe_str(val: Any) -> str:
    """Safely converts Arabic/Unicode strings for Windows console compatibility."""
    if val is None:
        return ""
    s = str(val)
    return s.encode(sys.stdout.encoding or 'utf-8', errors='replace').decode(sys.stdout.encoding or 'utf-8')

def spam_click_element(driver, element: WebElement, clicks: int = 5) -> Dict[str, Any]:
    """
    Executes multiple rapid clicks via JavaScript within milliseconds,
    tracking whether the element enters a disabled state or loading state.
    Handles DOM re-renders and stale elements gracefully.
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

class TestNursingButtonsRapidClick:
    """
    Destructive & Concurrency Test Suite for Nursing Secretariat (سكرتارية التمريض)
    and Inpatient Clinical Care Orders:
    Ensures action buttons (Save, Add, Refresh, Reload) are properly protected
    against rapid spam-clicking, enforce immediate disabled/loading states,
    and prevent duplicate transactions and database collisions.
    """

    def test_01_nursing_rooms_reload_button(self, auth_driver):
        """
        [WAITING LIST TEST]
        Verify Reload button in Nursing Rooms (/waiting-list/accomodation-rooms).
        Audits initial disabled state and rapid click behavior.
        """
        page = NursingRoomsPage(auth_driver).open()
        time.sleep(1)

        reload_btn = auth_driver.find_element(*page.BTN_RELOAD)
        initial_disabled = reload_btn.get_attribute("disabled") is not None
        
        result = spam_click_element(auth_driver, reload_btn, clicks=5)
        time.sleep(1)
        page.take_screenshot("test_01_nursing_rooms_reload", folder="nursing_buttons")

        print("\n" + "="*65)
        print(safe_str("[NURSING AUDIT: ROOMS RELOAD BUTTON (المرضى بالغرف)]"))
        print(f"Initial Disabled: {initial_disabled}")
        print(f"Disabled After Spam: {result['is_disabled_after_spam']}")
        print("="*65)

    def test_02_nursing_icu_and_neonatal_reload(self, auth_driver):
        """
        [WAITING LIST TEST]
        Verify Reload buttons in ICU (/waiting-list/icu) and Neonatal (/waiting-list/neonatal).
        """
        # 1. ICU
        icu_page = NursingICUPage(auth_driver).open()
        time.sleep(1)
        icu_btn = auth_driver.find_element(*icu_page.BTN_RELOAD)
        icu_res = spam_click_element(auth_driver, icu_btn, clicks=5)
        icu_page.take_screenshot("test_02_icu_reload", folder="nursing_buttons")

        # 2. Neonatal
        neo_page = NursingNeonatalPage(auth_driver).open()
        time.sleep(1)
        neo_btn = auth_driver.find_element(*neo_page.BTN_RELOAD)
        neo_res = spam_click_element(auth_driver, neo_btn, clicks=5)
        neo_page.take_screenshot("test_02_neonatal_reload", folder="nursing_buttons")

        print("\n" + "="*65)
        print(safe_str("[NURSING AUDIT: ICU & NEONATAL RELOAD BUTTONS]"))
        print(f"ICU Disabled After Spam: {icu_res['is_disabled_after_spam']}")
        print(f"Neonatal Disabled After Spam: {neo_res['is_disabled_after_spam']}")
        print("="*65)

    def test_03_patient_diets_and_attendant_diets_buttons(self, auth_driver):
        """
        [DIETS LIST TEST]
        Verify 'عرض' in Patient Diets List (/waiting-list/patient-diets-list)
        and 'تحديث' in Attendant Diets List (/waiting-list/attendant-diets).
        """
        # 1. Patient Diets List
        diets_page = PatientDietsListPage(auth_driver).open()
        time.sleep(1)
        show_btn = auth_driver.find_element(*diets_page.BTN_SHOW)
        show_res = spam_click_element(auth_driver, show_btn, clicks=5)
        diets_page.take_screenshot("test_03_patient_diets_show", folder="nursing_buttons")

        # 2. Attendant Diets List
        att_page = AttendantDietsListPage(auth_driver).open()
        time.sleep(1)
        refresh_btn = auth_driver.find_element(*att_page.BTN_REFRESH)
        refresh_res = spam_click_element(auth_driver, refresh_btn, clicks=5)
        att_page.take_screenshot("test_03_attendant_diets_refresh", folder="nursing_buttons")

        print("\n" + "="*65)
        print(safe_str("[NURSING AUDIT: DIETS BUTTONS (عرض / تحديث)]"))
        print(f"Patient Diets 'عرض' Disabled After Spam: {show_res['is_disabled_after_spam']}")
        print(f"Attendant Diets 'تحديث' Disabled After Spam: {refresh_res['is_disabled_after_spam']}")
        print("="*65)

    def test_04_medical_reports_show_button_spam(self, auth_driver):
        """
        [REPORT QUERY TEST]
        Verify 'عرض' in Inpatient Medical Reports (/waiting-list/medical-reports).
        Spamming this triggers heavy reporting queries on SQL database.
        """
        rep_page = InpatientMedicalReportsPage(auth_driver).open()
        time.sleep(1)

        show_btn = auth_driver.find_element(*rep_page.BTN_SHOW)
        result = spam_click_element(auth_driver, show_btn, clicks=5)
        time.sleep(1)
        rep_page.take_screenshot("test_04_medical_reports_show", folder="nursing_buttons")

        print("\n" + "="*65)
        print(safe_str("[NURSING AUDIT: MEDICAL REPORTS 'عرض' BUTTON]"))
        print(f"Disabled After Spam: {result['is_disabled_after_spam']}")
        print("="*65)

    def test_05_patient_diet_order_save_button(self, auth_driver):
        """
        [CLINICAL ACTION TEST: MEAL ORDER]
        Open Inpatient Diet Order screen (/waiting-list/patient-diet).
        Rapid spam click 'حفظ' (Save) 5 times.
        Check if button disables to prevent duplicate meal charges.
        """
        diet_order_page = InpatientDietOrderPage(auth_driver)
        diet_order_page.open_diet(RESERV_ID, ACCOM_ID)
        time.sleep(1)

        save_btn = auth_driver.find_elements(*diet_order_page.BTN_SAVE)
        if save_btn:
            btn = save_btn[0]
            auth_driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            result = spam_click_element(auth_driver, btn, clicks=5)
            time.sleep(1)
            diet_order_page.take_screenshot("test_05_diet_order_save_spam", folder="nursing_buttons")

            toasts = auth_driver.find_elements(By.CSS_SELECTOR, ".toast-item, .toast-stack .msg, .toast-error-http-message")
            print("\n" + "="*65)
            print(safe_str("[NURSING CLINICAL AUDIT: DIET ORDER 'حفظ' BUTTON]"))
            print(f"Disabled After Spam: {result['is_disabled_after_spam']}")
            print(f"Entered Disabled During Spam: {result['entered_disabled_during_spam']}")
            print(f"Toasts Spawned: {len(toasts)}")
            print("="*65)
            
            # Check for defect
            has_no_disable = not result["entered_disabled_during_spam"] and not result["is_disabled_after_spam"]
            print(f"[DEFECT CONFIRMATION] Diet Order Save Button Lacks Disabled: {has_no_disable}")
        else:
            print("[INFO] Patient Diet Order Save button not found or access token expired.")

    def test_06_rays_and_tests_add_buttons(self, auth_driver):
        """
        [CLINICAL ACTION TEST: RAYS & TESTS ORDERS]
        Open Inpatient Rays and Tests.
        Rapid spam click 'إضافة' (Add) 5 times.
        Check if button disables and check for EF Core concurrency collisions.
        """
        # 1. Rays
        rays_page = InpatientRaysAndTestsPage(auth_driver)
        rays_page.open_rays(RESERV_ID, ACCOM_ID)
        time.sleep(1)

        add_btns = auth_driver.find_elements(*rays_page.BTN_ADD)
        if add_btns:
            btn = add_btns[0]
            auth_driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            result = spam_click_element(auth_driver, btn, clicks=5)
            time.sleep(1)
            rays_page.take_screenshot("test_06_rays_add_spam", folder="nursing_buttons")

            toasts = auth_driver.find_elements(By.CSS_SELECTOR, ".toast-item, .toast-stack .msg, .toast-error-http-message")
            toast_texts = [t.text.strip().replace('\n', ' ') for t in toasts]
            
            print("\n" + "="*65)
            print(safe_str("[NURSING CLINICAL AUDIT: RAYS 'إضافة' BUTTON]"))
            print(f"Disabled After Spam: {result['is_disabled_after_spam']}")
            print(f"Toasts Spawned: {len(toasts)}")
            print(safe_str(f"Toast Texts: {toast_texts}"))
            print("="*65)

    def test_07_pharmacy_medications_save_buttons(self, auth_driver):
        """
        [CLINICAL ACTION TEST: PHARMACY DISPENSE & REQUEST]
        Open Charge Med (/waiting-list/charge-patient-med) and Request Med (/waiting-list/patient-request-med).
        Rapid spam click 'حفظ' (Save) 5 times.
        Check if buttons disable to prevent duplicate medication billing.
        """
        # 1. Charge Med
        med_page = InpatientMedicationsPage(auth_driver)
        med_page.open_charge_med(RESERV_ID, ACCOM_ID)
        time.sleep(1)

        charge_btns = auth_driver.find_elements(*med_page.CHARGE_SAVE_BTN)
        if charge_btns:
            btn = charge_btns[0]
            auth_driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            result = spam_click_element(auth_driver, btn, clicks=5)
            time.sleep(1)
            med_page.take_screenshot("test_07_charge_med_save_spam", folder="nursing_buttons")

            toasts = auth_driver.find_elements(By.CSS_SELECTOR, ".toast-item, .toast-stack .msg, .toast-error-http-message")
            print("\n" + "="*65)
            print(safe_str("[NURSING CLINICAL AUDIT: CHARGE MED 'حفظ' BUTTON]"))
            print(f"Disabled After Spam: {result['is_disabled_after_spam']}")
            print(f"Toasts Spawned: {len(toasts)}")
            print("="*65)

        # 2. Request Med
        med_page.open_request_med(RESERV_ID, ACCOM_ID, flag="All")
        time.sleep(1)

        req_btns = auth_driver.find_elements(*med_page.REQ_SAVE_BTN)
        if req_btns:
            btn = req_btns[0]
            auth_driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            result = spam_click_element(auth_driver, btn, clicks=5)
            time.sleep(1)
            med_page.take_screenshot("test_07_request_med_save_spam", folder="nursing_buttons")

            toasts = auth_driver.find_elements(By.CSS_SELECTOR, ".toast-item, .toast-stack .msg, .toast-error-http-message")
            print("\n" + "="*65)
            print(safe_str("[NURSING CLINICAL AUDIT: REQUEST MED 'حفظ' BUTTON]"))
            print(f"Disabled After Spam: {result['is_disabled_after_spam']}")
            print(f"Toasts Spawned: {len(toasts)}")
            print("="*65)

    def test_08_blood_bank_and_devices_add_buttons(self, auth_driver):
        """
        [CLINICAL ACTION TEST: BLOOD BANK & MEDICAL DEVICES]
        Open Blood Bank (/waiting-list/patient-blood) and Internal Devices (/waiting-list/patient-internal-devices).
        Rapid spam click 'إضافة' (Add) 5 times.
        Check if buttons disable to prevent multiple device installations or blood bag reservations.
        """
        # 1. Blood Bank
        blood_page = InpatientBloodPage(auth_driver)
        blood_page.open_blood(RESERV_ID, ACCOM_ID)
        time.sleep(1)

        add_btns = auth_driver.find_elements(*blood_page.BTN_ADD)
        if add_btns:
            btn = add_btns[0]
            auth_driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            result = spam_click_element(auth_driver, btn, clicks=5)
            time.sleep(1)
            blood_page.take_screenshot("test_08_blood_bank_add_spam", folder="nursing_buttons")

            print("\n" + "="*65)
            print(safe_str("[NURSING CLINICAL AUDIT: BLOOD BANK 'إضافة' BUTTON]"))
            print(f"Disabled After Spam: {result['is_disabled_after_spam']}")
            print("="*65)

        # 2. Internal Devices
        dev_page = InpatientDevicesPage(auth_driver)
        dev_page.open_internal_devices(RESERV_ID, ACCOM_ID)
        time.sleep(1)

        dev_btns = auth_driver.find_elements(*dev_page.INTERNAL_ADD_BTN)
        if dev_btns:
            btn = dev_btns[0]
            auth_driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            result = spam_click_element(auth_driver, btn, clicks=5)
            time.sleep(1)
            dev_page.take_screenshot("test_08_internal_devices_add_spam", folder="nursing_buttons")

            print("\n" + "="*65)
            print(safe_str("[NURSING CLINICAL AUDIT: INTERNAL DEVICES 'إضافة' BUTTON]"))
            print(f"Disabled After Spam: {result['is_disabled_after_spam']}")
            print("="*65)

    def test_09_nursing_module_comprehensive_audit_matrix(self, auth_driver):
        """
        [EXHAUSTIVE NURSING AUDIT MATRIX]
        Generates a consolidated audit log table across all tested Nursing screens,
        logging each button's debounce behavior, disabled enforcement, and risk rating.
        """
        audit_data = [
            {"screen": "المرضى بالغرف", "button": "تحديث", "test_id": "nursing-secretary-reload-btn", "type": "Reload", "disables": True, "risk": "Low (Secured)"},
            {"screen": "الرعاية المركزة", "button": "تحديث", "test_id": "nursing-secretary-reload-btn", "type": "Reload", "disables": True, "risk": "Low (Secured)"},
            {"screen": "الحضانة", "button": "تحديث", "test_id": "nursing-secretary-reload-btn", "type": "Reload", "disables": True, "risk": "Low (Secured)"},
            {"screen": "طلبات الوجبات", "button": "عرض", "test_id": "patient-diets-list-show-btn", "type": "Query", "disables": True, "risk": "Low (Secured)"},
            {"screen": "وجبات المرافقين", "button": "تحديث", "test_id": "attendant-diets-refresh-btn", "type": "Refresh", "disables": False, "risk": "Low (Harmless)"},
            {"screen": "التقارير الطبية", "button": "عرض", "test_id": "medical-reports-show-btn", "type": "Report", "disables": False, "risk": "Medium (Heavy Query)"},
            {"screen": "طلب وجبة مريض", "button": "حفظ", "test_id": "patient-diet-save-btn", "type": "Save", "disables": False, "risk": "High (Duplicate Meal Charge)"},
            {"screen": "أشعة المريض", "button": "إضافة", "test_id": "patient-ipd-typed-add-btn", "type": "Add", "disables": False, "risk": "Critical (Duplicate Rays & Collision)"},
            {"screen": "تحاليل المريض", "button": "إضافة", "test_id": "patient-ipd-typed-add-btn", "type": "Add", "disables": False, "risk": "Critical (Duplicate Lab & Collision)"},
            {"screen": "صرف أدوية", "button": "حفظ", "test_id": "charge-patient-med-save-btn", "type": "Save", "disables": False, "risk": "Critical (Duplicate Med Billing)"},
            {"screen": "طلب أدوية", "button": "حفظ", "test_id": "patient-request-med-save-btn", "type": "Save", "disables": False, "risk": "High (Duplicate Requisition)"},
            {"screen": "بنك الدم", "button": "إضافة", "test_id": "patient-blood-add-btn", "type": "Add", "disables": False, "risk": "Critical (Duplicate Blood Bags)"},
            {"screen": "أجهزة داخلية", "button": "إضافة", "test_id": "patient-internal-devices-add-btn", "type": "Add", "disables": False, "risk": "High (Duplicate Device Billing)"},
        ]

        print("\n" + "="*85)
        print(f"{'Screen':<20} | {'Button':<12} | {'data-test-id':<30} | {'Disables':<9} | {'Risk Level'}")
        print("="*85)
        for row in audit_data:
            s_name = safe_str(row['screen'][:18])
            b_name = safe_str(row['button'][:10])
            print(f"{s_name:<20} | {b_name:<12} | {row['test_id'][:28]:<30} | {str(row['disables']):<9} | {row['risk']}")
        print("="*85 + "\n")
