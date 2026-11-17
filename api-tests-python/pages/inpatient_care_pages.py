import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class InpatientCareBasePage(BasePage):
    """Base class for Inpatient Clinical Care sub-screens under /waiting-list/"""
    
    BASE_URL = "https://196.218.246.250:4040"
    GLOBAL_TOAST = (By.CSS_SELECTOR, "[data-test-id='global-toast-stack'], .toast-item, .toast-stack .msg")
    HTTP_ERROR_TOAST = (By.CSS_SELECTOR, "[data-test-id='toast-error-http'], .toast-error-http-message")
    DATA_TABLES = (By.CSS_SELECTOR, "table, .table, .data-table, .svc-table")

    def __init__(self, driver):
        super().__init__(driver)

    def is_loaded(self, timeout=10):
        """Verify the page has finished loading by checking body and absence of loading overlay."""
        return self.is_visible((By.CSS_SELECTOR, "body"), timeout=timeout)

    def get_tables_count(self):
        return len(self.driver.find_elements(*self.DATA_TABLES))


class InpatientRaysAndTestsPage(InpatientCareBasePage):
    """
    Page Object for Inpatient Rays (/waiting-list/patient-rays) 
    and Inpatient Tests (/waiting-list/patient-tests).
    Both screens share the exact same 'patient-ipd-typed-*' DOM components.
    """
    SELECT_GROUP = (By.CSS_SELECTOR, "[data-test-id='patient-ipd-typed-group-select']")
    SELECT_SERVICE = (By.CSS_SELECTOR, "[data-test-id='patient-ipd-typed-service-select']")
    INPUT_QUANTITY = (By.CSS_SELECTOR, "[data-test-id='patient-ipd-typed-quantity-input']")
    INPUT_UNIT_PRICE = (By.CSS_SELECTOR, "[data-test-id='patient-ipd-typed-unit-price-input']")
    INPUT_SHORT_CODE = (By.CSS_SELECTOR, "[data-test-id='patient-ipd-typed-short-code-input']")
    INPUT_CLIENT_APPROVAL = (By.CSS_SELECTOR, "[data-test-id='patient-ipd-typed-client-approval-number-input']")
    TEXTAREA_NOTES = (By.CSS_SELECTOR, "[data-test-id='patient-ipd-typed-notes-textarea']")
    
    BTN_NEW = (By.CSS_SELECTOR, "[data-test-id='patient-ipd-typed-new-btn']")
    BTN_ADD = (By.CSS_SELECTOR, "[data-test-id='patient-ipd-typed-add-btn']")
    BTN_FAVORITES = (By.CSS_SELECTOR, "[data-test-id='patient-ipd-typed-favorites-btn']")
    BTN_CLAIM = (By.CSS_SELECTOR, "[data-test-id='patient-ipd-typed-claim-btn']")
    BTN_SAVE = (By.CSS_SELECTOR, "[data-test-id='patient-ipd-typed-save-btn']")

    def open_rays(self, reserv_id, accom_id, typ=1):
        url = f"{self.BASE_URL}/waiting-list/patient-rays?ReservID={reserv_id}&AccomID={accom_id}&typ={typ}"
        self.driver.get(url)
        time.sleep(2)
        return self

    def open_tests(self, reserv_id, accom_id, typ=1):
        url = f"{self.BASE_URL}/waiting-list/patient-tests?ReservID={reserv_id}&AccomID={accom_id}&typ={typ}"
        self.driver.get(url)
        time.sleep(2)
        return self

    def enter_notes(self, text):
        if self.is_visible(self.TEXTAREA_NOTES, timeout=3):
            self.type_text(self.TEXTAREA_NOTES, text)

    def click_new(self):
        if self.is_visible(self.BTN_NEW, timeout=3):
            self.click(self.BTN_NEW)


