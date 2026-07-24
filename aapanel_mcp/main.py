#!/usr/bin/env python3
"""aaPanel MCP Server — Entry point.

Full-featured MCP server for aaPanel management.
Supports multi-instance management with 100+ tools covering all aaPanel modules.
"""

import logging
import sys

from .server import create_server


def main():
    """Start the aaPanel MCP server."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stderr,
    )

    try:
        mcp = create_server()
        mcp.run(transport="stdio")
    except FileNotFoundError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Failed to start aaPanel MCP server: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
