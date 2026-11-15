import pytest
from pages.navbar_page import NavbarPage

class TestNavbar:
    """Test suite for the Top Navbar Component."""

    @pytest.fixture(autouse=True)
    def setup_page(self, authenticated_driver):
        self.driver = authenticated_driver
        self.navbar = NavbarPage(self.driver)

    def test_navbar_visibility(self):
        """TC_NAV_01: Verify that top navbar is visible and brand logo exists."""
        assert self.navbar.is_navbar_visible(), "Top navbar should be visible on the page."
        brand_el = self.navbar.find(NavbarPage.BRAND_LOGO)
        assert brand_el.is_displayed(), "Navbar brand logo should be displayed."

    def test_reception_dropdown_toggle_and_items(self):
        """
        TC_NAV_02: Verify clicking 'مكتب الدخول' opens dropdown, displays 8 items,
        and clicking again closes it.
        """
        dropdown_name = "مكتب الدخول"
        
        # 1. Open dropdown
        self.navbar.open_dropdown(dropdown_name)
        assert self.navbar.is_dropdown_open(dropdown_name), f"Dropdown '{dropdown_name}' should have '.open' class."

        # 2. Verify items
        items = self.navbar.get_open_dropdown_items()
        assert len(items) == 8, f"Expected 8 dropdown items under '{dropdown_name}', found {len(items)}."
        
        expected_routes = [
            "/reception",
            "/reception/occupancy-report",
            "/reception/admission-discharge-report",
            "/reception/surgery-booking",
            "/waiting-list/leaving-requests",
            "/accountant/leaving-requests",
            "/reception/emergency-transfers",
            "/reception/leaving-approval-report"
        ]
        actual_hrefs = [item["href"] for item in items]
        for route in expected_routes:
            assert any(route in href for href in actual_hrefs), f"Route '{route}' should be present in dropdown items."

        # 3. Close dropdown
        self.navbar.close_dropdown(dropdown_name)
        assert not self.navbar.is_dropdown_open(dropdown_name), f"Dropdown '{dropdown_name}' should be closed."

    def test_dropdown_click_outside_dismiss(self):
        """TC_NAV_03: Verify clicking outside an open dropdown dismisses it."""
        dropdown_name = "مكتب الدخول"
        self.navbar.open_dropdown(dropdown_name)
        assert self.navbar.is_dropdown_open(dropdown_name), "Dropdown should be open before click-outside."

        self.navbar.click_outside()
        # Wait until closed
        import time
        time.sleep(0.5)
        assert not self.navbar.is_dropdown_open(dropdown_name), "Dropdown should close after clicking outside."

    def test_navigation_to_medical_file(self):
        """TC_NAV_04: Verify clicking 'الملف الطبى' navigates to /reception."""
        dropdown_name = "مكتب الدخول"
        self.navbar.open_dropdown(dropdown_name)
        self.navbar.click_dropdown_item_by_href("/reception")
        
        import time
        time.sleep(1)
        assert "/reception" in self.driver.current_url, f"Expected URL to contain '/reception', got '{self.driver.current_url}'."

