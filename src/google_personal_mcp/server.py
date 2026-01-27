import os
import sys
import logging
import asyncio
from typing import List, Optional, Tuple
from mcp.server import FastMCP
from googleapiclient.errors import HttpError
from datetime import datetime

from google_mcp_core.context import GoogleContext
from google_mcp_core.sheets import SheetsService
from google_mcp_core.drive import DriveService
from google_mcp_core.config import ConfigManager

# Verbose logging setup
VERBOSE = os.getenv('GOOGLE_MCP_VERBOSE', '').lower() in ('1', 'true', 'yes')
logging.basicConfig(
    level=logging.DEBUG if VERBOSE else logging.WARNING,
    format='[%(levelname)s] %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

# Initialize Config
config_manager = ConfigManager()

# --- MCP Server ---
mcp = FastMCP("Google Personal MCP Server")

def get_sheets_service(alias: str) -> Tuple[SheetsService, str]:
    resource = config_manager.get_sheet_resource(alias)
    context = GoogleContext(profile=resource.profile)
    return SheetsService(context), resource.id

def get_drive_service(alias: str) -> Tuple[DriveService, str]:
    resource = config_manager.get_folder_resource(alias)
    context = GoogleContext(profile=resource.profile)
    # Important: The drive service should be restricted to IDs for THIS profile
    allowed_ids = config_manager.get_allowed_folder_ids(resource.profile)
    return DriveService(context, allowed_folder_ids=allowed_ids), resource.id

# --- Sheets Tools ---

@mcp.tool()
def list_sheets(sheet_alias: str) -> list[str]:
    """Lists all sheets (tabs) in a given spreadsheet identified by its alias."""
    try:
        service, spreadsheet_id = get_sheets_service(sheet_alias)
        return service.list_sheet_titles(spreadsheet_id)
    except Exception as e:
        return [f"Error: {str(e)}"]

@mcp.tool()
def get_sheet_status(sheet_alias: str, range_name: str = "README!A1") -> dict:
    """Gets the status (values) of a sheet range."""
    try:
        service, spreadsheet_id = get_sheets_service(sheet_alias)
        values = service.read_range(spreadsheet_id, range_name)
        return {"status": "success", "data": values}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
def insert_prompt(sheet_tab_name: str, prompt_name: str, content: str, sheet_alias: str, author: str = "Google MCP") -> dict:
    """Inserts a prompt into a specific sheet tab."""
    try:
        service, spreadsheet_id = get_sheets_service(sheet_alias)
        timestamp = datetime.now().isoformat()
        values = [prompt_name, content, author, timestamp, author, timestamp]
        service.insert_row_at_top(spreadsheet_id, sheet_tab_name, values)
        return {"status": "success", "message": "Prompt inserted successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
def get_prompts(sheet_tab_name: str, sheet_alias: str) -> dict:
    """Gets all prompts from a sheet tab."""
    try:
        service, spreadsheet_id = get_sheets_service(sheet_alias)
        range_name = f"{sheet_tab_name}!A:F"
        raw_values = service.read_range(spreadsheet_id, range_name)

        if not raw_values:
            return {"status": "success", "prompts": []}

        headers = ["Name", "Content", "Created By", "Created At", "Last Modified By", "Last Modified At"]
        prompts = []
        for row in raw_values[1:]:
            prompt_dict = {
                headers[i]: row[i] if i < len(row) else ""
                for i in range(len(headers))
            }
            prompts.append(prompt_dict)

        return {"status": "success", "prompts": prompts}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- Drive Tools ---

@mcp.tool()
def list_drive_files(folder_alias: str) -> dict:
    """Lists files in a configured Google Drive folder."""
    try:
        service, folder_id = get_drive_service(folder_alias)
        files = service.list_files(folder_id)
        return {"status": "success", "files": files}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
def upload_file(local_path: str, folder_alias: str, filename: Optional[str] = None) -> dict:
    """Uploads a local file to a configured Google Drive folder."""
    try:
        service, folder_id = get_drive_service(folder_alias)
        file = service.upload_file(local_path, folder_id, filename)
        return {"status": "success", "file_id": file.get('id'), "message": "Upload successful"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
def get_file_content(file_id: str, folder_alias: str) -> dict:
    """Downloads a file's content from a specific folder alias."""
    try:
        service, _ = get_drive_service(folder_alias)
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            service.download_file(file_id, tmp.name)
            return {"status": "success", "local_path": tmp.name, "message": "File downloaded."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
def delete_file(file_id: str, folder_alias: str) -> dict:
    """Deletes a file from Google Drive."""
    try:
        service, _ = get_drive_service(folder_alias)
        service.remove_file(file_id)
        return {"status": "success", "message": f"File {file_id} deleted."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

async def async_main():
    await mcp.run_stdio_async()

def main():
    import anyio
    anyio.run(async_main)

if __name__ == "__main__":
    main()
