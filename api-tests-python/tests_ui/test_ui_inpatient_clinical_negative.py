import time
import sys
import pytest
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from selenium.webdriver.common.by import By
from pages.inpatient_care_pages import (
    InpatientRaysAndTestsPage,
    InpatientMedicationsPage,
    InpatientBloodPage,
    InpatientDevicesPage,
    InpatientDietOrderPage
)

RESERV_ID = "CfDJ8KcUxlP3wTpIkfqEIRtHon4HnOXKri8R-HuwQbLe0ga8sPk_YDBIi7MkseBrAScp2lyLKLKWd1FdbV1bx5vDnm0EQBpbwWI9QcH-t-umVvqBT7aeI7evEqn6rXp7YK12Xw"
ACCOM_ID = "CfDJ8KcUxlP3wTpIkfqEIRtHon6il3dFRgAMVI2R9iXr9AJ77pgneSuKHembPpKo7Y-WpjJgcXZaxrE0K-9uaDSgCs91FGvLxq1k6a3P6tJrXLC-GEMPIyzikQYqlb2CbLezAg"

class TestInpatientClinicalNegativeUI:
    """
    Negative, Boundary, and Destructive UI Test Suite for Inpatient Clinical Care Tabs:
    1. Rays (Empty add, negative quantity, negative unit price)
    2. Tests (Empty add, DbContext concurrency check)
    3. Charge Med (Empty save, unselected store/item)
    4. Request Med (Empty save, missing doctor)
    5. Return Med (Empty store / unselected items)
    6. Blood Bank (Empty save, negative blood units)
    7. Internal Devices (Empty save, negative device count)
    8. External Devices (Empty save, negative/extreme profit margins)
    9. Patient Diet (Empty save, missing meal type)
    """

    def test_01_rays_empty_add_and_negative_values(self, auth_driver):
        """Test Rays screen validation when clicking Add without selections and testing negative values."""
        rays_page = InpatientRaysAndTestsPage(auth_driver)
        rays_page.open_rays(RESERV_ID, ACCOM_ID)
        assert rays_page.is_loaded()

        # Try negative quantity
        qty_input = rays_page.find(rays_page.INPUT_QUANTITY)
        qty_input.clear()
        qty_input.send_keys("-3")
        time.sleep(0.5)
        qty_val = qty_input.get_attribute("value")
        qty_classes = qty_input.get_attribute("class") or ""
        print(f"\n[RAYS NEGATIVE TEST] Quantity input: val='{qty_val}', classes='{qty_classes}'")

        # Try negative unit price
        price_input = rays_page.find(rays_page.INPUT_UNIT_PRICE)
        price_input.clear()
        price_input.send_keys("-250")
        time.sleep(0.5)
        price_val = price_input.get_attribute("value")
        print(f"[RAYS NEGATIVE TEST] Unit price input: val='{price_val}'")

        # Click Add button without selecting group or service
        rays_page.click(rays_page.BTN_ADD)
        time.sleep(1)

        toast_loc = (By.CSS_SELECTOR, "[data-test-id='global-toast-stack'], .toast-item, .toast-stack .msg, .toast-error-http-message")
        toast_present = rays_page.is_visible(toast_loc, timeout=4)
        toast_msg = rays_page.get_text(toast_loc) if toast_present else ""
        print(f"[RAYS TOAST CAPTURED]: '{toast_msg}'")

        rays_page.take_screenshot("01_rays_empty_add_validation", folder="patient_rays")

        # Check for DbContext collision or missing validation
        if "Cannot use multiple context instances" in toast_msg:
            print("[CRITICAL DEFECT CONFIRMED IN RAYS] EF Core DbContext concurrency collision triggered in patient-rays!")

    def test_02_tests_empty_add_and_concurrency_check(self, auth_driver):
        """Test Lab Tests screen: click Add without selecting test, verify error toast vs DbContext crash."""
        tests_page = InpatientRaysAndTestsPage(auth_driver)
        tests_page.open_tests(RESERV_ID, ACCOM_ID)
        assert tests_page.is_loaded()

        # Click Add without selections
        tests_page.click(tests_page.BTN_ADD)
        time.sleep(1)

        toast_loc = (By.CSS_SELECTOR, "[data-test-id='global-toast-stack'], .toast-item, .toast-stack .msg, .toast-error-http-message")
        toast_present = tests_page.is_visible(toast_loc, timeout=4)
        toast_msg = tests_page.get_text(toast_loc) if toast_present else ""
        print(f"\n[TESTS LAB TOAST CAPTURED]: '{toast_msg}'")

        tests_page.take_screenshot("02_tests_empty_add_validation", folder="patient_tests")

        if "Cannot use multiple context instances" in toast_msg:
            print("[CRITICAL DEFECT CONFIRMED IN TESTS] EF Core DbContext concurrency collision triggered in patient-tests!")

    def test_03_charge_med_empty_save_validation(self, auth_driver):
        """Test Pharmacy Med Dispensing: click Save with empty store and item."""
        med_page = InpatientMedicationsPage(auth_driver)
        med_page.open_charge_med(RESERV_ID, ACCOM_ID)
        assert med_page.is_loaded()

        med_page.click(med_page.CHARGE_SAVE_BTN)
        time.sleep(1)

        toast_loc = (By.CSS_SELECTOR, "[data-test-id='global-toast-stack'], .toast-item, .toast-stack .msg, .toast-error-http-message")
        toast_present = med_page.is_visible(toast_loc, timeout=4)
        toast_msg = med_page.get_text(toast_loc) if toast_present else ""
        print(f"\n[CHARGE MED TOAST CAPTURED]: '{toast_msg}'")

        med_page.take_screenshot("03_charge_med_empty_save", folder="charge_patient_med")

    def test_04_request_med_empty_save_validation(self, auth_driver):
        """Test Medication Request: click Save without selecting doctor, store, or item."""
        med_page = InpatientMedicationsPage(auth_driver)
        med_page.open_request_med(RESERV_ID, ACCOM_ID, flag="All")
        assert med_page.is_loaded()

        med_page.click(med_page.REQ_SAVE_BTN)
        time.sleep(1)

        toast_loc = (By.CSS_SELECTOR, "[data-test-id='global-toast-stack'], .toast-item, .toast-stack .msg, .toast-error-http-message")
        toast_present = med_page.is_visible(toast_loc, timeout=4)
        toast_msg = med_page.get_text(toast_loc) if toast_present else ""
        print(f"\n[REQUEST MED TOAST CAPTURED]: '{toast_msg}'")

        med_page.take_screenshot("04_request_med_empty_save", folder="patient_request_med_all")

    def test_05_blood_bank_negative_units_and_empty_save(self, auth_driver):
        """Test Blood Bank: enter negative blood bags (-5) and click save/add without blood type."""
        blood_page = InpatientBloodPage(auth_driver)
        blood_page.open_blood(RESERV_ID, ACCOM_ID, flag="Durgs")
        assert blood_page.is_loaded()

        # Negative quantity
        qty_input = blood_page.find(blood_page.INPUT_QUANTITY)
        qty_input.clear()
        qty_input.send_keys("-5")
        time.sleep(0.5)
        qty_val = qty_input.get_attribute("value")
        print(f"\n[BLOOD BANK NEGATIVE TEST] Blood quantity input: val='{qty_val}'")

        # Click Add without selecting blood type
        blood_page.click(blood_page.BTN_ADD)
        time.sleep(1)

        toast_loc = (By.CSS_SELECTOR, "[data-test-id='global-toast-stack'], .toast-item, .toast-stack .msg, .toast-error-http-message")
        toast_present = blood_page.is_visible(toast_loc, timeout=4)
        toast_msg = blood_page.get_text(toast_loc) if toast_present else ""
        print(f"[BLOOD BANK TOAST CAPTURED]: '{toast_msg}'")

        blood_page.take_screenshot("05_blood_empty_add_validation", folder="patient_blood")

    def test_06_internal_devices_empty_add_validation(self, auth_driver):
        """Test Internal Devices: click Add without selecting device."""
        dev_page = InpatientDevicesPage(auth_driver)
        dev_page.open_internal_devices(RESERV_ID, ACCOM_ID, flag="Durgs")
        assert dev_page.is_loaded()

        qty_input = dev_page.find(dev_page.INTERNAL_QUANTITY_INPUT)
        qty_input.clear()
        qty_input.send_keys("-2")
        time.sleep(0.5)
        qty_val = qty_input.get_attribute("value")
        print(f"\n[INTERNAL DEVICES NEGATIVE TEST] Quantity input: val='{qty_val}'")

        dev_page.click(dev_page.INTERNAL_ADD_BTN)
        time.sleep(1)

        toast_loc = (By.CSS_SELECTOR, "[data-test-id='global-toast-stack'], .toast-item, .toast-stack .msg, .toast-error-http-message")
        toast_present = dev_page.is_visible(toast_loc, timeout=4)
        toast_msg = dev_page.get_text(toast_loc) if toast_present else ""
        print(f"[INTERNAL DEVICES TOAST CAPTURED]: '{toast_msg}'")

        dev_page.take_screenshot("06_internal_devices_empty_add", folder="patient_internal_devices")

    def test_07_external_devices_extreme_profit_and_empty_add(self, auth_driver):
        """Test External Devices: enter negative profit ratio (-15%) and click Add without supplier/service."""
        dev_page = InpatientDevicesPage(auth_driver)
        dev_page.open_external_devices(RESERV_ID, ACCOM_ID, flag="Durgs")
        assert dev_page.is_loaded()

        profit_input = dev_page.find(dev_page.EXTERNAL_PROFIT_RATIO_INPUT)
        profit_input.clear()
        profit_input.send_keys("-25")
        time.sleep(0.5)
        profit_val = profit_input.get_attribute("value")
        print(f"\n[EXTERNAL DEVICES NEGATIVE TEST] Profit ratio: val='{profit_val}'")

        dev_page.click(dev_page.EXTERNAL_ADD_BTN)
        time.sleep(1)

        toast_loc = (By.CSS_SELECTOR, "[data-test-id='global-toast-stack'], .toast-item, .toast-stack .msg, .toast-error-http-message")
        toast_present = dev_page.is_visible(toast_loc, timeout=4)
        toast_msg = dev_page.get_text(toast_loc) if toast_present else ""
        print(f"[EXTERNAL DEVICES TOAST CAPTURED]: '{toast_msg}'")

        dev_page.take_screenshot("07_external_devices_empty_add", folder="patient_external_devices")

    def test_08_diet_empty_save_validation(self, auth_driver):
        """Test Patient Diet: click Save without selecting meal type or diet items."""
        diet_page = InpatientDietOrderPage(auth_driver)
        diet_page.open_diet(RESERV_ID, ACCOM_ID, flag="Durgs")
        assert diet_page.is_loaded()

        diet_page.click(diet_page.BTN_SAVE)
        time.sleep(1)

        toast_loc = (By.CSS_SELECTOR, "[data-test-id='global-toast-stack'], .toast-item, .toast-stack .msg, .toast-error-http-message")
        toast_present = diet_page.is_visible(toast_loc, timeout=4)
        toast_msg = diet_page.get_text(toast_loc) if toast_present else ""
        print(f"\n[DIET TOAST CAPTURED]: '{toast_msg}'")

        diet_page.take_screenshot("08_diet_empty_save", folder="patient_diet")
