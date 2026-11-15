import logging
import time
from typing import Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage

logger = logging.getLogger("BayMaxLeavingApprovalReportPage")

class LeavingApprovalReportPage(BasePage):
    """Page object for Leaving Approval Report (/reception/leaving-approval-report)."""

    URL = "https://196.218.246.250:4040/reception/leaving-approval-report"

    # Locators
    PAGE_HEADER = (By.XPATH, "//div[contains(@class, 'page-header')]//span[contains(text(), 'تقرير تأكيد طلبات المغادرة')] | //div[contains(@class, 'page-header')]")
    DATE_FROM_INPUT = (By.XPATH, "//input[@data-test-id='leaving-approval-report-date-from-input']")
    DATE_TO_INPUT = (By.XPATH, "//input[@data-test-id='leaving-approval-report-date-to-input']")
    APPROVAL_TYPE_SELECT = (By.XPATH, "//ng-select[@data-test-id='leaving-approval-report-approval-type-select']")
    BTN_SEARCH = (By.XPATH, "//button[@data-test-id='leaving-approval-report-search-btn']")
    INPUT_FILTER = (By.XPATH, "//input[@data-test-id='leaving-approval-report-filter-input']")
    BTN_EXPORT_EXCEL = (By.XPATH, "//button[@data-test-id='leaving-approval-report-export-excel-btn']")

    def open(self) -> "LeavingApprovalReportPage":
        logger.info(f"Opening Leaving Approval Report page directly: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        """Verifies page header and search button are visible."""
        return self.is_visible(self.BTN_SEARCH, timeout=15)

    def get_header_title(self) -> str:
        """Returns header text."""
        return self.get_text(self.PAGE_HEADER)

    def get_date_from(self) -> str:
        """Returns current 'from date' value."""
        return self.find(self.DATE_FROM_INPUT).get_attribute("value")

    def get_date_to(self) -> str:
        """Returns current 'to date' value."""
        return self.find(self.DATE_TO_INPUT).get_attribute("value")

    def set_date_range(self, date_from: str, date_to: str) -> None:
        """Sets date range filter."""
        logger.info(f"Setting date range: {date_from} to {date_to}")
        self.set_date_input(self.DATE_FROM_INPUT, date_from)
        self.set_date_input(self.DATE_TO_INPUT, date_to)

    def click_search(self) -> None:
        """Clicks 'استعلام' search button."""
        logger.info("Clicking Search / استعلام button in Leaving Approval Report...")
        self.click(self.BTN_SEARCH)
        time.sleep(3)

    def filter_table(self, keyword: str) -> None:
        """Types query into instant filter."""
        logger.info(f"Filtering report results by: '{keyword}'")
        self.type_text(self.INPUT_FILTER, keyword)
        time.sleep(0.5)

    def clear_filter(self) -> None:
        """Clears instant filter input."""
        el = self.find(self.INPUT_FILTER)
        el.clear()
        el.send_keys(Keys.BACK_SPACE)
        time.sleep(0.5)

    def is_export_button_ready(self) -> bool:
        """Checks whether Excel export button is visible and enabled."""
        if not self.is_visible(self.BTN_EXPORT_EXCEL, timeout=10):
            return False
        btn = self.find(self.BTN_EXPORT_EXCEL)
        return btn.is_displayed() and btn.is_enabled()
