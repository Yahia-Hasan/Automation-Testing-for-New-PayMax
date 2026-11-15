import pytest
from pages.home_page import HomePage
from pages.emergency_transfers_page import EmergencyTransfersPage

class TestEmergencyTransfersUI:
    """UI Test Suite for Emergency Patient Transfers (/reception/emergency-transfers)."""

    def test_01_navigate_to_emergency_transfers(self, auth_driver):
        """Verify navigation from Top Navbar: مكتب الدخول -> طلبات تحويل المرضى من الطوارئ."""
        home = HomePage(auth_driver).open()
        assert home.is_loaded(), "Home dashboard failed to load."

        home.open_emergency_transfers()

        transfers_page = EmergencyTransfersPage(auth_driver)
        assert transfers_page.is_loaded(), "Emergency transfers page failed to load."
        assert "/reception/emergency-transfers" in auth_driver.current_url
        assert "طلبات تحويل المرضى من الطوارئ للداخلى" in transfers_page.get_header_title()
        transfers_page.take_screenshot("test_emergency_transfers_navigated")

    def test_02_verify_form_controls(self, auth_driver):
        """Verify date controls and search button."""
        transfers_page = EmergencyTransfersPage(auth_driver)
        assert transfers_page.is_visible(transfers_page.DATE_FROM_INPUT), "Date from input missing."
        assert transfers_page.is_visible(transfers_page.DATE_TO_INPUT), "Date to input missing."
        assert transfers_page.is_visible(transfers_page.BTN_SEARCH), "Search button missing."

        date_from = transfers_page.get_date_from()
        date_to = transfers_page.get_date_to()
        assert date_from, "Date from should have default value."
        assert date_to, "Date to should have default value."
        transfers_page.take_screenshot("test_emergency_transfers_form_controls")

    def test_03_search_action(self, auth_driver):
        """Verify clicking 'عرض' initiates search without error."""
        transfers_page = EmergencyTransfersPage(auth_driver)
        transfers_page.click_search()
        transfers_page.take_screenshot("test_emergency_transfers_searched")
