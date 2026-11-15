import pytest
from pages.home_page import HomePage
from pages.accountant_leaving_page import AccountantLeavingRequestsPage

class TestAccountantLeavingUI:
    """UI Test Suite for Patient Discharge Requests (/accountant/leaving-requests)."""

    def test_01_navigate_to_accountant_leaving(self, auth_driver):
        """Verify navigation from Top Navbar: مكتب الدخول -> طلبات خروج المرضى."""
        home = HomePage(auth_driver).open()
        assert home.is_loaded(), "Home dashboard failed to load."

        home.open_accountant_leaving_requests()

        leaving_page = AccountantLeavingRequestsPage(auth_driver)
        assert leaving_page.is_loaded(), "Accountant leaving requests page failed to load."
        assert "/accountant/leaving-requests" in auth_driver.current_url
        assert "طلبات خروج المرضى" in leaving_page.get_header_title()
        leaving_page.take_screenshot("test_accountant_leaving_navigated")

    def test_02_verify_form_controls(self, auth_driver):
        """Verify form controls: date inputs, select dropdowns, and search button."""
        leaving_page = AccountantLeavingRequestsPage(auth_driver)
        assert leaving_page.is_visible(leaving_page.DATE_FROM_INPUT), "Date from input missing."
        assert leaving_page.is_visible(leaving_page.DATE_TO_INPUT), "Date to input missing."
        assert leaving_page.is_visible(leaving_page.CLIENT_SELECT), "Client select missing."
        assert leaving_page.is_visible(leaving_page.ACCOM_TYPE_SELECT), "Accommodation type select missing."
        assert leaving_page.is_visible(leaving_page.ROOM_SELECT), "Room select missing."
        assert leaving_page.is_visible(leaving_page.BTN_SEARCH), "Search button missing."

        date_from = leaving_page.get_date_from()
        date_to = leaving_page.get_date_to()
        assert date_from, "Date from should have default value."
        assert date_to, "Date to should have default value."
        leaving_page.take_screenshot("test_accountant_leaving_form_controls")

    def test_03_search_action(self, auth_driver):
        """Verify clicking 'عرض' button initiates search and responds without error."""
        leaving_page = AccountantLeavingRequestsPage(auth_driver)
        leaving_page.click_search()
        leaving_page.take_screenshot("test_accountant_leaving_searched")
