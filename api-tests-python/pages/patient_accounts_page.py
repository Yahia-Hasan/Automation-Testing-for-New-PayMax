import time
import logging
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger("BayMaxPatientAccounts")

class UnregisteredInvoicesPage(BasePage):
    """Page Object for Open Statements of Account (/patient-accounts/unregistered-invoices)."""

    URL = "https://196.218.246.250:4040/patient-accounts/unregistered-invoices"

    INPUT_FROM_DATE = (By.CSS_SELECTOR, "[data-test-id='unregistered-invoices-from-date-input']")
    INPUT_TO_DATE = (By.CSS_SELECTOR, "[data-test-id='unregistered-invoices-to-date-input']")
    SELECT_CLIENTS = (By.CSS_SELECTOR, "[data-test-id='unregistered-invoices-clients-select']")
    SELECT_INS_COMPANIES = (By.CSS_SELECTOR, "[data-test-id='unregistered-invoices-ins-companies-select']")
    SELECT_FLOORS = (By.CSS_SELECTOR, "[data-test-id='unregistered-invoices-floors-select']")
    SELECT_ACC_TYPES = (By.CSS_SELECTOR, "[data-test-id='unregistered-invoices-acc-types-select']")
    SELECT_HOSPITAL_SECTION = (By.CSS_SELECTOR, "[data-test-id='unregistered-invoices-hospital-section-select']")
    BTN_SEARCH = (By.CSS_SELECTOR, "[data-test-id='unregistered-invoices-search-btn']")
    BTN_TODAY_ENTRANCE = (By.CSS_SELECTOR, "[data-test-id='unregistered-invoices-today-entrance-btn']")
    BTN_RESIDENTS = (By.CSS_SELECTOR, "[data-test-id='unregistered-invoices-residents-btn']")
    INPUT_SEARCH = (By.CSS_SELECTOR, "[data-test-id='unregistered-invoices-search-input']")
    BTN_EXPORT_EXCEL = (By.CSS_SELECTOR, "[data-test-id='unregistered-invoices-export-excel-btn']")

    def open(self) -> "UnregisteredInvoicesPage":
        logger.info(f"Opening Unregistered Invoices: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.INPUT_FROM_DATE, timeout=12) and self.is_visible(self.BTN_SEARCH)

    def click_search(self) -> None:
        self.click(self.BTN_SEARCH)
        time.sleep(2)

    def filter_today_entrance(self) -> None:
        self.click(self.BTN_TODAY_ENTRANCE)
        time.sleep(1)

    def filter_residents(self) -> None:
        self.click(self.BTN_RESIDENTS)
        time.sleep(1)


class RegisteredInvoicesPage(BasePage):
    """Page Object for Registered Patient Invoices (/patient-accounts/registered-invoices)."""

    URL = "https://196.218.246.250:4040/patient-accounts/registered-invoices"

    INPUT_FROM_DATE = (By.CSS_SELECTOR, "[data-test-id='registered-invoices-from-date-input']")
    INPUT_TO_DATE = (By.CSS_SELECTOR, "[data-test-id='registered-invoices-to-date-input']")
    SELECT_CLIENT = (By.CSS_SELECTOR, "[data-test-id='registered-invoices-client-select']")
    SELECT_INS_COMPANY = (By.CSS_SELECTOR, "[data-test-id='registered-invoices-ins-company-select']")
    SELECT_ACC_TYPES = (By.CSS_SELECTOR, "[data-test-id='registered-invoices-acc-types-select']")
    SELECT_HOSPITAL_SECTION = (By.CSS_SELECTOR, "[data-test-id='registered-invoices-hospital-section-select']")
    BTN_SEARCH = (By.CSS_SELECTOR, "[data-test-id='registered-invoices-search-btn']")
    BTN_TODAY_EXIT = (By.CSS_SELECTOR, "[data-test-id='registered-invoices-today-exit-btn']")
    INPUT_SEARCH = (By.CSS_SELECTOR, "[data-test-id='registered-invoices-search-input']")
    BTN_EXPORT_EXCEL = (By.CSS_SELECTOR, "[data-test-id='registered-invoices-export-excel-btn']")

    def open(self) -> "RegisteredInvoicesPage":
        logger.info(f"Opening Registered Invoices: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.INPUT_FROM_DATE, timeout=12) and self.is_visible(self.BTN_SEARCH)

    def click_search(self) -> None:
        self.click(self.BTN_SEARCH)
        time.sleep(2)

    def filter_today_exit(self) -> None:
        self.click(self.BTN_TODAY_EXIT)
        time.sleep(1)


class PatientCheckupsPage(BasePage):
    """Page Object for Inpatient Accounts (/patient-accounts/patient-checkups)."""

    URL = "https://196.218.246.250:4040/patient-accounts/patient-checkups"

    INPUT_FROM_DATE = (By.CSS_SELECTOR, "[data-test-id='patient-checkups-from-date-input']")
    INPUT_TO_DATE = (By.CSS_SELECTOR, "[data-test-id='patient-checkups-to-date-input']")
    BTN_SEARCH = (By.CSS_SELECTOR, "[data-test-id='patient-checkups-search-btn']")
    INPUT_SEARCH = (By.CSS_SELECTOR, "[data-test-id='patient-checkups-search-input']")
    BTN_EXPORT_EXCEL = (By.CSS_SELECTOR, "[data-test-id='patient-checkups-export-excel-btn']")

    def open(self) -> "PatientCheckupsPage":
        logger.info(f"Opening Patient Checkups / Inpatient Accounts: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.INPUT_FROM_DATE, timeout=12) and self.is_visible(self.BTN_SEARCH)

    def click_search(self) -> None:
        self.click(self.BTN_SEARCH)
        time.sleep(2)


class PatientSettlementsPage(BasePage):
    """Page Object for Patient Debts / Settlements (/patient-accounts/patient-settlements)."""

    URL = "https://196.218.246.250:4040/patient-accounts/patient-settlements"

    INPUT_FROM_DATE = (By.CSS_SELECTOR, "[data-test-id='patient-settlements-from-date-input']")
    INPUT_TO_DATE = (By.CSS_SELECTOR, "[data-test-id='patient-settlements-to-date-input']")
    INPUT_PATIENT_CODE = (By.CSS_SELECTOR, "[data-test-id='patient-settlements-patient-code-input']")
    SELECT_SEARCH_TYPE = (By.CSS_SELECTOR, "[data-test-id='patient-settlements-search-type-select']")
    BTN_SEARCH = (By.CSS_SELECTOR, "[data-test-id='patient-settlements-search-btn']")
    INPUT_SEARCH = (By.CSS_SELECTOR, "[data-test-id='patient-settlements-search-input']")
    BTN_EXPORT_EXCEL = (By.CSS_SELECTOR, "[data-test-id='patient-settlements-export-excel-btn']")

    def open(self) -> "PatientSettlementsPage":
        logger.info(f"Opening Patient Settlements / Debts: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.INPUT_FROM_DATE, timeout=12) and self.is_visible(self.BTN_SEARCH)

    def click_search(self) -> None:
        self.click(self.BTN_SEARCH)
        time.sleep(2)


class TechnicianBankPage(BasePage):
    """Page Object for Technician Bank (/patient-accounts/technician-bank)."""

    URL = "https://196.218.246.250:4040/patient-accounts/technician-bank"

    INPUT_FROM_DATE = (By.CSS_SELECTOR, "[data-test-id='technician-bank-from-date-input']")
    INPUT_TO_DATE = (By.CSS_SELECTOR, "[data-test-id='technician-bank-to-date-input']")
    SELECT_TECHNICIAN = (By.CSS_SELECTOR, "[data-test-id='technician-bank-technician-select']")
    SELECT_SERVICE = (By.CSS_SELECTOR, "[data-test-id='technician-bank-service-select']")
    SELECT_PATIENT = (By.CSS_SELECTOR, "[data-test-id='technician-bank-patient-select']")
    SELECT_PAYMENT_STATUS = (By.CSS_SELECTOR, "[data-test-id='technician-bank-payment-status-select']")
    SELECT_CONTRACT_TYPE = (By.CSS_SELECTOR, "[data-test-id='technician-bank-contract-type-select']")
    SELECT_CLIENT = (By.CSS_SELECTOR, "[data-test-id='technician-bank-client-select']")
    BTN_SEARCH = (By.CSS_SELECTOR, "[data-test-id='technician-bank-search-btn']")
    SELECT_TREASURY = (By.CSS_SELECTOR, "[data-test-id='technician-bank-treasury-select']")
    BTN_SAVE_SETTLEMENT = (By.CSS_SELECTOR, "[data-test-id='technician-bank-save-settlement-btn']")
    INPUT_SEARCH = (By.CSS_SELECTOR, "[data-test-id='technician-bank-search-input']")
    BTN_EXPORT_EXCEL = (By.CSS_SELECTOR, "[data-test-id='technician-bank-export-excel-btn']")
    CHECKBOX_SELECT_ALL = (By.CSS_SELECTOR, "[data-test-id='technician-bank-select-all-checkbox']")

    def open(self) -> "TechnicianBankPage":
        logger.info(f"Opening Technician Bank: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.INPUT_FROM_DATE, timeout=12) and self.is_visible(self.BTN_SEARCH)

    def click_search(self) -> None:
        self.click(self.BTN_SEARCH)
        time.sleep(2)


class MergePatientsPage(BasePage):
    """Page Object for Merge Patients (/patient-accounts/merge-patients)."""

    URL = "https://196.218.246.250:4040/patient-accounts/merge-patients"

    INPUT_CODE_FROM = (By.CSS_SELECTOR, "[data-test-id='merge-patients-code-from-input']")
    INPUT_CODE_TO = (By.CSS_SELECTOR, "[data-test-id='merge-patients-code-to-input']")
    BTN_MERGE = (By.CSS_SELECTOR, "[data-test-id='merge-patients-merge-btn']")

    def open(self) -> "MergePatientsPage":
        logger.info(f"Opening Merge Patients: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.INPUT_CODE_FROM, timeout=12) and self.is_visible(self.BTN_MERGE)

    def fill_codes(self, source_code: str, target_code: str) -> None:
        self.type_text(self.INPUT_CODE_FROM, source_code)
        self.type_text(self.INPUT_CODE_TO, target_code)