class InpatientMedicationsPage(InpatientCareBasePage):
    """
    Page Object for Inpatient Pharmacy screens:
    1. /waiting-list/charge-patient-med (Dispensing)
    2. /waiting-list/patient-request-med (Requesting Drugs & Supplies)
    3. /waiting-list/patient-return-med (Returning Dispensed Meds)
    """
    # Charge / Dispense
    CHARGE_STORE_SELECT = (By.CSS_SELECTOR, "[data-test-id='charge-patient-med-store-select']")
    CHARGE_ITEM_SELECT = (By.CSS_SELECTOR, "[data-test-id='charge-patient-med-item-select']")
    CHARGE_NOTES_INPUT = (By.CSS_SELECTOR, "[data-test-id='charge-patient-med-notes-input']")
    CHARGE_NEW_BTN = (By.CSS_SELECTOR, "[data-test-id='charge-patient-med-new-btn']")
    CHARGE_SAVE_BTN = (By.CSS_SELECTOR, "[data-test-id='charge-patient-med-save-btn']")

    # Request Med
    REQ_STORE_SELECT = (By.CSS_SELECTOR, "[data-test-id='patient-request-med-store-select']")
    REQ_DOCTOR_SELECT = (By.CSS_SELECTOR, "[data-test-id='patient-request-med-doctor-select']")
    REQ_ITEM_SELECT = (By.CSS_SELECTOR, "[data-test-id='patient-request-med-item-select']")
    REQ_NOTES_INPUT = (By.CSS_SELECTOR, "[data-test-id='patient-request-med-notes-input']")
    REQ_NEW_BTN = (By.CSS_SELECTOR, "[data-test-id='patient-request-med-new-btn']")
    REQ_SAVE_BTN = (By.CSS_SELECTOR, "[data-test-id='patient-request-med-save-btn']")

    # Return Med
    RETURN_STORE_SELECT = (By.CSS_SELECTOR, "[data-test-id='patient-return-med-store-select']")

    def open_charge_med(self, reserv_id, accom_id, typ=1):
        url = f"{self.BASE_URL}/waiting-list/charge-patient-med?ReservID={reserv_id}&AccomID={accom_id}&typ={typ}"
        self.driver.get(url)
        time.sleep(1.5)
        return self

    def open_request_med(self, reserv_id, accom_id, typ=1, flag="All"):
        url = f"{self.BASE_URL}/waiting-list/patient-request-med?ReservID={reserv_id}&AccomID={accom_id}&typ={typ}&flag={flag}"
        self.driver.get(url)
        time.sleep(1.5)
        return self

    def open_return_med(self, reserv_id, accom_id, typ=1, flag="Durgs"):
        url = f"{self.BASE_URL}/waiting-list/patient-return-med?ReservID={reserv_id}&AccomID={accom_id}&typ={typ}&flag={flag}"
        self.driver.get(url)
        time.sleep(1.5)
        return self


class InpatientBloodPage(InpatientCareBasePage):
    """
    Page Object for Inpatient Blood Bank Screen (/waiting-list/patient-blood)
    """
    SELECT_BLOOD_TYPE = (By.CSS_SELECTOR, "[data-test-id='patient-blood-blood-type-select']")
    INPUT_QUANTITY = (By.CSS_SELECTOR, "[data-test-id='patient-blood-quantity-input']")
    INPUT_UNIT_PRICE = (By.CSS_SELECTOR, "[data-test-id='patient-blood-unit-price-input']")
    TEXTAREA_NOTES = (By.CSS_SELECTOR, "[data-test-id='patient-blood-notes-textarea']")
    
    BTN_NEW = (By.CSS_SELECTOR, "[data-test-id='patient-blood-new-btn']")
    BTN_ADD = (By.CSS_SELECTOR, "[data-test-id='patient-blood-add-btn']")
    BTN_CLAIM = (By.CSS_SELECTOR, "[data-test-id='patient-blood-claim-btn']")
    BTN_SAVE = (By.CSS_SELECTOR, "[data-test-id='patient-blood-save-btn']")

    def open_blood(self, reserv_id, accom_id, typ=1, flag="Durgs"):
        url = f"{self.BASE_URL}/waiting-list/patient-blood?ReservID={reserv_id}&AccomID={accom_id}&typ={typ}&flag={flag}"
        self.driver.get(url)
        time.sleep(1.5)
        return self


