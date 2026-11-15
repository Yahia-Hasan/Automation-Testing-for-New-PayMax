import time
import logging
from typing import Optional, Dict
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger("BayMaxPatientAdmissionPage")

class PatientAdmissionPage(BasePage):
    """
    Page Object for the Inpatient Admission Screen (/reception/patient/{id}/admission).
    Handles admission details, responsible person, and tab switches (rooms, ICU, neonatal, surgeries, payments).
    """

    # Navigation and Action buttons
    BTN_BACK = (By.CSS_SELECTOR, "[data-test-id='patient-admission-back-btn']")
    BTN_SAVE = (By.CSS_SELECTOR, "[data-test-id='patient-admission-save-btn']")

    # Core Admission Fields
    INPUT_RESERVATION_ID = (By.CSS_SELECTOR, "[data-test-id='patient-admission-reservation-id-input']")
    INPUT_RESERVATION_DATE = (By.CSS_SELECTOR, "[data-test-id='patient-admission-reservation-date-input']")

    # Responsible Person Fields
    CHECKBOX_SAME_AS_PATIENT = (By.CSS_SELECTOR, "[data-test-id='patient-admission-same-as-patient-checkbox']")
    INPUT_RESPONSIBLE_NAME = (By.CSS_SELECTOR, "[data-test-id='patient-admission-responsible-name-input']")
    INPUT_RESPONSIBLE_PHONES = (By.CSS_SELECTOR, "[data-test-id='patient-admission-responsible-phones-input']")
    INPUT_RESPONSIBLE_ADDRESS = (By.CSS_SELECTOR, "[data-test-id='patient-admission-responsible-address-input']")

    # Notes
    TEXTAREA_NOTES = (By.CSS_SELECTOR, "[data-test-id='patient-admission-reserv-notes-textarea']")

    # Core Dropdowns
    SELECT_INS_COMPANY = (By.CSS_SELECTOR, "[data-test-id='patient-admission-ins-company-select']")
    SELECT_CASE_TYPE = (By.CSS_SELECTOR, "[data-test-id='patient-admission-case-type-select']")
    SELECT_SPECIALTY = (By.CSS_SELECTOR, "[data-test-id='patient-admission-specialty-select']")
    SELECT_DOCTOR = (By.CSS_SELECTOR, "[data-test-id='patient-admission-doctor-select']")
    SELECT_REFERRAL_SOURCE = (By.CSS_SELECTOR, "[data-test-id='patient-admission-referral-source-select']")
    SELECT_TRANSFER_DOCTOR = (By.CSS_SELECTOR, "[data-test-id='patient-admission-transfer-doctor-select']")
    SELECT_ICD = (By.CSS_SELECTOR, "[data-test-id='patient-admission-icd-select']")

    # Additional Checkboxes
    CHECKBOX_PACKAGE_CASE = (By.CSS_SELECTOR, "[data-test-id='patient-admission-package-case-checkbox']")
    CHECKBOX_CAN_VISIT = (By.CSS_SELECTOR, "[data-test-id='patient-admission-can-visit-checkbox']")
    CHECKBOX_VIP = (By.CSS_SELECTOR, "[data-test-id='patient-admission-vip-checkbox']")

    # Sub-tabs
    TAB_ROOMS = (By.CSS_SELECTOR, "[data-test-id='patient-admission-rooms-tab-btn']")
    TAB_ICU = (By.CSS_SELECTOR, "[data-test-id='patient-admission-icu-tab-btn']")
    TAB_NEONATAL = (By.CSS_SELECTOR, "[data-test-id='patient-admission-neonatal-tab-btn']")
    TAB_SURGERIES = (By.CSS_SELECTOR, "[data-test-id='patient-admission-surgeries-tab-btn']")
    TAB_PAYMENTS = (By.CSS_SELECTOR, "[data-test-id='patient-admission-payments-tab-btn']")
    TAB_DIAGNOSIS = (By.CSS_SELECTOR, "[data-test-id='patient-admission-diagnosis-tab-btn']")
    TAB_ATTACHMENTS = (By.CSS_SELECTOR, "[data-test-id='patient-admission-attachments-tab-btn']")

    # Surgeries Tab Form Elements
    SELECT_SURGERY_SPECIALTY = (By.CSS_SELECTOR, "[data-test-id='patient-admission-surgery-specialty-select']")
    SELECT_SURGERY_NAME = (By.CSS_SELECTOR, "[data-test-id='patient-admission-surgery-name-select']")
    INPUT_SURGERY_SHORT_CODE = (By.CSS_SELECTOR, "[data-test-id='patient-admission-surgery-short-code-input']")
    INPUT_SURGERY_DEGREE = (By.CSS_SELECTOR, "[data-test-id='patient-admission-surgery-degree-input']")
    SELECT_SURGERY_DOCTOR = (By.CSS_SELECTOR, "[data-test-id='patient-admission-surgery-doctor-select']")
    SELECT_SURGERY_PACKAGE = (By.CSS_SELECTOR, "[data-test-id='patient-admission-surgery-package-select']")
    INPUT_SURGERY_DATETIME = (By.CSS_SELECTOR, "[data-test-id='patient-admission-surgery-datetime-input']")
    BTN_ADD_SURGERY = (By.CSS_SELECTOR, "[data-test-id='patient-admission-add-surgery-btn']")

    # Payments Tab Elements
    ALERT_PAYMENTS_SAVE_FIRST = (By.CSS_SELECTOR, "[data-test-id='patient-admission-payments-save-first-warning-alert']")

    # Reports / Print Menu Button
    BTN_PRINT_MENU = (By.CSS_SELECTOR, "[data-test-id='patient-admission-print-menu-btn']")
    BTN_SAVE_BOTTOM = (By.CSS_SELECTOR, "[data-test-id='patient-admission-save-bottom-btn']")



    def open_for_patient(self, patient_id: int = 30854) -> "PatientAdmissionPage":
        """Navigates directly to the admission screen for a specific patient ID."""
        url = f"https://196.218.246.250:4040/reception/patient/{patient_id}/admission"
        logger.info(f"Navigating to Patient Admission URL: {url}")
        self.driver.get(url)
        self.find(self.BTN_SAVE, timeout=12)
        return self

    def is_admission_loaded(self) -> bool:
        """Checks if the admission page is loaded and save button is visible."""
        return self.is_visible(self.BTN_SAVE, timeout=10)

    def get_admission_form_data(self) -> Dict[str, str]:
        """Reads values from main admission inputs."""
        res_id = ""
        res_date = ""
        resp_name = ""
        resp_phones = ""
        resp_addr = ""

        if self.is_visible(self.INPUT_RESERVATION_ID, timeout=3):
            res_id = self.find(self.INPUT_RESERVATION_ID).get_attribute("value") or ""
        if self.is_visible(self.INPUT_RESERVATION_DATE, timeout=3):
            res_date = self.find(self.INPUT_RESERVATION_DATE).get_attribute("value") or ""
        if self.is_visible(self.INPUT_RESPONSIBLE_NAME, timeout=3):
            resp_name = self.find(self.INPUT_RESPONSIBLE_NAME).get_attribute("value") or ""
        if self.is_visible(self.INPUT_RESPONSIBLE_PHONES, timeout=3):
            resp_phones = self.find(self.INPUT_RESPONSIBLE_PHONES).get_attribute("value") or ""
        if self.is_visible(self.INPUT_RESPONSIBLE_ADDRESS, timeout=3):
            resp_addr = self.find(self.INPUT_RESPONSIBLE_ADDRESS).get_attribute("value") or ""

        return {
            "reservation_id": res_id,
            "reservation_date": res_date,
            "responsible_name": resp_name,
            "responsible_phones": resp_phones,
            "responsible_address": resp_addr
        }

    def switch_tab(self, tab_name: str) -> bool:
        """
        Switches between admission tabs: 'rooms', 'icu', 'neonatal', 'surgeries', 'payments', 'diagnosis', 'attachments'.
        """
        tab_map = {
            "rooms": self.TAB_ROOMS,
            "icu": self.TAB_ICU,
            "neonatal": self.TAB_NEONATAL,
            "surgeries": self.TAB_SURGERIES,
            "payments": self.TAB_PAYMENTS,
            "diagnosis": self.TAB_DIAGNOSIS,
            "attachments": self.TAB_ATTACHMENTS,
        }
        locator = tab_map.get(tab_name.lower())
        if not locator:
            raise ValueError(f"Unknown tab name: {tab_name}")

        logger.info(f"Switching to admission tab: {tab_name}")
        tab_elem = self.find(locator, timeout=5)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tab_elem)
        time.sleep(0.3)
        self.click(locator)
        time.sleep(1)
        return True

    def click_print_menu(self) -> None:
        """Clicks the 'طباعة' / print menu button."""
        logger.info("Clicking print menu button...")
        if self.is_visible(self.BTN_PRINT_MENU, timeout=3):
            btn = self.find(self.BTN_PRINT_MENU)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            self.click(self.BTN_PRINT_MENU)
            time.sleep(1)

    def toggle_same_as_patient_checkbox(self) -> None:
        """Toggles the 'نفس بيانات المريض' checkbox."""
        logger.info("Toggling 'نفس بيانات المريض' checkbox...")
        chk = self.find(self.CHECKBOX_SAME_AS_PATIENT, timeout=5)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", chk)
        self.click(self.CHECKBOX_SAME_AS_PATIENT)
        time.sleep(0.5)


    def click_save(self) -> None:
        """Clicks the 'حفظ' button on admission page."""
        logger.info("Clicking Save Admission button...")
        self.click(self.BTN_SAVE)
        time.sleep(1)

    def click_back(self) -> None:
        """Clicks the 'رجوع' button to return to reception."""
        logger.info("Clicking Back button on Admission page...")
        self.click(self.BTN_BACK)
        time.sleep(1.5)
