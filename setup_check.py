# Example setup script for Google Calendar API credentials

"""
Google Calendar API Setup Instructions
=====================================

IMPORTANT: To avoid the "access_denied" error (Error 403), follow these steps:

1. Go to Google Cloud Console: https://console.cloud.google.com/
2. Create a new project or select an existing one
3. Enable the Google Calendar API:
   - Go to APIs & Services > Library
   - Search for "Google Calendar API"
   - Click on it and press "Enable"

4. Configure OAuth consent screen (CRITICAL STEP):
   - Go to APIs & Services > OAuth consent screen
   - If prompted, choose "External" user type (if no option appears, proceed)
   - Fill in the required fields:
     * App name: "Goose Calendar Extension" (or your preferred name)
     * User support email: your email
     * Developer contact: your email
   - Navigate through the setup pages:
     * Scopes: Click "Save and Continue" (defaults are fine)
     * Test users: Add your email address (if this section appears)
     * Summary: Review and finish

5. Create credentials:
   - Go to APIs & Services > Credentials
   - Click "Create Credentials" > "OAuth 2.0 Client IDs"
   - Choose "Desktop application"
   - Give it a name (e.g., "Goose Calendar Extension")
   - Download the JSON file

6. Save the downloaded file as 'credentials.json' in your home directory:
   - On macOS/Linux: ~/credentials.json
   - On Windows: C:\\Users\\YourUsername\\credentials.json

7. Install the extension:
   pip install -e .

8. Test the extension with Goose!

Note: If you still get Error 403, make sure:
- Your email is added as a test user in the OAuth consent screen
- The OAuth consent screen is properly configured
- You're using the same Google account for testing that's listed as a test user
"""

import os


def check_credentials():
    """Check if credentials file exists and provide detailed setup guidance."""
    creds_path = os.path.expanduser('~/credentials.json')
    if os.path.exists(creds_path):
        print("✅ Credentials file found!")
        print("\nIf you're getting Error 403 (access_denied):")
        print("1. Go to Google Cloud Console > APIs & Services > OAuth consent screen")
        print("2. Complete the OAuth consent screen setup (all required fields)")
        print("3. If you see 'Test users' section, add your email there")
        print("4. If you're in Google Workspace and chose 'Internal', test users aren't needed")
        print("5. Use the same Google account for authentication that you configured")
        return True
    else:
        print("❌ Credentials file not found.")
        print(f"Please download your OAuth 2.0 credentials and save as: {creds_path}")
        print("\nIMPORTANT: Don't forget to configure the OAuth consent screen!")
        print("See the detailed instructions above.")
        return False


if __name__ == "__main__":
    print("Google Calendar Extension Setup Check")
    print("=" * 40)
    check_credentials()
