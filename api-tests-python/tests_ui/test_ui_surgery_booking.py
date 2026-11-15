import pytest
from pages.home_page import HomePage
from pages.surgery_booking_page import SurgeryBookingPage

class TestSurgeryBookingUI:
    """UI Test Suite for Surgery Booking (/reception/surgery-booking)."""

    def test_01_navigate_to_surgery_booking(self, auth_driver):
        """Verify navigation from Top Navbar: مكتب الدخول -> حجز العمليات."""
        home = HomePage(auth_driver).open()
        assert home.is_loaded(), "Home dashboard failed to load."

        home.open_surgery_booking()

        booking_page = SurgeryBookingPage(auth_driver)
        assert booking_page.is_loaded(), "Surgery booking page failed to load."
        assert "/reception/surgery-booking" in auth_driver.current_url
        assert "حجز العمليات" in booking_page.get_header_title()
        booking_page.take_screenshot("test_surgery_booking_navigated")

    def test_02_verify_form_fields_present(self, auth_driver):
        """Verify form controls: date, selectors, inputs, and action buttons."""
        booking_page = SurgeryBookingPage(auth_driver)
        assert booking_page.is_visible(booking_page.INPUT_DATE), "Date input missing."
        assert booking_page.is_visible(booking_page.SELECT_DOCTOR), "Doctor select missing."
        assert booking_page.is_visible(booking_page.SELECT_SPECIALTY), "Specialty select missing."
        assert booking_page.is_visible(booking_page.SELECT_SURGERY), "Surgery select missing."
        assert booking_page.is_visible(booking_page.SELECT_RESERVATION), "Reservation select missing."
        assert booking_page.is_visible(booking_page.INPUT_SHORT_CODE), "Patient short code input missing."
        assert booking_page.is_visible(booking_page.INPUT_PATIENT_NAME), "Patient name input missing."
        assert booking_page.is_visible(booking_page.BTN_SEARCH), "Search button missing."
        assert booking_page.is_visible(booking_page.BTN_ADD), "Add button missing."
        assert booking_page.is_visible(booking_page.BTN_CLEAR), "Clear button missing."

        date_val = booking_page.get_booking_date()
        assert date_val, "Date input should have a default date."
        booking_page.take_screenshot("test_surgery_booking_form_verified")

    def test_03_patient_inputs_and_clear_action(self, auth_driver):
        """Verify entering patient details and clearing via 'جديد' button."""
        booking_page = SurgeryBookingPage(auth_driver)
        booking_page.enter_patient_code("1202")
        booking_page.enter_patient_name("مريض تجريبي")

        assert booking_page.get_patient_code_value() == "1202"
        assert booking_page.get_patient_name_value() == "مريض تجريبي"
        booking_page.take_screenshot("test_surgery_booking_inputs_filled")

        booking_page.click_clear()
        assert booking_page.get_patient_code_value() == "", "Code input should be cleared."
        assert booking_page.get_patient_name_value() == "", "Name input should be cleared."
        booking_page.take_screenshot("test_surgery_booking_form_cleared")
