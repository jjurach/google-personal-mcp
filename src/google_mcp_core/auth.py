import os
import json
import logging
from typing import List, Optional
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

logger = logging.getLogger(__name__)

class AuthManager:
    def __init__(self, app_name: str = "google-personal-mcp"):
        self.app_name = app_name

    def get_config_dir(self, profile: str = "default") -> str:
        """Returns the configuration directory for a given profile."""
        base_dir = os.getenv('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
        config_dir = os.path.join(base_dir, self.app_name, "profiles", profile)
        os.makedirs(config_dir, exist_ok=True)
        return config_dir

    def get_credentials_path(self, profile: str = "default") -> str:
        """Get the path to credentials.json for a profile."""
        config_dir = self.get_config_dir(profile)
        path = os.path.join(config_dir, "credentials.json")

        if not os.path.exists(path):
            raise FileNotFoundError(
                f"credentials.json not found for profile '{profile}'.\n"
                f"Expected location: {path}\n"
                f"Place your OAuth 2.0 credentials file there and try again."
            )
        return path

    def get_token_path(self, profile: str = "default") -> str:
        """Get the path to token.json for a profile."""
        config_dir = self.get_config_dir(profile)
        return os.path.join(config_dir, "token.json")

    def get_credentials(self, profile: str = "default", scopes: List[str] = None) -> Credentials:
        """Get Google API credentials for the given profile and scopes.

        Args:
            profile: Profile name (default: "default")
            scopes: List of OAuth scopes to request

        Returns:
            google.oauth2.credentials.Credentials object

        Raises:
            FileNotFoundError: If credentials.json is not found in the profile directory
        """
        if scopes is None:
            scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

        token_path = self.get_token_path(profile)

        creds = None
        if os.path.exists(token_path):
            try:
                creds = Credentials.from_authorized_user_file(token_path)
                if creds and not creds.has_scopes(scopes):
                    logger.info(f"Token exists but lacks required scopes. Re-authenticating for profile '{profile}'...")
                    creds = None
            except Exception as e:
                logger.warning(f"Failed to load token from {token_path}: {e}")
                creds = None

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logger.debug(f"Refreshing token for profile '{profile}'...")
                creds.refresh(GoogleRequest())
            else:
                logger.info(f"Starting OAuth2 authentication for profile '{profile}'...")
                credentials_path = self.get_credentials_path(profile)
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, scopes)
                creds = flow.run_local_server(port=0)

            # Save token to profile directory
            with open(token_path, "w") as f:
                f.write(creds.to_json())
            logger.info(f"Authorization token saved to: {token_path}")

        return creds
