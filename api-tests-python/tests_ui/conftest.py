import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.legacy_login_page import LegacyLoginPage

@pytest.fixture(scope="session")
def driver():
    """
    Session-scoped Chrome WebDriver.
    Controls visibility with HEADLESS env var (defaults to headless=True for automated runs).
    To see the browser live, run with: $env:HEADLESS="false"
    """
    is_headless = os.getenv("HEADLESS", "false").lower() in ("true", "1", "yes")

    options = Options()
    if is_headless:
        options.add_argument("--headless=new")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument("--disable-web-security")
    options.add_argument("--start-maximized")
    options.set_capability("acceptInsecureCerts", True)

    try:
        service = Service(ChromeDriverManager().install())
        drv = webdriver.Chrome(service=service, options=options)
    except Exception:
        drv = webdriver.Chrome(options=options)

    drv.maximize_window()

    drv.implicitly_wait(10)
    yield drv
    drv.quit()

@pytest.fixture(scope="session")
def auth_driver(driver):
    """
    Navigates through the legacy login portal, selects Ad Doqi branch,
    and returns a driver ready on the modern Angular application.
    """
    login_page = LegacyLoginPage(driver)
    login_page.login_full_flow(
        username="sysadmin",
        password="Ma3an2025",
        branch_name="Ad Doqi"
    )
    return driver
