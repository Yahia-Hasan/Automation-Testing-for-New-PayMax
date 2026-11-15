import time
import pytest
from pages.inpatient_care_pages import (
    InpatientRaysAndTestsPage,
    InpatientMedicationsPage,
    InpatientBloodPage,
    InpatientDevicesPage,
    InpatientDietOrderPage
)

RESERV_ID = "CfDJ8KcUxlP3wTpIkfqEIRtHon4HnOXKri8R-HuwQbLe0ga8sPk_YDBIi7MkseBrAScp2lyLKLKWd1FdbV1bx5vDnm0EQBpbwWI9QcH-t-umVvqBT7aeI7evEqn6rXp7YK12Xw"
ACCOM_ID = "CfDJ8KcUxlP3wTpIkfqEIRtHon6il3dFRgAMVI2R9iXr9AJ77pgneSuKHembPpKo7Y-WpjJgcXZaxrE0K-9uaDSgCs91FGvLxq1k6a3P6tJrXLC-GEMPIyzikQYqlb2CbLezAg"

class TestInpatientClinicalCareUI:
    """
    Automated UI Test Suite for the 10 Inpatient Clinical Care Screens:
    1. Patient Rays (/waiting-list/patient-rays)
    2. Patient Tests (/waiting-list/patient-tests)
    3. Charge Patient Med (/waiting-list/charge-patient-med)
    4. Patient Request Med (flag=All)
    5. Patient Request Med (flag=Durgs)
    6. Patient Return Med (flag=Durgs)
    7. Patient Blood Bank (flag=Durgs)
    8. Patient Internal Devices (flag=Durgs)
    9. Patient External Devices (flag=Durgs)
    10. Patient Diet Order (flag=Durgs)
    """

    def test_01_patient_rays(self, auth_driver):
        """Test Inpatient Rays screen elements, inputs, and order tables."""
        rays_page = InpatientRaysAndTestsPage(auth_driver)
        rays_page.open_rays(RESERV_ID, ACCOM_ID)
        assert rays_page.is_loaded()

        assert rays_page.is_visible(rays_page.SELECT_GROUP, timeout=5)
        assert rays_page.is_visible(rays_page.SELECT_SERVICE, timeout=5)
        assert rays_page.is_visible(rays_page.INPUT_QUANTITY, timeout=5)
        assert rays_page.is_visible(rays_page.BTN_SAVE, timeout=5)

        rays_page.enter_notes("طلب أشعة رعاية مركزة - فحص آلي")
        rays_page.take_screenshot("01_patient_rays_loaded", folder="patient_rays")
        assert rays_page.get_tables_count() >= 1

    def test_02_patient_tests(self, auth_driver):
        """Test Inpatient Tests & Lab services screen elements and tables."""
        tests_page = InpatientRaysAndTestsPage(auth_driver)
        tests_page.open_tests(RESERV_ID, ACCOM_ID)
        assert tests_page.is_loaded()

        assert tests_page.is_visible(tests_page.SELECT_GROUP, timeout=5)
        assert tests_page.is_visible(tests_page.SELECT_SERVICE, timeout=5)
        assert tests_page.is_visible(tests_page.BTN_NEW, timeout=5)
        assert tests_page.is_visible(tests_page.BTN_SAVE, timeout=5)

        tests_page.enter_notes("طلب تحاليل دم دورية - فحص آلي")
        tests_page.take_screenshot("02_patient_tests_loaded", folder="patient_tests")
        assert tests_page.get_tables_count() >= 1

    def test_03_charge_patient_med(self, auth_driver):
        """Test Inpatient Pharmacy medication dispensing (charge) screen."""
        med_page = InpatientMedicationsPage(auth_driver)
        med_page.open_charge_med(RESERV_ID, ACCOM_ID)
        assert med_page.is_loaded()

        assert med_page.is_visible(med_page.CHARGE_STORE_SELECT, timeout=5)
        assert med_page.is_visible(med_page.CHARGE_ITEM_SELECT, timeout=5)
        assert med_page.is_visible(med_page.CHARGE_SAVE_BTN, timeout=5)

        if med_page.is_visible(med_page.CHARGE_NOTES_INPUT, timeout=3):
            med_page.type_text(med_page.CHARGE_NOTES_INPUT, "صرف أدوية للمريض - فحص آلي")

        med_page.take_screenshot("03_charge_patient_med_loaded", folder="charge_patient_med")
        assert med_page.get_tables_count() >= 1

    def test_04_patient_request_med_all(self, auth_driver):
        """Test Inpatient Medication & Supply request screen (flag=All)."""
        med_page = InpatientMedicationsPage(auth_driver)
        med_page.open_request_med(RESERV_ID, ACCOM_ID, flag="All")
        assert med_page.is_loaded()

        assert med_page.is_visible(med_page.REQ_STORE_SELECT, timeout=5)
        assert med_page.is_visible(med_page.REQ_DOCTOR_SELECT, timeout=5)
        assert med_page.is_visible(med_page.REQ_ITEM_SELECT, timeout=5)
        assert med_page.is_visible(med_page.REQ_SAVE_BTN, timeout=5)

        if med_page.is_visible(med_page.REQ_NOTES_INPUT, timeout=3):
            med_page.type_text(med_page.REQ_NOTES_INPUT, "طلب أدوية ومستلزمات عامة - فحص آلي")

        med_page.take_screenshot("04_request_med_all_loaded", folder="patient_request_med_all")
        assert med_page.get_tables_count() >= 1

    def test_05_patient_request_med_drugs(self, auth_driver):
        """Test Inpatient Medication request screen filtered for drugs only (flag=Durgs)."""
        med_page = InpatientMedicationsPage(auth_driver)
        med_page.open_request_med(RESERV_ID, ACCOM_ID, flag="Durgs")
        assert med_page.is_loaded()

        assert med_page.is_visible(med_page.REQ_STORE_SELECT, timeout=5)
        assert med_page.is_visible(med_page.REQ_DOCTOR_SELECT, timeout=5)
        assert med_page.is_visible(med_page.REQ_ITEM_SELECT, timeout=5)
        assert med_page.is_visible(med_page.REQ_SAVE_BTN, timeout=5)

        med_page.take_screenshot("05_request_med_drugs_loaded", folder="patient_request_med_drugs")
        assert med_page.get_tables_count() >= 1

    def test_06_patient_return_med_drugs(self, auth_driver):
        """Test Inpatient Medication return screen (flag=Durgs)."""
        med_page = InpatientMedicationsPage(auth_driver)
        med_page.open_return_med(RESERV_ID, ACCOM_ID, flag="Durgs")
        assert med_page.is_loaded()

        assert med_page.is_visible(med_page.RETURN_STORE_SELECT, timeout=5)
        med_page.take_screenshot("06_return_med_drugs_loaded", folder="patient_return_med")
        assert med_page.get_tables_count() >= 1

    def test_07_patient_blood(self, auth_driver):
        """Test Inpatient Blood Bank screen elements and tables."""
        blood_page = InpatientBloodPage(auth_driver)
        blood_page.open_blood(RESERV_ID, ACCOM_ID, flag="Durgs")
        assert blood_page.is_loaded()

        assert blood_page.is_visible(blood_page.SELECT_BLOOD_TYPE, timeout=5)
        assert blood_page.is_visible(blood_page.INPUT_QUANTITY, timeout=5)
        assert blood_page.is_visible(blood_page.BTN_SAVE, timeout=5)

        if blood_page.is_visible(blood_page.TEXTAREA_NOTES, timeout=3):
            blood_page.type_text(blood_page.TEXTAREA_NOTES, "طلب كيس دم فصيلة A+ للمريض")

        blood_page.take_screenshot("07_patient_blood_loaded", folder="patient_blood")
        assert blood_page.get_tables_count() >= 1

    def test_08_patient_internal_devices(self, auth_driver):
        """Test Inpatient Internal Medical Devices screen elements and tables."""
        devices_page = InpatientDevicesPage(auth_driver)
        devices_page.open_internal_devices(RESERV_ID, ACCOM_ID, flag="Durgs")
        assert devices_page.is_loaded()

        assert devices_page.is_visible(devices_page.INTERNAL_DEVICE_SELECT, timeout=5)
        assert devices_page.is_visible(devices_page.INTERNAL_QUANTITY_INPUT, timeout=5)
        assert devices_page.is_visible(devices_page.INTERNAL_SAVE_BTN, timeout=5)

        if devices_page.is_visible(devices_page.INTERNAL_NOTES_TEXTAREA, timeout=3):
            devices_page.type_text(devices_page.INTERNAL_NOTES_TEXTAREA, "تركيب جهاز داخلي للمريض")

        devices_page.take_screenshot("08_internal_devices_loaded", folder="patient_internal_devices")
        assert devices_page.get_tables_count() >= 1

    def test_09_patient_external_devices(self, auth_driver):
        """Test Inpatient External Medical Devices screen elements and pricing fields."""
        devices_page = InpatientDevicesPage(auth_driver)
        devices_page.open_external_devices(RESERV_ID, ACCOM_ID, flag="Durgs")
        assert devices_page.is_loaded()

        assert devices_page.is_visible(devices_page.EXTERNAL_DOCTOR_SELECT, timeout=5)
        assert devices_page.is_visible(devices_page.EXTERNAL_SUPPLIER_SELECT, timeout=5)
        assert devices_page.is_visible(devices_page.EXTERNAL_PROFIT_RATIO_INPUT, timeout=5)
        assert devices_page.is_visible(devices_page.EXTERNAL_SAVE_BTN, timeout=5)

        if devices_page.is_visible(devices_page.EXTERNAL_NOTES_TEXTAREA, timeout=3):
            devices_page.type_text(devices_page.EXTERNAL_NOTES_TEXTAREA, "توريد جهاز خارجي - فحص آلي")

        devices_page.take_screenshot("09_external_devices_loaded", folder="patient_external_devices")
        assert devices_page.get_tables_count() >= 1

    def test_10_patient_diet(self, auth_driver):
        """Test Inpatient Diet Order screen elements and meal configuration."""
        diet_page = InpatientDietOrderPage(auth_driver)
        diet_page.open_diet(RESERV_ID, ACCOM_ID, flag="Durgs")
        assert diet_page.is_loaded()

        assert diet_page.is_visible(diet_page.SELECT_MEAL_TYPE, timeout=5)
        assert diet_page.is_visible(diet_page.SELECT_DIET_ITEMS, timeout=5)
        assert diet_page.is_visible(diet_page.BTN_SAVE, timeout=5)

        if diet_page.is_visible(diet_page.INPUT_NOTES, timeout=3):
            diet_page.type_text(diet_page.INPUT_NOTES, "وجبة خالية من الملح - فحص آلي")

        diet_page.take_screenshot("10_patient_diet_loaded", folder="patient_diet")
