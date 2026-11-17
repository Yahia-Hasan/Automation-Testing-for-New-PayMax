import time
import logging
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger("BayMaxLabPage")

class LabWaitingListPage(BasePage):
    """Page Object for Lab Waiting List (/lab/waiting-list)."""

    URL = "https://196.218.246.250:4040/lab/waiting-list"

    INPUT_FROM_DATE = (By.CSS_SELECTOR, "[data-test-id='lab-waiting-list-from-date-input']")
    INPUT_TO_DATE = (By.CSS_SELECTOR, "[data-test-id='lab-waiting-list-to-date-input']")
    BTN_SEARCH = (By.CSS_SELECTOR, "[data-test-id='lab-waiting-list-search-btn']")
    INPUT_SEARCH = (By.CSS_SELECTOR, "[data-test-id='lab-waiting-list-search-input']")
    BTN_EXPORT = (By.CSS_SELECTOR, "[data-test-id='lab-waiting-list-export-btn']")

    def open(self) -> "LabWaitingListPage":
        logger.info(f"Opening Lab Waiting List: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.INPUT_FROM_DATE, timeout=12) and self.is_visible(self.BTN_SEARCH)

    def click_search(self) -> None:
        self.click(self.BTN_SEARCH)
        time.sleep(2)


class BloodWaitingListPage(BasePage):
    """Page Object for Blood Bank Waiting List (/lab/blood-waiting-list)."""

    URL = "https://196.218.246.250:4040/lab/blood-waiting-list"

    SELECT_PATIENT = (By.CSS_SELECTOR, "[data-test-id='blood-waiting-list-patient-select']")
    BTN_SEARCH = (By.CSS_SELECTOR, "[data-test-id='blood-waiting-list-search-btn']")
    INPUT_SEARCH = (By.CSS_SELECTOR, "[data-test-id='blood-waiting-list-search-input']")
    TABLE_ROWS = (By.CSS_SELECTOR, "[data-test-id='blood-waiting-list-row']")

    def open(self) -> "BloodWaitingListPage":
        logger.info(f"Opening Blood Waiting List: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.BTN_SEARCH, timeout=12) and self.is_visible(self.INPUT_SEARCH)

    def get_rows_count(self) -> int:
        return len(self.driver.find_elements(*self.TABLE_ROWS))

    def click_search(self) -> None:
        self.click(self.BTN_SEARCH)
        time.sleep(2)


class LabDetailsPage(BasePage):
    """Page Object for Detailed Lab Report (/lab/details)."""

    URL = "https://196.218.246.250:4040/lab/details"

    INPUT_FROM_DATE = (By.CSS_SELECTOR, "[data-test-id='lab-details-from-date-input']")
    INPUT_TO_DATE = (By.CSS_SELECTOR, "[data-test-id='lab-details-to-date-input']")
    SELECT_CLIENT = (By.CSS_SELECTOR, "[data-test-id='lab-details-client-select']")
    SELECT_DOCTOR = (By.CSS_SELECTOR, "[data-test-id='lab-details-doctor-select']")
    BTN_SEARCH = (By.CSS_SELECTOR, "[data-test-id='lab-details-search-btn']")
    BTN_EXPORT = (By.CSS_SELECTOR, "[data-test-id='lab-details-export-btn']")

    def open(self) -> "LabDetailsPage":
        logger.info(f"Opening Lab Details: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.INPUT_FROM_DATE, timeout=12) and self.is_visible(self.BTN_SEARCH)

    def click_search(self) -> None:
        self.click(self.BTN_SEARCH)
        time.sleep(2)


class BloodBankStatusPage(BasePage):
    """Page Object for Blood Bank Status (/lab/blood-bank-status)."""

    URL = "https://196.218.246.250:4040/lab/blood-bank-status"

    INPUT_FROM_DATE = (By.CSS_SELECTOR, "[data-test-id='blood-bank-status-from-date-input']")
    INPUT_TO_DATE = (By.CSS_SELECTOR, "[data-test-id='blood-bank-status-to-date-input']")
    BTN_SEARCH = (By.CSS_SELECTOR, "[data-test-id='blood-bank-status-search-btn']")
    BTN_EXPORT = (By.CSS_SELECTOR, "[data-test-id='blood-bank-status-export-btn']")

    def open(self) -> "BloodBankStatusPage":
        logger.info(f"Opening Blood Bank Status: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.INPUT_FROM_DATE, timeout=12) and self.is_visible(self.BTN_SEARCH)

    def click_search(self) -> None:
        self.click(self.BTN_SEARCH)
        time.sleep(2)


class LabResultsInquiryPage(BasePage):
    """Page Object for Lab Results Inquiry (/lab/results-inquiry)."""

    URL = "https://196.218.246.250:4040/lab/results-inquiry"

    INPUT_FROM_DATE = (By.CSS_SELECTOR, "[data-test-id='lab-results-inquiry-from-date-input']")
    INPUT_TO_DATE = (By.CSS_SELECTOR, "[data-test-id='lab-results-inquiry-to-date-input']")
    BTN_SEARCH = (By.CSS_SELECTOR, "[data-test-id='lab-results-inquiry-search-btn']")
    INPUT_SEARCH = (By.CSS_SELECTOR, "[data-test-id='lab-results-inquiry-search-input']")

    def open(self) -> "LabResultsInquiryPage":
        logger.info(f"Opening Lab Results Inquiry: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.INPUT_FROM_DATE, timeout=12) and self.is_visible(self.BTN_SEARCH)

    def click_search(self) -> None:
        self.click(self.BTN_SEARCH)
        time.sleep(2)
