"""Firewall management tools for aaPanel MCP server."""

from mcp.server.fastmcp import FastMCP
from ..client import client_manager
from ..utils import format_response


def register_firewall_tools(mcp: FastMCP) -> None:
    """Register all firewall management tools."""

    @mcp.tool()
    def firewall_get_list(server: str = "", page: int = 1, limit: int = 100) -> str:
        """List firewall rules (ports and IP rules).

        Args:
            server: Server name (optional)
            page: Page number (default 1)
            limit: Items per page (default 100)
        """
        client = client_manager.get_client(server or None)
        params = {"table": "firewall", "p": page, "limit": limit}
        data = client.request("/data?action=getData", params)
        return format_response(data)

    @mcp.tool()
    def firewall_add_port(
        server: str = "",
        port: str = "",
        type: str = "accept",
        ps: str = "",
    ) -> str:
        """Open a port in the firewall.

        Args:
            server: Server name (optional)
            port: Port number or range (e.g. 8080 or 3000-3100)
            type: Rule type (accept or drop)
            ps: Remark/description
        """
        client = client_manager.get_client(server or None)
        params = {"port": port, "type": type, "ps": ps}
        data = client.request("/firewall?action=AddAcceptPort", params)
        return format_response(data)

    @mcp.tool()
    def firewall_delete_port(server: str = "", id: str = "") -> str:
        """Close a port in the firewall.

        Args:
            server: Server name (optional)
            id: Rule ID to delete
        """
        client = client_manager.get_client(server or None)
        params = {"id": id}
        data = client.request("/firewall?action=DelAcceptPort", params)
        return format_response(data)

    @mcp.tool()
    def firewall_add_ip(
        server: str = "",
        ip: str = "",
        type: str = "accept",
        ps: str = "",
    ) -> str:
        """Add an IP rule to the firewall.

        Args:
            server: Server name (optional)
            ip: IP address or CIDR
            type: Rule type (accept or drop)
            ps: Remark/description
        """
        client = client_manager.get_client(server or None)
        params = {"ip": ip, "type": type, "ps": ps}
        data = client.request("/firewall?action=AddDropAddress", params)
        return format_response(data)

    @mcp.tool()
    def firewall_delete_ip(server: str = "", id: str = "") -> str:
        """Remove an IP rule from the firewall.

        Args:
            server: Server name (optional)
            id: Rule ID to delete
        """
        client = client_manager.get_client(server or None)
        params = {"id": id}
        data = client.request("/firewall?action=DelDropAddress", params)
        return format_response(data)

    @mcp.tool()
    def firewall_get_panel_port(server: str = "") -> str:
        """Get the current aaPanel access port.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/config?action=get_config")
        return format_response(data)

    @mcp.tool()
    def firewall_set_panel_port(server: str = "", port: str = "") -> str:
        """Change the aaPanel access port.

        Args:
            server: Server name (optional)
            port: New port number
        """
        client = client_manager.get_client(server or None)
        params = {"port": port}
        data = client.request("/config?action=setPanel", params)
        return format_response(data)

    @mcp.tool()
    def firewall_get_status(server: str = "") -> str:
        """Get firewall status (enabled/disabled, type).

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        params = {"table": "firewall", "p": 1, "limit": 100}
        data = client.request("/data?action=getData", params)
        return format_response(data)
