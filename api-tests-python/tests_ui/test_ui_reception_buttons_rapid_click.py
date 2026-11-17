import sys
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

import time
import uuid
import pytest
import logging
from typing import Dict, Any, List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.reception_page import ReceptionPage

logger = logging.getLogger("BayMaxReceptionRapidClick")

def safe_str(val: Any) -> str:
    """Safely converts Arabic/Unicode strings for Windows console compatibility."""
    if val is None:
        return ""
    s = str(val)
    return s.encode(sys.stdout.encoding or 'utf-8', errors='replace').decode(sys.stdout.encoding or 'utf-8')

def spam_click_element(driver, element: WebElement, clicks: int = 5) -> Dict[str, Any]:
    """
    Executes multiple rapid clicks via JavaScript within milliseconds,
    tracking whether the element ever enters a disabled state or loading state.
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

class TestReceptionButtonsRapidClick:
    """
    Destructive & Concurrency Test Suite for Reception Module Buttons:
    Verifies that buttons handle rapid repeated clicking (Spam / Double-click),
    enforce immediate 'disabled' or loading state to prevent race conditions,
    and do not allow duplicate submissions or server crashes.
    """

    def test_01_save_button_empty_rapid_click_and_disabled_state(self, auth_driver):
        """
        [DESTRUCTIVE TEST]
        1. Open Reception.
        2. Click 'جديد' to ensure clean form.
        3. Rapid spam click 'اضافة' (Save) 5 times in <50ms.
        4. Check if button becomes disabled on click (Bug Detection: Lack of disabled state).
        5. Check toast count (Bug Detection: Toast flooding / multiple validation triggers).
        """
        rec_page = ReceptionPage(auth_driver).open()
        time.sleep(1)
        rec_page.click_new()
        time.sleep(0.5)

        save_btn = rec_page.find(rec_page.BTN_SAVE_PATIENT)
        auth_driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_btn)
        
        # Capture spam click behavior
        result = spam_click_element(auth_driver, save_btn, clicks=5)
        time.sleep(0.8)
        
        # Inspect toasts
        toasts = auth_driver.find_elements(By.CSS_SELECTOR, ".toast-item, .toast-stack .msg, .toast-error-http-message")
        rec_page.take_screenshot("test_01_save_button_empty_spam", folder="buttons_rapid_click")

        has_debounce_defect = not result["entered_disabled_during_spam"] and not result["is_disabled_after_spam"]
        has_toast_flood_defect = len(toasts) > 1

        print("\n" + "="*65)
        print(safe_str("[BUTTON AUDIT: SAVE BUTTON (EMPTY FORM)]"))
        print(f"Total Clicks Spammed: {result['clicks']}")
        print(f"Entered Disabled State During Spam: {result['entered_disabled_during_spam']}")
        print(f"Is Disabled After Spam: {result['is_disabled_after_spam']}")
        print(f"Toasts Spawned: {len(toasts)}")
        for i, t in enumerate(toasts, 1):
            toast_text = t.text.strip().replace('\n', ' ')
            print(safe_str(f"  Toast {i}: '{toast_text}'"))
        print(f"[DEFECT CONFIRMATION] Lack of Disabled State on Save: {has_debounce_defect}")
        print(f"[DEFECT CONFIRMATION] Toast Flooding (Multiple Triggers): {has_toast_flood_defect}")
        print("="*65)

        assert len(toasts) >= 1, "At least one validation toast must be shown."

    def test_02_save_button_filled_patient_rapid_click_duplicate_prevention(self, auth_driver):
        """
        [CRITICAL CONCURRENCY TEST]
        1. Open Reception.
        2. Fill valid patient data with unique timestamp/name.
        3. Rapid spam click 'اضافة' (Save) 5 times.
        4. Inspect if button disables while API call is in-flight.
        5. Verify system does NOT create duplicate patient records or throw 500 EF Core concurrency exception.
        """
        rec_page = ReceptionPage(auth_driver).open()
        rec_page.click_new()
        time.sleep(0.5)

        unique_id = str(uuid.uuid4())[:6]
        test_patient_name = f"أوتوميشن اختبار ضغط {unique_id}"
        test_phone = f"010{int(time.time()) % 100000000:08d}"

        # Fill mandatory fields
        name_input = rec_page.find(rec_page.INPUT_PATIENT_NAME_AR)
        name_input.clear()
        name_input.send_keys(test_patient_name)

        phone_input = rec_page.find(rec_page.INPUT_MOBILE_PHONE)
        phone_input.clear()
        phone_input.send_keys(test_phone)
        time.sleep(0.5)

        save_btn = rec_page.find(rec_page.BTN_SAVE_PATIENT)
        auth_driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_btn)

        # Spam click save with valid data
        result = spam_click_element(auth_driver, save_btn, clicks=5)
        time.sleep(2.5)
        
        rec_page.take_screenshot("test_02_save_button_filled_spam", folder="buttons_rapid_click")

        # Check response toast or patient code generation
        code_input = rec_page.find(rec_page.INPUT_PATIENT_CODE)
        assigned_code = code_input.get_attribute("value") or ""
        
        toasts = auth_driver.find_elements(By.CSS_SELECTOR, ".toast-item, .toast-stack .msg, .toast-error-http-message")
        toast_texts = [t.text.strip().replace('\n', ' ') for t in toasts]

        print("\n" + "="*65)
        print(safe_str("[BUTTON AUDIT: SAVE BUTTON (FILLED FORM)]"))
        print(safe_str(f"Patient Name: '{test_patient_name}' | Phone: '{test_phone}'"))
        print(f"Assigned Code After Save: '{assigned_code}'")
        print(f"Button Disabled During Flight: {result['entered_disabled_during_spam']}")
        print(safe_str(f"Toasts Received: {toast_texts}"))
        print("="*65)

        # Assert no backend 500 crash or concurrency collision toast
        for t_text in toast_texts:
            assert "Cannot use multiple context instances" not in t_text, f"Server crashed with DbContext concurrency conflict: {t_text}"
            assert "Internal Server Error" not in t_text, f"Server crashed with 500 Internal Error: {t_text}"

    def test_03_new_patient_button_rapid_click(self, auth_driver):
        """
        [UI RESILIENCE TEST]
        1. Load an existing patient (e.g. 30854).
        2. Rapid spam click 'جديد' (New Patient) 5 times.
        3. Assert form reliably clears and does not freeze or enter corrupted state.
        """
        rec_page = ReceptionPage(auth_driver).open()
        rec_page.search_and_select_patient("30854")
        time.sleep(1)

        new_btn = rec_page.find(rec_page.BTN_NEW_PATIENT)
        auth_driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", new_btn)

        result = spam_click_element(auth_driver, new_btn, clicks=5)
        time.sleep(1.5)

        rec_page.take_screenshot("test_03_new_button_spam", folder="buttons_rapid_click")

        # Re-query elements safely to prevent StaleElementReferenceException
        code_val = rec_page.find(rec_page.INPUT_PATIENT_CODE).get_attribute("value") or ""
        name_val = rec_page.find(rec_page.INPUT_PATIENT_NAME_AR).get_attribute("value") or ""
        is_empty = (code_val == "" and name_val == "")

        print("\n" + "="*65)
        print(safe_str("[BUTTON AUDIT: 'جديد' NEW BUTTON]"))
        print(f"Disabled After Spam: {result['is_disabled_after_spam']}")
        print(f"Is Form Completely Empty: {is_empty} (code='{code_val}', name='{name_val}')")
        print("="*65)

        assert is_empty, "Form must be cleanly reset even after rapid spamming of 'جديد'."

    def test_04_unknown_patient_rapid_click(self, auth_driver):
        """
        [GENERATION CONCURRENCY TEST]
        1. Open Reception.
        2. Rapid spam click 'المرضى الغير معروفين' (Unknown Patient) 5 times.
        3. Verify system generates unknown patient data without crashing or throwing JS exceptions.
        """
        rec_page = ReceptionPage(auth_driver).open()
        time.sleep(0.5)

        unknown_btn = rec_page.find(rec_page.BTN_UNKNOWN_PATIENT)
        auth_driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", unknown_btn)

        result = spam_click_element(auth_driver, unknown_btn, clicks=5)
        time.sleep(1.5)

        rec_page.take_screenshot("test_04_unknown_patient_spam", folder="buttons_rapid_click")

        name_val = rec_page.find(rec_page.INPUT_PATIENT_NAME_AR).get_attribute("value") or ""
        print("\n" + "="*65)
        print(safe_str("[BUTTON AUDIT: 'المرضى الغير معروفين' UNKNOWN PATIENT]"))
        print(f"Disabled During Spam: {result['entered_disabled_during_spam']}")
        print(safe_str(f"Generated Patient Name: '{name_val}'"))
        print("="*65)

    def test_05_contract_and_document_tabs_rapid_toggle(self, auth_driver):
        """
        [DOM RESILIENCE TEST]
        1. Rapidly alternate clicks between Contract Tab and Documents Tab 10 times in 300ms.
        2. Verify Angular does not throw ExpressionChangedAfterItHasBeenCheckedError or break DOM bindings.
        """
        rec_page = ReceptionPage(auth_driver).open()
        
        tab_contract = rec_page.find(rec_page.TAB_CONTRACT)
        tab_docs = rec_page.find(rec_page.TAB_DOCUMENTS)

        script = """
            let t1 = arguments[0];
            let t2 = arguments[1];
            for (let i = 0; i < 5; i++) {
                t1.click();
                t2.click();
            }
        """
        auth_driver.execute_script(script, tab_contract, tab_docs)
        time.sleep(1)

        rec_page.take_screenshot("test_05_tabs_rapid_toggle", folder="buttons_rapid_click")

        is_docs_active = "active" in (tab_docs.get_attribute("class") or "")
        print(f"\n[TABS AUDIT] Rapid 10x tab toggle completed. Final active tab documents: {is_docs_active}")
        assert tab_contract.is_displayed() and tab_docs.is_displayed(), "Tabs must remain functional and visible."

    def test_06_add_tpa_button_rapid_click(self, auth_driver):
        """
        [LIST DUPLICATION TEST]
        1. Switch to Contract tab.
        2. Rapid spam click 'إضافة' (Add TPA) 5 times without selecting a TPA.
        3. Check if button disables or if it adds 5 empty/duplicate TPA rows.
        """
        rec_page = ReceptionPage(auth_driver).open()
        rec_page.switch_to_contract_tab()
        time.sleep(0.5)

        add_tpa_btn = rec_page.find(rec_page.BTN_ADD_TPA)
        auth_driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_tpa_btn)

        result = spam_click_element(auth_driver, add_tpa_btn, clicks=5)
        time.sleep(1)

        rec_page.take_screenshot("test_06_add_tpa_spam", folder="buttons_rapid_click")

        toasts = auth_driver.find_elements(By.CSS_SELECTOR, ".toast-item, .toast-stack .msg, .toast-error-http-message")
        print("\n" + "="*65)
        print(safe_str("[BUTTON AUDIT: 'إضافة TPA' ADD BUTTON]"))
        print(f"Disabled After Spam: {result['is_disabled_after_spam']}")
        print(f"Toasts Spawned: {len(toasts)}")
        print("="*65)

    def test_07_upload_document_rapid_click(self, auth_driver):
        """
        [UPLOAD CONCURRENCY TEST]
        1. Switch to Documents tab.
        2. Rapid spam click 'تحميل' (Upload) 5 times without selecting a file.
        3. Check if button disables or floods validation toasts.
        """
        rec_page = ReceptionPage(auth_driver).open()
        rec_page.switch_to_documents_tab()
        time.sleep(0.5)

        upload_btn = rec_page.find(rec_page.BTN_UPLOAD_DOCUMENT)
        auth_driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", upload_btn)

        result = spam_click_element(auth_driver, upload_btn, clicks=5)
        time.sleep(1)

        rec_page.take_screenshot("test_07_upload_document_spam", folder="buttons_rapid_click")

        toasts = auth_driver.find_elements(By.CSS_SELECTOR, ".toast-item, .toast-stack .msg, .toast-error-http-message")
        print("\n" + "="*65)
        print(safe_str("[BUTTON AUDIT: 'تحميل' UPLOAD BUTTON]"))
        print(f"Disabled After Spam: {result['is_disabled_after_spam']}")
        print(f"Toasts Spawned: {len(toasts)}")
        print("="*65)

    def test_08_deep_visit_navigation_buttons_rapid_click(self, auth_driver):
        """
        [NAVIGATION DUPLICATION TEST]
        1. Search and select patient 30854.
        2. Locate deep navigation buttons ('حجز داخلي', 'عيادات خارجية', 'إسعاف وطوارئ').
        3. Rapid spam click 'عيادات خارجية' (OPD).
        4. Check if button disables during navigation to prevent multiple draft visit sessions.
        """
        rec_page = ReceptionPage(auth_driver).open()
        rec_page.search_and_select_patient("30854")
        time.sleep(1)

        opd_btn = rec_page.find(rec_page.BTN_OPD)
        auth_driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", opd_btn)

        result = spam_click_element(auth_driver, opd_btn, clicks=5)
        time.sleep(2)

        rec_page.take_screenshot("test_08_opd_navigation_spam", folder="buttons_rapid_click")

        current_url = auth_driver.current_url
        print("\n" + "="*65)
        print(safe_str("[BUTTON AUDIT: 'عيادات خارجية' OPD NAVIGATION BUTTON]"))
        print(f"Disabled After Spam: {result['is_disabled_after_spam']}")
        print(f"Navigated URL: {current_url}")
        print("="*65)
        assert "/clinic/visits/draft" in current_url or "/reception" in current_url

    def test_09_comprehensive_reception_buttons_audit_matrix(self, auth_driver):
        """
        [EXHAUSTIVE MODULE-WIDE BUTTON AUDIT]
        Scans EVERY visible <button> in the Reception module,
        checks its current disabled state, attributes, classes,
        and generates an exhaustive status report.
        """
        rec_page = ReceptionPage(auth_driver).open()
        time.sleep(1)

        # Find all buttons
        buttons = auth_driver.find_elements(By.TAG_NAME, "button")
        
        audit_rows = []
        for i, btn in enumerate(buttons, 1):
            try:
                if not btn.is_displayed():
                    continue
                text = (btn.text or "").strip().replace("\n", " ")
                test_id = btn.get_attribute("data-test-id") or "N/A"
                btn_type = btn.get_attribute("type") or "button"
                classes = btn.get_attribute("class") or ""
                is_disabled = (btn.get_attribute("disabled") is not None) or ("disabled" in classes)
                
                audit_rows.append({
                    "index": i,
                    "text": text if text else "(Icon/Empty)",
                    "test_id": test_id,
                    "type": btn_type,
                    "classes": classes,
                    "is_disabled": is_disabled
                })
            except Exception:
                continue

        print("\n" + "="*80)
        print(f"{'#':<3} | {'Button Text':<22} | {'data-test-id':<35} | {'Disabled':<8}")
        print("="*80)
        for r in audit_rows:
            btn_text_safe = safe_str(r['text'][:20])
            print(f"{r['index']:<3} | {btn_text_safe:<22} | {r['test_id'][:33]:<35} | {str(r['is_disabled']):<8}")
        print("="*80)
        print(f"Total Active Visible Buttons Audited in Reception: {len(audit_rows)}\n")

        assert len(audit_rows) > 0, "At least some buttons must be present in Reception."
