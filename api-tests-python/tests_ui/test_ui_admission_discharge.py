import pytest
from pages.home_page import HomePage
from pages.admission_discharge_page import AdmissionDischargeReportPage

class TestAdmissionDischargeUI:
    """UI Test Suite for Admission & Discharge Report (/reception/admission-discharge-report)."""

    def test_01_navigate_to_admission_discharge_report(self, auth_driver):
        """Verify navigation from Top Navbar: مكتب الدخول -> تقرير الدخول والخروج."""
        home = HomePage(auth_driver).open()
        assert home.is_loaded(), "Home dashboard failed to load."

        home.open_admission_discharge_report()

        report_page = AdmissionDischargeReportPage(auth_driver)
        assert report_page.is_loaded(), "Admission & Discharge report failed to load."
        assert "/reception/admission-discharge-report" in auth_driver.current_url
        report_page.take_screenshot("test_admission_discharge_navigated")

    def test_02_verify_form_controls(self, auth_driver):
        """Verify presence and defaults of date inputs and filter selectors."""
        report_page = AdmissionDischargeReportPage(auth_driver)
        assert report_page.is_visible(report_page.DATE_FROM_INPUT), "Date from input missing."
        assert report_page.is_visible(report_page.DATE_TO_INPUT), "Date to input missing."
        assert report_page.is_visible(report_page.TYPE_SELECT), "Report type select missing."
        assert report_page.is_visible(report_page.DEGREE_SELECT), "Degree select missing."
        assert report_page.is_visible(report_page.FLOOR_SELECT), "Floor select missing."
        assert report_page.is_visible(report_page.INVOICE_STATUS_SELECT), "Invoice status select missing."
        assert report_page.is_visible(report_page.BTN_SEARCH), "Search button missing."

        date_from = report_page.get_date_from()
        date_to = report_page.get_date_to()
        assert date_from, "Date from should have a default date."
        assert date_to, "Date to should have a default date."

        report_page.take_screenshot("test_admission_discharge_form_controls")

    def test_03_search_and_load_data(self, auth_driver):
        """Verify clicking 'عرض' initiates search and UI responds."""
        report_page = AdmissionDischargeReportPage(auth_driver)
        report_page.click_search()

        # Check export button is ready
        assert report_page.is_export_button_ready(), "Export to Excel button should be visible and enabled."
        report_page.take_screenshot("test_admission_discharge_search_results")

    def test_04_instant_filter_and_export(self, auth_driver):
        """Verify instant filter input accepts queries and can be cleared."""
        report_page = AdmissionDischargeReportPage(auth_driver)
        assert report_page.is_visible(report_page.INPUT_FILTER), "Instant filter input missing."

        report_page.filter_table("محمد")
        report_page.take_screenshot("test_admission_discharge_filtered")

        report_page.clear_filter()
