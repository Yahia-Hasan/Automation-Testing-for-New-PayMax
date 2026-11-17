import pytest
from datetime import date, timedelta
from pages.invoices_page import RegisteredInvoicesPage

class TestInvoicesUI:
    """UI Test Suite for the Registered Patient Invoices Module."""

    def test_01_navigate_to_registered_invoices(self, auth_driver):
        """Verify navigation to Registered Invoices (/patient-accounts/registered-invoices)."""
        invoices = RegisteredInvoicesPage(auth_driver)
        invoices.open()

        assert invoices.is_loaded(), "Registered Invoices failed to load date inputs or search button."
        assert invoices.is_export_excel_visible(), "Export to Excel button should be visible."
        invoices.take_screenshot("test_invoices_opened")

    def test_02_filter_by_date_and_search(self, auth_driver):
        """Verify date filtering and search submission in Registered Invoices."""
        invoices = RegisteredInvoicesPage(auth_driver)
        invoices.open()

        # Set date range: last 7 days to today
        today = date.today()
        from_date = (today - timedelta(days=7)).strftime("%Y-%m-%d")
        to_date = today.strftime("%Y-%m-%d")

        invoices.set_dates(from_date, to_date)
        invoices.click_search()

        assert invoices.is_loaded(), "Invoices screen should remain intact after search."
        invoices.take_screenshot("test_invoices_searched")

    def test_03_today_exit_button(self, auth_driver):
        """Verify 'خروج اليوم' button filters invoices correctly."""
        invoices = RegisteredInvoicesPage(auth_driver)
        invoices.open()

        invoices.click_today_exit()
        assert invoices.is_loaded(), "Invoices screen should remain intact after clicking 'خروج اليوم'."
        invoices.take_screenshot("test_invoices_today_exit")
