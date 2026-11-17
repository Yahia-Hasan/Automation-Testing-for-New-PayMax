import time
import logging
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger("BayMaxOccupancyPage")

class OccupancyReportPage(BasePage):
    """Page Object for Hospital Occupancy Report (/reception/occupancy-report)."""

    URL = "https://196.218.246.250:4040/reception/occupancy-report"

    # Locators
    HEADER_TITLE = (By.XPATH, "//h1[contains(., 'تقرير الإشغال')]")
    
    # KPI Stats
    STAT_TOTAL_BEDS = (By.CSS_SELECTOR, ".occ-stats .stat:not(.occupied):not(.available):not(.pct) .stat-val")
    STAT_OCCUPIED_BEDS = (By.CSS_SELECTOR, ".occ-stats .stat.occupied .stat-val")
    STAT_AVAILABLE_BEDS = (By.CSS_SELECTOR, ".occ-stats .stat.available .stat-val")
    STAT_OCCUPANCY_PCT = (By.CSS_SELECTOR, ".occ-stats .stat.pct .stat-val")

    # Sub-Reports
    BTN_BY_FLOOR = (By.CSS_SELECTOR, "[data-test-id='occupancy-report-by-floor-btn']")
    BTN_BY_ROOM = (By.CSS_SELECTOR, "[data-test-id='occupancy-report-by-room-btn']")
    BTN_RATES = (By.CSS_SELECTOR, "[data-test-id='occupancy-report-rates-btn']")

    # Filters & Actions
    CHECKBOX_EMPTY_ONLY = (By.CSS_SELECTOR, "[data-test-id='occupancy-report-empty-only-checkbox']")
    CHECKBOX_ACTIVE_ROOMS_ONLY = (By.CSS_SELECTOR, "[data-test-id='occupancy-report-active-rooms-only-checkbox']")
    INPUT_SEARCH = (By.CSS_SELECTOR, "[data-test-id='occupancy-report-patient-search-input']")
    BTN_REFRESH = (By.CSS_SELECTOR, "[data-test-id='occupancy-report-refresh-btn']")
    BTN_EXPORT_EXCEL = (By.CSS_SELECTOR, "[data-test-id='occupancy-report-export-excel-btn']")

    # Content
    FLOOR_BLOCKS = (By.CSS_SELECTOR, ".floor-block")
    LOADING_CARD = (By.XPATH, "//div[contains(@class, 'state-card') and contains(., 'تحميل')]")

    def open(self) -> "OccupancyReportPage":
        logger.info(f"Opening Occupancy Report: {self.URL}")
        self.driver.get(self.URL)
        self.wait_for_data_loaded()
        return self

    def is_loaded(self) -> bool:
        """Verifies report header is displayed."""
        return self.is_visible(self.HEADER_TITLE, timeout=10)

    def wait_for_data_loaded(self, timeout: int = 25) -> bool:
        """Waits for loading state to finish and floor blocks or KPI cards to be visible."""
        logger.info("Waiting for occupancy data to load...")
        start_time = time.time()
        while time.time() - start_time < timeout:
            # Check if KPI total beds has a non-empty number
            if self.is_visible(self.STAT_TOTAL_BEDS, timeout=2):
                val = self.get_text(self.STAT_TOTAL_BEDS)
                if val and val.isdigit() and int(val) > 0:
                    logger.info(f"Occupancy data loaded successfully: total beds = {val}")
                    return True
            time.sleep(1)
        return False

    def get_kpi_summary(self) -> dict:
        """Returns the high-level hospital occupancy KPI dictionary."""
        return {
            "total_beds": self.get_text(self.STAT_TOTAL_BEDS) if self.is_visible(self.STAT_TOTAL_BEDS, timeout=3) else "",
            "occupied_beds": self.get_text(self.STAT_OCCUPIED_BEDS) if self.is_visible(self.STAT_OCCUPIED_BEDS, timeout=3) else "",
            "available_beds": self.get_text(self.STAT_AVAILABLE_BEDS) if self.is_visible(self.STAT_AVAILABLE_BEDS, timeout=3) else "",
            "occupancy_rate": self.get_text(self.STAT_OCCUPANCY_PCT) if self.is_visible(self.STAT_OCCUPANCY_PCT, timeout=3) else ""
        }

    def get_floors_count(self) -> int:
        """Returns the number of floor sections rendered."""
        elements = self.driver.find_elements(*self.FLOOR_BLOCKS)
        return len(elements)

    def search_query(self, text: str) -> None:
        """Types query into the patient/room/doctor search input."""
        logger.info(f"Searching occupancy report for: '{text}'")
        self.type_text(self.INPUT_SEARCH, text)
        time.sleep(1)

    def toggle_empty_only(self) -> None:
        """Toggles the 'الغرف الفارغة فقط' checkbox."""
        logger.info("Toggling 'الغرف الفارغة فقط' checkbox...")
        self.click(self.CHECKBOX_EMPTY_ONLY)
        time.sleep(1)

    def toggle_active_rooms_only(self) -> None:
        """Toggles the 'إخفاء الغرف الموقوف التسكين بها' checkbox."""
        logger.info("Toggling 'إخفاء الغرف الموقوف التسكين بها' checkbox...")
        self.click(self.CHECKBOX_ACTIVE_ROOMS_ONLY)
        time.sleep(1)

    def click_refresh(self) -> None:
        """Clicks the Refresh button."""
        logger.info("Clicking Refresh button in Occupancy Report...")
        self.click(self.BTN_REFRESH)
        time.sleep(2)
        self.wait_for_data_loaded(timeout=20)
