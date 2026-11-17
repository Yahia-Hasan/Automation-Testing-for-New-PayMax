import pytest
from pages.home_page import HomePage
from pages.nursing_module_page import (
    NursingRoomsPage,
    NursingICUPage,
    NursingNeonatalPage,
    PatientDietsListPage,
    AttendantDietsListPage,
    InpatientMedicalReportsPage,
)

class TestNursingModuleUI:
    """UI Test Suite covering all 6 Nursing Secretariat module screens."""

    def test_01_nursing_rooms(self, auth_driver):
        """1. Verify Nursing Inpatients in Rooms (/waiting-list/accomodation-rooms)."""
        home = HomePage(auth_driver).open()
        home.open_nursing_rooms()

        page = NursingRoomsPage(auth_driver)
        assert page.is_loaded(), "Nursing rooms page failed to load."
        assert "/waiting-list/accomodation-rooms" in auth_driver.current_url

        page.reload()
        page.take_screenshot("test_nursing_rooms_reloaded")

    def test_02_nursing_icu(self, auth_driver):
        """2. Verify Nursing ICU Patients (/waiting-list/icu)."""
        home = HomePage(auth_driver).open()
        home.open_nursing_icu()

        page = NursingICUPage(auth_driver)
        assert page.is_loaded(), "Nursing ICU page failed to load."
        assert "/waiting-list/icu" in auth_driver.current_url

        page.reload()
        page.take_screenshot("test_nursing_icu_reloaded")

    def test_03_nursing_neonatal(self, auth_driver):
        """3. Verify Nursing Neonatal Patients (/waiting-list/neonatal)."""
        home = HomePage(auth_driver).open()
        home.open_nursing_neonatal()

        page = NursingNeonatalPage(auth_driver)
        assert page.is_loaded(), "Nursing neonatal page failed to load."
        assert "/waiting-list/neonatal" in auth_driver.current_url

        page.reload()
        page.take_screenshot("test_nursing_neonatal_reloaded")

    def test_04_patient_diets_list(self, auth_driver):
        """4. Verify Patient Diets List (/waiting-list/patient-diets-list)."""
        home = HomePage(auth_driver).open()
        home.open_nursing_patient_diets()

        page = PatientDietsListPage(auth_driver)
        assert page.is_loaded(), "Patient diets list failed to load."
        assert "/waiting-list/patient-diets-list" in auth_driver.current_url

        page.click_show()
        page.take_screenshot("test_patient_diets_shown")

    def test_05_attendant_diets_list(self, auth_driver):
        """5. Verify Attendant Diets List (/waiting-list/attendant-diets)."""
        home = HomePage(auth_driver).open()
        home.open_nursing_attendant_diets()

        page = AttendantDietsListPage(auth_driver)
        assert page.is_loaded(), "Attendant diets list failed to load."
        assert "/waiting-list/attendant-diets" in auth_driver.current_url

        page.refresh()
        page.take_screenshot("test_attendant_diets_refreshed")

    def test_06_inpatient_medical_reports(self, auth_driver):
        """6. Verify Inpatient Medical Reports (/waiting-list/medical-reports)."""
        home = HomePage(auth_driver).open()
        home.open_nursing_med_reports()

        page = InpatientMedicalReportsPage(auth_driver)
        assert page.is_loaded(), "Inpatient medical reports failed to load."
        assert "/waiting-list/medical-reports" in auth_driver.current_url

        page.click_show()
        page.take_screenshot("test_inpatient_medical_reports_shown")
