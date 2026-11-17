import time
import logging
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger("BayMaxEmergencyModule")

class EmergencyWaitingListPage(BasePage):
    """Page Object for Emergency Waiting List (/emergency/waiting-list)."""

    URL = "https://196.218.246.250:4040/emergency/waiting-list"

    INPUT_SEARCH = (By.CSS_SELECTOR, "[data-test-id='emergency-waiting-list-search-input']")
    BTN_EXPORT_EXCEL = (By.CSS_SELECTOR, "[data-test-id='emergency-waiting-list-export-excel-btn']")
    TABLE_ROWS = (By.CSS_SELECTOR, "[data-test-id='emergency-waiting-list-row']")

    def open(self) -> "EmergencyWaitingListPage":
        logger.info(f"Opening Emergency Waiting List: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.INPUT_SEARCH, timeout=12)

    def search(self, query: str) -> None:
        self.type_text(self.INPUT_SEARCH, query)
        time.sleep(1)


class EmergencyEditVisitPage(BasePage):
    """Page Object for Edit Emergency Visit (/emergency/edit-visit)."""

    URL = "https://196.218.246.250:4040/emergency/edit-visit"

    INPUT_FROM_DATE = (By.CSS_SELECTOR, "[data-test-id='edit-emergency-visit-from-date-input']")
    INPUT_TO_DATE = (By.CSS_SELECTOR, "[data-test-id='edit-emergency-visit-to-date-input']")
    BTN_LOAD = (By.CSS_SELECTOR, "[data-test-id='edit-emergency-visit-load-btn']")
    INPUT_SEARCH = (By.CSS_SELECTOR, "[data-test-id='edit-emergency-visit-search-input']")
    BTN_EXPORT_EXCEL = (By.CSS_SELECTOR, "[data-test-id='edit-emergency-visit-export-excel-btn']")

    def open(self) -> "EmergencyEditVisitPage":
        logger.info(f"Opening Edit Emergency Visit: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.INPUT_FROM_DATE, timeout=12) and self.is_visible(self.BTN_LOAD)

    def click_load(self) -> None:
        self.click(self.BTN_LOAD)
        time.sleep(2)


class EmergencyAdmissionDischargePage(BasePage):
    """Page Object for Emergency Admission & Discharge (/emergency/admission-discharge-report)."""

    URL = "https://196.218.246.250:4040/emergency/admission-discharge-report"

    INPUT_FROM_DATE = (By.CSS_SELECTOR, "[data-test-id='emergency-cases-report-from-date-input']")
    INPUT_TO_DATE = (By.CSS_SELECTOR, "[data-test-id='emergency-cases-report-to-date-input']")
    SELECT_REPORT_TYPE = (By.CSS_SELECTOR, "[data-test-id='emergency-cases-report-report-type-select']")
    BTN_LOAD = (By.CSS_SELECTOR, "[data-test-id='emergency-cases-report-load-btn']")
    INPUT_SEARCH = (By.CSS_SELECTOR, "[data-test-id='emergency-cases-report-search-input']")
    BTN_EXPORT_EXCEL = (By.CSS_SELECTOR, "[data-test-id='emergency-cases-report-export-excel-btn']")

    def open(self) -> "EmergencyAdmissionDischargePage":
        logger.info(f"Opening Emergency Admission/Discharge: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.INPUT_FROM_DATE, timeout=12) and self.is_visible(self.BTN_LOAD)

    def click_load(self) -> None:
        self.click(self.BTN_LOAD)
        time.sleep(2)


class EmergencyMedicalReportsPage(BasePage):
    """Page Object for Emergency Medical Reports (/emergency/medical-reports)."""

    URL = "https://196.218.246.250:4040/emergency/medical-reports"

    INPUT_FROM_DATE = (By.CSS_SELECTOR, "input[type='date']")
    BTN_SHOW = (By.CSS_SELECTOR, "button.btn-primary")
    INPUT_SEARCH = (By.CSS_SELECTOR, "input.search-input")

    def open(self) -> "EmergencyMedicalReportsPage":
        logger.info(f"Opening Emergency Medical Reports: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.INPUT_FROM_DATE, timeout=12) and self.is_visible(self.BTN_SHOW)

    def click_show(self) -> None:
        self.click(self.BTN_SHOW)
        time.sleep(2)


class EmergencyBedOccupancyPage(BasePage):
    """Page Object for Emergency Bed Occupancy (/emergency/bed-occupancy)."""

    URL = "https://196.218.246.250:4040/emergency/bed-occupancy"

    INPUT_SEARCH = (By.CSS_SELECTOR, "[data-test-id='emergency-bed-occupancy-search-input']")
    BTN_EXPORT_EXCEL = (By.CSS_SELECTOR, "[data-test-id='emergency-bed-occupancy-export-excel-btn']")
    BTN_FLOOR_TOGGLE = (By.CSS_SELECTOR, "[data-test-id='emergency-bed-occupancy-floor-toggle-btn']")

    def open(self) -> "EmergencyBedOccupancyPage":
        logger.info(f"Opening Emergency Bed Occupancy: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.INPUT_SEARCH, timeout=12)


class EmergencyCancelLeavedPage(BasePage):
    """Page Object for Cancel Leaved Emergency Patient (/emergency/cancel-leaved)."""

    URL = "https://196.218.246.250:4040/emergency/cancel-leaved"

    INPUT_FROM_DATE = (By.CSS_SELECTOR, "[data-test-id='cancel-leaved-emergency-from-date-input']")
    INPUT_TO_DATE = (By.CSS_SELECTOR, "[data-test-id='cancel-leaved-emergency-to-date-input']")
    BTN_LOAD = (By.CSS_SELECTOR, "[data-test-id='cancel-leaved-emergency-load-btn']")

    def open(self) -> "EmergencyCancelLeavedPage":
        logger.info(f"Opening Cancel Leaved Emergency: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.INPUT_FROM_DATE, timeout=12) and self.is_visible(self.BTN_LOAD)

    def click_load(self) -> None:
        self.click(self.BTN_LOAD)
        time.sleep(2)
