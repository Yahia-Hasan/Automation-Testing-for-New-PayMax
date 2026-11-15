import time
import logging
from typing import List
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger("BayMaxEmergencyPage")

class EmergencyWaitingListPage(BasePage):
    """
    Page Object for the Emergency Waiting List screen (/emergency/waiting-list).
    """

    URL = "https://196.218.246.250:4040/emergency/waiting-list"

    SEARCH_INPUT = (By.CSS_SELECTOR, "[data-test-id='emergency-waiting-list-search-input']")
    BTN_EXPORT_EXCEL = (By.CSS_SELECTOR, "[data-test-id='emergency-waiting-list-export-excel-btn']")
    ROWS = (By.CSS_SELECTOR, "[data-test-id='emergency-waiting-list-row']")
    BTN_PREV_PAGE = (By.CSS_SELECTOR, "[data-test-id='emergency-waiting-list-prev-page-btn']")
    BTN_NEXT_PAGE = (By.CSS_SELECTOR, "[data-test-id='emergency-waiting-list-next-page-btn']")
    SELECT_PAGE_SIZE = (By.CSS_SELECTOR, "[data-test-id='emergency-waiting-list-page-size-select']")

    def open(self) -> "EmergencyWaitingListPage":
        """Navigate to Emergency Waiting List page."""
        logger.info(f"Navigating to Emergency Waiting List: {self.URL}")
        self.driver.get(self.URL)
        self.find(self.SEARCH_INPUT, timeout=12)
        return self

    def is_loaded(self) -> bool:
        """Verify the search input and export button are visible."""
        return self.is_visible(self.SEARCH_INPUT) and self.is_visible(self.BTN_EXPORT_EXCEL)

    def search(self, query: str) -> None:
        """Search inside the emergency waiting list."""
        logger.info(f"Filtering emergency waiting list for: '{query}'")
        search_elem = self.find(self.SEARCH_INPUT)
        search_elem.clear()
        search_elem.send_keys(query)
        time.sleep(1.5)

    def get_row_count(self) -> int:
        """Returns the number of displayed patient rows."""
        rows = self.driver.find_elements(*self.ROWS)
        return len(rows)

    def is_export_excel_visible(self) -> bool:
        """Checks if the Excel Export button is available."""
        return self.is_visible(self.BTN_EXPORT_EXCEL)
