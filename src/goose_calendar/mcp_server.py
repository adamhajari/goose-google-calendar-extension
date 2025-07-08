"""MCP Server for Google Calendar integration."""

import os
import pickle
from datetime import datetime, timedelta
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dateutil import parser as date_parser
from mcp.server.fastmcp import FastMCP
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData, INTERNAL_ERROR, INVALID_PARAMS

# Initialize the MCP server
mcp = FastMCP("calendar")

class CalendarManager:
    """Google Calendar manager for MCP server."""
    
    def __init__(self):
        self._service = None
        self._scopes = ['https://www.googleapis.com/auth/calendar']
        self._credentials_file = os.path.expanduser('~/credentials.json')
        self._token_file = os.path.expanduser('~/.goose_calendar_token.pickle')

    def _get_credentials(self) -> Optional[Credentials]:
        """Get or create Google Calendar API credentials."""
        creds = None
        
        if os.path.exists(self._token_file):
            with open(self._token_file, 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception:
                    if os.path.exists(self._token_file):
                        os.remove(self._token_file)
                    creds = None
            
            if not creds:
                if not os.path.exists(self._credentials_file):
                    raise McpError(ErrorData(
                        INVALID_PARAMS,
                        f"Credentials file not found at {self._credentials_file}. "
                        "Please download OAuth 2.0 credentials from Google Cloud Console."
                    ))
                
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self._credentials_file, self._scopes
                    )
                    creds = flow.run_local_server(port=0)
                except Exception as e:
                    if "access_denied" in str(e):
                        raise McpError(ErrorData(
                            INTERNAL_ERROR,
                            "Error 403: access_denied - Your app needs Google verification. "
                            "Add your email as a test user in Google Cloud Console OAuth consent screen."
                        ))
                    raise McpError(ErrorData(INTERNAL_ERROR, f"Authentication failed: {e}"))
            
            with open(self._token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        return creds

    def _get_service(self):
        """Get the Google Calendar service."""
        if self._service is None:
            creds = self._get_credentials()
            self._service = build('calendar', 'v3', credentials=creds)
        return self._service

# Initialize calendar manager
calendar_manager = CalendarManager()

@mcp.tool()
def list_events(days_ahead: int = 7, max_results: int = 10) -> str:
    """
    List upcoming calendar events.
    
    Args:
        days_ahead: Number of days ahead to look for events (default: 7)
        max_results: Maximum number of events to return (default: 10)
        
    Returns:
        String containing formatted list of events
    """
    try:
        service = calendar_manager._get_service()
        
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
        
    except McpError:
        raise
    except HttpError as error:
        raise McpError(ErrorData(INTERNAL_ERROR, f"Google Calendar API error: {error}"))
    except Exception as error:
        raise McpError(ErrorData(INTERNAL_ERROR, f"Unexpected error: {error}"))

@mcp.tool()
def add_event(
    title: str,
    start_time: str,
    end_time: Optional[str] = None,
    description: Optional[str] = None,
    location: Optional[str] = None,
    all_day: bool = False
) -> str:
    """
    Add a new calendar event.
    
    Args:
        title: Event title/summary
        start_time: Start time in natural language or ISO format
        end_time: End time in natural language or ISO format (optional)
        description: Event description (optional)
        location: Event location (optional)
        all_day: Whether this is an all-day event (default: False)
        
    Returns:
        String confirming event creation
    """
    try:
        service = calendar_manager._get_service()
        
        # Parse start time
        try:
            start_dt = date_parser.parse(start_time)
        except Exception:
            raise McpError(ErrorData(INVALID_PARAMS, f"Could not parse start time: {start_time}"))
        
        # Parse end time or set default
        if end_time:
            try:
                end_dt = date_parser.parse(end_time)
            except Exception:
                raise McpError(ErrorData(INVALID_PARAMS, f"Could not parse end time: {end_time}"))
        else:
            if all_day:
                end_dt = start_dt
            else:
                end_dt = start_dt + timedelta(hours=1)
        
        # Create event object
        event = {'summary': title}
        
        if all_day:
            event['start'] = {'date': start_dt.date().isoformat()}
            event['end'] = {'date': end_dt.date().isoformat()}
        else:
            event['start'] = {'dateTime': start_dt.isoformat(), 'timeZone': 'America/New_York'}
            event['end'] = {'dateTime': end_dt.isoformat(), 'timeZone': 'America/New_York'}
        
        if description:
            event['description'] = description
        if location:
            event['location'] = location
        
        # Create the event
        created_event = service.events().insert(calendarId='primary', body=event).execute()
        
        return f"✅ Event '{title}' created successfully! Event ID: {created_event['id']}"
        
    except McpError:
        raise
    except HttpError as error:
        raise McpError(ErrorData(INTERNAL_ERROR, f"Google Calendar API error: {error}"))
    except Exception as error:
        raise McpError(ErrorData(INTERNAL_ERROR, f"Unexpected error: {error}"))

@mcp.tool()
def edit_event(
    event_query: str,
    new_title: Optional[str] = None,
    new_start_time: Optional[str] = None,
    new_end_time: Optional[str] = None,
    new_description: Optional[str] = None,
    new_location: Optional[str] = None
) -> str:
    """
    Edit an existing calendar event.
    
    Args:
        event_query: Search query to find the event (title, date, etc.)
        new_title: New event title (optional)
        new_start_time: New start time (optional)
        new_end_time: New end time (optional)  
        new_description: New description (optional)
        new_location: New location (optional)
        
    Returns:
        String confirming event update
    """
    try:
        service = calendar_manager._get_service()
        
        # Search for events
        now = datetime.utcnow().isoformat() + 'Z'
        future = (datetime.utcnow() + timedelta(days=365)).isoformat() + 'Z'
        
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            timeMax=future,
            q=event_query,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        if not events:
            return f"No events found matching '{event_query}'"
        
        if len(events) > 1:
            result = f"Multiple events found matching '{event_query}'. Please be more specific:\\n\\n"
            for i, event in enumerate(events[:5], 1):
                start = event['start'].get('dateTime', event['start'].get('date'))
                summary = event.get('summary', 'No title')
                result += f"{i}. {summary} ({start})\\n"
            return result
        
        # Edit the found event
        event = events[0]
        event_id = event['id']
        
        if new_title:
            event['summary'] = new_title
        if new_description is not None:
            event['description'] = new_description
        if new_location is not None:
            event['location'] = new_location
        
        if new_start_time:
            try:
                start_dt = date_parser.parse(new_start_time)
                if 'date' in event['start']:
                    event['start']['date'] = start_dt.date().isoformat()
                else:
                    event['start']['dateTime'] = start_dt.isoformat()
            except Exception:
                raise McpError(ErrorData(INVALID_PARAMS, f"Could not parse new start time: {new_start_time}"))
        
        if new_end_time:
            try:
                end_dt = date_parser.parse(new_end_time)
                if 'date' in event['end']:
                    event['end']['date'] = end_dt.date().isoformat()
                else:
                    event['end']['dateTime'] = end_dt.isoformat()
            except Exception:
                raise McpError(ErrorData(INVALID_PARAMS, f"Could not parse new end time: {new_end_time}"))
        
        # Update the event
        service.events().update(
            calendarId='primary',
            eventId=event_id,
            body=event
        ).execute()
        
        return f"✅ Event '{event['summary']}' updated successfully!"
        
    except McpError:
        raise
    except HttpError as error:
        raise McpError(ErrorData(INTERNAL_ERROR, f"Google Calendar API error: {error}"))
    except Exception as error:
        raise McpError(ErrorData(INTERNAL_ERROR, f"Unexpected error: {error}"))

@mcp.tool()
def delete_event(event_query: str) -> str:
    """
    Delete a calendar event.
    
    Args:
        event_query: Search query to find the event to delete
        
    Returns:
        String confirming event deletion
    """
    try:
        service = calendar_manager._get_service()
        
        # Search for events
        now = datetime.utcnow().isoformat() + 'Z'
        future = (datetime.utcnow() + timedelta(days=365)).isoformat() + 'Z'
        
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            timeMax=future,
            q=event_query,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        if not events:
            return f"No events found matching '{event_query}'"
        
        if len(events) > 1:
            result = f"Multiple events found matching '{event_query}'. Please be more specific:\\n\\n"
            for i, event in enumerate(events[:5], 1):
                start = event['start'].get('dateTime', event['start'].get('date'))
                summary = event.get('summary', 'No title')
                result += f"{i}. {summary} ({start})\\n"
            return result
        
        # Delete the found event
        event = events[0]
        event_id = event['id']
        event_title = event.get('summary', 'Untitled Event')
        
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        
        return f"✅ Event '{event_title}' deleted successfully!"
        
    except McpError:
        raise
    except HttpError as error:
        raise McpError(ErrorData(INTERNAL_ERROR, f"Google Calendar API error: {error}"))
    except Exception as error:
        raise McpError(ErrorData(INTERNAL_ERROR, f"Unexpected error: {error}"))

if __name__ == "__main__":
    mcp.run()
