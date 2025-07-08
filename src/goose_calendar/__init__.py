"""Google Calendar integration for Goose AI."""

# Only import toolkit if goose dependencies are available
try:
    from .toolkit import CalendarToolkit
    __all__ = ["CalendarToolkit"]
except ImportError:
    # MCP server mode - toolkit dependencies not available
    __all__ = []

def main():
    """Main entry point for MCP server."""
    from .mcp_server import mcp
    mcp.run()
