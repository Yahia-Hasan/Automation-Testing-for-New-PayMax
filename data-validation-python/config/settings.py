import sys
from pathlib import Path

# Add shared/python-utils to sys.path
SHARED_UTILS = Path(__file__).resolve().parent.parent.parent / "shared" / "python-utils"
if str(SHARED_UTILS) not in sys.path:
    sys.path.insert(0, str(SHARED_UTILS))

from unified_config import UnifiedConfig as settings

LEGACY_LOGIN_URL = settings.LEGACY_LOGIN_URL
NEW_SYSTEM_URL = settings.NEW_SYSTEM_URL
SPA_BASE_URL = settings.SPA_BASE_URL
SYS_USERNAME = settings.SYS_USERNAME
SYS_PASSWORD = settings.SYS_PASSWORD
DEFAULT_TIMEOUT = settings.DEFAULT_TIMEOUT
HEADLESS = settings.HEADLESS
WINDOW_WIDTH = settings.WINDOW_WIDTH
WINDOW_HEIGHT = settings.WINDOW_HEIGHT

__all__ = [
    "settings",
    "LEGACY_LOGIN_URL",
    "NEW_SYSTEM_URL",
    "SPA_BASE_URL",
    "SYS_USERNAME",
    "SYS_PASSWORD",
    "DEFAULT_TIMEOUT",
    "HEADLESS",
    "WINDOW_WIDTH",
    "WINDOW_HEIGHT"
]
