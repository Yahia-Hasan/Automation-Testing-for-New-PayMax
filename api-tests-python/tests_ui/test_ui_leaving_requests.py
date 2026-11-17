import pytest
from pages.home_page import HomePage
from pages.leaving_requests_page import LeavingRequestsPage

class TestLeavingRequestsUI:
    """UI Test Suite for Inpatients Pending Discharge / Leaving Requests (/waiting-list/leaving-requests)."""

    def test_01_navigate_to_leaving_requests(self, auth_driver):
        """Verify navigation from Top Navbar: مكتب الدخول -> المرضى الداخلي قيد الخروج."""
        home = HomePage(auth_driver).open()
        assert home.is_loaded(), "Home dashboard failed to load."

        home.open_leaving_requests()

        leaving_page = LeavingRequestsPage(auth_driver)
        assert leaving_page.is_loaded(), "Leaving requests page failed to load."
        assert "/waiting-list/leaving-requests" in auth_driver.current_url
        assert "طلبات المغادرة" in leaving_page.get_header_title()
        leaving_page.take_screenshot("test_leaving_requests_navigated")

    def test_02_verify_table_columns_and_rows(self, auth_driver):
        """Verify table headers and that requests are loaded in table."""
        leaving_page = LeavingRequestsPage(auth_driver)
        headers = leaving_page.get_headers()
        assert "كود الدخول" in headers, "كود الدخول header missing."
        assert "كود المريض" in headers, "كود المريض header missing."
        assert "اسم المريض" in headers, "اسم المريض header missing."
        assert "الجهة" in headers, "الجهة header missing."
        assert "تاريخ التسجيل" in headers, "تاريخ التسجيل header missing."

        count = leaving_page.get_rows_count()
        assert count > 0, "Table should display pending leaving requests."

        first_row = leaving_page.get_first_row_data()
        assert first_row["admission_code"], "First row should have an admission code."
        assert first_row["patient_name"], "First row should have a patient name."
        leaving_page.take_screenshot("test_leaving_requests_table_data")

    def test_03_search_filter(self, auth_driver):
        """Verify instant search filters the table."""
        leaving_page = LeavingRequestsPage(auth_driver)
        first_row = leaving_page.get_first_row_data()
        patient_code = first_row["patient_code"]

        leaving_page.search(patient_code)
        filtered_count = leaving_page.get_rows_count()
        assert filtered_count >= 1, f"Search by {patient_code} should find matching row."
        leaving_page.take_screenshot("test_leaving_requests_searched")

        leaving_page.clear_search()

    def test_04_reload_button(self, auth_driver):
        """Verify reload button refreshes the table."""
        leaving_page = LeavingRequestsPage(auth_driver)
        assert leaving_page.is_visible(leaving_page.BTN_RELOAD), "Reload button missing."
        leaving_page.click_reload()
        assert leaving_page.get_rows_count() > 0, "Rows should reload successfully."
        leaving_page.take_screenshot("test_leaving_requests_reloaded")
