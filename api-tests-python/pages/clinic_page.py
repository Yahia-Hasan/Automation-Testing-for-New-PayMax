import time
import logging
from typing import Optional, List
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger("BayMaxClinicPage")

class ClinicWaitingListPage(BasePage):
    """
    Page Object for the Clinic Waiting List screen (/clinic/waiting-list).
    """

    URL = "https://196.218.246.250:4040/clinic/waiting-list"

    # Locators with data-test-id
    INPUT_DATE = (By.CSS_SELECTOR, "[data-test-id='clinic-waiting-list-date-input']")
    SELECT_DOCTOR = (By.CSS_SELECTOR, "[data-test-id='clinic-waiting-list-doctor-select']")
    SELECT_PAYMENT_STATUS = (By.CSS_SELECTOR, "[data-test-id='clinic-waiting-list-payment-status-select']")
    SELECT_DONE_STATUS = (By.CSS_SELECTOR, "[data-test-id='clinic-waiting-list-done-status-select']")
    BTN_SEARCH = (By.CSS_SELECTOR, "[data-test-id='clinic-waiting-list-search-btn']")

    def open(self) -> "ClinicWaitingListPage":
        logger.info(f"Opening Clinic Waiting List: {self.URL}")
        self.driver.get(self.URL)
        self.find(self.BTN_SEARCH, timeout=12)
        return self

    def set_date(self, date_str: str) -> "ClinicWaitingListPage":
        """Sets the filter date (e.g. YYYY-MM-DD)."""
        logger.info(f"Setting filter date to: {date_str}")
        date_elem = self.find(self.INPUT_DATE)
        self.driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", date_elem, date_str)
        time.sleep(0.5)
        return self

    def select_doctor(self, doctor_name: str) -> "ClinicWaitingListPage":
        """Selects a doctor from the ng-select dropdown."""
        logger.info(f"Selecting doctor: '{doctor_name}'...")
        self.select_ng_option(self.SELECT_DOCTOR, doctor_name)
        return self

    def click_search(self) -> None:
        """Clicks the search button to load the waiting list."""
        logger.info("Clicking Search in Clinic Waiting List...")
        self.click(self.BTN_SEARCH)
        time.sleep(2)

    def is_filter_panel_visible(self) -> bool:
        """Verifies that the date and doctor filters are displayed."""
        return self.is_visible(self.INPUT_DATE) and self.is_visible(self.BTN_SEARCH)
