import time
import logging
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger("BayMaxPhysicalTherapy")

class PhysicalTherapyWaitingListPage(BasePage):
    """Page Object for Physical Therapy Waiting List (/physical-therapy/waiting-list)."""

    URL = "https://196.218.246.250:4040/physical-therapy/waiting-list"

    INPUT_FROM_DATE = (By.CSS_SELECTOR, "[data-test-id='pt-waiting-list-from-date-input']")
    INPUT_TO_DATE = (By.CSS_SELECTOR, "[data-test-id='pt-waiting-list-to-date-input']")
    SELECT_SERVICE = (By.CSS_SELECTOR, "[data-test-id='pt-waiting-list-service-select']")
    SELECT_PATIENT_TYPE = (By.CSS_SELECTOR, "[data-test-id='pt-waiting-list-patient-type-select']")
    SELECT_STATUS = (By.CSS_SELECTOR, "[data-test-id='pt-waiting-list-status-select']")
    SELECT_PATIENT = (By.CSS_SELECTOR, "[data-test-id='pt-waiting-list-patient-select']")
    BTN_SEARCH = (By.CSS_SELECTOR, "[data-test-id='pt-waiting-list-search-btn']")
    INPUT_SEARCH = (By.CSS_SELECTOR, "[data-test-id='pt-waiting-list-search-input']")
    BTN_EXPORT_EXCEL = (By.CSS_SELECTOR, "[data-test-id='pt-waiting-list-export-excel-btn']")

    def open(self) -> "PhysicalTherapyWaitingListPage":
        logger.info(f"Opening Physical Therapy Waiting List: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.INPUT_FROM_DATE, timeout=12) and self.is_visible(self.BTN_SEARCH)

    def click_search(self) -> None:
        self.click(self.BTN_SEARCH)
        time.sleep(2)
