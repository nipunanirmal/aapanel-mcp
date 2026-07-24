"""Plugin/software management tools for aaPanel MCP server."""

from mcp.server.fastmcp import FastMCP
from ..client import client_manager
from ..utils import format_response


def register_plugin_tools(mcp: FastMCP) -> None:
    """Register all plugin and software management tools."""

    @mcp.tool()
    def plugin_list(
        server: str = "",
        type: str = "-1",
        query: str = "",
        page: int = 1,
        row: int = 30,
    ) -> str:
        """List installed software/plugins.

        Args:
            server: Server name (optional)
            type: Type filter (-1 for all)
            query: Search query (e.g. 'php', 'nginx')
            page: Page number (default 1)
            row: Items per page (default 30)
        """
        client = client_manager.get_client(server or None)
        params = {"type": type, "query": query, "p": page, "row": row, "force": 0}
        data = client.request("/plugin?action=get_soft_list", params)
        return format_response(data)

    @mcp.tool()
    def plugin_install(server: str = "", sName: str = "", version: str = "") -> str:
        """Install a software/plugin.

        Args:
            server: Server name (optional)
            sName: Software name (e.g. nginx, mysql, php-8.1)
            version: Version to install
        """
        client = client_manager.get_client(server or None)
        params = {"sName": sName, "version": version}
        data = client.request("/plugin?action=install_plugin", params)
        return format_response(data)

    @mcp.tool()
    def plugin_uninstall(server: str = "", sName: str = "", version: str = "") -> str:
        """Uninstall a software/plugin.

        Args:
            server: Server name (optional)
            sName: Software name
            version: Version to uninstall
        """
        client = client_manager.get_client(server or None)
        params = {"sName": sName, "version": version}
        data = client.request("/plugin?action=uninstall_plugin", params)
        return format_response(data)

    @mcp.tool()
    def plugin_get_info(server: str = "", sName: str = "") -> str:
        """Get information about a specific software/plugin.

        Args:
            server: Server name (optional)
            sName: Software name (e.g. nginx, apache, mysql, redis)
        """
        client = client_manager.get_client(server or None)
        params = {"sName": sName}
        data = client.request("/plugin?action=get_soft_find", params)
        return format_response(data)

    @mcp.tool()
    def plugin_get_installed_list(server: str = "") -> str:
        """List all installed plugins.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/plugin?action=getPluginList")
        return format_response(data)

    @mcp.tool()
    def plugin_set_status(
        server: str = "",
        sName: str = "",
        status: str = "1",
    ) -> str:
        """Enable or disable a plugin.

        Args:
            server: Server name (optional)
            sName: Plugin name
            status: 1=enable, 0=disable
        """
        client = client_manager.get_client(server or None)
        params = {"sName": sName, "status": status}
        data = client.request("/plugin?action=setPluginStatus", params)
        return format_response(data)

    @mcp.tool()
    def plugin_get_config(server: str = "", sName: str = "") -> str:
        """Get plugin configuration.

        Args:
            server: Server name (optional)
            sName: Plugin name
        """
        client = client_manager.get_client(server or None)
        params = {"sName": sName}
        data = client.request("/plugin?action=getPluginInfo", params)
        return format_response(data)

    @mcp.tool()
    def plugin_set_config(
        server: str = "",
        sName: str = "",
        config: str = "",
    ) -> str:
        """Set plugin configuration.

        Args:
            server: Server name (optional)
            sName: Plugin name
            config: Configuration data (JSON string)
        """
        client = client_manager.get_client(server or None)
        params = {"sName": sName, "config": config}
        data = client.request("/plugin?action=set_make_args", params)
        return format_response(data)
