"""Simple test of the Calendar toolkit without full Goose framework."""

import sys
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dateutil import parser as date_parser
import pickle


class SimpleCalendarToolkit:
    """A simplified version of the Calendar toolkit for testing."""

    def __init__(self):
        """Initialize the Calendar toolkit."""
        self._service = None
        self._scopes = ['https://www.googleapis.com/auth/calendar']
        self._credentials_file = os.path.expanduser('~/credentials.json')
        self._token_file = os.path.expanduser('~/.goose_calendar_token.pickle')

    def _get_credentials(self) -> Optional[Credentials]:
        """Get or create Google Calendar API credentials."""
        creds = None
        
        # Load existing token
        if os.path.exists(self._token_file):
            with open(self._token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # If there are no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Token refresh failed: {e}")
                    # Delete the old token and start fresh
                    if os.path.exists(self._token_file):
                        os.remove(self._token_file)
                    creds = None
            
            if not creds:
                if not os.path.exists(self._credentials_file):
                    raise FileNotFoundError(
                        f"Credentials file not found at {self._credentials_file}. "
                        "Please download your OAuth 2.0 credentials from Google Cloud Console."
                    )
                
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self._credentials_file, self._scopes
                    )
                    creds = flow.run_local_server(port=0)
                except Exception as e:
                    if "access_denied" in str(e):
                        raise Exception(
                            "Error 403: access_denied - Your app hasn't completed Google verification.\n"
                            "Solutions:\n"
                            "1. Go to Google Cloud Console > OAuth consent screen\n"
                            "2. Add your email as a 'Test user'\n"
                            "3. Ensure OAuth consent screen is properly configured\n"
                            "4. Use the same Google account that's listed as a test user\n"
                            "See TROUBLESHOOTING.md for detailed instructions."
                        )
                    else:
                        raise e
            
            # Save the credentials for next time
            with open(self._token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        return creds

    def _get_service(self):
        """Get the Google Calendar service."""
        if self._service is None:
            creds = self._get_credentials()
            self._service = build('calendar', 'v3', credentials=creds)
        return self._service

    def list_events(self, days_ahead: int = 7, max_results: int = 10) -> str:
        """List upcoming calendar events."""
        try:
            service = self._get_service()
            
            # Get events from now to specified days ahead
            now = datetime.utcnow().isoformat() + 'Z'
            end_time = (datetime.utcnow() + timedelta(days=days_ahead)).isoformat() + 'Z'
            
            events_result = service.events().list(
                calendarId='primary',
                timeMin=now,
                timeMax=end_time,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            if not events:
                return f"No upcoming events found in the next {days_ahead} days."
            
            result = f"Upcoming events (next {days_ahead} days):\\n\\n"
            
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                summary = event.get('summary', 'No title')
                
                # Parse and format the date/time
                if 'T' in start:  # Has time
                    dt = date_parser.parse(start)
                    formatted_time = dt.strftime('%Y-%m-%d at %I:%M %p')
                else:  # All-day event
                    dt = date_parser.parse(start)
                    formatted_time = dt.strftime('%Y-%m-%d (All day)')
                
                location = event.get('location', '')
                description = event.get('description', '')
                
                result += f"📅 **{summary}**\\n"
                result += f"   🕒 {formatted_time}\\n"
                if location:
                    result += f"   📍 {location}\\n"
                if description:
                    result += f"   📝 {description[:100]}{'...' if len(description) > 100 else ''}\\n"
                result += "\\n"
            
            return result
            
        except HttpError as error:
            return f"An error occurred: {error}"
        except FileNotFoundError as error:
            return str(error)
        except Exception as error:
            return f"Unexpected error: {error}"


def main():
    """Test the simplified Calendar toolkit."""
    print("Simplified Calendar Extension Test")
    print("=" * 40)
    
    # Initialize the toolkit
    toolkit = SimpleCalendarToolkit()
    
    # Check if credentials are set up
    try:
        # Try to get credentials (this will fail if not set up)
        toolkit._get_credentials()
        print("✅ Credentials are properly configured!")
        
        # Example: List upcoming events
        print("\\nListing upcoming events...")
        events = toolkit.list_events(days_ahead=7, max_results=5)
        print(events)
        
    except FileNotFoundError as e:
        print(f"❌ {e}")
        print("\\nTo set up Google Calendar API access:")
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
