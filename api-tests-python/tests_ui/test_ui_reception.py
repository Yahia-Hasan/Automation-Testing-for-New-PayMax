import pytest
from selenium.webdriver.common.by import By
from pages.home_page import HomePage
from pages.reception_page import ReceptionPage

class TestReceptionUI:
    """UI Test Suite for the Reception and Patient File Screen."""

    def test_01_navigate_to_reception_from_home(self, auth_driver):
        """Verify navigation from Dashboard to Reception (/reception)."""
        home = HomePage(auth_driver).open()
        assert home.is_loaded(), "Home dashboard failed to load."
        
        greeting = home.get_welcome_title()
        assert "Ma3n" in greeting or "مساء" in greeting or "صباح" in greeting, f"Unexpected greeting: {greeting}"

        # Navigate to Reception
        home.open_reception()
        reception = ReceptionPage(auth_driver)
        assert reception.is_visible(reception.SEARCH_INPUT), "Reception search input is not visible."

    def test_02_search_patient_by_code(self, auth_driver):
        """Verify patient search by Code ('30902') and form auto-fill."""
        reception = ReceptionPage(auth_driver)
        reception.open()

        success = reception.search_and_select_patient("30902")
        assert success, "Failed to search or select patient 30902 from dropdown."

        patient_data = reception.get_loaded_patient_data()
        assert patient_data["code"] == "30902", f"Expected code '30902', got '{patient_data['code']}'"
        assert len(patient_data["name_ar"]) > 0, "Patient Arabic name was not loaded."
        
        reception.take_screenshot("test_patient_30902_loaded")

    def test_03_search_patient_by_name(self, auth_driver):
        """Verify patient search by Name query ('علي') and select first result."""
        reception = ReceptionPage(auth_driver)
        reception.open()

        success = reception.search_and_select_patient("علي")
        assert success, "Failed to search patient by name query 'علي'."

        patient_data = reception.get_loaded_patient_data()
        assert len(patient_data["code"]) > 0, "Patient code should be populated after selection."
        assert "علي" in patient_data["name_ar"], f"Expected 'علي' in patient name, got '{patient_data['name_ar']}'"

    def test_04_new_patient_resets_form(self, auth_driver):
        """Verify clicking 'جديد' (New Patient) resets and clears the patient form."""
        reception = ReceptionPage(auth_driver)
        # First ensure a patient is loaded
        reception.search_and_select_patient("30902")
        assert not reception.is_form_empty(), "Form should contain patient data before resetting."

        # Click new
        reception.click_new()
        assert reception.is_form_empty(), "Form should be cleared after clicking 'جديد'."
        reception.take_screenshot("test_reception_form_cleared")

    def test_05_tabs_switching(self, auth_driver):
        """Verify switching between 'بيانات التعاقد' and 'المرفقات' tabs."""
        reception = ReceptionPage(auth_driver)
        reception.open()

        # Switch to Contract tab
        reception.switch_to_contract_tab()
        assert reception.is_visible(reception.SELECT_CLIENT) or reception.is_visible((By.CSS_SELECTOR, "[data-test-id='patient-data-client-select']")), "Contract fields not visible."

        # Switch to Documents tab
        reception.switch_to_documents_tab()
        assert reception.is_visible((By.CSS_SELECTOR, "[data-test-id='patient-data-document-title-input']")), "Documents fields not visible."

        # Switch back to Contract tab
        reception.switch_to_contract_tab()
        reception.take_screenshot("test_reception_contract_tab")
