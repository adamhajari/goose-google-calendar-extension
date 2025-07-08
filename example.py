"""Example usage of the Goose Calendar Extension."""

import sys
import os

# Add the src directory to the path for local testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from goose_calendar.toolkit import CalendarToolkit


def main():
    """Example of how to use the Calendar toolkit."""
    print("Goose Calendar Extension Example")
    print("=" * 40)
    
    # Initialize the toolkit
    toolkit = CalendarToolkit()
    
    # Check if credentials are set up
    try:
        # Try to get credentials (this will fail if not set up)
        toolkit._get_credentials()
        print("✅ Credentials are properly configured!")
        
        # Example: List upcoming events
        print("\nListing upcoming events...")
        events = toolkit.list_events(days_ahead=7, max_results=5)
        print(events)
        
    except FileNotFoundError as e:
        print(f"❌ {e}")
        print("\nTo set up Google Calendar API access:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a new project or select existing one")
        print("3. Enable Google Calendar API")
        print("4. Create OAuth 2.0 credentials for desktop application")
        print("5. Download credentials file as ~/credentials.json")
        print("6. Run this script again")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
