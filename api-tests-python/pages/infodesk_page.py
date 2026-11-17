import time
import logging
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage

logger = logging.getLogger("BayMaxInfoDeskPage")

class PriceListsPage(BasePage):
    """Page Object for InfoDesk Price Lists screen (/info-desk/price-lists)."""

    URL = "https://196.218.246.250:4040/info-desk/price-lists"

    SELECT_CLIENT = (By.CSS_SELECTOR, "[data-test-id='price-lists-client-select']")
    BTN_SEARCH = (By.CSS_SELECTOR, "[data-test-id='price-lists-search-btn']")

    def open(self) -> "PriceListsPage":
        logger.info(f"Opening Price Lists screen: {self.URL}")
        self.driver.get(self.URL)
        self.find(self.BTN_SEARCH, timeout=12)
        return self

    def click_search(self) -> None:
        """Clicks search to load price lists."""
        logger.info("Clicking Search on Price Lists...")
        self.click(self.BTN_SEARCH)
        time.sleep(2)

    def is_filter_visible(self) -> bool:
        """Verifies client select and search button are displayed."""
        return self.is_visible(self.SELECT_CLIENT) and self.is_visible(self.BTN_SEARCH)


class DoctorsListPage(BasePage):
    """Page Object for InfoDesk Doctors Directory screen (/info-desk/doctors)."""

    URL = "https://196.218.246.250:4040/info-desk/doctors"

    INPUT_SEARCH = (By.CSS_SELECTOR, "[data-test-id='doctors-list-search-input']")
    CHECKBOX_ACTIVE_ONLY = (By.CSS_SELECTOR, "[data-test-id='doctors-list-active-only-checkbox']")
    BTN_EXPORT_EXCEL = (By.CSS_SELECTOR, "[data-test-id='doctors-list-export-excel-btn']")

    def open(self) -> "DoctorsListPage":
        logger.info(f"Opening Doctors List screen: {self.URL}")
        self.driver.get(self.URL)
        self.find(self.INPUT_SEARCH, timeout=12)
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.INPUT_SEARCH) and self.is_visible(self.BTN_EXPORT_EXCEL)

    def search_doctor(self, query: str) -> None:
        """Search by doctor name or specialty."""
        logger.info(f"Searching doctors directory for: '{query}'")
        self.type_text(self.INPUT_SEARCH, query)
        time.sleep(1.5)


