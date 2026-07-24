"""Log management tools for aaPanel MCP server."""

from mcp.server.fastmcp import FastMCP
from ..client import client_manager
from ..utils import format_response


def register_log_tools(mcp: FastMCP) -> None:
    """Register all log management tools."""

    @mcp.tool()
    def logs_get_panel_logs(
        server: str = "",
        page: int = 1,
        limit: int = 20,
    ) -> str:
        """Get panel operation logs.

        Args:
            server: Server name (optional)
            page: Page number (default 1)
            limit: Items per page (default 20)
        """
        client = client_manager.get_client(server or None)
        params = {"table": "logs", "p": page, "limit": limit}
        data = client.request("/data?action=getData", params)
        return format_response(data)

    @mcp.tool()
    def logs_get_security_logs(
        server: str = "",
        page: int = 1,
        limit: int = 20,
    ) -> str:
        """Get security logs.

        Args:
            server: Server name (optional)
            page: Page number (default 1)
            limit: Items per page (default 20)
        """
        client = client_manager.get_client(server or None)
        params = {"page": page, "limit": limit}
        data = client.request("/ssh_security?action=get_logs", params)
        return format_response(data)

    @mcp.tool()
    def logs_get_error_logs(server: str = "", siteName: str = "") -> str:
        """Get error logs for a site.

        Args:
            server: Server name (optional)
            siteName: Site domain name
        """
        client = client_manager.get_client(server or None)
        params = {"siteName": siteName}
        data = client.request("/site?action=get_site_err_log", params)
        return format_response(data)

    @mcp.tool()
    def logs_get_site_logs(server: str = "", siteName: str = "") -> str:
        """Get access logs for a site.

        Args:
            server: Server name (optional)
            siteName: Site domain name
        """
        client = client_manager.get_client(server or None)
        params = {"siteName": siteName}
        data = client.request("/site?action=GetSiteLogs", params)
        return format_response(data)

    @mcp.tool()
    def logs_get_nginx_log(
        server: str = "",
        log_type: str = "error",
    ) -> str:
        """Read Nginx log file.

        Args:
            server: Server name (optional)
            log_type: Log type (error or access)
        """
        client = client_manager.get_client(server or None)
        log_path = "/www/server/nginx/logs/error.log" if log_type == "error" else "/www/wwwlogs/nginx.log"
        params = {"path": log_path}
        data = client.request("/files?action=GetFileBody", params)
        return format_response(data)

    @mcp.tool()
    def logs_get_apache_log(
        server: str = "",
        log_type: str = "error",
    ) -> str:
        """Read Apache log file.

        Args:
            server: Server name (optional)
            log_type: Log type (error or access)
        """
        client = client_manager.get_client(server or None)
        log_path = "/www/wwwlogs/error_log" if log_type == "error" else "/www/wwwlogs/access_log"
        params = {"path": log_path}
        data = client.request("/files?action=GetFileBody", params)
        return format_response(data)

    @mcp.tool()
    def logs_get_redis_log(server: str = "") -> str:
        """Read Redis log file.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        params = {"path": "/www/server/redis/redis.log"}
        data = client.request("/files?action=GetFileBody", params)
        return format_response(data)

    @mcp.tool()
    def logs_get_panel_log_file(server: str = "") -> str:
        """Read the aaPanel system log file.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        params = {"path": "/www/server/panel/data/error.log"}
        data = client.request("/files?action=GetFileBody", params)
        return format_response(data)