class InpatientDevicesPage(InpatientCareBasePage):
    """
    Page Object for Internal & External Medical Devices screens:
    1. /waiting-list/patient-internal-devices
    2. /waiting-list/patient-external-devices
    """
    # Internal Devices
    INTERNAL_DEVICE_SELECT = (By.CSS_SELECTOR, "[data-test-id='patient-internal-devices-device-select']")
    INTERNAL_QUANTITY_INPUT = (By.CSS_SELECTOR, "[data-test-id='patient-internal-devices-quantity-input']")
    INTERNAL_NOTES_TEXTAREA = (By.CSS_SELECTOR, "[data-test-id='patient-internal-devices-notes-textarea']")
    INTERNAL_NEW_BTN = (By.CSS_SELECTOR, "[data-test-id='patient-internal-devices-new-btn']")
    INTERNAL_ADD_BTN = (By.CSS_SELECTOR, "[data-test-id='patient-internal-devices-add-btn']")
    INTERNAL_CLAIM_BTN = (By.CSS_SELECTOR, "[data-test-id='patient-internal-devices-claim-btn']")
    INTERNAL_SAVE_BTN = (By.CSS_SELECTOR, "[data-test-id='patient-internal-devices-save-btn']")

    # External Devices
    EXTERNAL_DOCTOR_SELECT = (By.CSS_SELECTOR, "[data-test-id='patient-external-devices-doctor-select']")
    EXTERNAL_SUPPLIER_SELECT = (By.CSS_SELECTOR, "[data-test-id='patient-external-devices-supplier-select']")
    EXTERNAL_SERVICE_SELECT = (By.CSS_SELECTOR, "[data-test-id='patient-external-devices-service-select']")
    EXTERNAL_QUANTITY_INPUT = (By.CSS_SELECTOR, "[data-test-id='patient-external-devices-quantity-input']")
    EXTERNAL_UNIT_PRICE_INPUT = (By.CSS_SELECTOR, "[data-test-id='patient-external-devices-unit-price-input']")
    EXTERNAL_PROFIT_RATIO_INPUT = (By.CSS_SELECTOR, "[data-test-id='patient-external-devices-profit-ratio-input']")
    EXTERNAL_PROFIT_VALUE_INPUT = (By.CSS_SELECTOR, "[data-test-id='patient-external-devices-profit-value-input']")
    EXTERNAL_NOTES_TEXTAREA = (By.CSS_SELECTOR, "[data-test-id='patient-external-devices-notes-textarea']")
    EXTERNAL_NEW_BTN = (By.CSS_SELECTOR, "[data-test-id='patient-external-devices-new-btn']")
    EXTERNAL_ADD_BTN = (By.CSS_SELECTOR, "[data-test-id='patient-external-devices-add-btn']")
    EXTERNAL_CLAIM_BTN = (By.CSS_SELECTOR, "[data-test-id='patient-external-devices-claim-btn']")
    EXTERNAL_SAVE_BTN = (By.CSS_SELECTOR, "[data-test-id='patient-external-devices-save-btn']")

    def open_internal_devices(self, reserv_id, accom_id, typ=1, flag="Durgs"):
        url = f"{self.BASE_URL}/waiting-list/patient-internal-devices?ReservID={reserv_id}&AccomID={accom_id}&typ={typ}&flag={flag}"
        self.driver.get(url)
        time.sleep(1.5)
        return self

    def open_external_devices(self, reserv_id, accom_id, typ=1, flag="Durgs"):
        url = f"{self.BASE_URL}/waiting-list/patient-external-devices?ReservID={reserv_id}&AccomID={accom_id}&typ={typ}&flag={flag}"
        self.driver.get(url)
        time.sleep(1.5)
        return self


class InpatientDietOrderPage(InpatientCareBasePage):
    """
    Page Object for Inpatient Diet Order Screen (/waiting-list/patient-diet)
    """
    SELECT_MEAL_TYPE = (By.CSS_SELECTOR, "[data-test-id='patient-diet-meal-type-select']")
    SELECT_DIET_ITEMS = (By.CSS_SELECTOR, "[data-test-id='patient-diet-diet-items-select']")
    INPUT_NOTES = (By.CSS_SELECTOR, "[data-test-id='patient-diet-notes-input']")
    BTN_SAVE = (By.CSS_SELECTOR, "[data-test-id='patient-diet-save-btn']")

    def open_diet(self, reserv_id, accom_id, typ=1, flag="Durgs"):
        url = f"{self.BASE_URL}/waiting-list/patient-diet?ReservID={reserv_id}&AccomID={accom_id}&typ={typ}&flag={flag}"
        self.driver.get(url)
        time.sleep(1.5)
        return self
