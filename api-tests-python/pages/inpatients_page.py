import time
import logging
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage

logger = logging.getLogger("BayMaxInpatientsPage")

class InpatientsPage(BasePage):
    """Page Object for Inpatients / Room Residents (/reception/inpatients)."""

    URL = "https://196.218.246.250:4040/reception/inpatients"

    SEARCH_INPUT = (By.CSS_SELECTOR, "[data-test-id='inpatient-list-search-input']")
    BTN_REFRESH = (By.CSS_SELECTOR, "[data-test-id='inpatient-list-refresh-btn']")
    PAGE_HEADER = (By.XPATH, "//h1[contains(text(), 'المقيمين بالغرف')]")

    def open(self) -> "InpatientsPage":
        logger.info(f"Navigating to Inpatients page: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.SEARCH_INPUT, timeout=12)

    def search(self, query: str) -> None:
        logger.info(f"Filtering inpatients list for: '{query}'")
        self.type_text(self.SEARCH_INPUT, query)
        time.sleep(1.5)

    def refresh(self) -> None:
        logger.info("Clicking Refresh button in Inpatients list...")
        self.click(self.BTN_REFRESH)
        time.sleep(1.5)


class ICUInpatientsPage(BasePage):
    """Page Object for ICU Inpatients (/reception/icu)."""

    URL = "https://196.218.246.250:4040/reception/icu"

    SEARCH_INPUT = (By.CSS_SELECTOR, "[data-test-id='inpatient-list-search-input']")
    BTN_REFRESH = (By.CSS_SELECTOR, "[data-test-id='inpatient-list-refresh-btn']")
    PAGE_HEADER = (By.XPATH, "//h1[contains(text(), 'المقيمين بالرعاية المركزة')]")

    def open(self) -> "ICUInpatientsPage":
        logger.info(f"Navigating to ICU Inpatients page: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.SEARCH_INPUT, timeout=12)

    def get_header_title(self) -> str:
        return self.get_text(self.PAGE_HEADER)

    def search(self, query: str) -> None:
        self.type_text(self.SEARCH_INPUT, query)
        time.sleep(1.5)

    def refresh(self) -> None:
        self.click(self.BTN_REFRESH)
        time.sleep(1.5)


class NeonatalInpatientsPage(BasePage):
    """Page Object for Neonatal Inpatients (/reception/neonatal)."""

    URL = "https://196.218.246.250:4040/reception/neonatal"

    SEARCH_INPUT = (By.CSS_SELECTOR, "[data-test-id='inpatient-list-search-input']")
    BTN_REFRESH = (By.CSS_SELECTOR, "[data-test-id='inpatient-list-refresh-btn']")
    PAGE_HEADER = (By.XPATH, "//h1[contains(text(), 'المقيمين بالحضانة')]")

    def open(self) -> "NeonatalInpatientsPage":
        logger.info(f"Navigating to Neonatal Inpatients page: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.SEARCH_INPUT, timeout=12)

    def get_header_title(self) -> str:
        return self.get_text(self.PAGE_HEADER)

    def search(self, query: str) -> None:
        self.type_text(self.SEARCH_INPUT, query)
        time.sleep(1.5)

    def refresh(self) -> None:
        self.click(self.BTN_REFRESH)
        time.sleep(1.5)


class AttendantsPage(BasePage):
    """Page Object for Patient Attendants (/reception/attendants)."""

    URL = "https://196.218.246.250:4040/reception/attendants"

    BTN_LEAVE_ALL = (By.CSS_SELECTOR, "[data-test-id='attendant-list-leave-all-btn']")
    BTN_EXPORT_CSV = (By.CSS_SELECTOR, "[data-test-id='attendant-list-export-csv-btn']")
    SEARCH_INPUT = (By.CSS_SELECTOR, "[data-test-id='attendant-list-search-input']")
    PAGE_SIZE_SELECT = (By.CSS_SELECTOR, "[data-test-id='attendant-list-page-size-select']")

    def open(self) -> "AttendantsPage":
        logger.info(f"Navigating to Attendants page: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.SEARCH_INPUT, timeout=12) and self.is_visible(self.BTN_EXPORT_CSV)

    def search(self, query: str) -> None:
        self.type_text(self.SEARCH_INPUT, query)
        time.sleep(1)

    def clear_search(self) -> None:
        el = self.find(self.SEARCH_INPUT)
        el.clear()
        el.send_keys(Keys.BACK_SPACE)
        time.sleep(0.5)


class RoomManagementPage(BasePage):
    """Page Object for Room Management (/reception/room-management)."""

    URL = "https://196.218.246.250:4040/reception/room-management"

    TAB_ROOMS = (By.CSS_SELECTOR, "[data-test-id='room-management-rooms-tab-btn']")
    TAB_ICU = (By.CSS_SELECTOR, "[data-test-id='room-management-icu-tab-btn']")
    TAB_NEONATAL = (By.CSS_SELECTOR, "[data-test-id='room-management-neonatal-tab-btn']")
    SEARCH_INPUT = (By.CSS_SELECTOR, "[data-test-id='room-management-search-input']")
    TABLE_ROWS = (By.CSS_SELECTOR, "[data-test-id='room-management-row']")
    BTN_SHOW_DETAILS = (By.CSS_SELECTOR, "[data-test-id='room-management-show-details-btn']")

    def open(self) -> "RoomManagementPage":
        logger.info(f"Navigating to Room Management: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.TAB_ROOMS, timeout=12) and self.is_visible(self.SEARCH_INPUT)

    def get_rooms_count(self) -> int:
        return len(self.driver.find_elements(*self.TABLE_ROWS))

    def switch_to_icu_tab(self) -> None:
        self.click(self.TAB_ICU)
        time.sleep(1)

    def switch_to_neonatal_tab(self) -> None:
        self.click(self.TAB_NEONATAL)
        time.sleep(1)

    def switch_to_rooms_tab(self) -> None:
        self.click(self.TAB_ROOMS)
        time.sleep(1)

    def search_room(self, query: str) -> None:
        self.type_text(self.SEARCH_INPUT, query)
        time.sleep(1)

    def clear_search(self) -> None:
        el = self.find(self.SEARCH_INPUT)
        el.clear()
        el.send_keys(Keys.BACK_SPACE)
        time.sleep(0.5)


class RoomOccupancyMapPage(BasePage):
    """Page Object for Room Occupancy Map (/reception/rooms)."""

    URL = "https://196.218.246.250:4040/reception/rooms"

    PAGE_HEADER = (By.XPATH, "//h1[contains(text(), 'إشغال الغرف')] | //h2[contains(text(), 'إشغال الغرف')] | //div[contains(@class, 'page-header')]")
    BTN_BACK = (By.CSS_SELECTOR, "[data-test-id='accomodation-rooms-back-btn']")

    def open(self) -> "RoomOccupancyMapPage":
        logger.info(f"Navigating to Room Map: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.PAGE_HEADER, timeout=12) or self.is_visible(self.BTN_BACK, timeout=12)
