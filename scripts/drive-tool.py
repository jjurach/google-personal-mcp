import logging
from cyclopts import App
from google_mcp_core.context import GoogleContext
from google_mcp_core.drive import DriveService

# Suppress noisy google discovery logs
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

app = App()

@app.default
def list_all(profile: str = "default"):
    """Lists all files in Google Drive for a given profile."""
    try:
        # Request broader scopes to see all files, not just those created by the app
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive.readonly"
        ]
        context = GoogleContext(profile=profile, scopes=scopes)
        # We don't provide allowed_folder_ids here because this is a maintenance script
        service = DriveService(context)
        
        print(f"--- Listing all files for profile: {profile} ---")
        files = service.list_all_files()
        
        if not files:
            print("No files found.")
            return

        print(f"{'ID':<35} {'Type':<40} {'Name'}")
        print("-" * 100)
        for f in files:
            mtype = f.get('mimeType', 'unknown')
            # Shorten mimeType for display
            mtype = mtype.replace('application/vnd.google-apps.', 'g:')
            print(f"{f['id']:<35} {mtype:<40} {f['name']}")

    except Exception as e:
        print(f"Error: {e}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    app()
