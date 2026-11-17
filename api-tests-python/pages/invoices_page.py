import time
import logging
from typing import Optional
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger("BayMaxInvoicesPage")

class RegisteredInvoicesPage(BasePage):
    """
    Page Object for the Registered Patient Invoices screen (/patient-accounts/registered-invoices).
    """

    URL = "https://196.218.246.250:4040/patient-accounts/registered-invoices"

    INPUT_FROM_DATE = (By.CSS_SELECTOR, "[data-test-id='registered-invoices-from-date-input']")
    INPUT_TO_DATE = (By.CSS_SELECTOR, "[data-test-id='registered-invoices-to-date-input']")
    SELECT_CLIENT = (By.CSS_SELECTOR, "[data-test-id='registered-invoices-client-select']")
    SELECT_INS_COMPANY = (By.CSS_SELECTOR, "[data-test-id='registered-invoices-ins-company-select']")
    SELECT_ACC_TYPES = (By.CSS_SELECTOR, "[data-test-id='registered-invoices-acc-types-select']")
    SELECT_HOSPITAL_SECTION = (By.CSS_SELECTOR, "[data-test-id='registered-invoices-hospital-section-select']")
    BTN_SEARCH = (By.CSS_SELECTOR, "[data-test-id='registered-invoices-search-btn']")
    BTN_TODAY_EXIT = (By.CSS_SELECTOR, "[data-test-id='registered-invoices-today-exit-btn']")
    INPUT_SEARCH_FILTER = (By.CSS_SELECTOR, "[data-test-id='registered-invoices-search-input']")
    BTN_EXPORT_EXCEL = (By.CSS_SELECTOR, "[data-test-id='registered-invoices-export-excel-btn']")

    def open(self) -> "RegisteredInvoicesPage":
        """Navigate to Registered Invoices page."""
        logger.info(f"Navigating to Registered Invoices page: {self.URL}")
        self.driver.get(self.URL)
        self.find(self.BTN_SEARCH, timeout=12)
        return self

    def is_loaded(self) -> bool:
        """Verify the search button and date inputs are visible."""
        return self.is_visible(self.BTN_SEARCH) and self.is_visible(self.INPUT_FROM_DATE)

    def set_dates(self, from_date: str, to_date: str) -> None:
        """Set from and to date filter values (format: YYYY-MM-DD)."""
        logger.info(f"Setting invoice date filter: {from_date} to {to_date}")
        self.set_date_input(self.INPUT_FROM_DATE, from_date)
        self.set_date_input(self.INPUT_TO_DATE, to_date)


    def click_search(self) -> None:
        """Click the Search button."""
        logger.info("Clicking Search button on Registered Invoices...")
        self.click(self.BTN_SEARCH)
        time.sleep(2)

    def click_today_exit(self) -> None:
        """Click the 'خروج اليوم' button."""
        logger.info("Clicking 'خروج اليوم' button...")
        self.click(self.BTN_TODAY_EXIT)
        time.sleep(2)

    def filter_table(self, query: str) -> None:
        """Filter table results by query text."""
        logger.info(f"Filtering invoices table by: '{query}'")
        search_elem = self.find(self.INPUT_SEARCH_FILTER)
        search_elem.clear()
        search_elem.send_keys(query)
        time.sleep(1)

    def is_export_excel_visible(self) -> bool:
        """Checks if the Excel Export button is available."""
        return self.is_visible(self.BTN_EXPORT_EXCEL)
