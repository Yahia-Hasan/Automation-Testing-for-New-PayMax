import logging
import time
from typing import Optional
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger("BayMaxSurgeryBookingPage")

class SurgeryBookingPage(BasePage):
    """Page object for Surgery Booking (/reception/surgery-booking)."""

    URL = "https://196.218.246.250:4040/reception/surgery-booking"

    # Locators
    PAGE_HEADER = (By.XPATH, "//div[contains(@class, 'page-header')]//span[contains(text(), 'حجز العمليات')]")
    LOADING_SPINNER = (By.CSS_SELECTOR, ".loading-spinner")

    INPUT_DATE = (By.XPATH, "//input[@data-test-id='surgery-booking-date-input']")
    SELECT_DOCTOR = (By.XPATH, "//ng-select[@data-test-id='surgery-booking-doctor-select']")
    SELECT_SPECIALTY = (By.XPATH, "//ng-select[@data-test-id='surgery-booking-specialty-select']")
    SELECT_SURGERY = (By.XPATH, "//ng-select[@data-test-id='surgery-booking-surgery-select']")
    SELECT_RESERVATION = (By.XPATH, "//ng-select[@data-test-id='surgery-booking-reservation-select']")
    INPUT_SHORT_CODE = (By.XPATH, "//input[@data-test-id='surgery-booking-short-code-input']")
    INPUT_PATIENT_NAME = (By.XPATH, "//input[@data-test-id='surgery-booking-patient-name-input']")

    BTN_SEARCH = (By.XPATH, "//button[@data-test-id='surgery-booking-search-btn']")
    BTN_ADD = (By.XPATH, "//button[@data-test-id='surgery-booking-add-btn']")
    BTN_CLEAR = (By.XPATH, "//button[@data-test-id='surgery-booking-clear-btn']")

    def open(self) -> "SurgeryBookingPage":
        logger.info(f"Opening Surgery Booking page directly: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def wait_for_data_load(self, timeout: int = 20) -> None:
        """Waits for initial async loading spinner to disappear."""
        logger.info("Waiting for surgery booking data to finish loading...")
        start_time = time.time()
        while time.time() - start_time < timeout:
            spinners = self.driver.find_elements(*self.LOADING_SPINNER)
            visible_spinners = [s for s in spinners if s.is_displayed()]
            if not visible_spinners:
                logger.info(f"Loading completed after {time.time() - start_time:.1f}s")
                return
            time.sleep(0.5)
        logger.warning("Timeout waiting for loading spinner to disappear.")

    def is_loaded(self) -> bool:
        """Verifies surgery booking header and search button are loaded."""
        self.wait_for_data_load()
        return self.is_visible(self.BTN_SEARCH, timeout=10)

    def get_header_title(self) -> str:
        """Returns the page title text."""
        return self.get_text(self.PAGE_HEADER)

    def get_booking_date(self) -> str:
        """Returns the current booking date value."""
        return self.find(self.INPUT_DATE).get_attribute("value")

    def enter_patient_code(self, code: str) -> None:
        """Fills patient short code / file number."""
        logger.info(f"Entering patient short code: '{code}'")
        self.type_text(self.INPUT_SHORT_CODE, code)

    def enter_patient_name(self, name: str) -> None:
        """Fills patient name."""
        logger.info(f"Entering patient name: '{name}'")
        self.type_text(self.INPUT_PATIENT_NAME, name)

    def get_patient_code_value(self) -> str:
        """Returns patient code input value."""
        return self.find(self.INPUT_SHORT_CODE).get_attribute("value")

    def get_patient_name_value(self) -> str:
        """Returns patient name input value."""
        return self.find(self.INPUT_PATIENT_NAME).get_attribute("value")

    def click_search(self) -> None:
        """Clicks search button."""
        logger.info("Clicking Search button in surgery booking...")
        self.click(self.BTN_SEARCH)
        time.sleep(1)

    def click_clear(self) -> None:
        """Clicks new / clear button (جديد)."""
        logger.info("Clicking Clear / جديد button...")
        self.click(self.BTN_CLEAR)
        time.sleep(0.5)

    def is_add_button_ready(self) -> bool:
        """Checks if Add button (اضافة) is present and visible."""
        return self.is_visible(self.BTN_ADD, timeout=5)