class ShiftManagersPage(BasePage):
    """Page Object for Shift Managers (/info-desk/shift-managers)."""

    URL = "https://196.218.246.250:4040/info-desk/shift-managers"

    BTN_ADD_NEW = (By.CSS_SELECTOR, "[data-test-id='shift-managers-add-new-btn']")
    BTN_EXPORT_EXCEL = (By.CSS_SELECTOR, "[data-test-id='shift-managers-export-excel-btn']")
    INPUT_FILTER = (By.CSS_SELECTOR, "[data-test-id='shift-managers-filter-input']")
    TABLE_ROWS = (By.CSS_SELECTOR, "[data-test-id='shift-managers-row']")

    def open(self) -> "ShiftManagersPage":
        logger.info(f"Opening Shift Managers: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.BTN_ADD_NEW, timeout=12) and self.is_visible(self.INPUT_FILTER)

    def get_rows_count(self) -> int:
        return len(self.driver.find_elements(*self.TABLE_ROWS))

    def filter_table(self, query: str) -> None:
        self.type_text(self.INPUT_FILTER, query)
        time.sleep(1)

    def clear_filter(self) -> None:
        el = self.find(self.INPUT_FILTER)
        el.clear()
        el.send_keys(Keys.BACK_SPACE)
        time.sleep(0.5)


class SurgeryNamesPage(BasePage):
    """Page Object for Surgery Names (/info-desk/surgery-names)."""

    URL = "https://196.218.246.250:4040/info-desk/surgery-names"

    SELECT_SPECIALTY = (By.CSS_SELECTOR, "[data-test-id='surgery-names-specialty-select']")
    BTN_SEARCH = (By.CSS_SELECTOR, "[data-test-id='surgery-names-search-btn']")

    def open(self) -> "SurgeryNamesPage":
        logger.info(f"Opening Surgery Names: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.SELECT_SPECIALTY, timeout=12) and self.is_visible(self.BTN_SEARCH)

    def click_search(self) -> None:
        self.click(self.BTN_SEARCH)
        time.sleep(2)


class SurgeryPricesPage(BasePage):
    """Page Object for Surgery Prices (/info-desk/surgery-prices)."""

    URL = "https://196.218.246.250:4040/info-desk/surgery-prices"

    SELECT_CLIENT = (By.CSS_SELECTOR, "[data-test-id='surgery-prices-client-select']")
    SELECT_SPECIALTY = (By.CSS_SELECTOR, "[data-test-id='surgery-prices-specialty-select']")
    SELECT_SURGERY = (By.CSS_SELECTOR, "[data-test-id='surgery-prices-surgery-select']")
    BTN_SEARCH = (By.CSS_SELECTOR, "[data-test-id='surgery-prices-search-btn']")

    def open(self) -> "SurgeryPricesPage":
        logger.info(f"Opening Surgery Prices: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.SELECT_CLIENT, timeout=12) and self.is_visible(self.BTN_SEARCH)

    def click_search(self) -> None:
        self.click(self.BTN_SEARCH)
        time.sleep(2)


class SurgeryAgendaPage(BasePage):
    """Page Object for Surgery Agenda (/info-desk/surgery-agenda)."""

    URL = "https://196.218.246.250:4040/info-desk/surgery-agenda"

    INPUT_FROM_DATE = (By.CSS_SELECTOR, "[data-test-id='surgery-agenda-from-date-input']")
    INPUT_TO_DATE = (By.CSS_SELECTOR, "[data-test-id='surgery-agenda-to-date-input']")
    SELECT_DOCTOR = (By.CSS_SELECTOR, "[data-test-id='surgery-agenda-doctor-select']")
    SELECT_SPECIALTY = (By.CSS_SELECTOR, "[data-test-id='surgery-agenda-specialty-select']")
    SELECT_SURGERY_CODE = (By.CSS_SELECTOR, "[data-test-id='surgery-agenda-surgery-code-select']")
    BTN_SEARCH = (By.CSS_SELECTOR, "[data-test-id='surgery-agenda-search-btn']")

    def open(self) -> "SurgeryAgendaPage":
        logger.info(f"Opening Surgery Agenda: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.INPUT_FROM_DATE, timeout=12) and self.is_visible(self.BTN_SEARCH)

    def click_search(self) -> None:
        self.click(self.BTN_SEARCH)
        time.sleep(2)


class ClinicAgendaPage(BasePage):
    """Page Object for Clinic Agenda (/info-desk/clinic-agenda)."""

    URL = "https://196.218.246.250:4040/info-desk/clinic-agenda"

    INPUT_FROM_DATE = (By.CSS_SELECTOR, "[data-test-id='clinic-agenda-from-date-input']")
    INPUT_TO_DATE = (By.CSS_SELECTOR, "[data-test-id='clinic-agenda-to-date-input']")
    SELECT_DOCTOR = (By.CSS_SELECTOR, "[data-test-id='clinic-agenda-doctor-select']")
    SELECT_SERVICE_GROUP = (By.CSS_SELECTOR, "[data-test-id='clinic-agenda-service-group-select']")
    SELECT_SERVICE = (By.CSS_SELECTOR, "[data-test-id='clinic-agenda-service-select']")
    BTN_SEARCH = (By.CSS_SELECTOR, "[data-test-id='clinic-agenda-search-btn']")

    def open(self) -> "ClinicAgendaPage":
        logger.info(f"Opening Clinic Agenda: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.INPUT_FROM_DATE, timeout=12) and self.is_visible(self.BTN_SEARCH)

    def click_search(self) -> None:
        self.click(self.BTN_SEARCH)
        time.sleep(2)


class PhoneBookPage(BasePage):
    """Page Object for Phone Book (/info-desk/phone-book)."""

    URL = "https://196.218.246.250:4040/info-desk/phone-book"

    BTN_ADD_NEW = (By.CSS_SELECTOR, "[data-test-id='phone-book-add-new-btn']")
    INPUT_FILTER = (By.CSS_SELECTOR, "[data-test-id='phone-book-filter-input']")
    BTN_EXPORT_EXCEL = (By.CSS_SELECTOR, "[data-test-id='phone-book-export-excel-btn']")
    TABLE_ROWS = (By.CSS_SELECTOR, "[data-test-id='phone-book-row']")

    def open(self) -> "PhoneBookPage":
        logger.info(f"Opening Phone Book: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.INPUT_FILTER, timeout=12) and self.is_visible(self.BTN_ADD_NEW)

    def get_rows_count(self) -> int:
        return len(self.driver.find_elements(*self.TABLE_ROWS))

    def filter_table(self, query: str) -> None:
        self.type_text(self.INPUT_FILTER, query)
        time.sleep(1)

    def clear_filter(self) -> None:
        el = self.find(self.INPUT_FILTER)
        el.clear()
        el.send_keys(Keys.BACK_SPACE)
        time.sleep(0.5)


class SurgeriesWaitingListPage(BasePage):
    """Page Object for Surgeries Waiting List (/info-desk/surgeries)."""

    URL = "https://196.218.246.250:4040/info-desk/surgeries"

    INPUT_FROM_DATE = (By.CSS_SELECTOR, "[data-test-id='surgeries-waiting-from-date-input']")
    INPUT_TO_DATE = (By.CSS_SELECTOR, "[data-test-id='surgeries-waiting-to-date-input']")
    BTN_SEARCH = (By.CSS_SELECTOR, "[data-test-id='surgeries-waiting-search-btn']")

    def open(self) -> "SurgeriesWaitingListPage":
        logger.info(f"Opening Surgeries Waiting List: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.INPUT_FROM_DATE, timeout=12) and self.is_visible(self.BTN_SEARCH)

    def click_search(self) -> None:
        self.click(self.BTN_SEARCH)
        time.sleep(2)


class PackagesPage(BasePage):
    """Page Object for Packages Inquiry (/info-desk/packages)."""

    URL = "https://196.218.246.250:4040/info-desk/packages"

    SELECT_PACKAGE = (By.CSS_SELECTOR, "[data-test-id='packages-package-select']")
    SELECT_SURGERY = (By.CSS_SELECTOR, "[data-test-id='packages-surgery-select']")
    SELECT_SPECIALTY = (By.CSS_SELECTOR, "[data-test-id='packages-specialty-select']")
    SELECT_CLIENT = (By.CSS_SELECTOR, "[data-test-id='packages-client-select']")
    BTN_SEARCH = (By.CSS_SELECTOR, "[data-test-id='packages-search-btn']")
    INPUT_FILTER = (By.CSS_SELECTOR, "[data-test-id='packages-filter-input']")
    BTN_EXPORT_EXCEL = (By.CSS_SELECTOR, "[data-test-id='packages-export-excel-btn']")
    TABLE_ROWS = (By.CSS_SELECTOR, "[data-test-id='packages-row']")

    def open(self) -> "PackagesPage":
        logger.info(f"Opening Packages: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.SELECT_PACKAGE, timeout=12) and self.is_visible(self.BTN_SEARCH)

    def get_rows_count(self) -> int:
        return len(self.driver.find_elements(*self.TABLE_ROWS))

    def filter_table(self, query: str) -> None:
        self.type_text(self.INPUT_FILTER, query)
        time.sleep(1)

    def clear_filter(self) -> None:
        el = self.find(self.INPUT_FILTER)
        el.clear()
        el.send_keys(Keys.BACK_SPACE)
        time.sleep(0.5)
