import sys
from pathlib import Path

# Add shared/python-utils to sys.path
SHARED_UTILS = Path(__file__).resolve().parent.parent.parent / "shared" / "python-utils"
if str(SHARED_UTILS) not in sys.path:
    sys.path.insert(0, str(SHARED_UTILS))

from auth_manager import login_and_navigate_to_home

__all__ = ["login_and_navigate_to_home"]
