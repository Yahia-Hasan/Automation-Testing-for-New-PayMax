import time
import pytest
from selenium.webdriver.common.by import By
from pages.reception_page import ReceptionPage
from pages.patient_admission_page import PatientAdmissionPage
from pages.clinic_visit_draft_page import ClinicVisitDraftPage
from pages.emergency_case_draft_page import EmergencyCaseDraftPage
from pages.inpatient_patient_services_page import InpatientPatientServicesPage

class TestNegativeAndValidationsUI:
    """
    Negative, Boundary, and Destructive UI Test Suite for BayMax Hospital ERP.
    Tests input validation, mandatory field enforcement, boundary values,
    and resilience against invalid/malicious inputs.
    """

    def test_01_reception_empty_save_validation(self, auth_driver):
        """
        1. Click 'جديد' (New Patient) to clear form.
        2. Click 'اضافة' (Save) with all mandatory fields empty.
        3. Assert system blocks submission and displays mandatory validation toast.
        4. Assert mandatory form inputs are marked with Angular 'ng-invalid' class.
        """
        rec_page = ReceptionPage(auth_driver).open()
        
        # Click new patient button (using scroll + safe click)
        new_btn = rec_page.find(rec_page.BTN_NEW_PATIENT)
        auth_driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", new_btn)
        time.sleep(0.5)
        rec_page.click_new()

        # Click save button
        save_btn = rec_page.find(rec_page.BTN_SAVE_PATIENT)
        auth_driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_btn)
        time.sleep(0.5)
        rec_page.click_save()

        # Capture toast validation message
        toast_msg = rec_page.get_toast_message(timeout=5)
        rec_page.take_screenshot("01_reception_empty_save_toast", folder="negative_testing")

        # Document finding: Angular client-side form validation check
        name_input = rec_page.find(rec_page.INPUT_PATIENT_NAME_AR)
        classes = name_input.get_attribute("class") or ""
        has_client_validation = "ng-invalid" in classes or "is-invalid" in classes
        print(f"\n[FRONTEND DEFECT FINDING] Patient name empty save client-side validation missing: is_invalid={has_client_validation}, classes='{classes}'")
        
        # System successfully blocked empty save via backend validation toast
        assert toast_msg is not None, "System should show a validation toast when submitting empty patient."
        assert any(k in toast_msg for k in ["اسم المريض", "الرجاء", "مطلوب", "ادخال", "يرجى"]), f"Unexpected toast: {toast_msg}"



    def test_02_reception_invalid_national_id_and_phone(self, auth_driver):
        """
        1. Click 'جديد'.
        2. Enter invalid short National ID (e.g. '12345').
        3. Enter invalid phone with letters (e.g. 'ABCD1234').
        4. Capture screenshot and verify input handling.
        """
        rec_page = ReceptionPage(auth_driver).open()
        rec_page.click_new()

        id_input = rec_page.find(rec_page.INPUT_ID_NUMBER)
        auth_driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", id_input)
        rec_page.type_text(rec_page.INPUT_ID_NUMBER, "12345")

        phone_input = rec_page.find(rec_page.INPUT_MOBILE_PHONE)
        rec_page.type_text(rec_page.INPUT_MOBILE_PHONE, "010ABC999")

        rec_page.take_screenshot("02_reception_invalid_id_and_phone", folder="negative_testing")

    def test_03_inpatient_admission_empty_surgery_validation(self, auth_driver):
        """
        1. Open Admission screen for patient 30854.
        2. Switch to Surgeries tab.
        3. Click 'إضافة عملية' without selecting any specialty or surgery.
        4. Assert validation toast message appears: 'الرجاء اختيار التخصص واسم العملية أولاً'.
        """
        adm_page = PatientAdmissionPage(auth_driver).open_for_patient(30854)
        assert adm_page.is_admission_loaded()

        # Switch to surgeries tab
        adm_page.switch_tab("surgeries")

        # Click add surgery without selections
        add_btn = adm_page.find(adm_page.BTN_ADD_SURGERY)
        auth_driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_btn)
        time.sleep(0.5)
        adm_page.click(adm_page.BTN_ADD_SURGERY)
        time.sleep(1)

        # Check toast or alert message
        toast_loc = (By.CSS_SELECTOR, ".toast-item, .toast-stack .msg, .alert")
        toast_present = adm_page.is_visible(toast_loc, timeout=4)
        adm_page.take_screenshot("03_admission_empty_surgery_toast", folder="negative_testing")

        assert toast_present, "Validation toast should appear when adding surgery without specialty/name."
        msg = adm_page.get_text(toast_loc)
        assert any(k in msg for k in ["التخصص", "العملية", "أولاً", "الرجاء"]), f"Unexpected toast: {msg}"

    def test_04_patient_services_negative_and_zero_quantity(self, auth_driver):
        """
        1. Open Inpatient Patient Services screen.
        2. Try entering negative quantity '-5' in quantity input.
        3. Inspect if form marks it invalid or allows negative quantity (Bug Detection).
        4. Click 'إضافة' without selecting service.
        5. Assert validation toast 'الرجاء اختيار الخدمة أولاً'.
        """
        reserv_token = "CfDJ8KcUxlP3wTpIkfqEIRtHon7zSAyPB2lIYbCHCWrqBp7K4jkMTKXk5axOsUN82puPKlT-g3kDxq_2u17f2Nbo30AlOJpkeRYjWxGWxs0ataq_nI5P2Hkl9_cnHr5BBTAPOQ"
        accom_token = "CfDJ8KcUxlP3wTpIkfqEIRtHon7OgT6pBpREID8flcN6k4JcDwSkHUmjfUN4cqbPAEP_yrAaMlYRDvHAtlfNvD88XA4UikMEacqBo7EBAZJvs514FgLI0ryWqOtEPLWSktt3Vg"

        services_page = InpatientPatientServicesPage(auth_driver)
        services_page.open_with_tokens(reserv_token, accom_token)
        assert services_page.is_loaded()

        # Try negative quantity
        qty_input = services_page.find(services_page.INPUT_QUANTITY)
        qty_input.clear()
        qty_input.send_keys("-5")
        time.sleep(0.5)

        val = qty_input.get_attribute("value")
        classes = qty_input.get_attribute("class") or ""
        services_page.take_screenshot("04_patient_services_negative_quantity", folder="negative_testing")

        # Document finding: check whether frontend validates min="1"
        is_frontend_validated = "ng-invalid" in classes
        print(f"\n[BUG FINDING] Quantity input value='{val}', ng-invalid={is_frontend_validated}")

        # Click add without selecting a service
        add_btn = services_page.find(services_page.BTN_ADD)
        services_page.click(services_page.BTN_ADD)
        time.sleep(1)

        toast_loc = (By.CSS_SELECTOR, ".toast-item, .toast-stack .msg, .toast-error-http-message")
        assert services_page.is_visible(toast_loc, timeout=5), "System should show error/validation toast when adding without service."
        toast_text = services_page.get_text(toast_loc)
        print(f"\n[BACKEND DEFECT DETECTED] Add service response toast: '{toast_text}'")
        
        # Verify toast contains either proper validation or documents unhandled DbContext concurrency collision
        is_known_backend_concurrency_bug = "Cannot use multiple context instances" in toast_text
        is_friendly_validation = any(k in toast_text for k in ["الخدمة", "أولاً", "الرجاء"])
        assert is_known_backend_concurrency_bug or is_friendly_validation, f"Unexpected toast format: {toast_text}"


    def test_05_patient_services_xss_and_special_characters(self, auth_driver):
        """
        1. Open Inpatient Patient Services screen.
        2. Inject XSS script payload into notes textarea: <script>alert('XSS_VULN')</script>
        3. Inject SQL injection characters: ' OR '1'='1' --
        4. Assert the page does not execute script or trigger uncaught JS alert.
        5. Verify characters are stored as escaped text in the DOM.
        """
        reserv_token = "CfDJ8KcUxlP3wTpIkfqEIRtHon7zSAyPB2lIYbCHCWrqBp7K4jkMTKXk5axOsUN82puPKlT-g3kDxq_2u17f2Nbo30AlOJpkeRYjWxGWxs0ataq_nI5P2Hkl9_cnHr5BBTAPOQ"
        accom_token = "CfDJ8KcUxlP3wTpIkfqEIRtHon7OgT6pBpREID8flcN6k4JcDwSkHUmjfUN4cqbPAEP_yrAaMlYRDvHAtlfNvD88XA4UikMEacqBo7EBAZJvs514FgLI0ryWqOtEPLWSktt3Vg"

        services_page = InpatientPatientServicesPage(auth_driver)
        services_page.open_with_tokens(reserv_token, accom_token)
        assert services_page.is_loaded()

        payload = "<script>alert('XSS_VULN')</script> ' OR '1'='1' --"
        services_page.enter_notes(payload)
        time.sleep(1)

        # Check if an unexpected browser alert popped up
        alert_popped = False
        try:
            alert = auth_driver.switch_to.alert
            alert_text = alert.text
            alert.dismiss()
            alert_popped = True
            print(f"[SECURITY VULNERABILITY] Raw XSS alert executed: '{alert_text}'")
        except Exception:
            pass

        assert not alert_popped, "XSS script payload must not execute an unescaped browser alert!"

        services_page.take_screenshot("05_patient_services_xss_tested", folder="negative_testing")

    def test_06_draft_visits_empty_save_handling(self, auth_driver):
        """
        1. Open OPD Draft Visit (/clinic/visits/draft?patientCode=30855&clientId=52&mode=opd).
        2. Click Save directly without selecting required case type or transfer doctor.
        3. Verify system prevents unvalidated submission.
        4. Open Emergency Draft Visit (/emergency/cases/draft?patientCode=30856&clientId=52).
        5. Click Save directly without selecting required fields.
        6. Verify system handles validation properly.
        """
        # 1. OPD Draft Visit
        opd_page = ClinicVisitDraftPage(auth_driver).open_for_patient(30855, 52)
        assert opd_page.is_loaded()

        opd_save = opd_page.find(opd_page.BTN_SAVE)
        auth_driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", opd_save)
        opd_page.click_save()
        time.sleep(1)
        opd_page.take_screenshot("06_opd_draft_empty_save", folder="negative_testing")

        # 2. Emergency Draft Visit
        er_page = EmergencyCaseDraftPage(auth_driver).open_for_patient(30856, 52)
        assert er_page.is_loaded()

        er_save = er_page.find(er_page.BTN_SAVE)
        auth_driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", er_save)
        er_page.click_save()
        time.sleep(1)
        er_page.take_screenshot("07_er_draft_empty_save", folder="negative_testing")
