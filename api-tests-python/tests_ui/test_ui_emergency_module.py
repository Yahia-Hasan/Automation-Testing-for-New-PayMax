import pytest
from pages.home_page import HomePage
from pages.emergency_module_page import (
    EmergencyWaitingListPage,
    EmergencyEditVisitPage,
    EmergencyAdmissionDischargePage,
    EmergencyMedicalReportsPage,
    EmergencyBedOccupancyPage,
    EmergencyCancelLeavedPage,
)

class TestEmergencyModuleUI:
    """UI Test Suite covering all 6 Emergency module screens."""

    def test_01_emergency_waiting_list(self, auth_driver):
        """1. Verify Emergency Waiting List (/emergency/waiting-list)."""
        home = HomePage(auth_driver).open()
        home.open_emergency_waiting()

        page = EmergencyWaitingListPage(auth_driver)
        assert page.is_loaded(), "Emergency waiting list failed to load."
        assert "/emergency/waiting-list" in auth_driver.current_url

        page.search("مريض")
        page.take_screenshot("test_emergency_waiting_searched")

    def test_02_emergency_edit_visit(self, auth_driver):
        """2. Verify Edit Emergency Visit (/emergency/edit-visit)."""
        home = HomePage(auth_driver).open()
        home.open_emergency_edit_visit()

        page = EmergencyEditVisitPage(auth_driver)
        assert page.is_loaded(), "Edit emergency visit page failed to load."
        assert "/emergency/edit-visit" in auth_driver.current_url

        page.click_load()
        page.take_screenshot("test_emergency_edit_visit_loaded")

    def test_03_emergency_admission_discharge(self, auth_driver):
        """3. Verify Emergency Admission & Discharge (/emergency/admission-discharge-report)."""
        home = HomePage(auth_driver).open()
        home.open_emergency_adm_disch()

        page = EmergencyAdmissionDischargePage(auth_driver)
        assert page.is_loaded(), "Emergency admission/discharge report failed to load."
        assert "/emergency/admission-discharge-report" in auth_driver.current_url

        page.click_load()
        page.take_screenshot("test_emergency_adm_disch_loaded")

    def test_04_emergency_medical_reports(self, auth_driver):
        """4. Verify Emergency Medical Reports (/emergency/medical-reports)."""
        home = HomePage(auth_driver).open()
        home.open_emergency_med_reports()

        page = EmergencyMedicalReportsPage(auth_driver)
        assert page.is_loaded(), "Emergency medical reports page failed to load."
        assert "/emergency/medical-reports" in auth_driver.current_url

        page.click_show()
        page.take_screenshot("test_emergency_med_reports_shown")

    def test_05_emergency_bed_occupancy(self, auth_driver):
        """5. Verify Emergency Bed Occupancy (/emergency/bed-occupancy)."""
        home = HomePage(auth_driver).open()
        home.open_emergency_bed_occupancy()

        page = EmergencyBedOccupancyPage(auth_driver)
        assert page.is_loaded(), "Emergency bed occupancy page failed to load."
        assert "/emergency/bed-occupancy" in auth_driver.current_url

        page.take_screenshot("test_emergency_bed_occupancy_loaded")

    def test_06_emergency_cancel_leaved(self, auth_driver):
        """6. Verify Cancel Leaved Emergency Visit (/emergency/cancel-leaved)."""
        home = HomePage(auth_driver).open()
        home.open_emergency_cancel_leaved()

        page = EmergencyCancelLeavedPage(auth_driver)
        assert page.is_loaded(), "Cancel leaved emergency page failed to load."
        assert "/emergency/cancel-leaved" in auth_driver.current_url

        page.click_load()
        page.take_screenshot("test_emergency_cancel_leaved_loaded")
