"""Firewall management tools for aaPanel MCP server."""

from mcp.server.fastmcp import FastMCP
from ..client import client_manager
from ..utils import format_response, request_compat


def register_firewall_tools(mcp: FastMCP) -> None:
    """Register all firewall management tools."""

    @mcp.tool()
    def firewall_get_list(server: str = "", page: int = 1, limit: int = 100) -> str:
        """List firewall rules (ports and IP rules).

        Args:
            server: Server name (optional)
            page: Page number (default 1)
            limit: Items per page (default 100)
        """
        client = client_manager.get_client(server or None)
        params = {"table": "firewall", "p": page, "limit": limit}
        data = client.request("/data?action=getData", params)
        return format_response(data)

    @mcp.tool()
    def firewall_add_port(
        server: str = "",
        port: str = "",
        type: str = "accept",
        ps: str = "",
    ) -> str:
        """Open a port in the firewall.

        Args:
            server: Server name (optional)
            port: Port number or range (e.g. 8080 or 3000-3100)
            type: Rule type (accept or drop)
            ps: Remark/description
        """
        client = client_manager.get_client(server or None)
        params = {"port": port, "type": type, "ps": ps}
        data = client.request("/firewall?action=AddAcceptPort", params)
        return format_response(data)

    @mcp.tool()
    def firewall_delete_port(
        server: str = "",
        id: str = "",
        port: str = "",
        confirmed: bool = False,
    ) -> str:
        """Close a port in the firewall.

        Args:
            server: Server name (optional)
            id: Rule ID to delete
            port: Port number (optional, resolved from ID if omitted)
            confirmed: Must be True to confirm this destructive action
        """
        client = client_manager.get_client(server or None)
        resolved_port = port
        if id and not resolved_port and confirmed:
            fw_data = client.request("/data?action=getData", {"table": "firewall", "p": 1, "limit": 200})
            if isinstance(fw_data, dict):
                for row in fw_data.get("data", []):
                    if str(row.get("id")) == str(id):
                        resolved_port = str(row.get("port", ""))
                        break
        params = {"id": id, "port": resolved_port}
        data = client.request("/firewall?action=DelAcceptPort", params, confirmed=confirmed)
        return format_response(data)

    @mcp.tool()
    def firewall_add_ip(
        server: str = "",
        ip: str = "",
        type: str = "accept",
        ps: str = "",
    ) -> str:
        """Add an IP rule to the firewall.

        Args:
            server: Server name (optional)
            ip: IP address or CIDR
            type: Rule type (accept or drop)
            ps: Remark/description
        """
        client = client_manager.get_client(server or None)
        params = {"port": ip, "ip": ip, "type": type, "ps": ps}
        data = client.request("/firewall?action=AddDropAddress", params)
        return format_response(data)

    @mcp.tool()
    def firewall_delete_ip(
        server: str = "",
        id: str = "",
        ip: str = "",
        confirmed: bool = False,
    ) -> str:
        """Remove an IP rule from the firewall.

        Args:
            server: Server name (optional)
            id: Rule ID to delete
            ip: IP address (optional, resolved from ID if omitted)
            confirmed: Must be True to confirm this destructive action
        """
        client = client_manager.get_client(server or None)
        resolved_ip = ip
        if id and not resolved_ip and confirmed:
            fw_data = client.request("/data?action=getData", {"table": "firewall", "p": 1, "limit": 200})
            if isinstance(fw_data, dict):
                for row in fw_data.get("data", []):
                    if str(row.get("id")) == str(id):
                        resolved_ip = str(row.get("port", ""))
                        break
        params = {"id": id, "port": resolved_ip, "ip": resolved_ip}
        data = client.request("/firewall?action=DelDropAddress", params, confirmed=confirmed)
        return format_response(data)

    @mcp.tool()
    def firewall_get_panel_port(server: str = "") -> str:
        """Get the current aaPanel access port.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/config?action=get_config")
        return format_response(data)

    @mcp.tool()
    def firewall_set_panel_port(server: str = "", port: str = "") -> str:
        """Change the aaPanel access port.

        Args:
            server: Server name (optional)
            port: New port number
        """
        client = client_manager.get_client(server or None)
        cfg = client.request("/config?action=get_config")
        panel = cfg.get("panel", {}) if isinstance(cfg, dict) else {}
        params = {
            "port": port,
            "webname": cfg.get("webname", "aaPanel Linux panel") if isinstance(cfg, dict) else "aaPanel Linux panel",
            "domain": panel.get("domain", ""),
            "address": panel.get("address", ""),
            "limitip": panel.get("limitip", ""),
            "backup_path": cfg.get("backup_path", "/www/backup") if isinstance(cfg, dict) else "/www/backup",
            "sites_path": cfg.get("sites_path", "/www/wwwroot") if isinstance(cfg, dict) else "/www/wwwroot",
        }
        data = client.request("/config?action=setPanel", params)
        return format_response(data)

    @mcp.tool()
    def firewall_get_status(server: str = "") -> str:
        """Get firewall status (enabled/disabled, type).

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = request_compat(
            client,
            ["/v2/firewall/com/get_firewall_info", "/data?action=getData"],
            {"table": "firewall", "p": 1, "limit": 100},
        )
        return format_response(data)
