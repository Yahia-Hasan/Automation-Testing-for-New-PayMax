import logging
import time
from typing import Optional, List
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage

logger = logging.getLogger("BayMaxAdmissionDischargePage")

class AdmissionDischargeReportPage(BasePage):
    """Page object for Admission & Discharge Report (/reception/admission-discharge-report)."""

    URL = "https://196.218.246.250:4040/reception/admission-discharge-report"

    # Locators
    PAGE_HEADER = (By.XPATH, "//*[contains(text(), 'تقرير الدخول والخروج')]")
    DATE_FROM_INPUT = (By.XPATH, "//input[@data-test-id='admission-discharge-report-date-from-input']")
    DATE_TO_INPUT = (By.XPATH, "//input[@data-test-id='admission-discharge-report-date-to-input']")
    TYPE_SELECT = (By.XPATH, "//ng-select[@data-test-id='admission-discharge-report-type-select']")
    DEGREE_SELECT = (By.XPATH, "//ng-select[@data-test-id='admission-discharge-report-degree-select']")
    FLOOR_SELECT = (By.XPATH, "//ng-select[@data-test-id='admission-discharge-report-floor-select']")
    INVOICE_STATUS_SELECT = (By.XPATH, "//ng-select[@data-test-id='admission-discharge-report-invoice-status-select']")
    BTN_SEARCH = (By.XPATH, "//button[@data-test-id='admission-discharge-report-search-btn']")
    INPUT_FILTER = (By.XPATH, "//input[@data-test-id='admission-discharge-report-filter-input']")
    BTN_EXPORT_EXCEL = (By.XPATH, "//button[@data-test-id='admission-discharge-report-export-excel-btn']")
    TABLE_ROWS = (By.XPATH, "//tbody//tr")

    def open(self) -> "AdmissionDischargeReportPage":
        logger.info(f"Opening Admission & Discharge Report page directly: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        """Verifies report page and primary controls are visible."""
        return self.is_visible(self.BTN_SEARCH, timeout=15)

    def get_date_from(self) -> str:
        """Returns the current 'from date' value."""
        return self.find(self.DATE_FROM_INPUT).get_attribute("value")

    def get_date_to(self) -> str:
        """Returns the current 'to date' value."""
        return self.find(self.DATE_TO_INPUT).get_attribute("value")

    def set_date_range(self, date_from: str, date_to: str) -> None:
        """Sets the date range filter."""
        logger.info(f"Setting date range: {date_from} to {date_to}")
        self.set_date_input(self.DATE_FROM_INPUT, date_from)
        self.set_date_input(self.DATE_TO_INPUT, date_to)

    def click_search(self) -> None:
        """Clicks the 'عرض' (Search/Show) button and waits briefly for network request."""
        logger.info("Clicking Search / عرض button...")
        self.click(self.BTN_SEARCH)
        time.sleep(3)

    def filter_table(self, keyword: str) -> None:
        """Enters search term into the instant filter input."""
        logger.info(f"Filtering report results by keyword: '{keyword}'")
        self.type_text(self.INPUT_FILTER, keyword)
        time.sleep(0.5)

    def clear_filter(self) -> None:
        """Clears the instant filter."""
        el = self.find(self.INPUT_FILTER)
        el.clear()
        el.send_keys(Keys.BACK_SPACE)
        time.sleep(0.5)

    def is_export_button_ready(self) -> bool:
        """Verifies the export to excel button is present and enabled."""
        if not self.is_visible(self.BTN_EXPORT_EXCEL, timeout=10):
            return False
        btn = self.find(self.BTN_EXPORT_EXCEL)
        return btn.is_displayed() and btn.is_enabled()
