import pytest
from pages.home_page import HomePage
from pages.clinics_module_page import (
    ClinicWaitingListPage,
    ClinicVisitDetailsReportPage,
    ClinicPatientsPage,
    ClinicEditVisitPage,
    ClinicCancelLeavedVisitPage,
    ClinicMedicalReportsPage,
)

class TestClinicsModuleUI:
    """UI Test Suite covering all 6 Outpatient Clinics module screens."""

    def test_01_clinic_waiting_list(self, auth_driver):
        """1. Verify Clinic Waiting List (/clinic/waiting-list)."""
        home = HomePage(auth_driver).open()
        home.open_clinic_waiting()

        page = ClinicWaitingListPage(auth_driver)
        assert page.is_loaded(), "Clinic waiting list page failed to load."
        assert "/clinic/waiting-list" in auth_driver.current_url

        page.click_search()
        page.take_screenshot("test_clinic_waiting_searched")

    def test_02_clinic_details_report(self, auth_driver):
        """2. Verify Detailed Clinic Report (/clinic/visit-details-report)."""
        home = HomePage(auth_driver).open()
        home.open_clinic_details_report()

        page = ClinicVisitDetailsReportPage(auth_driver)
        assert page.is_loaded(), "Clinic visit details report failed to load."
        assert "/clinic/visit-details-report" in auth_driver.current_url

        page.click_search()
        page.take_screenshot("test_clinic_details_searched")

    def test_03_clinic_patients(self, auth_driver):
        """3. Verify Patients in Clinics (/clinic/patients)."""
        home = HomePage(auth_driver).open()
        home.open_clinic_patients()

        page = ClinicPatientsPage(auth_driver)
        assert page.is_loaded(), "Clinic patients page failed to load."
        assert "/clinic/patients" in auth_driver.current_url

        page.click_search()
        page.take_screenshot("test_clinic_patients_searched")

    def test_04_clinic_edit_visit(self, auth_driver):
        """4. Verify Edit Clinic Visit (/clinic/edit-visit)."""
        home = HomePage(auth_driver).open()
        home.open_clinic_edit_visit()

        page = ClinicEditVisitPage(auth_driver)
        assert page.is_loaded(), "Clinic edit visit page failed to load."
        assert "/clinic/edit-visit" in auth_driver.current_url

        page.click_search()
        page.take_screenshot("test_clinic_edit_visit_searched")

    def test_05_clinic_cancel_leaved(self, auth_driver):
        """5. Verify Cancel Leaved Clinic Visit (/clinic/cancel-leaved-visit)."""
        home = HomePage(auth_driver).open()
        home.open_clinic_cancel_leaved()

        page = ClinicCancelLeavedVisitPage(auth_driver)
        assert page.is_loaded(), "Cancel leaved clinic visit page failed to load."
        assert "/clinic/cancel-leaved-visit" in auth_driver.current_url

        page.click_search()
        page.take_screenshot("test_clinic_cancel_leaved_searched")

    def test_06_clinic_medical_reports(self, auth_driver):
        """6. Verify Clinic Medical Reports (/clinic/medical-reports)."""
        home = HomePage(auth_driver).open()
        home.open_clinic_med_reports()

        page = ClinicMedicalReportsPage(auth_driver)
        assert page.is_loaded(), "Clinic medical reports page failed to load."
        assert "/clinic/medical-reports" in auth_driver.current_url

        page.click_show()
        page.take_screenshot("test_clinic_med_reports_shown")
