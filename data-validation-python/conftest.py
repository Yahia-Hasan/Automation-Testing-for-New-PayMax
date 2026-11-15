import pytest
from utils.driver_factory import create_driver
from utils.auth import login_and_navigate_to_home

@pytest.fixture(scope="session")
def driver():
    """Session-scoped or function-scoped driver fixture."""
    driver_instance = create_driver()
    yield driver_instance
    driver_instance.quit()

@pytest.fixture(scope="session")
def authenticated_driver(driver):
    """Logs in and navigates to the new system home once per session."""
    login_and_navigate_to_home(driver)
    return driver

