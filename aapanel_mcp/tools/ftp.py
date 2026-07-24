"""FTP management tools for aaPanel MCP server."""

from mcp.server.fastmcp import FastMCP
from ..client import client_manager
from ..utils import format_response


def register_ftp_tools(mcp: FastMCP) -> None:
    """Register all FTP management tools."""

    @mcp.tool()
    def ftp_list(server: str = "", page: int = 1, limit: int = 100) -> str:
        """List all FTP users.

        Args:
            server: Server name (optional)
            page: Page number (default 1)
            limit: Items per page (default 100)
        """
        client = client_manager.get_client(server or None)
        params = {"table": "ftps", "p": page, "limit": limit}
        data = client.request("/data?action=getData", params)
        return format_response(data)

    @mcp.tool()
    def ftp_create(
        server: str = "",
        username: str = "",
        password: str = "",
        path: str = "",
        ps: str = "",
    ) -> str:
        """Create a new FTP user.

        Args:
            server: Server name (optional)
            username: FTP username
            password: FTP password
            path: Home directory path for the FTP user
            ps: Remark/description
        """
        client = client_manager.get_client(server or None)
        params = {"ftp_username": username, "ftp_password": password, "path": path, "ps": ps}
        data = client.request("/ftp?action=AddUser", params)
        return format_response(data)

    @mcp.tool()
    def ftp_delete(server: str = "", id: str = "", username: str = "") -> str:
        """Delete an FTP user.

        Args:
            server: Server name (optional)
            id: FTP user ID
            username: FTP username
        """
        client = client_manager.get_client(server or None)
        params = {"id": id, "username": username}
        data = client.request("/ftp?action=DeleteUser", params)
        return format_response(data)

    @mcp.tool()
    def ftp_set_password(
        server: str = "",
        id: str = "",
        username: str = "",
        password: str = "",
    ) -> str:
        """Change FTP user password.

        Args:
            server: Server name (optional)
            id: FTP user ID
            username: FTP username
            password: New password
        """
        client = client_manager.get_client(server or None)
        params = {"id": id, "username": username, "password": password}
        data = client.request("/ftp?action=SetUserPassword", params)
        return format_response(data)

    @mcp.tool()
    def ftp_set_status(server: str = "", id: str = "", username: str = "", status: str = "1") -> str:
        """Enable or disable an FTP user.

        Args:
            server: Server name (optional)
            id: FTP user ID
            username: FTP username
            status: 1=enable, 0=disable
        """
        client = client_manager.get_client(server or None)
        params = {"id": id, "username": username, "status": status}
        data = client.request("/ftp?action=SetStatus", params)
        return format_response(data)
