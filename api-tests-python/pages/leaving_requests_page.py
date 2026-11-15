import logging
import time
from typing import List, Dict
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage

logger = logging.getLogger("BayMaxLeavingRequestsPage")

class LeavingRequestsPage(BasePage):
    """Page object for Inpatients Pending Discharge / Leaving Requests (/waiting-list/leaving-requests)."""

    URL = "https://196.218.246.250:4040/waiting-list/leaving-requests"

    # Locators
    PAGE_HEADER = (By.XPATH, "//h1[contains(text(), 'طلبات المغادرة')]")
    INPUT_SEARCH = (By.XPATH, "//input[@data-test-id='leaving-requests-search-input']")
    BTN_RELOAD = (By.XPATH, "//button[@data-test-id='leaving-requests-reload-btn']")
    TABLE_HEADERS = (By.XPATH, "//table//thead//th")
    TABLE_ROWS = (By.XPATH, "//tr[@data-test-id='leaving-requests-row']")
    PAGE_SIZE_SELECT = (By.XPATH, "//select[@data-test-id='leaving-requests-page-size-select']")
    BTN_PREV_PAGE = (By.XPATH, "//button[@data-test-id='leaving-requests-prev-page-btn']")
    BTN_NEXT_PAGE = (By.XPATH, "//button[@data-test-id='leaving-requests-next-page-btn']")
    BTNS_PAGE_NUMBERS = (By.XPATH, "//button[@data-test-id='leaving-requests-page-btn']")

    def open(self) -> "LeavingRequestsPage":
        logger.info(f"Opening Leaving Requests page directly: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        """Verifies leaving requests header and table are visible."""
        return self.is_visible(self.PAGE_HEADER, timeout=15)

    def get_header_title(self) -> str:
        """Returns the page header title."""
        return self.get_text(self.PAGE_HEADER)

    def get_headers(self) -> List[str]:
        """Returns list of table header names."""
        elements = self.driver.find_elements(*self.TABLE_HEADERS)
        return [el.text.strip() for el in elements if el.text.strip()]

    def get_rows_count(self) -> int:
        """Returns number of displayed patient rows."""
        rows = self.driver.find_elements(*self.TABLE_ROWS)
        return len(rows)

    def get_first_row_data(self) -> Dict[str, str]:
        """Extracts data from the first row."""
        rows = self.driver.find_elements(*self.TABLE_ROWS)
        if not rows:
            return {}
        tds = [td.text.strip() for td in rows[0].find_elements(By.TAG_NAME, "td")]
        return {
            "admission_code": tds[0] if len(tds) > 0 else "",
            "patient_code": tds[1] if len(tds) > 1 else "",
            "patient_name": tds[2] if len(tds) > 2 else "",
            "client": tds[3] if len(tds) > 3 else "",
            "registered_by": tds[4] if len(tds) > 4 else "",
            "registration_date": tds[5] if len(tds) > 5 else ""
        }

    def search(self, query: str) -> None:
        """Enters search term into the table search input."""
        logger.info(f"Searching leaving requests table with: '{query}'")
        self.type_text(self.INPUT_SEARCH, query)
        time.sleep(1)

    def clear_search(self) -> None:
        """Clears the table search input."""
        logger.info("Clearing table search input...")
        el = self.find(self.INPUT_SEARCH)
        el.clear()
        el.send_keys(Keys.BACK_SPACE)
        time.sleep(1)

    def click_reload(self) -> None:
        """Clicks reload button."""
        logger.info("Clicking reload button...")
        self.click(self.BTN_RELOAD)
        time.sleep(1.5)
