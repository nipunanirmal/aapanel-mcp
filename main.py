#!/usr/bin/env python3
"""aaPanel MCP Server — Entry point script.

Run: python main.py
"""

import logging
import sys

from aapanel_mcp.server import create_server


def main():
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
