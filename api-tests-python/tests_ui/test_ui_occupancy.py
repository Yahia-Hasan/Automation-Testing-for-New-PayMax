import pytest
from pages.home_page import HomePage
from pages.occupancy_page import OccupancyReportPage

class TestOccupancyUI:
    """UI Test Suite for the Hospital Occupancy Report (/reception/occupancy-report)."""

    def test_01_navigate_to_occupancy_report_via_navbar(self, auth_driver):
        """Verify navigation from Top Navbar: مكتب الدخول -> تقرير إشغال المستشفى."""
        home = HomePage(auth_driver).open()
        assert home.is_loaded(), "Home dashboard failed to load."

        home.open_occupancy_report()

        occ_page = OccupancyReportPage(auth_driver)
        assert occ_page.is_loaded(), "Occupancy report header failed to load."
        assert "/reception/occupancy-report" in auth_driver.current_url
        occ_page.take_screenshot("test_occupancy_navigated")

    def test_02_verify_kpi_metrics(self, auth_driver):
        """Verify KPI statistics cards (Total Beds, Occupied, Available, Occupancy %)."""
        occ_page = OccupancyReportPage(auth_driver)
        occ_page.wait_for_data_loaded(timeout=25)

        kpi = occ_page.get_kpi_summary()
        assert kpi["total_beds"].isdigit() and int(kpi["total_beds"]) > 0, f"Invalid total beds: {kpi['total_beds']}"
        assert kpi["occupied_beds"].isdigit(), f"Invalid occupied beds: {kpi['occupied_beds']}"
        assert kpi["available_beds"].isdigit(), f"Invalid available beds: {kpi['available_beds']}"
        assert "%" in kpi["occupancy_rate"], f"Invalid occupancy rate: {kpi['occupancy_rate']}"

        # Consistency check: Total = Occupied + Available
        total = int(kpi["total_beds"])
        occupied = int(kpi["occupied_beds"])
        available = int(kpi["available_beds"])
        assert total == occupied + available, f"Math mismatch: {total} != {occupied} + {available}"

        occ_page.take_screenshot("test_occupancy_kpi_verified")

    def test_03_verify_floors_list(self, auth_driver):
        """Verify that hospital floors list is loaded and rendered."""
        occ_page = OccupancyReportPage(auth_driver)
        floors_count = occ_page.get_floors_count()
        assert floors_count >= 10, f"Expected at least 10 floors, but found {floors_count}"

        occ_page.take_screenshot("test_occupancy_floors_list")

    def test_04_toggle_filter_checkboxes(self, auth_driver):
        """Verify toggling 'الغرف الفارغة فقط' and 'إخفاء الغرف الموقوف التسكين بها'."""
        occ_page = OccupancyReportPage(auth_driver)
        assert occ_page.is_visible(occ_page.CHECKBOX_EMPTY_ONLY), "Empty only checkbox missing."
        assert occ_page.is_visible(occ_page.CHECKBOX_ACTIVE_ROOMS_ONLY), "Active rooms only checkbox missing."

        occ_page.toggle_empty_only()
        occ_page.take_screenshot("test_occupancy_empty_only_checked")

        occ_page.toggle_empty_only()  # uncheck
        occ_page.toggle_active_rooms_only()
        occ_page.take_screenshot("test_occupancy_active_only_checked")

        occ_page.toggle_active_rooms_only()  # uncheck

    def test_05_search_filter(self, auth_driver):
        """Verify typing in search input field."""
        occ_page = OccupancyReportPage(auth_driver)
        assert occ_page.is_visible(occ_page.INPUT_SEARCH), "Search input field missing."

        occ_page.search_query("101")
        occ_page.take_screenshot("test_occupancy_search_101")

        # Clear search
        occ_page.search_query("")

    def test_06_sub_report_buttons(self, auth_driver):
        """Verify sub-report export/print buttons and excel export button exist."""
        occ_page = OccupancyReportPage(auth_driver)
        assert occ_page.is_visible(occ_page.BTN_BY_FLOOR), "تقرير الإشغال بالأدوار button missing."
        assert occ_page.is_visible(occ_page.BTN_BY_ROOM), "تقرير الإشغال بالغرف button missing."
        assert occ_page.is_visible(occ_page.BTN_RATES), "تقرير قوة المستشفي button missing."
        assert occ_page.is_visible(occ_page.BTN_EXPORT_EXCEL), "Export to Excel button missing."
        assert occ_page.is_visible(occ_page.BTN_REFRESH), "Refresh button missing."

        occ_page.take_screenshot("test_occupancy_subreports_verified")
