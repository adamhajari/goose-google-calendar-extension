# Google Calendar Goose Extension

A custom Goose extension that allows you to list, add, and edit Google Calendar events directly from your Goose conversations.

## Features

- **List Events**: View upcoming calendar events
- **Add Events**: Create new calendar events with details
- **Edit Events**: Modify existing calendar events
- **Smart Scheduling**: Natural language event creation

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/goose-calendar-extension.git
cd goose-calendar-extension
```

2. Install the extension:
```bash
pip install -e .
```

3. Set up Google Calendar API credentials:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Google Calendar API
   - **Configure OAuth consent screen** (Important to avoid Error 403):
     * Go to APIs & Services > OAuth consent screen
     * If prompted, choose "External" user type (if this option doesn't appear, proceed to next step)
     * Fill in required fields:
       - App name: "Goose Calendar Extension" (or your preferred name)
       - User support email: your email address
       - Developer contact information: your email address
     * Click "Save and Continue"
     * On the "Scopes" page, click "Save and Continue" (default scopes are fine)
     * On the "Test users" page, click "Add users" and add your email address
     * Click "Save and Continue"
   - Create credentials (OAuth 2.0 client ID for desktop application)
   - Download the credentials file and save it as `credentials.json` in your home directory

## Usage

Once installed, the extension will be automatically available in Goose. You can use natural language commands like:

- "List my events for today"
- "Add a meeting tomorrow at 2 PM"
- "Schedule a doctor appointment next Friday at 10 AM"
- "Edit my 3 PM meeting to move it to 4 PM"

## Configuration

The extension will prompt you to authenticate with Google Calendar on first use. Your authentication token will be stored securely for future use.

# Using with Goose Desktop

## Installation for Goose Desktop

The Goose desktop application handles extensions differently than the command-line version. Here's how to set up the Google Calendar extension:

### Method 1: Install via Package Manager

1. **Install the extension globally**:
   ```bash
   pip install -e .
   ```
   (You've already done this step)

2. **Create a global configuration file**:
   Create or edit `~/.config/goose/goose.toml`:
   ```toml
   [tools]
   calendar = "goose_calendar.toolkit:CalendarToolkit"
   ```

3. **Restart Goose Desktop** to load the new extension

### Method 2: Manual Configuration in Goose Desktop

1. **Open Goose Desktop**
2. **Go to Settings/Preferences**
3. **Look for "Extensions" or "Toolkits" section**
4. **Add the calendar toolkit**:
   - Toolkit name: `calendar`
   - Module path: `goose_calendar.toolkit:CalendarToolkit`

### Method 3: Configuration File Location

The desktop version might look for configuration in different locations:
- **macOS**: `~/Library/Application Support/Goose/goose.toml`
- **Windows**: `%APPDATA%/Goose/goose.toml`
- **Linux**: `~/.config/goose/goose.toml`

Create the configuration file in the appropriate location:
```toml
[tools]
calendar = "goose_calendar.toolkit:CalendarToolkit"

[settings]
# Optional calendar settings
calendar.default_timezone = "America/New_York"
calendar.max_events = 20
```

### Verification Steps

1. **Restart Goose Desktop** after adding the configuration
2. **Test the extension** by asking Goose:
   - "List my calendar events"
   - "What's on my calendar today?"
   - "Add a meeting tomorrow at 2 PM"

### Troubleshooting Desktop Version

If the extension doesn't appear:

1. **Check Goose Desktop logs** (usually in the app's menu under Help > Show Logs)
2. **Verify Python environment**: The desktop version might use a different Python environment
3. **Install in system Python**: Try installing the extension in your system Python:
   ```bash
   pip3 install -e . --break-system-packages
   ```
4. **Check extension loading**: Look for error messages about "calendar" toolkit in the logs

## ✅ Ready for Goose Desktop

This extension is now properly structured as an **MCP server** and ready to be added to Goose Desktop! 

### Quick Setup for Goose Desktop

1. **Get your command path**:
   ```bash
   cd /Users/adamhajari/Develop/goose-calendar-ext-cp
   source venv/bin/activate
   which python
   ```

2. **Add extension in Goose Desktop**:
   - Go to Settings > Extensions > Add
   - Type: `StandardIO`
   - ID: `calendar`
   - Name: `Google Calendar`
   - Command: `[YOUR_PATH_FROM_STEP_1] -m goose_calendar`

3. **Restart Goose Desktop** and test with: "What tools do you have?"

For detailed setup instructions, see **[GOOSE_DESKTOP_SETUP.md](GOOSE_DESKTOP_SETUP.md)**

## Development

To contribute to this extension:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details.
