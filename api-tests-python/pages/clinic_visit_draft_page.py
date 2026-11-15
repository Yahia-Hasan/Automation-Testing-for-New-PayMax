import time
import logging
from typing import Optional, Dict
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger("BayMaxClinicVisitDraftPage")

class ClinicVisitDraftPage(BasePage):
    """
    Page Object for Outpatient Draft Visit screen (/clinic/visits/draft).
    """

    # Action buttons
    BTN_BACK = (By.CSS_SELECTOR, "[data-test-id='opd-visit-draft-back-btn']")
    BTN_SAVE = (By.CSS_SELECTOR, "[data-test-id='opd-visit-draft-save-btn']")
    BTN_CANCEL = (By.CSS_SELECTOR, "[data-test-id='opd-visit-draft-cancel-btn']")

    # Select Dropdowns
    SELECT_CASE_TYPE = (By.CSS_SELECTOR, "[data-test-id='opd-visit-draft-case-type-select']")
    SELECT_INS_COMPANY = (By.CSS_SELECTOR, "[data-test-id='opd-visit-draft-ins-company-select']")
    SELECT_TRANSFER_DOCTOR = (By.CSS_SELECTOR, "[data-test-id='opd-visit-draft-transfer-doctor-select']")
    SELECT_ICD = (By.CSS_SELECTOR, "[data-test-id='opd-visit-draft-icd-select']")

    def open_for_patient(self, patient_code: int = 30855, client_id: int = 52) -> "ClinicVisitDraftPage":
        """Navigates directly to the OPD Draft Visit page."""
        url = f"https://196.218.246.250:4040/clinic/visits/draft?patientCode={patient_code}&clientId={client_id}&mode=opd"
        logger.info(f"Navigating to OPD Visit Draft URL: {url}")
        self.driver.get(url)
        self.find(self.BTN_SAVE, timeout=12)
        return self

    def is_loaded(self) -> bool:
        """Checks if the draft visit page is loaded and buttons are visible."""
        return self.is_visible(self.BTN_SAVE, timeout=10)

    def is_select_present(self, locator) -> bool:
        """Checks if a given select element is present on the page."""
        return self.is_visible(locator, timeout=5)

    def click_save(self) -> None:
        """Clicks Save button."""
        logger.info("Clicking OPD Draft Visit Save button...")
        self.click(self.BTN_SAVE)
        time.sleep(1)

    def click_cancel(self) -> None:
        """Clicks Cancel button."""
        logger.info("Clicking OPD Draft Visit Cancel button...")
        self.click(self.BTN_CANCEL)
        time.sleep(1)

    def click_back(self) -> None:
        """Clicks Back button."""
        logger.info("Clicking OPD Draft Visit Back button...")
        self.click(self.BTN_BACK)
        time.sleep(1.5)
