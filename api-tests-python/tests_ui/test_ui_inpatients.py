import pytest
from pages.home_page import HomePage
from pages.inpatients_page import (
    InpatientsPage,
    ICUInpatientsPage,
    NeonatalInpatientsPage,
    AttendantsPage,
    RoomManagementPage,
    RoomOccupancyMapPage,
)

class TestInpatientsUI:
    """UI Test Suite covering all 6 Resident Patients & Rooms screens."""

    def test_01_navigate_to_inpatients_rooms(self, auth_driver):
        """1. Verify navigation to Inpatients Rooms (/reception/inpatients) via navbar."""
        home = HomePage(auth_driver).open()
        home.open_inpatients_rooms()

        inpatients = InpatientsPage(auth_driver)
        assert inpatients.is_loaded(), "Inpatients page failed to load search input."
        assert "/reception/inpatients" in auth_driver.current_url
        inpatients.take_screenshot("test_inpatients_opened")

    def test_02_search_and_refresh_inpatients(self, auth_driver):
        """2. Verify search input and refresh button functionality in Inpatients."""
        inpatients = InpatientsPage(auth_driver)
        inpatients.open()

        inpatients.search("احمد")
        inpatients.refresh()

        assert inpatients.is_loaded(), "Inpatients page should remain loaded after refresh."
        inpatients.take_screenshot("test_inpatients_refreshed")

    def test_03_navigate_to_icu_inpatients(self, auth_driver):
        """3. Verify ICU Inpatients screen (/reception/icu)."""
        home = HomePage(auth_driver).open()
        home.open_icu()

        icu_page = ICUInpatientsPage(auth_driver)
        assert icu_page.is_loaded(), "ICU Inpatients page failed to load."
        assert "/reception/icu" in auth_driver.current_url
        assert "المقيمين بالرعاية المركزة" in icu_page.get_header_title()
        icu_page.take_screenshot("test_icu_navigated")

    def test_04_navigate_to_neonatal_inpatients(self, auth_driver):
        """4. Verify Neonatal Inpatients screen (/reception/neonatal)."""
        home = HomePage(auth_driver).open()
        home.open_neonatal()

        neonatal_page = NeonatalInpatientsPage(auth_driver)
        assert neonatal_page.is_loaded(), "Neonatal Inpatients page failed to load."
        assert "/reception/neonatal" in auth_driver.current_url
        assert "المقيمين بالحضانة" in neonatal_page.get_header_title()
        neonatal_page.take_screenshot("test_neonatal_navigated")

    def test_05_patient_attendants(self, auth_driver):
        """5. Verify Patient Attendants screen (/reception/attendants)."""
        home = HomePage(auth_driver).open()
        home.open_attendants()

        attendants_page = AttendantsPage(auth_driver)
        assert attendants_page.is_loaded(), "Attendants page failed to load."
        assert "/reception/attendants" in auth_driver.current_url

        attendants_page.search("محمد")
        attendants_page.take_screenshot("test_attendants_searched")
        attendants_page.clear_search()

    def test_06_room_management_table_and_tabs(self, auth_driver):
        """6. Verify Room Management screen (/reception/room-management) and tabs."""
        home = HomePage(auth_driver).open()
        home.open_room_management()

        rooms_page = RoomManagementPage(auth_driver)
        assert rooms_page.is_loaded(), "Room Management page failed to load."
        assert rooms_page.get_rooms_count() > 0, "Room Management table should display rooms."

        # Switch to ICU tab
        rooms_page.switch_to_icu_tab()
        rooms_page.take_screenshot("test_room_management_icu_tab")

        # Switch to Neonatal tab
        rooms_page.switch_to_neonatal_tab()
        rooms_page.take_screenshot("test_room_management_neonatal_tab")

        # Switch back to Rooms tab and search
        rooms_page.switch_to_rooms_tab()
        rooms_page.search_room("101")
        rooms_page.take_screenshot("test_room_management_searched")
        rooms_page.clear_search()

    def test_07_room_occupancy_map(self, auth_driver):
        """7. Verify Room Occupancy Map (/reception/rooms)."""
        home = HomePage(auth_driver).open()
        home.open_room_map()

        map_page = RoomOccupancyMapPage(auth_driver)
        assert map_page.is_loaded(), "Room Occupancy Map failed to load."
        assert "/reception/rooms" in auth_driver.current_url
        map_page.take_screenshot("test_room_map_navigated")
