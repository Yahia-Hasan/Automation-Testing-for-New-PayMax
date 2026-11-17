import os
import json
from pathlib import Path
from typing import Any, Dict, Optional

def get_project_root() -> Path:
    """Returns the absolute Path of the project root directory."""
    # This file is in shared/python-utils/file_utils.py -> parent.parent.parent is root
    return Path(__file__).resolve().parent.parent.parent

def get_shared_dir() -> Path:
    """Returns the absolute Path of the shared directory."""
    return get_project_root() / "shared"

def get_config_dir() -> Path:
    """Returns the absolute Path of the shared/config directory."""
    return get_shared_dir() / "config"

def get_test_data_dir() -> Path:
    """Returns the absolute Path of the shared/test-data directory."""
    return get_shared_dir() / "test-data"

def load_json(file_path: Path | str) -> Dict[str, Any]:
    """Loads and returns JSON data from a file."""
    path = Path(file_path)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(file_path: Path | str, data: Any, indent: int = 2) -> None:
    """Saves data to a JSON file with utf-8 encoding."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)
