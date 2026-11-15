import logging
import time
from typing import Optional
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger("BayMaxEmergencyTransfersPage")

class EmergencyTransfersPage(BasePage):
    """Page object for Emergency Patient Transfers (/reception/emergency-transfers)."""

    URL = "https://196.218.246.250:4040/reception/emergency-transfers"

    # Locators
    PAGE_HEADER = (By.XPATH, "//h1[contains(text(), 'طلبات تحويل المرضى من الطوارئ للداخلى')]")
    DATE_FROM_INPUT = (By.XPATH, "//input[@data-test-id='emergency-transfers-date-from-input']")
    DATE_TO_INPUT = (By.XPATH, "//input[@data-test-id='emergency-transfers-date-to-input']")
    BTN_SEARCH = (By.XPATH, "//button[@data-test-id='emergency-transfers-search-btn']")

    def open(self) -> "EmergencyTransfersPage":
        logger.info(f"Opening Emergency Transfers page directly: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        """Verifies page header and search button are visible."""
        return self.is_visible(self.PAGE_HEADER, timeout=15) and self.is_visible(self.BTN_SEARCH, timeout=10)

    def get_header_title(self) -> str:
        """Returns the page header text."""
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
        """Clicks 'عرض' search button."""
        logger.info("Clicking Search / عرض button in Emergency Transfers...")
        self.click(self.BTN_SEARCH)
        time.sleep(2)
