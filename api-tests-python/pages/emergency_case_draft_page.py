import time
import logging
from typing import Optional, Dict
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger("BayMaxEmergencyCaseDraftPage")

class EmergencyCaseDraftPage(BasePage):
    """
    Page Object for Emergency Draft Visit screen (/emergency/cases/draft).
    """

    # Action buttons
    BTN_BACK = (By.CSS_SELECTOR, "[data-test-id='emergency-visit-draft-back-btn']")
    BTN_SAVE = (By.CSS_SELECTOR, "[data-test-id='emergency-visit-draft-save-btn']")
    BTN_CANCEL = (By.CSS_SELECTOR, "[data-test-id='emergency-visit-draft-cancel-btn']")

    # Form Fields
    INPUT_NOTES = (By.CSS_SELECTOR, "[data-test-id='emergency-visit-draft-notes-input']")

    # Select Dropdowns
    SELECT_CASE_TYPE = (By.CSS_SELECTOR, "[data-test-id='emergency-visit-draft-case-type-select']")
    SELECT_DOCTOR = (By.CSS_SELECTOR, "[data-test-id='emergency-visit-draft-doctor-select']")
    SELECT_SPECIALTY = (By.CSS_SELECTOR, "[data-test-id='emergency-visit-draft-specialty-select']")
    SELECT_TRANSFER_DOCTOR = (By.CSS_SELECTOR, "[data-test-id='emergency-visit-draft-transfer-doctor-select']")
    SELECT_INS_COMPANY = (By.CSS_SELECTOR, "[data-test-id='emergency-visit-draft-ins-company-select']")
    SELECT_ICD = (By.CSS_SELECTOR, "[data-test-id='emergency-visit-draft-icd-select']")

    def open_for_patient(self, patient_code: int = 30856, client_id: int = 52) -> "EmergencyCaseDraftPage":
        """Navigates directly to the Emergency Case Draft page."""
        url = f"https://196.218.246.250:4040/emergency/cases/draft?patientCode={patient_code}&clientId={client_id}"
        logger.info(f"Navigating to Emergency Case Draft URL: {url}")
        self.driver.get(url)
        self.find(self.BTN_SAVE, timeout=12)
        return self

    def is_loaded(self) -> bool:
        """Checks if the emergency case draft page is loaded and buttons are visible."""
        return self.is_visible(self.BTN_SAVE, timeout=10)

    def is_select_present(self, locator) -> bool:
        """Checks if a given select element is present on the page."""
        return self.is_visible(locator, timeout=5)

    def enter_notes(self, text: str) -> None:
        """Enters text into the notes input field."""
        logger.info(f"Entering notes: '{text}'")
        self.type_text(self.INPUT_NOTES, text)

    def click_save(self) -> None:
        """Clicks Save button."""
        logger.info("Clicking Emergency Case Draft Save button...")
        self.click(self.BTN_SAVE)
        time.sleep(1)

    def click_cancel(self) -> None:
        """Clicks Cancel button."""
        logger.info("Clicking Emergency Case Draft Cancel button...")
        self.click(self.BTN_CANCEL)
        time.sleep(1)

    def click_back(self) -> None:
        """Clicks Back button."""
        logger.info("Clicking Emergency Case Draft Back button...")
        self.click(self.BTN_BACK)
        time.sleep(1.5)
