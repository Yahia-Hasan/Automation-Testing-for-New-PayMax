import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage

logger = logging.getLogger("BayMaxRaysPage")

class RaysWaitingListPage(BasePage):
    """Page Object for Rays Waiting List (/rays/waiting-list)."""

    URL = "https://196.218.246.250:4040/rays/waiting-list"

    INPUT_FROM_DATE = (By.CSS_SELECTOR, "[data-test-id='rays-waiting-list-from-date-input']")
    INPUT_TO_DATE = (By.CSS_SELECTOR, "[data-test-id='rays-waiting-list-to-date-input']")
    BTN_SEARCH = (By.CSS_SELECTOR, "[data-test-id='rays-waiting-list-search-btn']")

    BTN_DEPT_ALL = (By.CSS_SELECTOR, "[data-test-id='rays-waiting-list-dept-all-btn']")
    BTN_DEPT_INPATIENT = (By.CSS_SELECTOR, "[data-test-id='rays-waiting-list-dept-inpatient-btn']")
    BTN_DEPT_EMERGENCY = (By.CSS_SELECTOR, "[data-test-id='rays-waiting-list-dept-emergency-btn']")
    BTN_DEPT_OUTPATIENT = (By.CSS_SELECTOR, "[data-test-id='rays-waiting-list-dept-outpatient-btn']")

    INPUT_SEARCH = (By.CSS_SELECTOR, "[data-test-id='rays-waiting-list-search-input']")
    BTN_EXPORT_EXCEL = (By.CSS_SELECTOR, "[data-test-id='rays-waiting-list-export-excel-btn']")

    def open(self) -> "RaysWaitingListPage":
        logger.info(f"Opening Rays Waiting List: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.BTN_SEARCH, timeout=12) and self.is_visible(self.BTN_DEPT_ALL)

    def click_search(self) -> None:
        self.click(self.BTN_SEARCH)
        time.sleep(2)

    def filter_emergency(self) -> None:
        self.click(self.BTN_DEPT_EMERGENCY)
        time.sleep(1)

    def filter_inpatient(self) -> None:
        self.click(self.BTN_DEPT_INPATIENT)
        time.sleep(1)

    def filter_all(self) -> None:
        self.click(self.BTN_DEPT_ALL)
        time.sleep(1)


class RaysStatusPage(BasePage):
    """Page Object for Rays Status (/rays/status)."""

    URL = "https://196.218.246.250:4040/rays/status"

    INPUT_FROM_DATE = (By.CSS_SELECTOR, "[data-test-id='rays-status-from-date-input']")
    INPUT_TO_DATE = (By.CSS_SELECTOR, "[data-test-id='rays-status-to-date-input']")
    SELECT_PATIENT_TYPE = (By.CSS_SELECTOR, "[data-test-id='rays-status-patient-type-select']")
    SELECT_STATUS = (By.CSS_SELECTOR, "[data-test-id='rays-status-status-select']")
    BTN_SEARCH = (By.CSS_SELECTOR, "[data-test-id='rays-status-search-btn']")
    INPUT_SEARCH = (By.CSS_SELECTOR, "[data-test-id='rays-status-search-input']")

    def open(self) -> "RaysStatusPage":
        logger.info(f"Opening Rays Status: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.INPUT_FROM_DATE, timeout=12) and self.is_visible(self.BTN_SEARCH)

    def click_search(self) -> None:
        self.click(self.BTN_SEARCH)
        time.sleep(2)


class RaysDetailsPage(BasePage):
    """Page Object for Rays Detailed Report (/rays/details)."""

    URL = "https://196.218.246.250:4040/rays/details"

    INPUT_FROM_DATE = (By.CSS_SELECTOR, "[data-test-id='rays-details-from-date-input']")
    INPUT_TO_DATE = (By.CSS_SELECTOR, "[data-test-id='rays-details-to-date-input']")
    SELECT_CLIENT = (By.CSS_SELECTOR, "[data-test-id='rays-details-client-select']")
    SELECT_DOCTOR = (By.CSS_SELECTOR, "[data-test-id='rays-details-doctor-select']")
    BTN_SEARCH = (By.CSS_SELECTOR, "[data-test-id='rays-details-search-btn']")

    def open(self) -> "RaysDetailsPage":
        logger.info(f"Opening Rays Details: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.INPUT_FROM_DATE, timeout=12) and self.is_visible(self.BTN_SEARCH)

    def click_search(self) -> None:
        self.click(self.BTN_SEARCH)
        time.sleep(2)
