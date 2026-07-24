"""Crontab management tools for aaPanel MCP server."""

from mcp.server.fastmcp import FastMCP
from ..client import client_manager
from ..utils import format_response


def register_crontab_tools(mcp: FastMCP) -> None:
    """Register all crontab management tools."""

    @mcp.tool()
    def crontab_list(
        server: str = "",
        page: int = 1,
        limit: int = 100,
        search: str = "",
    ) -> str:
        """List all cron jobs.

        Args:
            server: Server name (optional)
            page: Page number (default 1)
            limit: Items per page (default 100)
            search: Search keyword (optional)
        """
        client = client_manager.get_client(server or None)
        params = {"p": page, "count": limit, "search": search, "type_id": "", "order_param": ""}
        data = client.request("/crontab?action=GetCrontab", params)
        return format_response(data)

    @mcp.tool()
    def crontab_create(
        server: str = "",
        name: str = "",
        type: str = "day",
        where1: str = "",
        hour: str = "0",
        minute: str = "0",
        week: str = "1",
        sType: str = "toShell",
        sBody: str = "",
        sName: str = "",
        sFile: str = "",
        backupTo: str = "localhost",
        save: str = "3",
        urladdress: str = "",
    ) -> str:
        """Create a new cron job.

        Args:
            server: Server name (optional)
            name: Task name
            type: Schedule type (day, week, month, hour, minute, nminute, etc.)
            where1: Day of month (for month type)
            hour: Hour (0-23)
            minute: Minute (0-59)
            week: Day of week (1-7, for week type)
            sType: Task type (toShell, site, database, path, url, etc.)
            sBody: Shell command or script content
            sName: Site/database name (for backup tasks)
            sFile: File path (for path backup)
            backupTo: Backup destination (localhost, remote server path)
            save: Number of backup copies to keep
            urladdress: URL (for URL tasks)
        """
        client = client_manager.get_client(server or None)
        params = {
            "name": name,
            "type": type,
            "where1": where1,
            "hour": hour,
            "minute": minute,
            "week": week,
            "sType": sType,
            "sBody": sBody,
            "sName": sName,
            "sFile": sFile,
            "backupTo": backupTo,
            "save": save,
            "urladdress": urladdress,
        }
        data = client.request("/crontab?action=AddCrontab", params)
        return format_response(data)

    @mcp.tool()
    def crontab_delete(server: str = "", id: str = "") -> str:
        """Delete a cron job.

        Args:
            server: Server name (optional)
            id: Cron job ID
        """
        client = client_manager.get_client(server or None)
        params = {"id": id}
        data = client.request("/crontab?action=DelCrontab", params)
        return format_response(data)

    @mcp.tool()
    def crontab_modify(
        server: str = "",
        id: str = "",
        name: str = "",
        type: str = "day",
        where1: str = "",
        hour: str = "0",
        minute: str = "0",
        week: str = "1",
        sType: str = "toShell",
        sBody: str = "",
        sName: str = "",
        sFile: str = "",
        backupTo: str = "localhost",
        save: str = "3",
        urladdress: str = "",
    ) -> str:
        """Modify an existing cron job.

        Args:
            server: Server name (optional)
            id: Cron job ID
            (other params same as crontab_create)
        """
        client = client_manager.get_client(server or None)
        params = {
            "id": id,
            "name": name,
            "type": type,
            "where1": where1,
            "hour": hour,
            "minute": minute,
            "week": week,
            "sType": sType,
            "sBody": sBody,
            "sName": sName,
            "sFile": sFile,
            "backupTo": backupTo,
            "save": save,
            "urladdress": urladdress,
        }
        data = client.request("/crontab?action=modify_crond", params)
        return format_response(data)

    @mcp.tool()
    def crontab_start(server: str = "", id: str = "") -> str:
        """Execute a cron job immediately.

        Args:
            server: Server name (optional)
            id: Cron job ID
        """
        client = client_manager.get_client(server or None)
        params = {"id": id}
        data = client.request("/crontab?action=StartTask", params)
        return format_response(data)

    @mcp.tool()
    def crontab_get_logs(server: str = "", id: str = "") -> str:
        """Get execution logs for a cron job.

        Args:
            server: Server name (optional)
            id: Cron job ID
        """
        client = client_manager.get_client(server or None)
        params = {"id": id}
        data = client.request("/crontab?action=GetLogs", params)
        return format_response(data)

    @mcp.tool()
    def crontab_get_backup_list(server: str = "", id: str = "", search: str = "") -> str:
        """Get backup list for a cron job.

        Args:
            server: Server name (optional)
            id: Cron job ID
            search: Search keyword (optional)
        """
        client = client_manager.get_client(server or None)
        params = {"id": id, "search": search}
        data = client.request("/crontab?action=get_backup_list", params)
        return format_response(data)
