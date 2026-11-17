import pytest
from pages.home_page import HomePage
from pages.leaving_approval_report_page import LeavingApprovalReportPage

class TestLeavingApprovalReportUI:
    """UI Test Suite for Leaving Approval Report (/reception/leaving-approval-report)."""

    def test_01_navigate_to_leaving_approval_report(self, auth_driver):
        """Verify navigation from Top Navbar: مكتب الدخول -> تقرير تأكيد طلبات المغادرة."""
        home = HomePage(auth_driver).open()
        assert home.is_loaded(), "Home dashboard failed to load."

        home.open_leaving_approval_report()

        report_page = LeavingApprovalReportPage(auth_driver)
        assert report_page.is_loaded(), "Leaving approval report page failed to load."
        assert "/reception/leaving-approval-report" in auth_driver.current_url
        assert "تقرير تأكيد طلبات المغادرة" in report_page.get_header_title()
        report_page.take_screenshot("test_leaving_approval_navigated")

    def test_02_verify_form_controls(self, auth_driver):
        """Verify date controls, approval type selector, and search button."""
        report_page = LeavingApprovalReportPage(auth_driver)
        assert report_page.is_visible(report_page.DATE_FROM_INPUT), "Date from input missing."
        assert report_page.is_visible(report_page.DATE_TO_INPUT), "Date to input missing."
        assert report_page.is_visible(report_page.APPROVAL_TYPE_SELECT), "Approval type select missing."
        assert report_page.is_visible(report_page.BTN_SEARCH), "Search button missing."

        date_from = report_page.get_date_from()
        date_to = report_page.get_date_to()
        assert date_from, "Date from should have default value."
        assert date_to, "Date to should have default value."
        report_page.take_screenshot("test_leaving_approval_form_controls")

    def test_03_query_and_verify_actions(self, auth_driver):
        """Verify clicking 'استعلام' executes query and enables export/filter controls."""
        report_page = LeavingApprovalReportPage(auth_driver)
        report_page.click_search()

        assert report_page.is_export_button_ready(), "Export to Excel button should be enabled."
        assert report_page.is_visible(report_page.INPUT_FILTER), "Instant filter input should be visible."

        report_page.filter_table("محمد")
        report_page.take_screenshot("test_leaving_approval_filtered")

        report_page.clear_filter()
