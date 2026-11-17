import time
import logging
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger("BayMaxNursingModule")

class NursingRoomsPage(BasePage):
    """Page Object for Nursing Inpatients in Rooms (/waiting-list/accomodation-rooms)."""

    URL = "https://196.218.246.250:4040/waiting-list/accomodation-rooms"

    BTN_RELOAD = (By.CSS_SELECTOR, "[data-test-id='nursing-secretary-reload-btn']")
    INPUT_SEARCH = (By.CSS_SELECTOR, "[data-test-id='nursing-secretary-search-input']")

    def open(self) -> "NursingRoomsPage":
        logger.info(f"Opening Nursing Inpatients in Rooms: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.BTN_RELOAD, timeout=12)

    def reload(self) -> None:
        self.click(self.BTN_RELOAD)
        time.sleep(1)


class NursingICUPage(BasePage):
    """Page Object for Nursing ICU Patients (/waiting-list/icu)."""

    URL = "https://196.218.246.250:4040/waiting-list/icu"

    BTN_RELOAD = (By.CSS_SELECTOR, "[data-test-id='nursing-secretary-reload-btn']")
    INPUT_SEARCH = (By.CSS_SELECTOR, "[data-test-id='nursing-secretary-search-input']")

    def open(self) -> "NursingICUPage":
        logger.info(f"Opening Nursing ICU Patients: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.BTN_RELOAD, timeout=12)

    def reload(self) -> None:
        self.click(self.BTN_RELOAD)
        time.sleep(1)


class NursingNeonatalPage(BasePage):
    """Page Object for Nursing Neonatal Patients (/waiting-list/neonatal)."""

    URL = "https://196.218.246.250:4040/waiting-list/neonatal"

    BTN_RELOAD = (By.CSS_SELECTOR, "[data-test-id='nursing-secretary-reload-btn']")
    INPUT_SEARCH = (By.CSS_SELECTOR, "[data-test-id='nursing-secretary-search-input']")

    def open(self) -> "NursingNeonatalPage":
        logger.info(f"Opening Nursing Neonatal Patients: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.BTN_RELOAD, timeout=12)

    def reload(self) -> None:
        self.click(self.BTN_RELOAD)
        time.sleep(1)


class PatientDietsListPage(BasePage):
    """Page Object for Patient Diets List (/waiting-list/patient-diets-list)."""

    URL = "https://196.218.246.250:4040/waiting-list/patient-diets-list"

    SELECT_DIET = (By.CSS_SELECTOR, "[data-test-id='patient-diets-list-diet-select']")
    BTN_SHOW = (By.CSS_SELECTOR, "[data-test-id='patient-diets-list-show-btn']")
    INPUT_SEARCH = (By.CSS_SELECTOR, "[data-test-id='patient-diets-list-search-input']")

    def open(self) -> "PatientDietsListPage":
        logger.info(f"Opening Patient Diets List: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.BTN_SHOW, timeout=12)

    def click_show(self) -> None:
        self.click(self.BTN_SHOW)
        time.sleep(2)


class AttendantDietsListPage(BasePage):
    """Page Object for Attendant Diets List (/waiting-list/attendant-diets)."""

    URL = "https://196.218.246.250:4040/waiting-list/attendant-diets"

    BTN_REFRESH = (By.CSS_SELECTOR, "[data-test-id='attendant-diets-refresh-btn']")
    INPUT_SEARCH = (By.CSS_SELECTOR, "[data-test-id='attendant-diets-search-input']")

    def open(self) -> "AttendantDietsListPage":
        logger.info(f"Opening Attendant Diets List: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.BTN_REFRESH, timeout=12)

    def refresh(self) -> None:
        self.click(self.BTN_REFRESH)
        time.sleep(1)


class InpatientMedicalReportsPage(BasePage):
    """Page Object for Inpatient Medical Reports (/waiting-list/medical-reports)."""

    URL = "https://196.218.246.250:4040/waiting-list/medical-reports"

    INPUT_FROM_DATE = (By.CSS_SELECTOR, "[data-test-id='medical-reports-from-date-input']")
    INPUT_TO_DATE = (By.CSS_SELECTOR, "[data-test-id='medical-reports-to-date-input']")
    SELECT_CLIENT = (By.CSS_SELECTOR, "[data-test-id='medical-reports-client-select']")
    SELECT_INSURANCE_COMPANY = (By.CSS_SELECTOR, "[data-test-id='medical-reports-insurance-company-select']")
    SELECT_INVOICE_STATUS = (By.CSS_SELECTOR, "[data-test-id='medical-reports-invoice-status-select']")
    BTN_SHOW = (By.CSS_SELECTOR, "[data-test-id='medical-reports-show-btn']")
    INPUT_SEARCH = (By.CSS_SELECTOR, "[data-test-id='medical-reports-search-input']")

    def open(self) -> "InpatientMedicalReportsPage":
        logger.info(f"Opening Inpatient Medical Reports: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.INPUT_FROM_DATE, timeout=12) and self.is_visible(self.BTN_SHOW)

    def click_show(self) -> None:
        self.click(self.BTN_SHOW)
        time.sleep(2)
