import os
import time
import json
import logging
from typing import Dict, Any, Optional
import requests
import urllib3
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from unified_config import UnifiedConfig
from driver_factory import create_driver
from file_utils import get_project_root

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("AuthManager")


def login_and_navigate_to_home(
    driver: WebDriver,
    timeout: int = UnifiedConfig.DEFAULT_TIMEOUT,
    username: str = UnifiedConfig.SYS_USERNAME,
    password: str = UnifiedConfig.SYS_PASSWORD,
    branch_name: str = UnifiedConfig.LEGACY_BRANCH
) -> None:
    """
    Executes the complete legacy login bridge into the modern Hospital system:
    1. Opens legacy login URL (port 80)
    2. Clicks 'btnWorkspaceHospital'
    3. Enters credentials (sysadmin/Ma3an2025) and clicks 'btnLogin'
    4. Selects branch in Telerik RadComboBox (Ad Doqi) and clicks 'btnContinue'
    5. Navigates to modern system URL (https://...:4040/home)
    6. Waits for Angular top-navbar to ensure full hydration
    """
    wait = WebDriverWait(driver, timeout)

    logger.info(f"Navigating to Legacy Login: {UnifiedConfig.LEGACY_LOGIN_URL}")
    driver.get(UnifiedConfig.LEGACY_LOGIN_URL)

    # Step 1: Click Hospital Workspace button
    try:
        btn_hospital = wait.until(
            EC.element_to_be_clickable((By.ID, "btnWorkspaceHospital")),
            message="Timed out waiting for btnWorkspaceHospital"
        )
        driver.execute_script("arguments[0].click();", btn_hospital)
    except Exception as e:
        logger.info(f"Workspace button already bypassed or not present: {e}")

    try:
        wait.until(EC.invisibility_of_element_located((By.ID, "pnlWorkspace")))
    except Exception:
        pass

    # Step 2: Enter credentials
    user_input = wait.until(EC.element_to_be_clickable((By.ID, "txtInvUserName")))
    pass_input = wait.until(EC.element_to_be_clickable((By.ID, "txtInvPassword")))
    btn_login = wait.until(EC.element_to_be_clickable((By.ID, "btnLogin")))

    user_input.clear()
    user_input.send_keys(username)
    pass_input.clear()
    pass_input.send_keys(password)
    driver.execute_script("arguments[0].click();", btn_login)

    # Step 3: Wait for Branch selection page
    logger.info("Waiting for branch selection page...")
    wait.until(
        lambda d: "frmSelectBranch" in d.current_url or "SelectBranch" in d.current_url,
        message="Timed out waiting for branch selection page"
    )

    try:
        driver.execute_script(f"""
            var combo = (typeof $find === 'function') ? $find('ddlBranches') : null;
            if (combo) {{
                var item = combo.findItemByText('{branch_name}') || combo.get_items().getItem(0);
                if (item) item.select();
            }}
        """)
    except Exception as e:
        logger.warning(f"Telerik combo selection script: {e}")

    time.sleep(1)
    btn_continue = wait.until(EC.element_to_be_clickable((By.ID, "btnContinue")))
    driver.execute_script("arguments[0].click();", btn_continue)

    # Step 4: Wait for landing page and session cookies
    logger.info("Waiting for legacy landing page...")
    wait.until(
        lambda d: "frmLandingPage.aspx" in d.current_url or "SelectBranch" not in d.current_url,
        message="Waiting for postback to landing page"
    )
    time.sleep(2)

    # Step 5: Navigate to modern system
    logger.info(f"Navigating to Modern System: {UnifiedConfig.NEW_SYSTEM_URL}")
    driver.get(UnifiedConfig.NEW_SYSTEM_URL)

    # Wait for Angular URL and top navbar/layout
    wait.until(
        lambda d: ":4040" in d.current_url,
        message="Timed out waiting for new system URL on port 4040"
    )
    time.sleep(3)
    logger.info("Successfully reached modern hospital system.")


def extract_baymax_token(driver: WebDriver) -> Optional[str]:
    """Extracts JWT token from localStorage or sessionStorage."""
    token = driver.execute_script("""
        return window.localStorage.getItem('baymax_token') 
            || window.localStorage.getItem('token')
            || window.sessionStorage.getItem('baymax_token')
            || window.sessionStorage.getItem('token');
    """)
    return token


class BayMaxSeleniumAuth:
    """Class wrapper for backward compatibility with baymax-api-automation."""

    def __init__(self, headless: bool = True):
        self.headless = headless
        self.driver = create_driver(headless=self.headless)
        self.cookies: Dict[str, Any] = {}
        self.token: Optional[str] = None

    def perform_full_login(
        self,
        username: str = UnifiedConfig.SYS_USERNAME,
        password: str = UnifiedConfig.SYS_PASSWORD,
        branch_name: str = UnifiedConfig.LEGACY_BRANCH
    ) -> Dict[str, Any]:
        try:
            login_and_navigate_to_home(
                self.driver,
                username=username,
                password=password,
                branch_name=branch_name
            )
            time.sleep(2)
            self.token = extract_baymax_token(self.driver)
            
            # Extract cookies
            raw_cookies = self.driver.get_cookies()
            self.cookies = {c["name"]: c["value"] for c in raw_cookies}

            result = {
                "success": bool(self.token),
                "current_url": self.driver.current_url,
                "token": self.token,
                "cookies": self.cookies
            }

            # Cache session to shared root session.json
            session_file = get_project_root() / "shared" / "config" / "session.json"
            try:
                session_file.parent.mkdir(parents=True, exist_ok=True)
                with open(session_file, "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2)
            except Exception as e:
                logger.warning(f"Could not write session file: {e}")

            return result
        except Exception as e:
            logger.error(f"Selenium login failed: {e}")
            return {"success": False, "error": str(e), "token": None, "cookies": {}}

    def close(self):
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass


def get_authenticated_token(force_refresh: bool = False) -> str:
    """
    Returns a valid Bearer JWT token:
    1. Tries reading cached token from shared/config/session.json (or local session.json).
    2. Validates against /api/auth/me endpoint.
    3. If invalid/expired/missing, performs headless Selenium login bridge.
    """
    session_paths = [
        get_project_root() / "shared" / "config" / "session.json",
        get_project_root() / "session.json",
        Path("session.json")
    ]

    token = None
    if not force_refresh:
        for p in session_paths:
            if p.exists():
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        token = data.get("token")
                        if token:
                            break
                except Exception:
                    pass

    # Validate token if found
    if token:
        try:
            url = f"{UnifiedConfig.BASE_URL}/api/auth/me"
            res = requests.get(
                url,
                headers={"Authorization": f"Bearer {token}"},
                timeout=5,
                verify=False
            )
            if res.status_code == 200:
                logger.info("Cached JWT token is valid.")
                return token
            logger.info("Cached token expired or unauthorized. Refreshing...")
        except Exception as e:
            logger.warning(f"Token validation check failed: {e}")

    # Launch bridge
    logger.info("Launching headless Selenium bridge to acquire fresh JWT token...")
    auth = BayMaxSeleniumAuth(headless=True)
    try:
        res = auth.perform_full_login()
        token = res.get("token")
    finally:
        auth.close()

    if not token:
        raise RuntimeError("Failed to acquire JWT token via Selenium authentication bridge.")

    return token
