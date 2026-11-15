import time
import pytest
from pages.reception_page import ReceptionPage
from pages.patient_admission_page import PatientAdmissionPage
from pages.clinic_visit_draft_page import ClinicVisitDraftPage
from pages.emergency_case_draft_page import EmergencyCaseDraftPage

class TestDeepPatientVisitsUI:
    """
    Test suite for deep, nested patient visit workflows:
    1. Inpatient Admission (/reception/patient/{id}/admission)
    2. Outpatient Clinic Draft Visit (/clinic/visits/draft?patientCode={code}&clientId={id}&mode=opd)
    3. Emergency Case Draft Visit (/emergency/cases/draft?patientCode={code}&clientId={id})
    """

    def test_01_inpatient_admission_full_flow(self, auth_driver):
        """
        1. Access Inpatient Admission from Reception toolbar.
        2. Verify patient admission fields and responsible person form.
        3. Switch across all 5 sub-tabs (Rooms, ICU, Neonatal, Surgeries, Payments).
        4. Test navigation back to reception.
        """
        rec_page = ReceptionPage(auth_driver).open()
        patient_found = rec_page.search_and_select_patient("30854")
        assert patient_found, "Patient 30854 could not be found or selected in Reception search."

        # Click "حجز داخلي" toolbar button
        rec_page.open_patient_admission()

        adm_page = PatientAdmissionPage(auth_driver)
        assert adm_page.is_admission_loaded(), "Inpatient admission page failed to load."
        assert "/reception/patient/" in auth_driver.current_url and "/admission" in auth_driver.current_url

        # Check core form elements
        form_data = adm_page.get_admission_form_data()
        assert form_data is not None
        adm_page.take_screenshot("01_admission_overview")

        # Test "Same as patient" checkbox toggle
        adm_page.toggle_same_as_patient_checkbox()
        adm_page.take_screenshot("02_admission_same_as_patient_toggled")
        adm_page.toggle_same_as_patient_checkbox()

        # Switch across all 5 tabs and verify their contents
        # 1. Rooms
        adm_page.switch_tab("rooms")
        adm_page.take_screenshot("03_tab_rooms")

        # 2. ICU
        adm_page.switch_tab("icu")
        adm_page.take_screenshot("04_tab_icu")

        # 3. Neonatal
        adm_page.switch_tab("neonatal")
        adm_page.take_screenshot("05_tab_neonatal")

        # 4. Surgeries
        adm_page.switch_tab("surgeries")
        assert adm_page.is_visible(adm_page.SELECT_SURGERY_SPECIALTY, timeout=5), "Surgeries specialty select missing."
        assert adm_page.is_visible(adm_page.SELECT_SURGERY_NAME, timeout=5), "Surgeries name select missing."
        adm_page.take_screenshot("06_tab_surgeries")

        # 5. Payments
        adm_page.switch_tab("payments")
        assert adm_page.is_visible(adm_page.ALERT_PAYMENTS_SAVE_FIRST, timeout=5), "Payments warning alert should be displayed."
        adm_page.take_screenshot("07_tab_payments")

        # 6. Diagnosis Tab
        adm_page.switch_tab("diagnosis")
        adm_page.take_screenshot("08_tab_diagnosis")

        # 7. Attachments Tab
        adm_page.switch_tab("attachments")
        adm_page.take_screenshot("09_tab_attachments")

        # Test Print / Report menu
        adm_page.click_print_menu()
        adm_page.take_screenshot("10_print_menu_clicked")


        # Test Back button navigation
        adm_page.click_back()
        assert "/reception" in auth_driver.current_url, "Clicking back did not return to reception page."

    def test_02_outpatient_clinic_visit_draft(self, auth_driver):
        """
        1. Select patient 30855 in Reception.
        2. Click 'عيادات خارجية' toolbar button.
        3. Verify navigation to /clinic/visits/draft?patientCode=...&mode=opd.
        4. Validate dropdowns (case type, insurance company, transfer doctor, ICD).
        5. Verify buttons (Save, Cancel, Back).
        """
        rec_page = ReceptionPage(auth_driver).open()
        patient_found = rec_page.search_and_select_patient("30855")
        assert patient_found, "Patient 30855 could not be found or selected in Reception search."

        # Click "عيادات خارجية" button
        rec_page.open_patient_opd()

        opd_page = ClinicVisitDraftPage(auth_driver)
        assert opd_page.is_loaded(), "Outpatient visit draft page failed to load."
        assert "/clinic/visits/draft" in auth_driver.current_url
        assert "mode=opd" in auth_driver.current_url

        # Validate form dropdown controls
        assert opd_page.is_select_present(opd_page.SELECT_CASE_TYPE), "Case type select missing."
        assert opd_page.is_select_present(opd_page.SELECT_INS_COMPANY), "Insurance company select missing."
        assert opd_page.is_select_present(opd_page.SELECT_TRANSFER_DOCTOR), "Transfer doctor select missing."
        assert opd_page.is_select_present(opd_page.SELECT_ICD), "ICD select missing."

        opd_page.take_screenshot("01_clinic_visit_draft_loaded")

        # Test Back button navigation
        opd_page.click_back()
        assert "/reception" in auth_driver.current_url, "Clicking back did not return to reception page."

    def test_03_emergency_case_draft(self, auth_driver):
        """
        1. Select patient 30856 in Reception.
        2. Click 'إسعاف وطوارئ' toolbar button.
        3. Verify navigation to /emergency/cases/draft?patientCode=...
        4. Validate emergency form controls, dropdowns, and notes input.
        5. Test writing notes and returning via back button.
        """
        rec_page = ReceptionPage(auth_driver).open()
        patient_found = rec_page.search_and_select_patient("30856")
        assert patient_found, "Patient 30856 could not be found or selected in Reception search."

        # Click "إسعاف وطوارئ" button
        rec_page.open_patient_emergency()

        er_page = EmergencyCaseDraftPage(auth_driver)
        assert er_page.is_loaded(), "Emergency case draft page failed to load."
        assert "/emergency/cases/draft" in auth_driver.current_url

        # Validate form dropdown controls
        assert er_page.is_select_present(er_page.SELECT_CASE_TYPE), "Case type select missing."
        assert er_page.is_select_present(er_page.SELECT_DOCTOR), "Doctor select missing."
        assert er_page.is_select_present(er_page.SELECT_SPECIALTY), "Specialty select missing."
        assert er_page.is_select_present(er_page.SELECT_TRANSFER_DOCTOR), "Transfer doctor select missing."
        assert er_page.is_select_present(er_page.SELECT_INS_COMPANY), "Insurance company select missing."
        assert er_page.is_select_present(er_page.SELECT_ICD), "ICD select missing."

        # Enter notes
        er_page.enter_notes("مريض طوارئ - فحص سريري واختبارات معملية فورية")
        er_page.take_screenshot("01_emergency_case_draft_loaded")

        # Test Back button navigation
        er_page.click_back()
        assert "/reception" in auth_driver.current_url, "Clicking back did not return to reception page."
