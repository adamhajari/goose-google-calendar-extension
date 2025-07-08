# Troubleshooting Google Calendar API Setup

## Error 403: access_denied

This error occurs when your Google Cloud project is in testing mode and hasn't been properly configured. Here's how to fix it:

### Step 1: Configure OAuth Consent Screen

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Navigate to **APIs & Services > OAuth consent screen**
4. **User Type Selection**:
   - If you see options, choose **"External"** (unless you have a Google Workspace account, then choose "Internal")
   - If you don't see user type options, this means:
     * You're in a Google Workspace organization (it's automatically set to "Internal")
     * OR the consent screen is already partially configured
     * Simply proceed to the next step
5. Fill in the OAuth consent screen form:
   - **App name**: "Goose Calendar Extension" (or your preferred name)
   - **User support email**: Your email address
   - **App logo**: Optional (can skip)
   - **App domain**: Leave blank for testing
   - **Developer contact information**: Your email address
6. Click **"Save and Continue"**

### Step 2: Add Test Users

1. After filling the app information, you'll go through several pages:
   - **Scopes page**: Click "Save and Continue" (default scopes are sufficient)
   - **Test users page**: This is where you add yourself
2. On the **"Test users"** page:
   - Click **"Add users"**
   - Add your email address (the same one you'll use for authentication)
   - Click **"Add"** then **"Save and Continue"**
3. **Summary page**: Review and click "Back to dashboard"

**Important**: If you're in a Google Workspace organization and chose "Internal", you may not see a "Test users" section - that's normal, all users in your organization can access the app.

### Step 3: Verify Scopes

1. Go to the **"Scopes"** section of the OAuth consent screen
2. Make sure the following scope is added:
   - `https://www.googleapis.com/auth/calendar`

### Step 4: Publishing Status

For development/testing purposes, you don't need to publish your app. Keep it in "Testing" status, but make sure you're added as a test user.

### Step 5: Re-download Credentials

After configuring the OAuth consent screen:
1. Go to **APIs & Services > Credentials**
2. Delete the old OAuth 2.0 Client ID (if you had one)
3. Create a new **OAuth 2.0 Client ID**
4. Choose **"Desktop application"**
5. Download the new JSON file
6. Save it as `~/credentials.json`

### Step 6: Clear Previous Tokens

If you've attempted authentication before:
```bash
rm ~/.goose_calendar_token.pickle
```

This will force a fresh authentication flow.

### Step 7: Test Again

Run the setup check:
```bash
python setup_check.py
```

Or test with the simple test:
```bash
python simple_test.py
```

## Common Issues

### "This app isn't verified"
- This warning is normal for apps in testing mode
- Click "Advanced" → "Go to [App Name] (unsafe)" to proceed
- This only appears during development

### "The OAuth client was not found"
- Make sure you've downloaded the correct credentials file
- Verify the file is named exactly `credentials.json`
- Check that it's in your home directory

### "Invalid scope"
- Ensure the Calendar API is enabled in your Google Cloud project
- Verify the scope `https://www.googleapis.com/auth/calendar` is correctly configured

### "Project not found"
- Make sure you're working in the correct Google Cloud project
- Verify billing is enabled (even for free tier usage)

## Different Account Types and Scenarios

### Personal Google Account
- You'll see "External" user type option
- Must add yourself as a test user
- App stays in "Testing" status (which is fine for development)

### Google Workspace Account
- May only see "Internal" user type, or no selection at all
- If "Internal": All users in your organization can access the app
- No need to add test users (they're automatically included)

### No User Type Selection Visible
This can happen when:
1. **Project already configured**: The consent screen was partially set up before
2. **Workspace restrictions**: Your organization has specific policies
3. **Existing configuration**: Someone else already started the setup

**Solution**: Simply proceed with filling out the app information. The key is completing all required fields and ensuring your email has access.

## Quick Checklist

Before testing authentication:
- ✅ Google Calendar API is enabled
- ✅ OAuth consent screen is configured with app name and contact info
- ✅ Your email is added as test user (if section exists)
- ✅ Credentials file downloaded and saved as ~/credentials.json
- ✅ Using the same Google account you configured in the consent screen

## Alternative: Using Service Account (Advanced)

For automated/server environments, you might prefer a service account:

1. Create a service account in Google Cloud Console
2. Download the service account key (JSON)
3. Grant the service account access to your calendar
4. Modify the authentication code to use service account credentials

This approach bypasses the OAuth consent screen but requires manual calendar sharing.

## Goose Desktop - MCP Server Extension Setup

Based on the official Goose documentation, Goose Desktop expects extensions to be **MCP servers**. This extension is properly structured as an MCP server. Here's how to add it:

### Step 1: Verify Installation

First, make sure the extension is properly installed:

```bash
cd /Users/adamhajari/Develop/goose-calendar-ext-cp
source venv/bin/activate
pip install -e .
```

### Step 2: Get the Correct Command Path

Run this to get the exact Python path for your command:

```bash
cd /Users/adamhajari/Develop/goose-calendar-ext-cp
source venv/bin/activate
which python
```

This will output something like: `/Users/adamhajari/Develop/goose-calendar-ext-cp/venv/bin/python`

### Step 3: Add Extension to Goose Desktop

1. **Open Goose Desktop**
2. **Go to Settings > Extensions > Add**
3. **Fill in the form with these values**:

   - **Type**: `StandardIO`
   - **ID**: `calendar` 
   - **Name**: `Google Calendar`
   - **Description**: `Google Calendar integration - list, add, edit, and delete calendar events`
   - **Command**: `/Users/adamhajari/Develop/goose-calendar-ext-cp/venv/bin/python -m goose_calendar`

   **Important**: Replace `/Users/adamhajari/Develop/goose-calendar-ext-cp/venv/bin/python` with the actual path from Step 2.

4. **Save the extension**
5. **Restart Goose Desktop**

### Step 4: Alternative Command Options

If the above doesn't work, try these command variations:

**Option A**: Direct server file
```
/Users/adamhajari/Develop/goose-calendar-ext-cp/venv/bin/python /Users/adamhajari/Develop/goose-calendar-ext-cp/src/goose_calendar/mcp_server.py
```

**Option B**: With directory change (use this as a single command)
```
cd /Users/adamhajari/Develop/goose-calendar-ext-cp && source venv/bin/activate && python -m goose_calendar
```

### Step 5: Verify Extension is Working

1. **Restart Goose Desktop completely**
2. **Open a new chat** and ask: "What tools do you have?"
3. **Look for these calendar tools**:
   - `list_calendar_events`
   - `add_calendar_event` 
   - `edit_calendar_event`
   - `delete_calendar_event`

### Step 6: Test Calendar Functionality

Try these commands with Goose:
- "List my calendar events for today"
- "Add a meeting tomorrow at 2 PM called 'Team standup'"
- "What's on my calendar this week?"

### What These Fields Mean

- **Type**: `StandardIO` tells Goose this is an MCP server using stdin/stdout communication
- **ID**: Unique identifier for your extension
- **Name**: Display name shown in Goose
- **Description**: Brief explanation of what the extension does
- **Command**: Exact command to start your MCP server

### Troubleshooting Extension Loading

**If the extension doesn't appear**:

1. **Check command path**: Verify the Python path is correct and executable
2. **Test manually**: Run the exact command in terminal to ensure it works
3. **Check logs**: Look for errors in Goose Desktop developer tools
4. **Virtual environment**: Ensure the command includes the virtual environment's Python

**Common Command Issues**:
- Use absolute paths, not relative ones
- Include the full path to the virtual environment's Python
- Make sure all dependencies are installed in the virtual environment
- Verify the command works when run manually in terminal

### Method 2: Configuration File Method

If there's no GUI option, create/edit the configuration file directly:

**For macOS** (try both locations):
- `~/Library/Application Support/Goose/config.toml`
- `~/Library/Application Support/Goose/goose.toml`
- `~/.config/goose/goose.toml`

**Add this configuration**:
```toml
[tools]
calendar = "goose_calendar.toolkit:CalendarToolkit"

[extensions]
# Alternative format that some versions use
calendar = {
    module = "goose_calendar.toolkit",
    class = "CalendarToolkit",
    enabled = true
}
```

### Method 3: Through Goose Desktop Console/Debug

1. **Open Developer Tools** in Goose Desktop:
   - Look for "View" > "Developer Tools" or "Toggle Developer Tools"
   - Or press `Cmd+Option+I` (macOS) / `Ctrl+Shift+I` (Windows/Linux)

2. **In the console, try**:
   ```javascript
   // Check if extensions can be loaded manually
   window.goose.loadExtension('goose_calendar.toolkit:CalendarToolkit');
   
   // Or check available extensions
   console.log(window.goose.extensions);
   ```

### Method 4: Check Goose Desktop Documentation

1. **In Goose Desktop, look for**:
   - Help > Documentation
   - Help > Extension Guide
   - Settings > About Extensions

2. **Common extension formats**:
   - Some versions use: `module_name.class_name`
   - Others use: `module_name:class_name`
   - Try both: `goose_calendar.toolkit.CalendarToolkit` and `goose_calendar.toolkit:CalendarToolkit`

### Method 5: Install as Development Extension

If Goose Desktop has a development mode:

1. **Enable Developer Mode** (if available in settings)
2. **Add Local Extension Path**: Point to your project directory
   - Path: `/Users/adamhajari/Develop/goose-calendar-ext-cp/src`
3. **Import**: `goose_calendar.toolkit:CalendarToolkit`

### Troubleshooting Manual Setup

**If the extension still doesn't appear**:

1. **Check Python Environment**: Goose Desktop might use its own Python
   ```bash
   # Find where Goose Desktop's Python is
   which python3
   # Install there too
   /path/to/goose/python -m pip install -e /Users/adamhajari/Develop/goose-calendar-ext-cp
   ```

2. **Check Extension Loading Errors**:
   - Look in Goose Desktop logs/console for import errors
   - Common location: `~/Library/Logs/Goose/` (macOS)

3. **Alternative Installation**:
   ```bash
   # Install with all dependencies globally
   pip3 install --user -e /Users/adamhajari/Develop/goose-calendar-ext-cp
   ```

4. **Verify Installation Location**:
   ```bash
   python3 -c "import goose_calendar; print(goose_calendar.__file__)"
   ```

### What to Look For in Settings

In Goose Desktop settings, look for fields like:
- **Toolkit Name**: `calendar`
- **Module**: `goose_calendar.toolkit`
- **Class**: `CalendarToolkit`
- **Full Path**: `goose_calendar.toolkit:CalendarToolkit`
- **Entry Point**: `calendar = goose_calendar.toolkit:CalendarToolkit`
