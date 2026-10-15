"""Deployment tools for aaPanel MCP server."""

from mcp.server.fastmcp import FastMCP
from ..client import client_manager
from ..utils import format_response, request_compat


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
        params = {"p": page, "limit": limit}
        data = request_compat(
            client,
            ["/v2/deployment?action=GetList", "/deployment?action=GetList"],
            params,
        )
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
            id: Deployment package name or ID (e.g. WordPress, Drupal, Laravel)
            siteName: Target site domain name
            phpVersion: PHP version to use
        """
        client = client_manager.get_client(server or None)
        params = {
            "dname": id,
            "id": id,
            "site_name": siteName,
            "siteName": siteName,
            "php_version": phpVersion,
        }
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
