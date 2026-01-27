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

    def find_credentials_file(self, profile: str = "default", filename: str = 'credentials.json') -> str:
        """Find credentials file by checking multiple locations."""
        search_paths = [
            # 1. Explicit profile directory
            os.path.join(self.get_config_dir(profile), filename),
            # 2. Environment variable (only for credentials.json)
            os.getenv('GOOGLE_PERSONAL_CREDENTIALS') if filename == 'credentials.json' else None,
            # 3. Legacy location (backwards compatibility)
            os.path.join(os.path.expanduser(f'~/.google-personal-mcp'), filename),
            # 4. Current working directory
            os.path.join(os.getcwd(), filename),
        ]

        for path in search_paths:
            if path and os.path.exists(path):
                return path

        raise FileNotFoundError(f"{filename} not found for profile '{profile}'.")

    def get_credentials(self, profile: str = "default", scopes: List[str] = None) -> Credentials:
        """Authenticates and returns credentials for the given profile and scopes."""
        if scopes is None:
            # Default to a broad scope if none provided, or keep it minimal?
            # For now, let's assume the user knows what they want.
            scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file"]

        config_dir = self.get_config_dir(profile)
        token_path = os.path.join(config_dir, "token.json")
        
        creds = None
        if os.path.exists(token_path):
            try:
                # Load without forcing scopes, so we see what the token actually has
                creds = Credentials.from_authorized_user_file(token_path)
                if creds and not creds.has_scopes(scopes):
                    logger.info(f"Credentials exist but lack requested scopes: {scopes}. Triggering re-auth.")
                    creds = None
            except Exception as e:
                logger.warning(f"Failed to load or validate credentials from {token_path}: {e}")
                creds = None

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logger.debug(f"Refreshing token for profile '{profile}'...")
                creds.refresh(GoogleRequest())
            else:
                logger.info(f"Starting OAuth2 flow for profile '{profile}'...")
                credentials_path = self.find_credentials_file(profile, "credentials.json")
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, scopes)
                creds = flow.run_local_server(port=0)

            # Save the credentials
            with open(token_path, "w") as token:
                token.write(creds.to_json())
            logger.info(f"Token saved to: {token_path}")

        return creds
