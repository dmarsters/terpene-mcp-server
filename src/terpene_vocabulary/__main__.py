"""
Local execution script for Terpene Vocabulary MCP server.

Usage:
    python -m terpene_vocabulary

This runs the server locally for testing and development.
For production, use FastMCP Cloud deployment.
"""

from .server import mcp

if __name__ == "__main__":
    mcp.run()
