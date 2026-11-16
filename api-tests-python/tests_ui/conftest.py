import sys
from pathlib import Path
import pytest

# Ensure shared utilities and local pages are resolvable
root_dir = Path(__file__).resolve().parent.parent.parent
shared_utils = str(root_dir / "shared" / "python-utils")
api_python = str(root_dir / "api-tests-python")
if shared_utils not in sys.path:
    sys.path.insert(0, shared_utils)
if api_python not in sys.path:
    sys.path.insert(0, api_python)

from driver_factory import create_driver
from auth_manager import login_and_navigate_to_home

@pytest.fixture(scope="session")
def driver():
    """Session-scoped Chrome WebDriver using shared DriverFactory."""
    drv = create_driver()
    yield drv
    drv.quit()

@pytest.fixture(scope="session")
def auth_driver(driver):
    """
    Authenticates through the shared AuthManager legacy login bridge
    and returns a driver ready on the modern Angular application.
    """
    login_and_navigate_to_home(driver)
    return driver
