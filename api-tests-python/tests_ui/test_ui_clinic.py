import pytest
from datetime import date
from pages.home_page import HomePage
from pages.clinic_page import ClinicWaitingListPage

class TestClinicUI:
    """UI Test Suite for the Outpatient Clinic Module."""

    def test_01_navigate_to_clinic_waiting_list(self, auth_driver):
        """Verify navigation to Clinic Waiting List (/clinic/waiting-list)."""
        home = HomePage(auth_driver)
        home.open_clinic_waiting_list()

        clinic_page = ClinicWaitingListPage(auth_driver)
        assert clinic_page.is_filter_panel_visible(), "Clinic filters (Date / Search button) should be visible."
        clinic_page.take_screenshot("test_clinic_waiting_list_opened")

    def test_02_filter_by_date_and_search(self, auth_driver):
        """Verify applying date filter and clicking search in Clinic Waiting List."""
        clinic_page = ClinicWaitingListPage(auth_driver)
        clinic_page.open()

        today_str = date.today().strftime("%Y-%m-%d")
        clinic_page.set_date(today_str)
        clinic_page.click_search()

        assert clinic_page.is_visible(clinic_page.BTN_SEARCH), "Search button should still be visible after filtering."
        clinic_page.take_screenshot("test_clinic_waiting_list_searched")
