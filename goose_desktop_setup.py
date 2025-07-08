#!/usr/bin/env python3
"""
Goose Desktop Extension Setup Helper
Helps configure the Google Calendar extension for Goose Desktop
"""

import os
import json

def create_config_files():
    """Create configuration files in multiple locations."""
    
    config_content_toml = """[tools]
calendar = "goose_calendar.toolkit:CalendarToolkit"

[settings]
calendar.default_timezone = "America/New_York"
calendar.max_events = 20
"""
    
    config_content_detailed = """[extensions]
calendar = {
    module = "goose_calendar.toolkit",
    class = "CalendarToolkit",
    enabled = true,
    description = "Google Calendar integration for listing, adding, and editing calendar events"
}
"""

    # Possible Goose Desktop configuration locations
    config_locations = [
        "~/.config/goose/goose.toml",
        "~/Library/Application Support/Goose/goose.toml",
        "~/Library/Application Support/Goose/config.toml",
        "~/Library/Application Support/Goose/extensions.toml",
        "~/.goose/config.toml",
        "~/.goose/goose.toml"
    ]
    
    print("🔧 Creating Goose configuration files...")
    
    for location in config_locations:
        full_path = os.path.expanduser(location)
        directory = os.path.dirname(full_path)
        
        # Create directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)
        
        # Write basic config
        try:
            with open(full_path, 'w') as f:
                f.write(config_content_toml)
            print(f"✅ Created: {location}")
        except Exception as e:
            print(f"⚠️  Could not create {location}: {e}")
    
    # Also create a detailed extensions config
    detailed_locations = [
        "~/Library/Application Support/Goose/extensions.toml",
        "~/.config/goose/extensions.toml"
    ]
    
    for location in detailed_locations:
        full_path = os.path.expanduser(location)
        directory = os.path.dirname(full_path)
        os.makedirs(directory, exist_ok=True)
        
        try:
            with open(full_path, 'w') as f:
                f.write(config_content_detailed)
            print(f"✅ Created detailed config: {location}")
        except Exception as e:
            print(f"⚠️  Could not create {location}: {e}")

def create_package_json():
    """Create a package.json style config for Electron-based apps."""
    
    package_config = {
        "name": "goose-calendar-extension",
        "version": "0.1.0",
        "description": "Google Calendar integration for Goose",
        "main": "goose_calendar.toolkit:CalendarToolkit",
        "toolkit": {
            "name": "calendar",
            "module": "goose_calendar.toolkit",
            "class": "CalendarToolkit"
        }
    }
    
    locations = [
        "~/Library/Application Support/Goose/extensions/calendar/package.json",
        "~/.config/goose/extensions/calendar/package.json"
    ]
    
    for location in locations:
        full_path = os.path.expanduser(location)
        directory = os.path.dirname(full_path)
        os.makedirs(directory, exist_ok=True)
        
        try:
            with open(full_path, 'w') as f:
                json.dump(package_config, f, indent=2)
            print(f"✅ Created package.json: {location}")
        except Exception as e:
            print(f"⚠️  Could not create {location}: {e}")

def print_manual_instructions():
    """Print manual setup instructions."""
    
    print("\\n" + "="*60)
    print("📋 MANUAL SETUP INSTRUCTIONS FOR GOOSE DESKTOP")
    print("="*60)
    
    print("\\n1. 🔧 In Goose Desktop Settings, look for:")
    print("   - Extensions")
    print("   - Toolkits") 
    print("   - Custom Tools")
    print("   - Add-ons")
    print("   - Integrations")
    
    print("\\n2. ➕ Add new extension with these details:")
    print("   📝 Name: calendar")
    print("   📝 Module: goose_calendar.toolkit:CalendarToolkit")
    print("   📝 Description: Google Calendar integration")
    
    print("\\n3. 🔄 Alternative module formats to try:")
    print("   - goose_calendar.toolkit:CalendarToolkit")
    print("   - goose_calendar.toolkit.CalendarToolkit")
    print("   - calendar")
    
    print("\\n4. 🎯 What the extension provides:")
    print("   - list_events: View calendar events")
    print("   - add_event: Create new events")
    print("   - edit_event: Modify existing events")
    print("   - delete_event: Remove events")
    
    print("\\n5. 🔍 After adding, test with:")
    print("   - 'List my calendar events'")
    print("   - 'Add a meeting tomorrow at 2 PM'")
    
    print("\\n6. 🐛 If it doesn't work, check:")
    print("   - Restart Goose Desktop")
    print("   - Check Help > Show Logs for errors")
    print("   - Try different module path formats")

def main():
    """Main setup function."""
    print("Goose Desktop Calendar Extension Setup")
    print("="*40)
    
    # Create all possible config files
    create_config_files()
    
    # Create package.json style configs
    create_package_json()
    
    # Print manual instructions
    print_manual_instructions()
    
    print("\\n🎉 Setup complete! Now:")
    print("1. Restart Goose Desktop")
    print("2. Check Settings for Extensions/Toolkits")
    print("3. Manually add the calendar extension if needed")
    print("4. Test with calendar commands")

if __name__ == "__main__":
    main()
