# Google Sheets MCP Server

This subproject implements a Managed Code Project (MCP) server that interacts with Google Sheets to store and retrieve prompts and ideas. It allows MCP clients to manage textual content, including metadata like timestamps and authorship, across various sheets (tabs) in a specified Google Spreadsheet.

## Setup Instructions

1.  **Navigate to the project directory:**
    ```bash
    cd google-personal-mcp
    ```

2.  **Create and activate a virtual environment (if you haven't already):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    pip install -e ../external/fastmcp
    ```

## Google Sheets API Authentication

To allow the MCP server to interact with your Google Sheets, you need to set up Google Sheets API access and obtain `credentials.json`.

1.  **Enable the Google Sheets and Drive APIs:**
    *   Go to the [Google Cloud Console](https://console.cloud.google.com/).
    *   Create a new project or select an existing one.
    *   Navigate to "APIs & Services" > "Enabled APIs & Services".
    *   Search for "Google Sheets API" and enable it.
    *   Search for "Google Drive API" and enable it.

2.  **Create OAuth 2.0 Client IDs:**
    *   In the Google Cloud Console, go to "APIs & Services" > "Credentials".
    *   Click "CREATE CREDENTIALS" > "OAuth client ID".
    *   Choose "Desktop app" as the application type.
    *   Give it a name (e.g., "GoogleSheetsMCP").
    *   Click "CREATE".

3.  **Download `credentials.json`:**
    *   After creating the client ID, a dialog will appear with your client ID and client secret.
    *   Click "DOWNLOAD JSON" to save the `credentials.json` file.
    *   **Rename the downloaded file to `credentials.json`** and place it in one of the supported locations (see below).

    **Important:** `credentials.json` and the generated `token.json` (after the first successful authentication) are sensitive files and are already added to `.gitignore` to prevent them from being committed to your version control system.

## Credential File Locations

The server automatically searches for `credentials.json` and `token.json` in multiple locations (in priority order):

1. **Environment variable** (credentials.json only): `$GOOGLE_PERSONAL_CREDENTIALS`
2. **XDG config directory**: `~/.config/google-personal-mcp/credentials.json`
3. **Home directory**: `~/.google-personal-mcp/credentials.json`
4. **Current working directory**: `./credentials.json` (useful for development)
5. **Script installation directory**: Same directory as the installed script

You can place your `credentials.json` file in any of these locations. The recommended location for normal use is `~/.config/google-personal-mcp/credentials.json`.

**Example setup:**
```bash
mkdir -p ~/.config/google-personal-mcp
mv ~/Downloads/credentials.json ~/.config/google-personal-mcp/
```

**Using environment variable (optional):**
```bash
export GOOGLE_PERSONAL_CREDENTIALS=/path/to/your/credentials.json
```

## Verbose Logging

Enable verbose logging to see detailed information about credential file search, authentication, and API operations:

```bash
export GOOGLE_PERSONAL_MCP_VERBOSE=1
```

When verbose mode is enabled, the server will display:
- Which credential/token file location was used
- Authentication flow steps
- API operation details
- Debugging information for troubleshooting

To disable verbose logging:
```bash
export GOOGLE_PERSONAL_MCP_VERBOSE=0
# or simply unset the variable
unset GOOGLE_PERSONAL_MCP_VERBOSE
```

## Drive Tool & Diagnostics

The project includes a utility script `scripts/drive-tool.py` to help diagnose authentication issues and list files in your Google Drive. This tool is independent of the main MCP server but shares the same authentication profile (`default` by default).

**Usage:**
```bash
python3 scripts/drive-tool.py
```

**Features:**
*   **Lists all files:** It requests the `drive.readonly` scope to see *all* files in your Drive, not just those created by this app (unlike the main server which uses the restricted `drive.file` scope).
*   **Auto-Remediation:** If your current cached token (`token.json`) lacks the necessary permissions, the tool will automatically detect this and trigger a re-authentication flow. You will be prompted to visit a URL to authorize the broader scopes.
*   **Diagnostics:** Useful for verifying that your `credentials.json` is working and that the application can successfully talk to the Google Drive API. If this tool works but the server doesn't, the issue is likely in the server configuration or specific file restrictions.

## Running the MCP Server

The `fastmcp` server can be run directly.

1.  **Ensure your virtual environment is active:**
    ```bash
    source venv/bin/activate
    ```

2.  **Run the server:**
    ```bash
    python main.py
    ```
    The server will run in the foreground. You can stop it by pressing `Ctrl+C`.

The server will typically be accessible via a `fastmcp` client, which can then invoke the exposed tools.

## Configuring .gemini/settings.json

To use this MCP server with Gemini, add the following configuration to your `.gemini/settings.json` file:

```json
{
  "mcpServers": {
    "google-sheets": {
      "command": "google-personal-mcp",
      "args": [],
      "env": {}
    }
  }
}
```

**With verbose logging enabled:**
```json
{
  "mcpServers": {
    "google-sheets": {
      "command": "google-personal-mcp",
      "args": [],
      "env": {
        "GOOGLE_PERSONAL_MCP_VERBOSE": "1"
      }
    }
  }
}
```

**Notes:**
- Ensure the package is installed with `pip install -e .` so that the `google-personal-mcp` command is available in your PATH
- The `cwd` parameter is optional now - the server will automatically search for credentials in standard locations
- If you want to specify a custom credential location, use the `GOOGLE_PERSONAL_CREDENTIALS` environment variable in the `env` section

## Available Tools

The following tools are exposed by the `fastmcp` server:

*   **`list_sheets(spreadsheet_id: str = DEFAULT_SPREADSHEET_ID) -> list[str]`**: Lists all sheets (tabs) in a given spreadsheet.
*   **`create_sheet(new_sheet_name: str, spreadsheet_id: str = DEFAULT_SPREADSHEET_ID) -> dict`**: Creates a new sheet (tab) in a given spreadsheet.
*   **`get_sheet_status(spreadsheet_id: str = DEFAULT_SPREADSHEET_ID, range_name: str = "README!A1") -> dict`**: Gets the status of a sheet (reads data from a specified range).
*   **`insert_prompt(sheet_name: str, prompt_name: str, content: str, author: str = "Google Sheets MCP", spreadsheet_id: str = DEFAULT_SPREADSHEET_ID) -> dict`**: Inserts a prompt into a sheet.
*   **`get_prompts(sheet_name: str, spreadsheet_id: str = DEFAULT_SPREADSHEET_ID) -> dict`**: Gets all prompts from a sheet.
*   **`initialize_readme_sheet(spreadsheet_id: str = DEFAULT_SPREADSHEET_ID) -> dict`**: Initializes the "README" sheet with some default content.

These tools are designed to be invoked programmatically via a `fastmcp` client. For example, using a `fastmcp` client library in Python, you might call `client.tools.list_sheets()`.

## MCP Server Verification

### Simple Verification Test

For quick verification that your MCP server is working correctly, use this simple test prompt:

**Simple Test Prompt:**
```
Use the Google Sheets MCP tool to list all prompts from the 'Gemini Prompts' sheet. Just show me the raw data exactly as returned by the tool.
```

**Why this works for verification:**
- This prompt forces the AI to use the `get_prompts` tool
- You can easily verify by checking if the AI returns actual prompt data from your sheet
- No complex summarization required - just raw tool output
- Clear success indicator: if you see actual prompt names/content from your sheet, the MCP connection is working

**Quick Verification Steps:**
1. Add a test prompt to the "Gemini Prompts" sheet using the `insert_prompt` tool (e.g., name: "Test Prompt", content: "This is a test")
2. Send the simple test prompt above to Gemini/Claude
3. Verify the AI shows your actual test prompt data (not generic responses)
4. Success = MCP server is connected and working

### Advanced Test Prompt

For comprehensive testing, use this prompt which requires the AI to summarize sheet content:

**Advanced Test Prompt:**
```
Use the Google Sheets MCP tool to get all prompts from the 'Gemini Prompts' sheet and provide a comprehensive summary of their content, including key themes and any notable patterns you observe.
```

**Expected Behavior:**
- The AI should successfully call the `get_prompts` tool on the "Gemini Prompts" sheet
- If the sheet exists and contains prompts, the AI will receive the prompt data and generate a summary
- If the sheet is empty or doesn't exist, the AI should report this clearly
- The MCP server connection is working if the AI can access the tool and retrieve data (or report appropriate errors)

**Prerequisites:**
- Ensure the "Gemini Prompts" sheet exists in your spreadsheet (create it if needed using the `create_sheet` tool)
- Add some test prompts to the sheet using the `insert_prompt` tool for meaningful verification
- Confirm your MCP client (Gemini/Claude) is configured to use this server

**Verification Steps:**
1. Send the test prompt above to your AI assistant
2. Check that it attempts to use the Google Sheets MCP tools (you may see tool call indicators in the interface)
3. Verify the AI provides a summary based on actual sheet data rather than generic responses
4. If the AI cannot access the tools, check your MCP server configuration and authentication

## Summarization Test Prompt

For easy verification that the MCP server is working correctly with summarization capabilities:

**Test Prompt:**
```
Please use the Google Sheets MCP tool to retrieve all prompts from the 'Gemini Prompts' sheet and provide a detailed summary of their content, including the total number of prompts, key themes, and any patterns you notice in the prompt names or content.
```

**Why this works for verification:**
- Forces the AI to call the `get_prompts` tool on the "Gemini Prompts" sheet
- Requires actual data processing (counting, summarizing, pattern recognition)
- Easy to verify: if you see specific details from your actual sheet data, the MCP connection works
- Clear failure indicator: if the AI gives generic responses instead of your actual data, the server isn't connected

**Quick Verification Steps:**
1. Ensure the "Gemini Prompts" sheet exists and contains at least 2-3 test prompts
2. Send the test prompt above to Gemini/Claude
3. Check that the AI response includes:
   - Actual prompt names/content from your sheet (not generic examples)
   - A specific count of prompts (e.g., "There are 5 prompts in total")
   - Real themes/patterns from your actual data
4. Success = MCP server is connected and functioning correctly

**Prerequisites:**
- "Gemini Prompts" sheet exists in your spreadsheet
- Sheet contains some test prompts (use `insert_prompt` tool to add them if needed)
- MCP client properly configured to use this server

## Connecting to MCP Clients

This MCP server can be connected to any MCP-compatible client that supports the MCP protocol. The server exposes tools for programmatic Google Sheets access, allowing clients to manage spreadsheet content, store prompts, and retrieve data across multiple sheets.