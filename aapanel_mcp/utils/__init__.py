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
        if data.get("status") is False and ("msg" in data or "error_type" in data):
            msg = data.get("msg", "Unknown error")
            endpoint = data.get("endpoint", "")
            error_type = data.get("error_type", "")
            parts = [f"Error: {msg}"]
            if endpoint:
                parts.append(f"Endpoint: {endpoint}")
            if error_type:
                parts.append(f"Type: {error_type}")
            return " | ".join(parts)
        if data.get("status") == -1 and "message" in data:
            msg = data.get("message")
            if isinstance(msg, dict) and "result" in msg:
                msg = msg["result"]
            return f"Error: {msg}"
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


# Markers indicating an endpoint/action does not exist on this panel version
_MISSING_MARKERS = (
    "404",
    "not found",
    "not exist",
    "does not exist",
    "no such",
    "不存在",
    "module not found",
    "not found method",
)


def is_missing_endpoint(data: Any) -> bool:
    """Check whether a response indicates the endpoint/action is absent on this
    aaPanel version (HTTP 404, 'not found method', 'module not found', etc.).

    Deliberately narrow: parameter errors, plugin-missing errors, safety blocks,
    and confirmation gates are NOT treated as missing endpoints, so callers only
    fall back when the route itself is unavailable.
    """
    if not isinstance(data, dict):
        return False
    if data.get("blocked_by_safety") or data.get("confirmation_required"):
        return False
    msg = str(data.get("msg", "") or data.get("message", "") or "").lower()
    if isinstance(data.get("message"), dict):
        msg = str(data["message"]).lower()
    if data.get("error_type") == "HTTPStatusError":
        return "404" in msg
    if data.get("status") is False or data.get("status") == -1:
        return any(marker in msg for marker in _MISSING_MARKERS)
    return False


def request_compat(
    client,
    endpoints,
    params: dict | None = None,
    confirmed: bool = False,
    method: str = "POST",
):
    """Try endpoints in order, falling back when a route is missing on this panel.

    Use for endpoints that differ between aaPanel versions (e.g. v1 vs v2 routes).
    The first response that does NOT look like a missing route is returned; if all
    endpoints are missing, the last response is returned so the caller sees the
    most informative error.

    Args:
        client: aaPanelClient instance
        endpoints: endpoint string or ordered list of endpoint strings
        params: request parameters
        confirmed: destructive-operation confirmation flag (passed to every attempt)
        method: HTTP method
    """
    if isinstance(endpoints, str):
        endpoints = [endpoints]
    last: Any = {"status": False, "msg": "No endpoints configured"}
    for endpoint in endpoints:
        try:
            data = client.request(endpoint, params, method=method, confirmed=confirmed)
        except Exception as e:
            last = {"status": False, "msg": str(e), "endpoint": endpoint}
            continue
        if not is_missing_endpoint(data):
            return data
        last = data
    return last
