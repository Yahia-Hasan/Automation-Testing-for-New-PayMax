import pytest
from pages.home_page import HomePage
from pages.rays_page import (
    RaysWaitingListPage,
    RaysStatusPage,
    RaysDetailsPage,
)

class TestRaysUI:
    """UI Test Suite covering all 3 Rays / Radiology screens."""

    def test_01_rays_waiting_list(self, auth_driver):
        """1. Verify Rays Waiting List (/rays/waiting-list)."""
        home = HomePage(auth_driver).open()
        home.open_rays_waiting()

        waiting_page = RaysWaitingListPage(auth_driver)
        assert waiting_page.is_loaded(), "Rays waiting list page failed to load."
        assert "/rays/waiting-list" in auth_driver.current_url

        waiting_page.filter_emergency()
        waiting_page.take_screenshot("test_rays_waiting_emergency")

        waiting_page.filter_all()
        waiting_page.click_search()
        waiting_page.take_screenshot("test_rays_waiting_searched")

    def test_02_rays_status(self, auth_driver):
        """2. Verify Rays Status (/rays/status)."""
        home = HomePage(auth_driver).open()
        home.open_rays_status()

        status_page = RaysStatusPage(auth_driver)
        assert status_page.is_loaded(), "Rays status page failed to load."
        assert "/rays/status" in auth_driver.current_url

        status_page.click_search()
        status_page.take_screenshot("test_rays_status_searched")

    def test_03_rays_details(self, auth_driver):
        """3. Verify Rays Detailed Report (/rays/details)."""
        home = HomePage(auth_driver).open()
        home.open_rays_details()

        details_page = RaysDetailsPage(auth_driver)
        assert details_page.is_loaded(), "Rays details page failed to load."
        assert "/rays/details" in auth_driver.current_url

        details_page.click_search()
        details_page.take_screenshot("test_rays_details_searched")
