"""Deployment tools for aaPanel MCP server."""

from mcp.server.fastmcp import FastMCP
from ..client import client_manager
from ..utils import format_response


def register_deployment_tools(mcp: FastMCP) -> None:
    """Register all deployment tools."""

    @mcp.tool()
    def deployment_get_list(
        server: str = "",
        page: int = 1,
        limit: int = 20,
    ) -> str:
        """List available deployment packages.

        Args:
            server: Server name (optional)
            page: Page number (default 1)
            limit: Items per page (default 20)
        """
        client = client_manager.get_client(server or None)
        params = {"name": "deployment", "fun": "get_list", "p": page, "limit": limit}
        data = client.request("/plugin?action=a", params)
        return format_response(data)

    @mcp.tool()
    def deployment_install(
        server: str = "",
        id: str = "",
        siteName: str = "",
        phpVersion: str = "",
    ) -> str:
        """Install a deployment package to a site.

        Args:
            server: Server name (optional)
            id: Deployment package ID
            siteName: Target site domain name
            phpVersion: PHP version to use
        """
        client = client_manager.get_client(server or None)
        params = {"id": id, "siteName": siteName, "php_version": phpVersion}
        data = client.request("/deployment?action=SetupPackage", params)
        return format_response(data)

    @mcp.tool()
    def deployment_get_speed(server: str = "", id: str = "") -> str:
        """Get deployment progress for an ongoing installation.

        Args:
            server: Server name (optional)
            id: Deployment task ID
        """
        client = client_manager.get_client(server or None)
        params = {"id": id}
        data = client.request("/deployment?action=GetSpeed", params)
        return format_response(data)
