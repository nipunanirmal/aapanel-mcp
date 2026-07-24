"""SSH security management tools for aaPanel MCP server."""

from mcp.server.fastmcp import FastMCP
from ..client import client_manager
from ..utils import format_response


def register_ssh_tools(mcp: FastMCP) -> None:
    """Register all SSH management tools."""

    @mcp.tool()
    def ssh_get_info(server: str = "") -> str:
        """Get SSH service configuration information.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/firewall?action=GetSshInfo")
        return format_response(data)

    @mcp.tool()
    def ssh_set_info(
        server: str = "",
        port: str = "22",
        password_auth: str = "1",
        root_login: str = "1",
    ) -> str:
        """Update SSH service configuration.

        Args:
            server: Server name (optional)
            port: SSH port number
            password_auth: 1=allow password auth, 0=disable
            root_login: 1=allow root login, 0=disable
        """
        client = client_manager.get_client(server or None)
        params = {
            "port": port,
            "password_auth": password_auth,
            "root_login": root_login,
        }
        data = client.request("/firewall?action=SetSshPort", params)
        return format_response(data)

    @mcp.tool()
    def ssh_get_logs(
        server: str = "",
        page: int = 1,
        limit: int = 20,
        search: str = "",
    ) -> str:
        """Get SSH login logs.

        Args:
            server: Server name (optional)
            page: Page number (default 1)
            limit: Items per page (default 20)
            search: Search keyword (IP or username)
        """
        client = client_manager.get_client(server or None)
        params = {"table": "logs", "p": page, "limit": limit}
        if search:
            params["search"] = search
        data = client.request("/data?action=getData", params)
        return format_response(data)

    @mcp.tool()
    def ssh_get_security_status(server: str = "") -> str:
        """Get SSH security audit status.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/firewall?action=GetSshInfo")
        return format_response(data)
