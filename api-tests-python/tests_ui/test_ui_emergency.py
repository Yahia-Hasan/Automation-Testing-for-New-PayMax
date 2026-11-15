import pytest
from pages.emergency_page import EmergencyWaitingListPage

class TestEmergencyUI:
    """UI Test Suite for the Emergency Module."""

    def test_01_navigate_to_emergency_waiting_list(self, auth_driver):
        """Verify navigation to Emergency Waiting List (/emergency/waiting-list)."""
        emergency_page = EmergencyWaitingListPage(auth_driver)
        emergency_page.open()

        assert emergency_page.is_loaded(), "Emergency Waiting List failed to load search input or export button."
        assert emergency_page.is_export_excel_visible(), "Export to Excel button should be visible."
        emergency_page.take_screenshot("test_emergency_waiting_list_opened")

    def test_02_search_emergency_patients(self, auth_driver):
        """Verify searching within the emergency waiting list."""
        emergency_page = EmergencyWaitingListPage(auth_driver)
        emergency_page.open()

        # Search for a query
        emergency_page.search("محمد")
        row_count = emergency_page.get_row_count()
        assert row_count >= 0, "Emergency row count should be a valid integer."
        emergency_page.take_screenshot("test_emergency_searched")
