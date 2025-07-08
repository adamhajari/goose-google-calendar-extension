<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Goose Calendar Extension Development Instructions

This workspace contains a custom Goose extension for Google Calendar integration. When working on this project:

## Key Components
- **Toolkit Structure**: Follow the Goose toolkit pattern with `@tool` decorators
- **Google Calendar API**: Use the Google Calendar API v3 for all calendar operations
- **Authentication**: Handle OAuth 2.0 flow for Google Calendar access
- **Error Handling**: Provide clear, user-friendly error messages

## Development Guidelines
- Use proper type hints for all function parameters and return values
- Follow Python best practices and PEP 8 style guidelines
- Ensure all tools have comprehensive docstrings explaining parameters and return values
- Handle edge cases gracefully (missing credentials, API errors, etc.)
- Use natural language processing for flexible date/time parsing

## API Integration
- Always authenticate users before making Calendar API calls
- Store credentials securely using pickle for token persistence
- Handle token refresh automatically
- Provide clear instructions for initial setup

## Testing Considerations
- Test with various date/time formats
- Test error scenarios (network issues, authentication failures)
- Verify proper handling of all-day vs. timed events
- Test event search and modification functionality
