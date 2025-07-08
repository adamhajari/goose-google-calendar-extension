# Quick Setup Guide for Goose Desktop

This guide shows you how to add the Google Calendar extension to Goose Desktop.

## Step 1: Get Your Command Path

Open Terminal and run:

```bash
cd /Users/adamhajari/Develop/goose-calendar-ext-cp
source venv/bin/activate
which python
```

Copy the output (it will look like `/Users/adamhajari/Develop/goose-calendar-ext-cp/venv/bin/python`).

## Step 2: Add Extension in Goose Desktop

1. **Open Goose Desktop**
2. **Go to Settings > Extensions > Add**
3. **Fill in these fields**:

   | Field | Value |
   |-------|-------|
   | **Type** | `StandardIO` |
   | **ID** | `calendar` |
   | **Name** | `Google Calendar` |
   | **Description** | `Google Calendar integration - list, add, edit, and delete calendar events` |
   | **Command** | `[YOUR_PATH_FROM_STEP_1] -m goose_calendar` |

   Replace `[YOUR_PATH_FROM_STEP_1]` with the path you copied.

4. **Save** and **Restart** Goose Desktop

## Step 3: Test

Ask Goose: "What tools do you have?"

You should see calendar tools like:
- `list_calendar_events`
- `add_calendar_event`
- `edit_calendar_event`
- `delete_calendar_event`

## Example Commands

- "List my calendar events for today"
- "Add a meeting tomorrow at 2 PM"
- "What's on my calendar this week?"

## Troubleshooting

If it doesn't work:

1. **Test the command manually** in Terminal:
   ```bash
   cd /Users/adamhajari/Develop/goose-calendar-ext-cp
   source venv/bin/activate
   python -m goose_calendar
   ```
   (It should start and wait for input - press Ctrl+C to stop)

2. **Try alternative command** in Goose Desktop:
   ```
   /Users/adamhajari/Develop/goose-calendar-ext-cp/venv/bin/python /Users/adamhajari/Develop/goose-calendar-ext-cp/src/goose_calendar/mcp_server.py
   ```

3. **Check the logs** in Goose Desktop developer tools

For more detailed troubleshooting, see `TROUBLESHOOTING.md`.
