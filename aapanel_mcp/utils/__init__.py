"""Utility functions for aaPanel MCP server."""

import json
from typing import Any


def format_response(data: Any) -> str:
    """Format API response as readable text for MCP tool output."""
    if isinstance(data, dict):
        if data.get("blocked_by_safety"):
            return f"BLOCKED: {data.get('msg', 'Operation blocked by safety guard')}"
        if data.get("confirmation_required"):
            return f"CONFIRMATION REQUIRED: {data.get('msg', 'Destructive action needs user confirmation')}"
        if data.get("status") is False:
            msg = data.get("msg", "Unknown error")
            endpoint = data.get("endpoint", "")
            error_type = data.get("error_type", "")
            parts = [f"Error: {msg}"]
            if endpoint:
                parts.append(f"Endpoint: {endpoint}")
            if error_type:
                parts.append(f"Type: {error_type}")
            return " | ".join(parts)
        return json.dumps(data, indent=2, ensure_ascii=False, default=str)
    if isinstance(data, list):
        return json.dumps(data, indent=2, ensure_ascii=False, default=str)
    return str(data)


def parse_response(data: Any) -> dict | list:
    """Parse API response into a clean dict/list."""
    if isinstance(data, dict):
        if data.get("status") is False:
            return {"success": False, "error": data.get("msg", "Unknown error")}
        return {"success": True, "data": data}
    if isinstance(data, list):
        return {"success": True, "data": data}
    return {"success": True, "data": str(data)}
