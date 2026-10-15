"""SSH security management tools for aaPanel MCP server."""

from mcp.server.fastmcp import FastMCP
from ..client import client_manager
from ..utils import format_response, request_compat


def register_ssh_tools(mcp: FastMCP) -> None:
    """Register all SSH management tools."""

    @mcp.tool()
    def ssh_get_info(server: str = "") -> str:
        """Get SSH service configuration information.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = request_compat(
            client,
            ["/v2/safe/ssh/GetSshInfo", "/firewall?action=GetSshInfo"],
        )
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
        results = {}
        if port:
            results["port"] = client.request("/firewall?action=SetSshPort", {"port": port})
        if str(password_auth) in ("1", "true", "True", "yes"):
            results["password_auth"] = client.request("/ssh_security?action=set_password")
        elif str(password_auth) in ("0", "false", "False", "no"):
            results["password_auth"] = client.request("/ssh_security?action=stop_password", confirmed=True)
        if str(root_login) in ("1", "true", "True", "yes"):
            results["root_login"] = client.request("/ssh_security?action=set_root", {"p_type": "yes"})
        elif str(root_login) in ("0", "false", "False", "no"):
            results["root_login"] = client.request("/ssh_security?action=stop_root", confirmed=True)
        return format_response(results)

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
        params = {"p": page, "page": page, "limit": limit, "search": search, "select": "ALL", "table": "logs"}
        data = request_compat(
            client,
            ["/v2/mod/ssh/com/get_ssh_list", "/data?action=getData"],
            params,
        )
        return format_response(data)

    @mcp.tool()
    def ssh_get_security_status(server: str = "") -> str:
        """Get SSH security audit status.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = request_compat(
            client,
            ["/ssh_security?action=san_ssh_security", "/firewall?action=GetSshInfo"],
        )
        return format_response(data)
