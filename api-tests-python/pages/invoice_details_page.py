import time
import logging
from typing import Optional, Dict, List
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger("BayMaxInvoiceDetailsPage")

class InvoiceDetailsPage(BasePage):
    """
    Page Object for Invoice Details (/patient-accounts/invoice-details?rid=...).
    Handles both Unregistered Invoices (open accounts) and Registered Invoices.
    """

    # Navigation & Action Buttons (handles both data-test-id conventions)
    BTN_BACK = (By.CSS_SELECTOR, "[data-test-id='invoice-details-back-btn'], [data-test-id='inv-details-back-btn'], button.btn-back")
    BTN_CANCEL_INVOICE = (By.CSS_SELECTOR, "[data-test-id='invoice-details-cancel-invoice-btn']")
    BTN_REPORTS_DROPDOWN = (By.CSS_SELECTOR, "[data-test-id='invoice-details-reports-dropdown-btn']")
    BTN_PRINT_STATEMENT = (By.CSS_SELECTOR, "[data-test-id='invoice-details-print-statement-dropdown-btn']")
    BTN_HISTORY = (By.CSS_SELECTOR, "[data-test-id='invoice-details-history-btn']")
    BTN_TRACKING = (By.CSS_SELECTOR, "[data-test-id='invoice-details-tracking-btn']")
    BTN_INFORM_EXIT = (By.CSS_SELECTOR, "[data-test-id='invoice-details-inform-exit-btn']")

    # Tabs (Registered / Comprehensive View)
    TAB_ACCOUNTING = (By.CSS_SELECTOR, "[data-test-id='invoice-details-tab-accounting']")
    TAB_SURGERIES = (By.CSS_SELECTOR, "[data-test-id='invoice-details-tab-surgeries']")
    TAB_ACCOMMODATIONS = (By.CSS_SELECTOR, "[data-test-id='invoice-details-tab-accommodations']")
    TAB_ICU = (By.CSS_SELECTOR, "[data-test-id='invoice-details-tab-icu']")
    TAB_NURSERY = (By.CSS_SELECTOR, "[data-test-id='invoice-details-tab-nursery']")
    TAB_ATTENDANTS = (By.CSS_SELECTOR, "[data-test-id='invoice-details-tab-attendants']")
    TAB_FOOD = (By.CSS_SELECTOR, "[data-test-id='invoice-details-tab-food']")
    TAB_PAYMENT_ORDERS = (By.CSS_SELECTOR, "[data-test-id='invoice-details-tab-paymentOrders']")
    TAB_SUMMARY = (By.CSS_SELECTOR, "[data-test-id='invoice-details-tab-summary']")

    # Tables & Value Cells
    TABLE_SERVICES = (By.CSS_SELECTOR, "table.data-table, table.acct-table, table")
    TABLE_ROWS = (By.CSS_SELECTOR, "table.data-table tbody tr, table.acct-table tbody tr, table tbody tr")


    # Patient & Invoice Info Values
    VAL_PATIENT_NAME = (By.CSS_SELECTOR, "[data-test-id='inv-details-patient-name-val']")
    VAL_INVOICE_NUMBER = (By.CSS_SELECTOR, "[data-test-id='inv-details-invoice-number-val']")
    VAL_PATIENT_TOTAL = (By.CSS_SELECTOR, "[data-test-id='inv-details-patient-total-val'], [data-test-id='invoice-details-total-patient-cash-input']")
    VAL_COMPANY_TOTAL = (By.CSS_SELECTOR, "[data-test-id='inv-details-company-total-val'], [data-test-id='invoice-details-total-credit-input']")
    VAL_NET_TOTAL = (By.CSS_SELECTOR, "[data-test-id='inv-details-net-total-val'], [data-test-id='invoice-details-total-after-tax-input']")

    def open_for_reservation(self, rid: int) -> "InvoiceDetailsPage":
        """Navigates to the invoice details page for a given reservation ID."""
        url = f"https://196.218.246.250:4040/patient-accounts/invoice-details?rid={rid}"
        logger.info(f"Opening Invoice Details: {url}")
        self.driver.get(url)
        time.sleep(3)
        return self

    def is_loaded(self) -> bool:
        """Checks if the invoice details page has loaded by verifying back button or tables."""
        return self.is_visible(self.BTN_BACK, timeout=10) or self.is_visible(self.TABLE_SERVICES, timeout=10)

    def switch_tab(self, tab_name: str) -> bool:
        """Switches between invoice tabs for registered invoices."""
        tab_map = {
            "accounting": self.TAB_ACCOUNTING,
            "surgeries": self.TAB_SURGERIES,
            "accommodations": self.TAB_ACCOMMODATIONS,
            "icu": self.TAB_ICU,
            "nursery": self.TAB_NURSERY,
            "attendants": self.TAB_ATTENDANTS,
            "food": self.TAB_FOOD,
            "payment_orders": self.TAB_PAYMENT_ORDERS,
            "summary": self.TAB_SUMMARY,
        }
        locator = tab_map.get(tab_name.lower())
        if not locator or not self.is_visible(locator, timeout=3):
            logger.info(f"Tab {tab_name} not present in this invoice view.")
            return False

        logger.info(f"Switching to invoice tab: {tab_name}")
        tab_elem = self.find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tab_elem)
        time.sleep(0.3)
        self.click(locator)
        time.sleep(1)
        return True

    def get_services_row_count(self, timeout: int = 10) -> int:
        """Counts how many items/services are in the invoice table."""
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr, [data-test-id='inv-details-services-table'] tbody tr"))
            )
        except Exception:
            pass
        rows = self.find_all(self.TABLE_ROWS, timeout=3)
        return len(rows)


    def is_registered_invoice(self) -> bool:
        """Determines if the loaded invoice is a registered invoice."""
        return self.is_visible(self.BTN_CANCEL_INVOICE, timeout=3) or self.is_visible(self.TAB_ACCOUNTING, timeout=3)

    def click_back(self) -> None:
        """Clicks the Back button."""
        logger.info("Clicking Back button on Invoice Details...")
        if self.is_visible(self.BTN_BACK, timeout=5):
            self.click(self.BTN_BACK)
            time.sleep(1.5)
