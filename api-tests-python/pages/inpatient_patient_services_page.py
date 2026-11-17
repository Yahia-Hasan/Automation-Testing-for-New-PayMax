import time
import logging
from typing import Optional, List, Dict
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger("BayMaxInpatientPatientServicesPage")

class InpatientPatientServicesPage(BasePage):
    """
    Page Object for Inpatient Patient Services (/waiting-list/patient-services).
    Allows adding and managing services (Lab, Rays, Blood Bank, Procedures, Medications, Diets).
    """

    # Service Form Controls
    SELECT_GROUP = (By.CSS_SELECTOR, "[data-test-id='patient-services-group-select']")
    INPUT_SHORT_CODE = (By.CSS_SELECTOR, "[data-test-id='patient-services-short-code-input']")
    SELECT_SERVICE = (By.CSS_SELECTOR, "[data-test-id='patient-services-service-select']")
    INPUT_APPROVAL = (By.CSS_SELECTOR, "[data-test-id='patient-services-client-approval-number-input']")
    SELECT_DOCTOR = (By.CSS_SELECTOR, "[data-test-id='patient-services-doctor-select']")
    SELECT_TECHNICIAN = (By.CSS_SELECTOR, "[data-test-id='patient-services-technician-select']")
    INPUT_QUANTITY = (By.CSS_SELECTOR, "[data-test-id='patient-services-quantity-input']")
    INPUT_UNIT_PRICE = (By.CSS_SELECTOR, "[data-test-id='patient-services-unit-price-input']")
    TEXTAREA_NOTES = (By.CSS_SELECTOR, "[data-test-id='patient-services-notes-textarea']")

    # Action Buttons
    BTN_ADD = (By.CSS_SELECTOR, "[data-test-id='patient-services-add-btn']")
    BTN_SAVE = (By.CSS_SELECTOR, "[data-test-id='patient-services-save-btn']")
    BTN_NEW = (By.CSS_SELECTOR, "[data-test-id='patient-services-new-btn']")
    BTN_CLAIM = (By.CSS_SELECTOR, "[data-test-id='patient-services-claim-btn']")
    BTN_FAVORITES = (By.CSS_SELECTOR, "[data-test-id='patient-services-favorites-btn']")

    # Service Categories / Filter Tabs
    TAB_ALL = (By.CSS_SELECTOR, "[data-test-id='patient-services-all-tab-btn']")
    TAB_LAB = (By.CSS_SELECTOR, "[data-test-id='patient-services-lab-tab-btn']")
    TAB_RAYS = (By.CSS_SELECTOR, "[data-test-id='patient-services-rays-tab-btn']")
    TAB_BLOOD = (By.CSS_SELECTOR, "[data-test-id='patient-services-blood-tab-btn']")
    TAB_PROCEDURES = (By.CSS_SELECTOR, "[data-test-id='patient-services-procedures-tab-btn']")
    TAB_MEDICATIONS = (By.CSS_SELECTOR, "[data-test-id='patient-services-medications-tab-btn']")
    TAB_DIETS = (By.CSS_SELECTOR, "[data-test-id='patient-services-diets-tab-btn']")

    # Tables
    TABLES = (By.CSS_SELECTOR, "table.svc-table, table.req-table, table")


    def open_with_tokens(self, reserv_token: str, accom_token: str) -> "InpatientPatientServicesPage":
        """Opens the patient services page with given encrypted reservation and accommodation tokens."""
        url = f"https://196.218.246.250:4040/waiting-list/patient-services?ReservID={reserv_token}&AccomID={accom_token}&typ=1&flag=All"
        logger.info(f"Opening Inpatient Patient Services: {url[:100]}...")
        self.driver.get(url)
        time.sleep(3)
        return self

    def is_loaded(self) -> bool:
        """Checks if the services form has loaded."""
        return self.is_visible(self.SELECT_GROUP, timeout=12) or self.is_visible(self.BTN_ADD, timeout=12)

    def select_service_group(self, group_name: str) -> None:
        """Selects service group (e.g. 'معمل', 'أشعة', 'بنك دم') in ng-select."""
        logger.info(f"Selecting service group: {group_name}")
        self.select_ng_option(self.SELECT_GROUP, group_name)
        time.sleep(1)

    def enter_short_code(self, code: str) -> None:
        """Enters service short code."""
        logger.info(f"Entering short code: {code}")
        self.type_text(self.INPUT_SHORT_CODE, code)

    def enter_notes(self, notes: str) -> None:
        """Enters notes in textarea."""
        logger.info(f"Entering notes: {notes}")
        self.type_text(self.TEXTAREA_NOTES, notes)

    def switch_category_tab(self, category: str) -> bool:
        """Switches between category tabs: 'all', 'lab', 'rays', 'blood', 'procedures', 'medications', 'diets'."""
        tab_map = {
            "all": self.TAB_ALL,
            "lab": self.TAB_LAB,
            "rays": self.TAB_RAYS,
            "blood": self.TAB_BLOOD,
            "procedures": self.TAB_PROCEDURES,
            "medications": self.TAB_MEDICATIONS,
            "diets": self.TAB_DIETS,
        }
        locator = tab_map.get(category.lower())
        if not locator or not self.is_visible(locator, timeout=3):
            logger.info(f"Category tab {category} not available or visible.")
            return False

        logger.info(f"Switching category tab to: {category}")
        tab_elem = self.find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tab_elem)
        time.sleep(0.3)
        self.click(locator)
        time.sleep(1)
        return True

    def click_favorites(self) -> None:
        """Clicks favorites button."""
        logger.info("Clicking favorites button...")
        if self.is_visible(self.BTN_FAVORITES, timeout=3):
            self.click(self.BTN_FAVORITES)
            time.sleep(1)

    def click_new(self) -> None:
        """Clicks 'جديد' button to reset service inputs."""
        logger.info("Clicking new service button...")
        if self.is_visible(self.BTN_NEW, timeout=3):
            self.click(self.BTN_NEW)
            time.sleep(1)

    def get_tables_count(self, timeout: int = 10) -> int:
        """Returns total tables rendered on the services screen."""
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.TABLES)
            )
        except Exception:
            pass
        return len(self.find_all(self.TABLES, timeout=3))

