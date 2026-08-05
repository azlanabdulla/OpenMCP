import os
import json
from pathlib import Path
from typing import Optional

CONFIG_DIR = Path.home() / ".openmcp"
CONFIG_FILE = CONFIG_DIR / "config.json"

def get_registry_url() -> str:
    return os.environ.get("OPENMCP_REGISTRY_URL", "http://localhost:8000/api/v1")

def load_config() -> dict:
    if not CONFIG_FILE.exists():
        return {}
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_config(config: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def set_token(token: str) -> None:
    config = load_config()
    config["access_token"] = token
    save_config(config)

def get_token() -> Optional[str]:
    return load_config().get("access_token")

def clear_token() -> None:
    config = load_config()
    if "access_token" in config:
        del config["access_token"]
        save_config(config)
