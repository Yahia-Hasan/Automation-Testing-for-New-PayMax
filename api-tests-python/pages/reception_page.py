import time
import logging
from typing import Optional, List, Dict
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger("BayMaxReceptionPage")

class ReceptionPage(BasePage):
    """
    Page Object for the Reception / Patient File screen (/reception).
    Uses robust [data-test-id] attributes implemented in the Angular app.
    """

    URL = "https://196.218.246.250:4040/reception"

    # Search Locators
    SEARCH_INPUT = (By.CSS_SELECTOR, "[data-test-id='patient-data-search-input']")
    SEARCH_DROPDOWN = (By.CLASS_NAME, "search-dropdown")
    SEARCH_ITEMS = (By.CSS_SELECTOR, ".search-dropdown .search-item")

    # Patient Form Fields
    INPUT_PATIENT_CODE = (By.CSS_SELECTOR, "[data-test-id='patient-data-patient-code-input']")
    INPUT_PATIENT_NAME_AR = (By.CSS_SELECTOR, "[data-test-id='patient-data-patient-name-input']")
    INPUT_PATIENT_NAME_EN = (By.CSS_SELECTOR, "[data-test-id='patient-data-patient-name-en-input']")
    INPUT_MOBILE_PHONE = (By.CSS_SELECTOR, "[data-test-id='patient-data-mobile-phone-input']")
    INPUT_HOME_PHONE = (By.CSS_SELECTOR, "[data-test-id='patient-data-home-phone-input']")
    INPUT_ID_NUMBER = (By.CSS_SELECTOR, "[data-test-id='patient-data-id-number-input']")
    INPUT_BIRTH_DATE = (By.CSS_SELECTOR, "[data-test-id='patient-data-birth-date-input']")
    INPUT_ADDRESS = (By.CSS_SELECTOR, "[data-test-id='patient-data-address-input']")
    TEXTAREA_NOTES = (By.CSS_SELECTOR, "[data-test-id='patient-data-notes-textarea']")

    # Dropdowns / Selects
    SELECT_NATIONALITY = (By.CSS_SELECTOR, "[data-test-id='patient-data-nationality-select']")
    SELECT_ID_TYPE = (By.CSS_SELECTOR, "[data-test-id='patient-data-id-type-select']")
    SELECT_GENDER = (By.CSS_SELECTOR, "[data-test-id='patient-data-gender-select']")
    SELECT_RELIGION = (By.CSS_SELECTOR, "[data-test-id='patient-data-religion-select']")
    SELECT_MARITAL_STATUS = (By.CSS_SELECTOR, "[data-test-id='patient-data-marital-status-select']")
    SELECT_CITY = (By.CSS_SELECTOR, "[data-test-id='patient-data-city-select']")
    SELECT_ZONE = (By.CSS_SELECTOR, "[data-test-id='patient-data-zone-select']")
    SELECT_CLIENT = (By.CSS_SELECTOR, "[data-test-id='patient-data-client-select']")
    SELECT_INS_COMPANY = (By.CSS_SELECTOR, "[data-test-id='patient-data-ins-company-select']")
    SELECT_TPA = (By.CSS_SELECTOR, "[data-test-id='patient-data-tpa-select']")

    # Tabs and Action Buttons
    BTN_NEW_PATIENT = (By.CSS_SELECTOR, "[data-test-id='patient-data-new-btn']")
    BTN_SAVE_PATIENT = (By.CSS_SELECTOR, "[data-test-id='patient-data-save-btn']")
    TAB_CONTRACT = (By.CSS_SELECTOR, "[data-test-id='patient-data-contract-tab-btn']")
    TAB_DOCUMENTS = (By.CSS_SELECTOR, "[data-test-id='patient-data-documents-tab-btn']")
    BTN_UNKNOWN_PATIENT = (By.CSS_SELECTOR, "[data-test-id='patient-data-unknown-patient-btn']")

    BTN_ADD_TPA = (By.CSS_SELECTOR, "[data-test-id='patient-data-add-tpa-btn']")
    BTN_UPLOAD_DOCUMENT = (By.CSS_SELECTOR, "[data-test-id='patient-data-upload-document-btn']")

    # Deep Visit Navigation Buttons (Available after patient selection)
    BTN_ADMISSION = (By.CSS_SELECTOR, "[data-test-id='patient-data-admission-btn']")
    BTN_OPD = (By.CSS_SELECTOR, "[data-test-id='patient-data-opd-btn']")
    BTN_EMERGENCY = (By.CSS_SELECTOR, "[data-test-id='patient-data-emergency-btn']")


    def open(self) -> "ReceptionPage":
        """Navigates to /reception and waits for search input."""
        logger.info(f"Opening Reception page: {self.URL}")
        self.driver.get(self.URL)
        self.find(self.SEARCH_INPUT, timeout=12)
        return self

    def search_and_select_patient(self, query: str) -> bool:
        """
        Types query (code or name) into the search box,
        waits for the dropdown, and clicks the matching patient.
        """
        logger.info(f"Searching for patient with query: '{query}'...")
        search_elem = self.find(self.SEARCH_INPUT, timeout=10)
        search_elem.clear()
        search_elem.send_keys(query)
        time.sleep(2)

        # Wait for search results dropdown
        if not self.is_visible(self.SEARCH_DROPDOWN, timeout=5):
            logger.warning(f"No search results dropdown appeared for query '{query}'.")
            return False

        items = self.find_all(self.SEARCH_ITEMS, timeout=5)
        logger.info(f"Found {len(items)} matching patients in dropdown.")
        if not items:
            return False

        # Click the first result
        first_item = items[0]
        logger.info(f"Selecting patient: {first_item.text.replace(chr(10), ' | ')}")
        first_item.click()
        time.sleep(2)
        return True

    def get_loaded_patient_data(self) -> Dict[str, str]:
        """Returns currently loaded patient details from the form fields."""
        return {
            "code": self.find(self.INPUT_PATIENT_CODE).get_attribute("value") or "",
            "name_ar": self.find(self.INPUT_PATIENT_NAME_AR).get_attribute("value") or "",
            "name_en": self.find(self.INPUT_PATIENT_NAME_EN).get_attribute("value") or "",
            "mobile": self.find(self.INPUT_MOBILE_PHONE).get_attribute("value") or "",
            "id_number": self.find(self.INPUT_ID_NUMBER).get_attribute("value") or ""
        }

    def click_new(self) -> None:
        """Clicks the 'جديد' button to reset the form for a new patient entry."""
        logger.info("Clicking 'جديد' (New Patient) button...")
        self.click(self.BTN_NEW_PATIENT)
        time.sleep(1)

    def is_form_empty(self) -> bool:
        """Checks if the patient code and name fields are empty."""
        code = self.find(self.INPUT_PATIENT_CODE).get_attribute("value") or ""
        name = self.find(self.INPUT_PATIENT_NAME_AR).get_attribute("value") or ""
        return code == "" and name == ""

    def switch_to_contract_tab(self) -> None:
        """Switches to the Contract / Insurance tab."""
        logger.info("Switching to Contract tab...")
        self.click(self.TAB_CONTRACT)
        time.sleep(0.5)

    def switch_to_documents_tab(self) -> None:
        """Switches to the Documents / Attachments tab."""
        logger.info("Switching to Documents tab...")
        self.click(self.TAB_DOCUMENTS)
        time.sleep(0.5)

    def click_save(self) -> None:
        """Clicks the 'اضافة' (Save) button."""
        logger.info("Clicking 'اضافة' (Save Patient) button...")
        self.click(self.BTN_SAVE_PATIENT)
        time.sleep(1)

    def get_toast_message(self, timeout: int = 5) -> Optional[str]:
        """Gets visible text from the toast notification if displayed."""
        toast_loc = (By.CSS_SELECTOR, ".toast-item, .toast-stack .msg")
        if self.is_visible(toast_loc, timeout=timeout):
            msg = self.get_text(toast_loc)
            logger.info(f"Toast notification appeared: '{msg}'")
            return msg
        return None

    def open_patient_admission(self) -> None:
        """Clicks the 'حجز داخلي' button to open Inpatient Admission for the selected patient."""
        logger.info("Clicking 'حجز داخلي' (Admission) button...")
        self.click(self.BTN_ADMISSION)
        time.sleep(2)

    def open_patient_opd(self) -> None:
        """Clicks the 'عيادات خارجية' button to open OPD Visit draft for the selected patient."""
        logger.info("Clicking 'عيادات خارجية' (OPD Visit) button...")
        self.click(self.BTN_OPD)
        time.sleep(2)

    def open_patient_emergency(self) -> None:
        """Clicks the 'إسعاف وطوارئ' button to open Emergency Case draft for the selected patient."""
        logger.info("Clicking 'إسعاف وطوارئ' (Emergency Visit) button...")
        self.click(self.BTN_EMERGENCY)
        time.sleep(2)
