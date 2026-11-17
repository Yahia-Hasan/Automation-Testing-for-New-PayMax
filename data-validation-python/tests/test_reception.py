import pytest
from datetime import datetime
from pages.reception_page import ReceptionPage

class TestReception:
    """
    Test suite for the Reception / Medical File Page (الملف الطبى / بيانات المريض).
    Covers component presence, dynamic business logic (WhatsApp copy, Age calculation),
    and client-side input validation.
    """

    @pytest.fixture(autouse=True)
    def setup_page(self, authenticated_driver):
        self.driver = authenticated_driver
        self.reception = ReceptionPage(self.driver)
        self.reception.navigate_to()

    def test_reception_page_elements_presence(self):
        """
        TC_REC_01: Verify that Reception form loads properly with all key input fields
        and actions available.
        """
        assert self.reception.is_page_loaded(), "Reception form should be loaded and visible."
        
        # Verify critical elements are visible
        assert self.reception.is_visible(ReceptionPage.SEARCH_INPUT), "Search box should be visible."
        assert self.reception.is_visible(ReceptionPage.PATIENT_NAME_INPUT), "Patient name input should be visible."
        assert self.reception.is_visible(ReceptionPage.MOBILE_PHONE_INPUT), "Mobile phone input should be visible."
        assert self.reception.is_visible(ReceptionPage.BIRTH_DATE_INPUT), "Birth date input should be visible."
        assert self.reception.is_visible(ReceptionPage.SAVE_BTN), "Save button should be visible."
        assert self.reception.is_visible(ReceptionPage.NEW_BTN), "New button should be visible."

    def test_whatsapp_same_as_mobile_mirroring(self):
        """
        TC_REC_02: Business Rule #4:
        Selecting 'نفس رقم الواتساب' should automatically copy the mobile number
        into the WhatsApp field and disable manual input.
        """
        test_mobile = "01012345678"
        
        # 1. Reset form
        self.reception.click_new()
        
        # 2. Enter mobile number
        self.reception.enter_mobile_phone(test_mobile)
        
        # 3. Check 'نفس رقم الواتساب'
        if not self.reception.is_whatsapp_same_checked():
            self.reception.toggle_whatsapp_same()
            
        # 4. Verify value in WhatsApp matches mobile
        whatsapp_val = self.reception.get_whatsapp_value()
        assert whatsapp_val == test_mobile, (
            f"Expected WhatsApp to mirror mobile '{test_mobile}', but got '{whatsapp_val}'."
        )
        
        # 5. Reset form for clean teardown
        self.reception.click_new()

    def test_birth_date_auto_age_calculation(self):
        """
        TC_REC_03: Business Rule #5:
        Entering a valid birth date should automatically calculate and populate the age in years.
        """
        # 1. Reset form
        self.reception.click_new()
        
        # 2. Enter birth date (e.g. 2000-05-15)
        birth_year = 2000
        birth_date = f"{birth_year}-05-15"
        self.reception.enter_birth_date(birth_date)
        
        # 3. Calculate expected age (current_year - 2000)
        current_year = datetime.now().year
        expected_age_approx = current_year - birth_year
        
        # 4. Verify calculated age in years
        age_val = self.reception.get_age_years()
        assert age_val != "", "Age years should be automatically calculated and populated."
        actual_age = int(age_val)
        assert abs(actual_age - expected_age_approx) <= 1, (
            f"Expected age close to {expected_age_approx}, but got {actual_age}."
        )
        
        # 5. Reset form
        self.reception.click_new()

    def test_empty_form_save_validation(self):
        """
        TC_REC_04: Negative Validation:
        Clicking 'اضافة' (Save) with an empty form must trigger the validation toast:
        'يرجى إدخال اسم المريض'.
        """
        # 1. Reset form to ensure clean state
        self.reception.click_new()
        
        # 2. Click Save without entering patient name
        self.reception.click_save()
        
        # 3. Verify validation toast appears
        toast_msg = self.reception.wait_for_toast("يرجى إدخال اسم المريض", timeout=5)
        assert "يرجى إدخال اسم المريض" in toast_msg, (
            f"Expected validation toast 'يرجى إدخال اسم المريض', but got: '{toast_msg}'"
        )
