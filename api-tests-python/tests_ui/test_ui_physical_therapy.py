import pytest
from pages.home_page import HomePage
from pages.physical_therapy_page import PhysicalTherapyWaitingListPage

class TestPhysicalTherapyUI:
    """UI Test Suite covering Physical Therapy screens."""

    def test_01_pt_waiting_list(self, auth_driver):
        """1. Verify Physical Therapy Waiting List (/physical-therapy/waiting-list)."""
        home = HomePage(auth_driver).open()
        home.open_pt_waiting_list()

        pt_page = PhysicalTherapyWaitingListPage(auth_driver)
        assert pt_page.is_loaded(), "Physical therapy waiting list failed to load."
        assert "/physical-therapy/waiting-list" in auth_driver.current_url

        pt_page.click_search()
        pt_page.take_screenshot("test_pt_waiting_searched")
