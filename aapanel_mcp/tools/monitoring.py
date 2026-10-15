"""Monitoring tools for aaPanel MCP server."""

import time
from mcp.server.fastmcp import FastMCP
from ..client import client_manager
from ..utils import format_response, request_compat


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
        """Get historical monitoring data (CPU/memory, disk I/O, network I/O) for a time range.

        Args:
            server: Server name (optional)
            start: Start time (unix timestamp, defaults to 1 hour ago)
            end: End time (unix timestamp, defaults to now)
        """
        client = client_manager.get_client(server or None)
        now = int(time.time())
        params = {
            "start": start or str(now - 3600),
            "end": end or str(now),
        }
        results = {
            "cpu_mem": client.request("/ajax?action=GetCpuIo", params),
            "disk_io": client.request("/ajax?action=GetDiskIo", params),
            "network_io": client.request("/ajax?action=GetNetWorkIo", params),
        }
        return format_response(results)

    @mcp.tool()
    def monitor_get_process_list(server: str = "") -> str:
        """Get list of running processes and resource load.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = request_compat(
            client,
            ["/v2/monitor/process_management/specific_resource_load_type", "/ajax?action=GetProcessList"],
        )
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
    def monitor_get_php_status(server: str = "", version: str = "") -> str:
        """Get PHP status information.

        Args:
            server: Server name (optional)
            version: PHP version (e.g. 83; auto-detected if omitted)
        """
        client = client_manager.get_client(server or None)
        resolved_ver = version
        if not resolved_ver:
            cfg = client.request("/config?action=get_config")
            if isinstance(cfg, dict):
                for php in cfg.get("php", []):
                    if php.get("setup"):
                        resolved_ver = str(php.get("version", ""))
                        break
        params = {"version": resolved_ver or "83"}
        data = client.request("/ajax?action=GetPHPStatus", params)
        return format_response(data)
