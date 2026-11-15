import pytest
from pages.home_page import HomePage
from pages.infodesk_page import (
    PriceListsPage,
    DoctorsListPage,
    ShiftManagersPage,
    SurgeryNamesPage,
    SurgeryPricesPage,
    SurgeryAgendaPage,
    ClinicAgendaPage,
    PhoneBookPage,
    SurgeriesWaitingListPage,
    PackagesPage,
)

class TestInfoDeskUI:
    """Comprehensive UI Test Suite covering all 10 InfoDesk Screens."""

    def test_01_navigate_to_price_lists(self, auth_driver):
        """1. Verify navigation from Home to InfoDesk Price Lists."""
        home = HomePage(auth_driver).open()
        home.open_price_lists()

        price_lists = PriceListsPage(auth_driver)
        assert price_lists.is_filter_visible(), "Client dropdown and search button should be visible."
        price_lists.take_screenshot("test_price_lists_opened")

    def test_02_search_price_lists(self, auth_driver):
        """2. Verify clicking search on Price Lists screen."""
        price_lists = PriceListsPage(auth_driver)
        price_lists.open()
        price_lists.click_search()

        assert price_lists.is_visible(price_lists.BTN_SEARCH), "Search button should be visible."
        price_lists.take_screenshot("test_price_lists_searched")

    def test_03_doctors_directory_search(self, auth_driver):
        """3. Verify searching doctors directory in InfoDesk (/info-desk/doctors)."""
        doctors_page = DoctorsListPage(auth_driver)
        doctors_page.open()

        assert doctors_page.is_loaded(), "Doctors list page failed to load."
        doctors_page.search_doctor("باطنة")
        assert doctors_page.is_loaded(), "Doctors page should remain functional after search."
        doctors_page.take_screenshot("test_doctors_searched")

    def test_04_shift_managers(self, auth_driver):
        """4. Verify Shift Managers page (/info-desk/shift-managers)."""
        home = HomePage(auth_driver).open()
        home.open_shift_managers()

        shift_page = ShiftManagersPage(auth_driver)
        assert shift_page.is_loaded(), "Shift managers page failed to load."
        assert shift_page.get_rows_count() > 0, "Shift managers table should have rows."

        shift_page.filter_table("2026")
        shift_page.take_screenshot("test_shift_managers_filtered")
        shift_page.clear_filter()

    def test_05_surgery_names(self, auth_driver):
        """5. Verify Surgery Names page (/info-desk/surgery-names)."""
        home = HomePage(auth_driver).open()
        home.open_surgery_names()

        names_page = SurgeryNamesPage(auth_driver)
        assert names_page.is_loaded(), "Surgery names page failed to load."
        names_page.click_search()
        names_page.take_screenshot("test_surgery_names_searched")

    def test_06_surgery_prices(self, auth_driver):
        """6. Verify Surgery Prices page (/info-desk/surgery-prices)."""
        home = HomePage(auth_driver).open()
        home.open_surgery_prices()

        prices_page = SurgeryPricesPage(auth_driver)
        assert prices_page.is_loaded(), "Surgery prices page failed to load."
        prices_page.click_search()
        prices_page.take_screenshot("test_surgery_prices_searched")

    def test_07_surgery_agenda(self, auth_driver):
        """7. Verify Surgery Agenda page (/info-desk/surgery-agenda)."""
        home = HomePage(auth_driver).open()
        home.open_surgery_agenda()

        agenda_page = SurgeryAgendaPage(auth_driver)
        assert agenda_page.is_loaded(), "Surgery agenda page failed to load."
        agenda_page.click_search()
        agenda_page.take_screenshot("test_surgery_agenda_searched")

    def test_08_clinic_agenda(self, auth_driver):
        """8. Verify Clinic Agenda page (/info-desk/clinic-agenda)."""
        home = HomePage(auth_driver).open()
        home.open_clinic_agenda()

        clinic_agenda = ClinicAgendaPage(auth_driver)
        assert clinic_agenda.is_loaded(), "Clinic agenda page failed to load."
        clinic_agenda.click_search()
        clinic_agenda.take_screenshot("test_clinic_agenda_searched")

    def test_09_phone_book(self, auth_driver):
        """9. Verify Phone Book directory (/info-desk/phone-book)."""
        home = HomePage(auth_driver).open()
        home.open_phone_book()

        phone_page = PhoneBookPage(auth_driver)
        assert phone_page.is_loaded(), "Phone book page failed to load."
        assert phone_page.get_rows_count() > 0, "Phone book directory should display contact rows."

        phone_page.filter_table("مستشفى")
        phone_page.take_screenshot("test_phone_book_filtered")
        phone_page.clear_filter()

    def test_10_surgeries_waiting(self, auth_driver):
        """10. Verify Surgeries Waiting List (/info-desk/surgeries)."""
        home = HomePage(auth_driver).open()
        home.open_surgery_waiting()

        waiting_page = SurgeriesWaitingListPage(auth_driver)
        assert waiting_page.is_loaded(), "Surgeries waiting page failed to load."
        waiting_page.click_search()
        waiting_page.take_screenshot("test_surgeries_waiting_searched")

    def test_11_packages(self, auth_driver):
        """11. Verify Packages inquiry page (/info-desk/packages)."""
        home = HomePage(auth_driver).open()
        home.open_packages()

        pkg_page = PackagesPage(auth_driver)
        assert pkg_page.is_loaded(), "Packages page failed to load."
        assert pkg_page.get_rows_count() > 0, "Packages table should display available packages."

        pkg_page.filter_table("عادية")
        pkg_page.take_screenshot("test_packages_filtered")
        pkg_page.clear_filter()
