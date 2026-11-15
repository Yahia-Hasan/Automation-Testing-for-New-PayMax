import time
import logging
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger("BayMaxClinicsModule")

class ClinicWaitingListPage(BasePage):
    """Page Object for Clinic Waiting List (/clinic/waiting-list)."""

    URL = "https://196.218.246.250:4040/clinic/waiting-list"

    INPUT_DATE = (By.CSS_SELECTOR, "[data-test-id='clinic-waiting-list-date-input']")
    SELECT_DOCTOR = (By.CSS_SELECTOR, "[data-test-id='clinic-waiting-list-doctor-select']")
    SELECT_PAYMENT_STATUS = (By.CSS_SELECTOR, "[data-test-id='clinic-waiting-list-payment-status-select']")
    SELECT_DONE_STATUS = (By.CSS_SELECTOR, "[data-test-id='clinic-waiting-list-done-status-select']")
    BTN_SEARCH = (By.CSS_SELECTOR, "[data-test-id='clinic-waiting-list-search-btn']")

    def open(self) -> "ClinicWaitingListPage":
        logger.info(f"Opening Clinic Waiting List: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.INPUT_DATE, timeout=12) and self.is_visible(self.BTN_SEARCH)

    def click_search(self) -> None:
        self.click(self.BTN_SEARCH)
        time.sleep(2)


class ClinicVisitDetailsReportPage(BasePage):
    """Page Object for Detailed Clinic Report (/clinic/visit-details-report)."""

    URL = "https://196.218.246.250:4040/clinic/visit-details-report"

    INPUT_FROM_DATE = (By.CSS_SELECTOR, "[data-test-id='visit-details-report-from-date-input']")
    INPUT_TO_DATE = (By.CSS_SELECTOR, "[data-test-id='visit-details-report-to-date-input']")
    SELECT_CLIENT = (By.CSS_SELECTOR, "[data-test-id='visit-details-report-client-select']")
    BTN_SEARCH = (By.CSS_SELECTOR, "[data-test-id='visit-details-report-search-btn']")

    def open(self) -> "ClinicVisitDetailsReportPage":
        logger.info(f"Opening Detailed Clinic Report: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.INPUT_FROM_DATE, timeout=12) and self.is_visible(self.BTN_SEARCH)

    def click_search(self) -> None:
        self.click(self.BTN_SEARCH)
        time.sleep(2)


class ClinicPatientsPage(BasePage):
    """Page Object for Patients in Clinics (/clinic/patients)."""

    URL = "https://196.218.246.250:4040/clinic/patients"

    INPUT_FROM_DATE = (By.CSS_SELECTOR, "[data-test-id='patients-in-clinics-from-date-input']")
    INPUT_TO_DATE = (By.CSS_SELECTOR, "[data-test-id='patients-in-clinics-to-date-input']")
    SELECT_CLIENT = (By.CSS_SELECTOR, "[data-test-id='patients-in-clinics-client-select']")
    BTN_SEARCH = (By.CSS_SELECTOR, "[data-test-id='patients-in-clinics-search-btn']")
    INPUT_SEARCH = (By.CSS_SELECTOR, "[data-test-id='patients-in-clinics-search-input']")
    BTN_EXPORT = (By.CSS_SELECTOR, "[data-test-id='patients-in-clinics-export-btn']")

    def open(self) -> "ClinicPatientsPage":
        logger.info(f"Opening Patients in Clinics: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.INPUT_FROM_DATE, timeout=12) and self.is_visible(self.BTN_SEARCH)

    def click_search(self) -> None:
        self.click(self.BTN_SEARCH)
        time.sleep(2)


class ClinicEditVisitPage(BasePage):
    """Page Object for Edit Clinic Visit (/clinic/edit-visit)."""

    URL = "https://196.218.246.250:4040/clinic/edit-visit"

    INPUT_FROM_DATE = (By.CSS_SELECTOR, "[data-test-id='edit-visit-from-date-input']")
    INPUT_TO_DATE = (By.CSS_SELECTOR, "[data-test-id='edit-visit-to-date-input']")
    BTN_SEARCH = (By.CSS_SELECTOR, "[data-test-id='edit-visit-search-btn']")

    def open(self) -> "ClinicEditVisitPage":
        logger.info(f"Opening Edit Clinic Visit: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.INPUT_FROM_DATE, timeout=12) and self.is_visible(self.BTN_SEARCH)

    def click_search(self) -> None:
        self.click(self.BTN_SEARCH)
        time.sleep(2)


class ClinicCancelLeavedVisitPage(BasePage):
    """Page Object for Cancel Leaved Clinic Visit (/clinic/cancel-leaved-visit)."""

    URL = "https://196.218.246.250:4040/clinic/cancel-leaved-visit"

    INPUT_FROM_DATE = (By.CSS_SELECTOR, "[data-test-id='cancel-leaved-visit-from-date-input']")
    INPUT_TO_DATE = (By.CSS_SELECTOR, "[data-test-id='cancel-leaved-visit-to-date-input']")
    BTN_SEARCH = (By.CSS_SELECTOR, "[data-test-id='cancel-leaved-visit-search-btn']")

    def open(self) -> "ClinicCancelLeavedVisitPage":
        logger.info(f"Opening Cancel Leaved Clinic Visit: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.INPUT_FROM_DATE, timeout=12) and self.is_visible(self.BTN_SEARCH)

    def click_search(self) -> None:
        self.click(self.BTN_SEARCH)
        time.sleep(2)


class ClinicMedicalReportsPage(BasePage):
    """Page Object for Outpatient Clinics Medical Reports (/clinic/medical-reports)."""

    URL = "https://196.218.246.250:4040/clinic/medical-reports"

    INPUT_FROM_DATE = (By.CSS_SELECTOR, "[data-test-id='visit-medical-reports-from-date-input']")
    INPUT_TO_DATE = (By.CSS_SELECTOR, "[data-test-id='visit-medical-reports-to-date-input']")
    SELECT_INVOICE_STATUS = (By.CSS_SELECTOR, "[data-test-id='visit-medical-reports-invoice-status-select']")
    SELECT_CLIENT = (By.CSS_SELECTOR, "[data-test-id='visit-medical-reports-client-select']")
    SELECT_INS_COMPANY = (By.CSS_SELECTOR, "[data-test-id='visit-medical-reports-ins-company-select']")
    BTN_SHOW = (By.CSS_SELECTOR, "[data-test-id='visit-medical-reports-show-btn']")
    INPUT_SEARCH = (By.CSS_SELECTOR, "[data-test-id='visit-medical-reports-search-input']")

    def open(self) -> "ClinicMedicalReportsPage":
        logger.info(f"Opening Clinic Medical Reports: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.INPUT_FROM_DATE, timeout=12) and self.is_visible(self.BTN_SHOW)

    def click_show(self) -> None:
        self.click(self.BTN_SHOW)
        time.sleep(2)
