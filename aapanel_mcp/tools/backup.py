"""Backup and task management tools for aaPanel MCP server."""

from mcp.server.fastmcp import FastMCP
from ..client import client_manager
from ..utils import format_response


def register_backup_tools(mcp: FastMCP) -> None:
    """Register all backup and task management tools."""

    @mcp.tool()
    def backup_list(
        server: str = "",
        type: str = "site",
        page: int = 1,
        limit: int = 100,
    ) -> str:
        """List all backups.

        Args:
            server: Server name (optional)
            type: Backup type (site, database, path)
            page: Page number (default 1)
            limit: Items per page (default 100)
        """
        client = client_manager.get_client(server or None)
        type_map = {"site": "0", "database": "1", "path": "2"}
        params = {"table": "backup", "p": page, "limit": limit}
        if type in type_map:
            params["type"] = type_map[type]
        data = client.request("/data?action=getData", params)
        return format_response(data)

    @mcp.tool()
    def backup_create(
        server: str = "",
        type: str = "site",
        id: str = "",
        name: str = "",
    ) -> str:
        """Create a backup.

        Args:
            server: Server name (optional)
            type: Backup type (site, database, path)
            id: Target ID (site ID or database ID)
            name: Target name (or directory path for path backup)
        """
        client = client_manager.get_client(server or None)
        if type == "database":
            if id:
                return format_response(client.request("/database?action=ToBackup", {"id": id}))
            return format_response(client.request("/bak?action=backup_database", {"name": name}))
        if type == "path":
            return format_response(client.request("/bak?action=backup_path", {"path": name or id}))
        if id:
            return format_response(client.request("/site?action=ToBackup", {"id": id}))
        return format_response(client.request("/bak?action=backup_site", {"name": name}))

    @mcp.tool()
    def backup_delete(server: str = "", id: str = "", confirmed: bool = False) -> str:
        """Delete a backup.

        Args:
            server: Server name (optional)
            id: Backup ID
            confirmed: Must be True to confirm this destructive action
        """
        client = client_manager.get_client(server or None)
        params = {"id": id}
        data = client.request("/site?action=DelBackup", params, confirmed=confirmed)
        return format_response(data)

    @mcp.tool()
    def task_list(server: str = "") -> str:
        """List background tasks.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/task?action=get_task_lists")
        return format_response(data)

    @mcp.tool()
    def task_get_info(server: str = "", id: str = "") -> str:
        """Get background task details.

        Args:
            server: Server name (optional)
            id: Task ID
        """
        client = client_manager.get_client(server or None)
        params = {"table": "tasks", "id": id}
        data = client.request("/data?action=getFind", params)
        return format_response(data)

    @mcp.tool()
    def task_remove(server: str = "", id: str = "", confirmed: bool = False) -> str:
        """Remove/cancel a background task.

        Args:
            server: Server name (optional)
            id: Task ID
            confirmed: Must be True to confirm this destructive action
        """
        client = client_manager.get_client(server or None)
        params = {"id": id}
        data = client.request("/task?action=remove_task", params, confirmed=confirmed)
        return format_response(data)
