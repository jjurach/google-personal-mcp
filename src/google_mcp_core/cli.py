"""Command-line interface for Google Personal MCP Server.

Provides tools for managing Google Drive, Sheets, and authentication profiles.
"""

import logging
from cyclopts import App
from datetime import datetime

from google_mcp_core.context import GoogleContext
from google_mcp_core.sheets import SheetsService
from google_mcp_core.drive import DriveService
from google_mcp_core.config import ConfigManager

# Suppress noisy google discovery logs
logging.getLogger("googleapiclient.discovery_cache").setLevel(logging.ERROR)
logging.basicConfig(level=logging.WARNING, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = App(help_format="markdown")
config_manager = ConfigManager()


# --- Configuration Commands ---

config_app = App()


@config_app.command
def list_sheets(profile: str = "default"):
    """List all configured Google Sheets for a profile."""
    sheets = config_manager.list_sheets(profile)

    if not sheets:
        print(f"No configured sheets for profile '{profile}'")
        return

    print(f"\n📊 Configured Sheets (profile: {profile})")
    print("-" * 80)
    print(f"{'Alias':<20} {'Spreadsheet ID':<45} {'Description'}")
    print("-" * 80)

    for alias, config in sheets.items():
        desc = config.description or "(no description)"
        print(f"{alias:<20} {config.id:<45} {desc}")


@config_app.command
def list_folders(profile: str = "default"):
    """List all configured Google Drive folders for a profile."""
    folders = config_manager.list_folders(profile)

    if not folders:
        print(f"No configured folders for profile '{profile}'")
        return

    print(f"\n📁 Configured Folders (profile: {profile})")
    print("-" * 80)
    print(f"{'Alias':<20} {'Folder ID':<45} {'Description'}")
    print("-" * 80)

    for alias, config in folders.items():
        desc = config.description or "(no description)"
        print(f"{alias:<20} {config.id:<45} {desc}")


# --- Drive Commands ---

drive_app = App()


@drive_app.command
def list_all_files(profile: str = "default"):
    """List all files in Google Drive for a profile.

    Requests broader scopes to see all files, not just those created by the app.
    """
    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive.readonly",
        ]
        context = GoogleContext(profile=profile, scopes=scopes)
        service = DriveService(context)

        print(f"\n📂 All Drive Files (profile: {profile})")
        print("-" * 100)
        files = service.list_all_files()

        if not files:
            print("No files found.")
            return

        print(f"{'ID':<35} {'Type':<40} {'Name'}")
        print("-" * 100)
        for f in files:
            mtype = f.get("mimeType", "unknown")
            mtype = mtype.replace("application/vnd.google-apps.", "g:")
            print(f"{f['id']:<35} {mtype:<40} {f['name']}")

    except Exception as e:
        print(f"Error: {e}")


@drive_app.command
def list_files(folder_alias: str, profile: str = "default"):
    """List files in a configured Google Drive folder."""
    try:
        folder_config = config_manager.get_folder_resource(folder_alias)
        context = GoogleContext(profile=profile)
        allowed_ids = config_manager.get_allowed_folder_ids(profile)
        service = DriveService(context, allowed_folder_ids=allowed_ids)

        print(f"\n📁 Files in '{folder_alias}' (profile: {profile})")
        print("-" * 100)
        files = service.list_files(folder_config.id)

        if not files:
            print("No files found.")
            return

        print(f"{'ID':<35} {'Type':<40} {'Name'}")
        print("-" * 100)
        for f in files:
            mtype = f.get("mimeType", "unknown")
            mtype = mtype.replace("application/vnd.google-apps.", "g:")
            print(f"{f['id']:<35} {mtype:<40} {f['name']}")

    except Exception as e:
        print(f"Error: {e}")


# --- Sheets Commands ---

sheets_app = App()


@sheets_app.command
def list_tabs(sheet_alias: str, profile: str = "default"):
    """List all tabs (sheets) within a configured spreadsheet."""
    try:
        sheet_config = config_manager.get_sheet_resource(sheet_alias)
        context = GoogleContext(profile=profile)
        service = SheetsService(context)

        print(f"\n📊 Tabs in '{sheet_alias}' (profile: {profile})")
        print("-" * 50)
        tabs = service.list_sheet_titles(sheet_config.id)

        if not tabs:
            print("No tabs found.")
            return

        for i, tab in enumerate(tabs, 1):
            print(f"{i}. {tab}")

    except Exception as e:
        print(f"Error: {e}")


@sheets_app.command
def get_status(sheet_alias: str, range_name: str = "README!A1", profile: str = "default"):
    """Get the status (values) of a sheet range."""
    try:
        sheet_config = config_manager.get_sheet_resource(sheet_alias)
        context = GoogleContext(profile=profile)
        service = SheetsService(context)

        print(f"\n📋 Status from '{sheet_alias}' {range_name} (profile: {profile})")
        print("-" * 80)
        values = service.read_range(sheet_config.id, range_name)

        if not values:
            print("No data found.")
            return

        for row in values:
            print(row)

    except Exception as e:
        print(f"Error: {e}")


@sheets_app.command
def get_prompts(sheet_alias: str, sheet_tab_name: str, profile: str = "default"):
    """Get all prompts from a sheet tab."""
    try:
        sheet_config = config_manager.get_sheet_resource(sheet_alias)
        context = GoogleContext(profile=profile)
        service = SheetsService(context)

        print(f"\n💭 Prompts from '{sheet_alias}' - {sheet_tab_name} (profile: {profile})")
        print("-" * 100)

        range_name = f"{sheet_tab_name}!A:F"
        raw_values = service.read_range(sheet_config.id, range_name)

        if not raw_values:
            print("No prompts found.")
            return

        headers = [
            "Name",
            "Content",
            "Created By",
            "Created At",
            "Last Modified By",
            "Last Modified At",
        ]

        # Print header
        print(f"{'Name':<25} {'Content':<50} {'Created By':<15}")
        print("-" * 100)

        for row in raw_values[1:]:
            name = row[0] if len(row) > 0 else ""
            content = row[1] if len(row) > 1 else ""
            author = row[2] if len(row) > 2 else ""

            # Truncate content for display
            content_display = (content[:47] + "...") if len(content) > 50 else content

            print(f"{name:<25} {content_display:<50} {author:<15}")

    except Exception as e:
        print(f"Error: {e}")


@sheets_app.command
def insert_prompt(
    sheet_alias: str,
    sheet_tab_name: str,
    prompt_name: str,
    content: str,
    author: str = "CLI User",
    profile: str = "default",
):
    """Insert a prompt into a sheet tab."""
    try:
        sheet_config = config_manager.get_sheet_resource(sheet_alias)
        context = GoogleContext(profile=profile)
        service = SheetsService(context)

        timestamp = datetime.now().isoformat()
        values = [prompt_name, content, author, timestamp, author, timestamp]
        service.insert_row_at_top(sheet_config.id, sheet_tab_name, values)

        print(f"✅ Prompt inserted successfully into '{sheet_alias}' - {sheet_tab_name}")

    except Exception as e:
        print(f"Error: {e}")


# --- Root Commands ---

app.command(config_app, name="config")
app.command(drive_app, name="drive")
app.command(sheets_app, name="sheets")


def main():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
