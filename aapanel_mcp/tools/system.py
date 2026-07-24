"""System management tools for aaPanel MCP server."""

from mcp.server.fastmcp import FastMCP
from ..client import client_manager
from ..utils import format_response


def register_system_tools(mcp: FastMCP) -> None:
    """Register all system management tools."""

    @mcp.tool()
    def system_get_status(server: str = "") -> str:
        """Get comprehensive system status including CPU, memory, disk, network, and load.

        Args:
            server: Server name (optional, uses default if not specified)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/system?action=GetNetWork")
        return format_response(data)

    @mcp.tool()
    def system_get_cpu_info(server: str = "") -> str:
        """Get CPU information including model, cores, and usage.

        Args:
            server: Server name (optional, uses default if not specified)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/system?action=GetNetWork")
        return format_response(data)

    @mcp.tool()
    def system_get_mem_info(server: str = "") -> str:
        """Get memory information including total, used, and free memory.

        Args:
            server: Server name (optional, uses default if not specified)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/system?action=GetMemInfo")
        return format_response(data)

    @mcp.tool()
    def system_get_disk_info(server: str = "") -> str:
        """Get disk information including partitions and usage.

        Args:
            server: Server name (optional, uses default if not specified)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/system?action=GetDiskInfo")
        return format_response(data)

    @mcp.tool()
    def system_get_network_info(server: str = "") -> str:
        """Get network interface information.

        Args:
            server: Server name (optional, uses default if not specified)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/system?action=GetNetWork")
        return format_response(data)

    @mcp.tool()
    def system_get_system_version(server: str = "") -> str:
        """Get operating system version information.

        Args:
            server: Server name (optional, uses default if not specified)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/system?action=GetAllInfo")
        return format_response(data)

    @mcp.tool()
    def system_get_all_info(server: str = "") -> str:
        """Get all system information at once (comprehensive overview).

        Args:
            server: Server name (optional, uses default if not specified)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/system?action=GetAllInfo")
        return format_response(data)

    @mcp.tool()
    def system_restart_server(server: str = "") -> str:
        """Restart the server. Use with caution!

        Args:
            server: Server name (optional, uses default if not specified)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/system?action=RestartServer")
        return format_response(data)

    @mcp.tool()
    def system_restart_panel(server: str = "") -> str:
        """Restart the aaPanel service.

        Args:
            server: Server name (optional, uses default if not specified)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/system?action=RepPanel")
        return format_response(data)

    @mcp.tool()
    def system_clear_cache(server: str = "") -> str:
        """Clear system cache to free up memory.

        Args:
            server: Server name (optional, uses default if not specified)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/system?action=ClearSystem")
        return format_response(data)

    @mcp.tool()
    def system_service_admin(
        server: str = "",
        service: str = "",
        act: str = "",
    ) -> str:
        """Start, stop, or restart a service (nginx, apache, mysql, etc.).

        Args:
            server: Server name (optional)
            service: Service name (nginx, apache, mysql, redis, pure-ftpd, etc.)
            act: Action (start, stop, restart, reload)
        """
        client = client_manager.get_client(server or None)
        params = {"name": service, "act": act}
        data = client.request("/system?action=ServiceAdmin", params)
        return format_response(data)

    @mcp.tool()
    def system_get_boot_time(server: str = "") -> str:
        """Get system boot time.

        Args:
            server: Server name (optional, uses default if not specified)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/system?action=GetNetWork")
        return format_response(data)
