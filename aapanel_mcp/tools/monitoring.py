"""Monitoring tools for aaPanel MCP server."""

from mcp.server.fastmcp import FastMCP
from ..client import client_manager
from ..utils import format_response


def register_monitoring_tools(mcp: FastMCP) -> None:
    """Register all monitoring tools."""

    @mcp.tool()
    def monitor_get_realtime(server: str = "") -> str:
        """Get real-time system monitoring data (CPU, memory, network, disk I/O).

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/system?action=GetNetWork")
        return format_response(data)

    @mcp.tool()
    def monitor_get_history(
        server: str = "",
        start: str = "",
        end: str = "",
    ) -> str:
        """Get historical monitoring data for a time range.

        Args:
            server: Server name (optional)
            start: Start time (timestamp or date string)
            end: End time (timestamp or date string)
        """
        client = client_manager.get_client(server or None)
        params = {"start": start, "end": end}
        data = client.request("/monitor?action=GetHistory", params)
        return format_response(data)

    @mcp.tool()
    def monitor_get_process_list(server: str = "") -> str:
        """Get list of running processes.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/ajax?action=GetProcessList")
        return format_response(data)

    @mcp.tool()
    def monitor_get_nginx_status(server: str = "") -> str:
        """Get Nginx status information.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/ajax?action=GetNginxStatus")
        return format_response(data)

    @mcp.tool()
    def monitor_get_php_status(server: str = "") -> str:
        """Get PHP status information.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/ajax?action=GetPHPStatus")
        return format_response(data)
