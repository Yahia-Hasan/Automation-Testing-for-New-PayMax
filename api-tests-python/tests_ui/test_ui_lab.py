import pytest
from pages.home_page import HomePage
from pages.lab_page import (
    LabWaitingListPage,
    BloodWaitingListPage,
    LabDetailsPage,
    BloodBankStatusPage,
    LabResultsInquiryPage,
)

class TestLabUI:
    """UI Test Suite covering all 5 Laboratory & Blood Bank screens."""

    def test_01_lab_waiting_list(self, auth_driver):
        """1. Verify Lab Waiting List (/lab/waiting-list)."""
        home = HomePage(auth_driver).open()
        home.open_lab_waiting()

        waiting_page = LabWaitingListPage(auth_driver)
        assert waiting_page.is_loaded(), "Lab waiting list page failed to load."
        assert "/lab/waiting-list" in auth_driver.current_url

        waiting_page.click_search()
        waiting_page.take_screenshot("test_lab_waiting_searched")

    def test_02_blood_waiting_list(self, auth_driver):
        """2. Verify Blood Bank Waiting List (/lab/blood-waiting-list)."""
        home = HomePage(auth_driver).open()
        home.open_lab_blood_waiting()

        blood_page = BloodWaitingListPage(auth_driver)
        assert blood_page.is_loaded(), "Blood bank waiting list failed to load."
        assert "/lab/blood-waiting-list" in auth_driver.current_url
        assert blood_page.get_rows_count() > 0, "Blood bank waiting list should have request rows."

        blood_page.take_screenshot("test_blood_waiting_loaded")

    def test_03_lab_details(self, auth_driver):
        """3. Verify Detailed Lab Report (/lab/details)."""
        home = HomePage(auth_driver).open()
        home.open_lab_details()

        details_page = LabDetailsPage(auth_driver)
        assert details_page.is_loaded(), "Lab details report failed to load."
        assert "/lab/details" in auth_driver.current_url

        details_page.click_search()
        details_page.take_screenshot("test_lab_details_searched")

    def test_04_blood_bank_status(self, auth_driver):
        """4. Verify Blood Bank Status Inquiry (/lab/blood-bank-status)."""
        home = HomePage(auth_driver).open()
        home.open_lab_blood_status()

        status_page = BloodBankStatusPage(auth_driver)
        assert status_page.is_loaded(), "Blood bank status page failed to load."
        assert "/lab/blood-bank-status" in auth_driver.current_url

        status_page.click_search()
        status_page.take_screenshot("test_blood_status_searched")

    def test_05_lab_results_inquiry(self, auth_driver):
        """5. Verify Lab Results Inquiry (/lab/results-inquiry)."""
        home = HomePage(auth_driver).open()
        home.open_lab_results_inquiry()

        inquiry_page = LabResultsInquiryPage(auth_driver)
        assert inquiry_page.is_loaded(), "Lab results inquiry page failed to load."
        assert "/lab/results-inquiry" in auth_driver.current_url

        inquiry_page.click_search()
        inquiry_page.take_screenshot("test_lab_results_searched")
