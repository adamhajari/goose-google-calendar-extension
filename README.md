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
git clone https://github.com/adamhajari/goose-google-calendar-extension.git
cd goose-google-calendar-extension
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

This extension is structured as an **MCP server** for Goose Desktop integration.

### Step 1: Install Dependencies

1. **Clone and install the extension**:
   ```bash
   git clone https://github.com/adamhajari/goose-google-calendar-extension.git
   cd goose-google-calendar-extension
   python3 -m venv venv
   source venv/bin/activate
   pip install -e .
   ```

2. **Set up Google Calendar API credentials** (same as above in main Installation section)

### Step 2: Get Your Command Path

```bash
cd {path-to-repo}
source venv/bin/activate
which python
```

Copy the output (e.g., `{path-to-repo}/venv/bin/python`)

### Step 3: Add Extension in Goose Desktop

1. **Open Goose Desktop**
2. **Go to Settings > Extensions > Add**
3. **Fill in these fields**:

   | Field | Value |
   |-------|-------|
   | **Type** | `StandardIO` |
   | **ID** | `calendar` |
   | **Name** | `Google Calendar` |
   | **Description** | `Google Calendar integration - list, add, edit, and delete calendar events` |
   | **Command** | `[YOUR_PATH_FROM_STEP_2] -m goose_calendar` |

   Replace `[YOUR_PATH_FROM_STEP_2]` with the path you copied.

4. **Save** and **Restart** Goose Desktop

### Step 4: Test the Extension

Ask Goose: "What tools do you have?"

You should see calendar tools like:
- `list_calendar_events`
- `add_calendar_event`
- `edit_calendar_event`
- `delete_calendar_event`

### Example Commands

- "List my calendar events for today"
- "Add a meeting tomorrow at 2 PM"
- "What's on my calendar this week?"

### Troubleshooting

If the extension doesn't work:

1. **Test the command manually** in Terminal:
   ```bash
   cd {path-to-repo}
   source venv/bin/activate
   python -m goose_calendar
   ```
   (It should start and wait for input - press Ctrl+C to stop)

2. **Try alternative command** in Goose Desktop:
   ```
   {path-to-repo}/venv/bin/python {path-to-repo}/src/goose_calendar/mcp_server.py
   ```

3. **Check the logs** in Goose Desktop developer tools

For more detailed troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

## Development

To contribute to this extension:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details.
