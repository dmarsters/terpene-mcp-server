"""
FastMCP Cloud entry point for Terpene Vocabulary server.

For FastMCP Cloud deployment, the entry point function must RETURN the server object.
The cloud platform handles the event loop and server.run() call.
"""

from .server import mcp

def handler():
    """Entry point for FastMCP Cloud deployment."""
    return mcp
