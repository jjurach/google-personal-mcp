import os
import json
import logging
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class ResourceConfig(BaseModel):
    id: str
    profile: str = "default"
    description: Optional[str] = None

class AppConfig(BaseModel):
    sheets: Dict[str, ResourceConfig] = Field(default_factory=dict)
    drive_folders: Dict[str, ResourceConfig] = Field(default_factory=dict)

class ConfigManager:
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._get_default_config_path()
        self.config = self._load_config()

    def _get_default_config_path(self) -> str:
        base_dir = os.getenv('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
        return os.path.join(base_dir, 'google-personal-mcp', 'config.json')

    def _load_config(self) -> AppConfig:
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    data = json.load(f)
                return AppConfig(**data)
            except Exception as e:
                logger.error(f"Failed to load config from {self.config_path}: {e}")
                return AppConfig()
        else:
            return AppConfig()

    def get_sheet_resource(self, alias: str) -> ResourceConfig:
        if alias in self.config.sheets:
            return self.config.sheets[alias]
        raise ValueError(f"Access Denied: Sheet alias '{alias}' not found in configuration.")

    def get_folder_resource(self, alias: str) -> ResourceConfig:
        if alias in self.config.drive_folders:
            return self.config.drive_folders[alias]
        raise ValueError(f"Access Denied: Folder alias '{alias}' not found in configuration.")

    def get_allowed_folder_ids(self, profile_name: Optional[str] = None) -> List[str]:
        """Returns folder IDs, optionally filtered by profile."""
        if profile_name:
            return [r.id for r in self.config.drive_folders.values() if r.profile == profile_name]
        return [r.id for r in self.config.drive_folders.values()]

    def save_config(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            f.write(self.config.model_dump_json(indent=2))
