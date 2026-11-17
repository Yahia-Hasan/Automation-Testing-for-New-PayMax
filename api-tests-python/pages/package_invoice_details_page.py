import time
import logging
from typing import Optional, Dict
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger("BayMaxPackageInvoiceDetailsPage")

class PackageInvoiceDetailsPage(BasePage):
    """
    Page Object for Quantitative Package Invoice Details screen
    (/patient-accounts/package-invoice-details?rid=...).
    """

    # Navigation & Actions
    BTN_BACK = (By.CSS_SELECTOR, "[data-test-id='pkg-inv-back-btn'], button.btn-back, [data-test-id='invoice-details-back-btn']")
    BTN_PRINT = (By.CSS_SELECTOR, "[data-test-id='pkg-inv-print-btn']")
    BTN_EXCEL = (By.CSS_SELECTOR, "[data-test-id='pkg-inv-excel-btn']")

    # Package Info Elements
    VAL_PATIENT_NAME = (By.CSS_SELECTOR, "[data-test-id='pkg-inv-patient-name-val']")
    VAL_PATIENT_CODE = (By.CSS_SELECTOR, "[data-test-id='pkg-inv-patient-code-val']")
    VAL_PACKAGE_NAME = (By.CSS_SELECTOR, "[data-test-id='pkg-inv-package-name-val']")
    VAL_PACKAGE_PRICE = (By.CSS_SELECTOR, "[data-test-id='pkg-inv-package-price-val']")

    # Items Table
    TABLE_ITEMS = (By.CSS_SELECTOR, "table.data-table, table.acct-table, table")
    TABLE_ROWS = (By.CSS_SELECTOR, "table.data-table tbody tr, table.acct-table tbody tr, table tbody tr")


    # Totals
    VAL_TOTAL_CONSUMED = (By.CSS_SELECTOR, "[data-test-id='pkg-inv-total-consumed-val']")
    VAL_TOTAL_EXTRA = (By.CSS_SELECTOR, "[data-test-id='pkg-inv-total-extra-val']")
    VAL_NET_AMOUNT = (By.CSS_SELECTOR, "[data-test-id='pkg-inv-net-amount-val']")

    def open_for_reservation(self, rid: int) -> "PackageInvoiceDetailsPage":
        """Navigates to the Quantitative Package Invoice Details page."""
        url = f"https://196.218.246.250:4040/patient-accounts/package-invoice-details?rid={rid}"
        logger.info(f"Opening Quantitative Package Invoice: {url}")
        self.driver.get(url)
        time.sleep(3)
        return self

    def is_loaded(self) -> bool:
        """Checks if the package invoice details page has loaded."""
        return self.is_visible(self.TABLE_ITEMS, timeout=10) or self.is_visible(self.BTN_BACK, timeout=10)

    def get_items_count(self, timeout: int = 10) -> int:
        """Returns the number of rows in the package consumption table."""
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr, [data-test-id='pkg-inv-items-table'] tbody tr"))
            )
        except Exception:
            pass
        rows = self.find_all(self.TABLE_ROWS, timeout=3)
        return len(rows)


    def click_back(self) -> None:
        """Clicks Back button."""
        logger.info("Clicking Back button on Package Invoice Details...")
        if self.is_visible(self.BTN_BACK, timeout=5):
            self.click(self.BTN_BACK)
            time.sleep(1.5)
