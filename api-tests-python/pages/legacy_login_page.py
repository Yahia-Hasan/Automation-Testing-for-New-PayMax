import time
import logging
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger("BayMaxLoginPage")

class LegacyLoginPage(BasePage):
    """Page object representing the legacy WebForms authentication portal."""

    LEGACY_LOGIN_URL = "http://196.218.246.250/sysadmin/login.aspx?macAdd=000000000000"
    MODERN_HOME_URL = "https://196.218.246.250:4040/home"

    # Locators
    BTN_WORKSPACE_HOSPITAL = (By.ID, "btnWorkspaceHospital")
    INPUT_USERNAME = (By.ID, "txtInvUserName")
    INPUT_PASSWORD = (By.ID, "txtInvPassword")
    BTN_LOGIN = (By.ID, "btnLogin")
    INPUT_BRANCH_COMBO = (By.ID, "ddlBranches_Input")
    BTN_BRANCH_ARROW = (By.ID, "ddlBranches_Arrow")
    BTN_CONTINUE = (By.ID, "btnContinue")

    def open(self) -> "LegacyLoginPage":
        logger.info(f"Opening legacy login portal: {self.LEGACY_LOGIN_URL}")
        self.driver.get(self.LEGACY_LOGIN_URL)
        time.sleep(2)
        return self

    def select_hospital_workspace(self) -> "LegacyLoginPage":
        try:
            if self.is_visible(self.BTN_WORKSPACE_HOSPITAL, timeout=3):
                logger.info("Clicking on 'Hospital' workspace card...")
                self.click(self.BTN_WORKSPACE_HOSPITAL)
                time.sleep(2)
        except Exception as e:
            logger.info(f"Hospital workspace already selected or not shown: {e}")
        return self

    def enter_credentials(self, username: str = "sysadmin", password: str = "Ma3an2025") -> "LegacyLoginPage":
        logger.info(f"Entering credentials for: {username}")
        self.type_text(self.INPUT_USERNAME, username)
        self.type_text(self.INPUT_PASSWORD, password)
        logger.info("Clicking Log in...")
        self.click(self.BTN_LOGIN)
        time.sleep(3)
        return self

    def select_branch(self, branch_name: str = "Ad Doqi") -> "LegacyLoginPage":
        logger.info(f"Selecting branch '{branch_name}' via Telerik RadComboBox...")
        try:
            self.driver.execute_script(f"""
                var combo = $find('ddlBranches');
                if (combo) {{
                    var item = combo.findItemByText('{branch_name}') || combo.get_items().getItem(0);
                    if (item) item.select();
                }}
            """)
        except Exception:
            # Fallback to UI click
            if self.is_visible(self.BTN_BRANCH_ARROW, timeout=3):
                self.click(self.BTN_BRANCH_ARROW)
                time.sleep(1)
                item_loc = (By.XPATH, f"//li[contains(text(), '{branch_name}')]")
                self.click(item_loc)

        time.sleep(1)
        logger.info("Clicking 'متابعة' on branch page...")
        self.click(self.BTN_CONTINUE)
        time.sleep(4)
        return self

    def navigate_to_modern_home(self) -> "LegacyLoginPage":
        logger.info(f"Navigating to modern Angular portal: {self.MODERN_HOME_URL}")
        self.driver.get(self.MODERN_HOME_URL)
        time.sleep(4)
        self.wait_for_url_contains(":4040/home", timeout=15)
        logger.info(f"Successfully reached modern home: {self.driver.current_url}")
        return self

    def login_full_flow(
        self,
        username: str = "sysadmin",
        password: str = "Ma3an2025",
        branch_name: str = "Ad Doqi"
    ) -> "LegacyLoginPage":
        """Executes the complete legacy login bridge into the modern system."""
        (
            self.open()
            .select_hospital_workspace()
            .enter_credentials(username, password)
            .select_branch(branch_name)
            .navigate_to_modern_home()
        )
        return self
