#!/usr/bin/env python3
"""
Verification script for Goose Calendar Extension setup
"""

import os
import sys

def check_extension_installation():
    """Check if the extension can be imported."""
    print("🔍 Checking extension installation...")
    
    try:
        import goose_calendar.toolkit
        from goose_calendar.toolkit import CalendarToolkit
        print("✅ Extension can be imported successfully")
        
        # Try to instantiate the toolkit
        toolkit = CalendarToolkit()
        print("✅ CalendarToolkit can be instantiated")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Other error: {e}")
        return False

def check_credentials():
    """Check if Google Calendar credentials are set up."""
    print("\\n🔍 Checking Google Calendar credentials...")
    
    creds_path = os.path.expanduser('~/credentials.json')
    if os.path.exists(creds_path):
        print("✅ Credentials file found at ~/credentials.json")
        return True
    else:
        print("❌ Credentials file not found")
        print("   Please download OAuth 2.0 credentials from Google Cloud Console")
        print("   and save as ~/credentials.json")
        return False

def check_config_files():
    """Check if Goose configuration files exist."""
    print("\\n🔍 Checking Goose configuration files...")
    
    config_locations = [
        "~/.config/goose/goose.toml",
        "~/Library/Application Support/Goose/goose.toml"
    ]
    
    found_config = False
    for location in config_locations:
        full_path = os.path.expanduser(location)
        if os.path.exists(full_path):
            print(f"✅ Configuration found at {location}")
            found_config = True
            
            # Check if it contains our calendar configuration
            try:
                with open(full_path, 'r') as f:
                    content = f.read()
                    if 'calendar = "goose_calendar.toolkit:CalendarToolkit"' in content:
                        print("✅ Calendar extension is configured in the file")
                    else:
                        print("⚠️  Calendar extension not found in configuration")
            except Exception as e:
                print(f"⚠️  Could not read config file: {e}")
    
    if not found_config:
        print("❌ No Goose configuration files found")
        print("   Configuration files have been created for you")
    
    return found_config

def main():
    """Run all verification checks."""
    print("Goose Calendar Extension - Setup Verification")
    print("=" * 50)
    
    all_good = True
    
    # Check extension installation
    if not check_extension_installation():
        all_good = False
    
    # Check credentials
    if not check_credentials():
        all_good = False
    
    # Check config files
    check_config_files()
    
    print("\\n" + "=" * 50)
    if all_good:
        print("🎉 Setup looks good! Next steps:")
        print("1. Restart Goose Desktop")
        print("2. Try asking: 'List my calendar events'")
        print("3. Or: 'Add a meeting tomorrow at 2 PM'")
    else:
        print("⚠️  Some setup issues found. Please address them above.")
    
    print("\\n📚 For troubleshooting, see TROUBLESHOOTING.md")

if __name__ == "__main__":
    main()
