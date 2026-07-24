"""Database management tools for aaPanel MCP server."""

from mcp.server.fastmcp import FastMCP
from ..client import client_manager
from ..utils import format_response


def register_database_tools(mcp: FastMCP) -> None:
    """Register all database management tools."""

    @mcp.tool()
    def database_list(server: str = "", page: int = 1, limit: int = 100) -> str:
        """List all databases on the panel.

        Args:
            server: Server name (optional)
            page: Page number (default 1)
            limit: Items per page (default 100)
        """
        client = client_manager.get_client(server or None)
        params = {"table": "databases", "p": page, "limit": limit}
        data = client.request("/data?action=getData", params)
        return format_response(data)

    @mcp.tool()
    def database_create(
        server: str = "",
        name: str = "",
        username: str = "",
        password: str = "",
        ps: str = "",
        access: str = "127.0.0.1",
    ) -> str:
        """Create a new database.

        Args:
            server: Server name (optional)
            name: Database name
            username: Database username
            password: Database password
            ps: Database remark/description
            access: Access permission (127.0.0.1 for local, % for all)
        """
        client = client_manager.get_client(server or None)
        params = {
            "name": name,
            "db_user": username,
            "password": password,
            "ps": ps,
            "access": access,
        }
        data = client.request("/database?action=AddDatabase", params)
        return format_response(data)

    @mcp.tool()
    def database_delete(server: str = "", id: str = "", name: str = "") -> str:
        """Delete a database.

        Args:
            server: Server name (optional)
            id: Database ID
            name: Database name
        """
        client = client_manager.get_client(server or None)
        params = {"id": id, "name": name}
        data = client.request("/database?action=DeleteDatabase", params)
        return format_response(data)

    @mcp.tool()
    def database_set_password(
        server: str = "",
        id: str = "",
        name: str = "",
        password: str = "",
    ) -> str:
        """Change database password.

        Args:
            server: Server name (optional)
            id: Database ID
            name: Database name
            password: New password
        """
        client = client_manager.get_client(server or None)
        params = {"id": id, "name": name, "password": password}
        data = client.request("/database?action=ResDatabasePassword", params)
        return format_response(data)

    @mcp.tool()
    def database_backup(server: str = "", id: str = "") -> str:
        """Backup a database.

        Args:
            server: Server name (optional)
            id: Database ID
        """
        client = client_manager.get_client(server or None)
        params = {"id": id}
        data = client.request("/database?action=ToBackup", params)
        return format_response(data)

    @mcp.tool()
    def database_get_backups(server: str = "", id: str = "") -> str:
        """List database backups.

        Args:
            server: Server name (optional)
            id: Database ID
        """
        client = client_manager.get_client(server or None)
        params = {"table": "backup", "p": 1, "limit": 100, "search": id}
        data = client.request("/data?action=getData", params)
        return format_response(data)

    @mcp.tool()
    def database_delete_backup(server: str = "", id: str = "") -> str:
        """Delete a database backup.

        Args:
            server: Server name (optional)
            id: Backup ID
        """
        client = client_manager.get_client(server or None)
        params = {"id": id}
        data = client.request("/database?action=DelBackup", params)
        return format_response(data)

    @mcp.tool()
    def database_set_access(server: str = "", name: str = "", access: str = "127.0.0.1") -> str:
        """Set database access permissions.

        Args:
            server: Server name (optional)
            name: Database name
            access: Access permission (127.0.0.1 for local, % for all hosts)
        """
        client = client_manager.get_client(server or None)
        params = {"name": name, "access": access}
        data = client.request("/database?action=SetDatabaseAccess", params)
        return format_response(data)

    @mcp.tool()
    def database_get_mysql_status(server: str = "") -> str:
        """Get MySQL server status.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/database?action=GetRunStatus")
        return format_response(data)

    @mcp.tool()
    def database_get_error_log(server: str = "") -> str:
        """Get MySQL error log.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/database?action=GetErrorLog")
        return format_response(data)

    @mcp.tool()
    def database_get_slow_log(server: str = "") -> str:
        """Get MySQL slow query log.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/database?action=GetSlowLogs")
        return format_response(data)

    @mcp.tool()
    def database_get_info(server: str = "", id: str = "") -> str:
        """Get database details.

        Args:
            server: Server name (optional)
            id: Database ID
        """
        client = client_manager.get_client(server or None)
        params = {"table": "databases", "p": 1, "limit": 100}
        data = client.request("/data?action=getData", params)
        if isinstance(data, dict) and "data" in data and id:
            filtered = [d for d in data["data"] if str(d.get("id")) == str(id)]
            data["data"] = filtered
        return format_response(data)
