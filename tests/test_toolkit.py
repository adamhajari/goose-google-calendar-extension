"""Tests for the Calendar toolkit."""

import unittest
from unittest.mock import Mock, patch, MagicMock
from src.goose_calendar.toolkit import CalendarToolkit


class TestCalendarToolkit(unittest.TestCase):
    """Test cases for CalendarToolkit."""

    def setUp(self):
        """Set up test fixtures."""
        self.toolkit = CalendarToolkit()

    @patch('src.goose_calendar.toolkit.build')
    @patch('src.goose_calendar.toolkit.Credentials')
    def test_get_service(self, mock_creds, mock_build):
        """Test service initialization."""
        mock_service = Mock()
        mock_build.return_value = mock_service
        
        with patch.object(self.toolkit, '_get_credentials', return_value=mock_creds):
            service = self.toolkit._get_service()
            
        self.assertEqual(service, mock_service)
        mock_build.assert_called_once_with('calendar', 'v3', credentials=mock_creds)

    @patch('src.goose_calendar.toolkit.CalendarToolkit._get_service')
    def test_list_events_no_events(self, mock_get_service):
        """Test listing events when no events exist."""
        mock_service = Mock()
        mock_events_result = {'items': []}
        mock_service.events().list().execute.return_value = mock_events_result
        mock_get_service.return_value = mock_service
        
        result = self.toolkit.list_events()
        
        self.assertIn("No upcoming events found", result)

    @patch('src.goose_calendar.toolkit.CalendarToolkit._get_service')
    def test_add_event_success(self, mock_get_service):
        """Test successful event creation."""
        mock_service = Mock()
        mock_created_event = {'id': 'test_event_id'}
        mock_service.events().insert().execute.return_value = mock_created_event
        mock_get_service.return_value = mock_service
        
        result = self.toolkit.add_event(
            title="Test Event",
            start_time="2025-07-03 14:00",
            end_time="2025-07-03 15:00"
        )
        
        self.assertIn("created successfully", result)
        self.assertIn("test_event_id", result)


if __name__ == '__main__':
    unittest.main()
