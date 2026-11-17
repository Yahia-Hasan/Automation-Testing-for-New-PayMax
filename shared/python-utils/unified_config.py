import os
from pathlib import Path
from dotenv import load_dotenv
from file_utils import get_config_dir, get_project_root

# Load central .env file from shared/config
env_file = get_config_dir() / ".env"
if env_file.exists():
    load_dotenv(env_file)

class UnifiedConfig:
    """Centralized configuration object for the entire automation framework."""
    
    # Root Paths
    PROJECT_ROOT = get_project_root()
    SHARED_DIR = PROJECT_ROOT / "shared"
    CONFIG_DIR = SHARED_DIR / "config"
    TEST_DATA_DIR = SHARED_DIR / "test-data"
    
    # URLs
    LEGACY_LOGIN_URL = os.getenv("LEGACY_LOGIN_URL", "http://196.218.246.250/sysadmin/login.aspx?macAdd=000000000000")
    LEGACY_BRANCH = os.getenv("LEGACY_BRANCH", "Ad Doqi")
    LEGACY_BRANCH_PAGE_URL = os.getenv("LEGACY_BRANCH_PAGE_URL", "http://196.218.246.250/sysAdmin/Home/frmSelectBranch.aspx")
    LEGACY_LANDING_URL = os.getenv("LEGACY_LANDING_URL", "http://196.218.246.250/sysAdmin/Home/frmLandingPage.aspx")
    
    SPA_BASE_URL = os.getenv("SPA_BASE_URL", "https://196.218.246.250:4040")
    NEW_SYSTEM_URL = os.getenv("NEW_SYSTEM_URL", "https://196.218.246.250:4040/home")
    FRONTEND_HOME_URL = os.getenv("FRONTEND_HOME_URL", "https://196.218.246.250:4040/home")
    FRONTEND_RECEPTION_URL = os.getenv("FRONTEND_RECEPTION_URL", "https://196.218.246.250:4040/reception")
    
    # Backend REST API
    BASE_URL = os.getenv("BAYMAX_BASE_URL", os.getenv("API_BASE_URL", "https://196.218.246.250:4040/Patients-Modern-BE")).rstrip("/")
    BAYMAX_BASE_URL = BASE_URL
    API_BASE_URL = BASE_URL
    
    # Credentials
    SYS_USERNAME = os.getenv("SYS_USERNAME", os.getenv("BAYMAX_USERNAME", "sysadmin"))
    SYS_PASSWORD = os.getenv("SYS_PASSWORD", os.getenv("BAYMAX_PASSWORD", "Ma3an2025"))
    USERNAME = SYS_USERNAME
    PASSWORD = SYS_PASSWORD
    
    # Timeouts & Wait settings
    TIMEOUT = int(os.getenv("BAYMAX_TIMEOUT", os.getenv("DEFAULT_TIMEOUT", "15")))
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "25"))
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "0"))
    EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "15"))
    
    # Browser
    BROWSER = os.getenv("BROWSER", "chrome")
    HEADLESS = os.getenv("HEADLESS", "true").lower() in ("true", "1", "yes")
    WINDOW_WIDTH = int(os.getenv("WINDOW_WIDTH", "1920"))
    WINDOW_HEIGHT = int(os.getenv("WINDOW_HEIGHT", "1080"))
    
    # Test entity IDs
    PATIENT_CODE = os.getenv("BAYMAX_PATIENT_CODE", "")
    VISIT_CODE = os.getenv("BAYMAX_VISIT_CODE", "")
    RESERVATION_ID = os.getenv("BAYMAX_RESERVATION_ID", "")
    EMERGENCY_ID = os.getenv("BAYMAX_EMERGENCY_ID", "")

Config = UnifiedConfig
settings = UnifiedConfig
