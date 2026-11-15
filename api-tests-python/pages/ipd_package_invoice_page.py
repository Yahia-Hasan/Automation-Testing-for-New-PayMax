import time
import logging
from typing import Optional, Dict
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger("BayMaxIpdPackageInvoicePage")

class IpdPackageInvoicePage(BasePage):
    """
    Page Object for Financial IPD Package Invoice screen
    (/patient-accounts/ipd-package-invoice?rid=...).
    """

    # Navigation & Action Buttons
    BTN_BACK = (By.CSS_SELECTOR, "[data-test-id='ipd-pkg-back-btn'], button.btn-back, [data-test-id='invoice-details-back-btn']")
    BTN_PRINT = (By.CSS_SELECTOR, "[data-test-id='ipd-pkg-print-btn']")
    BTN_EXCEL = (By.CSS_SELECTOR, "[data-test-id='ipd-pkg-excel-btn']")

    # Financial Limit Elements
    VAL_PATIENT_NAME = (By.CSS_SELECTOR, "[data-test-id='ipd-pkg-patient-name-val']")
    VAL_PACKAGE_LIMIT = (By.CSS_SELECTOR, "[data-test-id='ipd-pkg-package-limit-val']")
    VAL_CONSUMED_AMOUNT = (By.CSS_SELECTOR, "[data-test-id='ipd-pkg-consumed-amount-val']")
    VAL_REMAINING_AMOUNT = (By.CSS_SELECTOR, "[data-test-id='ipd-pkg-remaining-amount-val']")
    VAL_EXTRA_CHARGE = (By.CSS_SELECTOR, "[data-test-id='ipd-pkg-extra-charge-val']")

    # Services Table
    TABLE_SERVICES = (By.CSS_SELECTOR, "table.data-table, table.acct-table, table")
    TABLE_ROWS = (By.CSS_SELECTOR, "table.data-table tbody tr, table.acct-table tbody tr, table tbody tr")


    def open_for_reservation(self, rid: int) -> "IpdPackageInvoicePage":
        """Navigates to the Financial Package Invoice page."""
        url = f"https://196.218.246.250:4040/patient-accounts/ipd-package-invoice?rid={rid}"
        logger.info(f"Opening Financial Package Invoice: {url}")
        self.driver.get(url)
        time.sleep(3)
        return self

    def is_loaded(self) -> bool:
        """Checks if the financial package invoice page has loaded."""
        return self.is_visible(self.TABLE_SERVICES, timeout=10) or self.is_visible(self.BTN_BACK, timeout=10)

    def get_services_count(self, timeout: int = 10) -> int:
        """Returns the number of service rows in the financial limit breakdown."""
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr, [data-test-id='ipd-pkg-services-table'] tbody tr"))
            )
        except Exception:
            pass
        rows = self.find_all(self.TABLE_ROWS, timeout=3)
        return len(rows)


    def click_back(self) -> None:
        """Clicks Back button."""
        logger.info("Clicking Back button on Financial Package Invoice...")
        if self.is_visible(self.BTN_BACK, timeout=5):
            self.click(self.BTN_BACK)
            time.sleep(1.5)
