from typing import Optional, List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
from config import settings

class ReceptionPage(BasePage):
    """
    Page Object for the Reception / Medical File component (الملف الطبى / بيانات المريض).
    Route: /reception
    Component: <app-patient-data>
    """

    # --- Locators (Primary: [data-test-id] / [test-id]) ---
    TOAST_STACK = (By.CSS_SELECTOR, "[data-test-id='global-toast-stack'], [test-id='global-toast-stack']")
    TOAST_ITEM = (By.CSS_SELECTOR, ".toast-item")
    TOAST_MSG = (By.CSS_SELECTOR, ".toast-item .msg")
    
    # Top Action Bar
    UNKNOWN_PATIENT_BTN = (By.CSS_SELECTOR, "[data-test-id='patient-data-unknown-patient-btn'], [test-id='patient-data-unknown-patient-btn']")
    RESERVATION_AGENDA_BTN = (By.CSS_SELECTOR, "[data-test-id='patient-data-reservation-agenda-btn'], [test-id='patient-data-reservation-agenda-btn']")
    SEARCH_INPUT = (By.CSS_SELECTOR, "[data-test-id='patient-data-search-input'], [test-id='patient-data-search-input']")
    
    # Core Patient Info
    PATIENT_CODE_INPUT = (By.CSS_SELECTOR, "[data-test-id='patient-data-patient-code-input'], [test-id='patient-data-patient-code-input']")
    PATIENT_NAME_INPUT = (By.CSS_SELECTOR, "[data-test-id='patient-data-patient-name-input'], [test-id='patient-data-patient-name-input']")
    PATIENT_NAME_EN_INPUT = (By.CSS_SELECTOR, "[data-test-id='patient-data-patient-name-en-input'], [test-id='patient-data-patient-name-en-input']")
    MOBILE_PHONE_INPUT = (By.CSS_SELECTOR, "[data-test-id='patient-data-mobile-phone-input'], [test-id='patient-data-mobile-phone-input']")
    HOME_PHONE_INPUT = (By.CSS_SELECTOR, "[data-test-id='patient-data-home-phone-input'], [test-id='patient-data-home-phone-input']")
    WHATSAPP_SAME_CHECKBOX = (By.CSS_SELECTOR, "[data-test-id='patient-data-whatsapp-same-checkbox'], [test-id='patient-data-whatsapp-same-checkbox']")
    WHATSAPP_INPUT = (By.CSS_SELECTOR, "[data-test-id='patient-data-whatsapp-input'], [test-id='patient-data-whatsapp-input']")
    
    # Demographics & IDs
    NATIONALITY_SELECT = (By.CSS_SELECTOR, "[data-test-id='patient-data-nationality-select'], [test-id='patient-data-nationality-select']")
    ID_TYPE_SELECT = (By.CSS_SELECTOR, "[data-test-id='patient-data-id-type-select'], [test-id='patient-data-id-type-select']")
    ID_NUMBER_INPUT = (By.CSS_SELECTOR, "[data-test-id='patient-data-id-number-input'], [test-id='patient-data-id-number-input']")
    BIRTH_DATE_INPUT = (By.CSS_SELECTOR, "[data-test-id='patient-data-birth-date-input'], [test-id='patient-data-birth-date-input']")
    RELIGION_SELECT = (By.CSS_SELECTOR, "[data-test-id='patient-data-religion-select'], [test-id='patient-data-religion-select']")
    AGE_YEARS_INPUT = (By.CSS_SELECTOR, "[data-test-id='patient-data-age-years-input'], [test-id='patient-data-age-years-input']")
    AGE_MONTHS_INPUT = (By.CSS_SELECTOR, "[data-test-id='patient-data-age-months-input'], [test-id='patient-data-age-months-input']")
    MARITAL_STATUS_SELECT = (By.CSS_SELECTOR, "[data-test-id='patient-data-marital-status-select'], [test-id='patient-data-marital-status-select']")
    GENDER_SELECT = (By.CSS_SELECTOR, "[data-test-id='patient-data-gender-select'], [test-id='patient-data-gender-select']")
    
    # Address & Location
    ADDRESS_INPUT = (By.CSS_SELECTOR, "[data-test-id='patient-data-address-input'], [test-id='patient-data-address-input']")
    CITY_SELECT = (By.CSS_SELECTOR, "[data-test-id='patient-data-city-select'], [test-id='patient-data-city-select']")
    ZONE_SELECT = (By.CSS_SELECTOR, "[data-test-id='patient-data-zone-select'], [test-id='patient-data-zone-select']")
    BUILDING_NUMBER_INPUT = (By.CSS_SELECTOR, "[data-test-id='patient-data-building-number-input'], [test-id='patient-data-building-number-input']")
    
    # Additional Details
    JOB_SELECT = (By.CSS_SELECTOR, "[data-test-id='patient-data-job-select'], [test-id='patient-data-job-select']")
    KNOWING_CHANNEL_SELECT = (By.CSS_SELECTOR, "[data-test-id='patient-data-knowing-channel-select'], [test-id='patient-data-knowing-channel-select']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "[data-test-id='patient-data-email-input'], [test-id='patient-data-email-input']")
    CONTACT_METHOD_SELECT = (By.CSS_SELECTOR, "[data-test-id='patient-data-contact-method-select'], [test-id='patient-data-contact-method-select']")
    CONTACT_TIME_INPUT = (By.CSS_SELECTOR, "[data-test-id='patient-data-contact-time-input'], [test-id='patient-data-contact-time-input']")
    CHILDREN_COUNT_SELECT = (By.CSS_SELECTOR, "[data-test-id='patient-data-children-count-select'], [test-id='patient-data-children-count-select']")
    SPECIALITY_INPUT = (By.CSS_SELECTOR, "[data-test-id='patient-data-speciality-input'], [test-id='patient-data-speciality-input']")
    HOBBY_INPUT = (By.CSS_SELECTOR, "[data-test-id='patient-data-hobby-input'], [test-id='patient-data-hobby-input']")
    NOTES_TEXTAREA = (By.CSS_SELECTOR, "[data-test-id='patient-data-notes-textarea'], [test-id='patient-data-notes-textarea']")
    ADDED_BY_INPUT = (By.CSS_SELECTOR, "[data-test-id='patient-data-added-by-input'], [test-id='patient-data-added-by-input']")
    ADDED_DATE_INPUT = (By.CSS_SELECTOR, "[data-test-id='patient-data-added-date-input'], [test-id='patient-data-added-date-input']")
    
    # Tabs
    CONTRACT_TAB_BTN = (By.CSS_SELECTOR, "[data-test-id='patient-data-contract-tab-btn'], [test-id='patient-data-contract-tab-btn']")
    DOCUMENTS_TAB_BTN = (By.CSS_SELECTOR, "[data-test-id='patient-data-documents-tab-btn'], [test-id='patient-data-documents-tab-btn']")
    
    # Action Buttons
    SAVE_BTN = (By.CSS_SELECTOR, "[data-test-id='patient-data-save-btn'], [test-id='patient-data-save-btn']")
    NEW_BTN = (By.CSS_SELECTOR, "[data-test-id='patient-data-new-btn'], [test-id='patient-data-new-btn']")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def navigate_to(self) -> "ReceptionPage":
        """Navigates directly to the Reception page."""
        target_url = f"{settings.SPA_BASE_URL}/reception"
        if target_url not in self.driver.current_url:
            self.driver.get(target_url)
        self.wait_page_loaded()
        return self

    def wait_page_loaded(self) -> None:
        """Waits until key components of the page are ready."""
        self.wait_visible(self.PATIENT_NAME_INPUT)
        self.wait_visible(self.SEARCH_INPUT)

    def is_page_loaded(self) -> bool:
        """Returns True if the reception patient form is loaded and visible."""
        return self.is_visible(self.PATIENT_NAME_INPUT) and self.is_visible(self.SAVE_BTN)

    def get_patient_name(self) -> str:
        """Returns current value in the patient name input."""
        el = self.find(self.PATIENT_NAME_INPUT)
        return el.get_attribute("value") or ""

    def enter_patient_name(self, name: str) -> None:
        """Types patient name in Arabic and triggers Angular events."""
        self.send_keys(self.PATIENT_NAME_INPUT, name)
        el = self.find(self.PATIENT_NAME_INPUT)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input')); arguments[0].dispatchEvent(new Event('change'));", el)

    def enter_mobile_phone(self, phone: str) -> None:
        """Types mobile phone number and triggers Angular events."""
        self.send_keys(self.MOBILE_PHONE_INPUT, phone)
        el = self.find(self.MOBILE_PHONE_INPUT)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input')); arguments[0].dispatchEvent(new Event('change'));", el)

    def is_whatsapp_same_checked(self) -> bool:
        """Checks if WhatsApp same as mobile checkbox is checked."""
        el = self.find(self.WHATSAPP_SAME_CHECKBOX)
        return el.is_selected()

    def toggle_whatsapp_same(self) -> None:
        """Clicks the WhatsApp same as mobile checkbox."""
        chk = self.find(self.WHATSAPP_SAME_CHECKBOX)
        self.driver.execute_script("arguments[0].click();", chk)

    def get_whatsapp_value(self) -> str:
        """Returns current value of the WhatsApp input."""
        el = self.find(self.WHATSAPP_INPUT)
        return el.get_attribute("value") or ""

    def is_whatsapp_disabled(self) -> bool:
        """Checks if WhatsApp input is disabled."""
        el = self.find(self.WHATSAPP_INPUT)
        return not el.is_enabled() or el.get_attribute("disabled") is not None

    def enter_birth_date(self, date_str: str) -> None:
        """Enters birth date in YYYY-MM-DD format using native event dispatching."""
        el = self.find(self.BIRTH_DATE_INPUT)
        self.driver.execute_script(
            "arguments[0].value = arguments[1]; "
            "arguments[0].dispatchEvent(new Event('input')); "
            "arguments[0].dispatchEvent(new Event('change'));",
            el,
            date_str
        )

    def get_age_years(self) -> str:
        """Returns the calculated age in years."""
        el = self.find(self.AGE_YEARS_INPUT)
        return el.get_attribute("value") or ""

    def click_unknown_patient(self) -> None:
        """Clicks the unknown patient (مريض غير معروف) button."""
        self.click(self.UNKNOWN_PATIENT_BTN)

    def click_new(self) -> None:
        """Clicks the New (جديد) button to clear/reset the form."""
        self.click(self.NEW_BTN)

    def click_save(self) -> None:
        """Clicks the Save (اضافة / حفظ) button safely with scrolling."""
        btn = self.find(self.SAVE_BTN)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        self.click(self.SAVE_BTN)

    def search_patient(self, query: str) -> None:
        """Enters search term into the quick search box."""
        self.send_keys(self.SEARCH_INPUT, query)

    def get_toast_messages(self) -> List[str]:
        """Returns visible toast notification messages if any."""
        items = self.find_all(self.TOAST_MSG, timeout=3)
        return [item.text.strip() for item in items if item.is_displayed() and item.text.strip()]

    def wait_for_toast(self, expected_substring: str, timeout: int = 5) -> str:
        """Waits until a toast containing expected text appears."""
        def check(d):
            msgs = self.get_toast_messages()
            for m in msgs:
                if expected_substring in m:
                    return m
            return False

        return WebDriverWait(self.driver, timeout).until(
            check,
            message=f"Toast with text '{expected_substring}' did not appear within {timeout}s."
        )
