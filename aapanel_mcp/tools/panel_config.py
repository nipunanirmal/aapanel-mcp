"""Panel configuration tools for aaPanel MCP server."""

from mcp.server.fastmcp import FastMCP
from ..client import client_manager
from ..utils import format_response, request_compat


def register_config_tools(mcp: FastMCP) -> None:
    """Register all panel configuration tools."""

    @mcp.tool()
    def config_get_settings(server: str = "") -> str:
        """Get panel configuration settings.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/config?action=get_config")
        return format_response(data)

    @mcp.tool()
    def config_set_password(server: str = "", password1: str = "", password2: str = "") -> str:
        """Change the panel admin password.

        Args:
            server: Server name (optional)
            password1: New password
            password2: Confirm new password
        """
        client = client_manager.get_client(server or None)
        params = {"password1": password1, "password2": password2 or password1}
        data = client.request("/config?action=setPassword", params)
        return format_response(data)

    @mcp.tool()
    def config_set_username(server: str = "", username: str = "") -> str:
        """Change the panel admin username.

        Args:
            server: Server name (optional)
            username: New username
        """
        client = client_manager.get_client(server or None)
        params = {"username1": username, "username2": username, "username": username}
        data = client.request("/config?action=setUsername", params)
        return format_response(data)

    @mcp.tool()
    def config_get_panel_ssl(server: str = "") -> str:
        """Get panel SSL configuration status.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = request_compat(
            client,
            ["/config?action=GetPanelSSL", "/ssl?action=GetPanelSSL"],
        )
        return format_response(data)

    @mcp.tool()
    def config_save_panel_ssl(
        server: str = "",
        key: str = "",
        csr: str = "",
    ) -> str:
        """Configure SSL for the panel itself.

        Args:
            server: Server name (optional)
            key: Private key content
            csr: Certificate content
        """
        client = client_manager.get_client(server or None)
        params = {"privateKey": key, "certPem": csr, "key": key, "csr": csr}
        data = request_compat(
            client,
            ["/config?action=SavePanelSSL", "/ssl?action=SavePanelSSL"],
            params,
        )
        return format_response(data)

    @mcp.tool()
    def config_set_admin_path(server: str = "", admin_path: str = "") -> str:
        """Change the panel admin access path (security URL suffix).

        Args:
            server: Server name (optional)
            admin_path: New admin path (must start with /)
        """
        client = client_manager.get_client(server or None)
        params = {"admin_path": admin_path}
        data = client.request("/config?action=set_admin_path", params)
        return format_response(data)

    @mcp.tool()
    def config_set_basic_auth(
        server: str = "",
        open_basic_auth: str = "0",
        basic_user: str = "",
        basic_pwd: str = "",
    ) -> str:
        """Configure HTTP basic authentication for the panel.

        Args:
            server: Server name (optional)
            open_basic_auth: 1=enable, 0=disable
            basic_user: Basic auth username
            basic_pwd: Basic auth password
        """
        client = client_manager.get_client(server or None)
        is_open = "True" if str(open_basic_auth).lower() in ("1", "true") else "False"
        params = {
            "open": is_open,
            "open_basic_auth": open_basic_auth,
            "basic_user": basic_user,
            "basic_pwd": basic_pwd,
        }
        data = client.request("/config?action=set_basic_auth", params)
        return format_response(data)

    @mcp.tool()
    def config_get_users(server: str = "") -> str:
        """List panel users.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/config?action=get_users")
        return format_response(data)

    @mcp.tool()
    def config_set_debug(server: str = "", debug: str = "0") -> str:
        """Enable or disable panel debug mode.

        Args:
            server: Server name (optional)
            debug: 1=enable, 0=disable
        """
        client = client_manager.get_client(server or None)
        params = {"debug": debug}
        data = client.request("/config?action=set_debug", params)
        return format_response(data)

    @mcp.tool()
    def config_close_panel(server: str = "", confirmed: bool = False) -> str:
        """Close/disable the panel.

        Args:
            server: Server name (optional)
            confirmed: Must be True to confirm this destructive action
        """
        client = client_manager.get_client(server or None)
        data = client.request("/config?action=ClosePanel", confirmed=confirmed)
        return format_response(data)

    @mcp.tool()
    def config_get_login_log(server: str = "", page: int = 1, limit: int = 20) -> str:
        """Get panel login logs.

        Args:
            server: Server name (optional)
            page: Page number (default 1)
            limit: Items per page (default 20)
        """
        client = client_manager.get_client(server or None)
        params = {"p": page, "page": page, "limit": limit}
        data = client.request("/config?action=get_login_log", params)
        return format_response(data)

    @mcp.tool()
    def config_set_ip_whitelist(server: str = "", ips: str = "", action: str = "add") -> str:
        """Set or query IP whitelist for panel login notifications.

        Args:
            server: Server name (optional)
            ips: IP address(es), comma or newline-separated (empty to list current whitelist)
            action: Operation type (get, add, del, clear)
        """
        client = client_manager.get_client(server or None)
        if not ips and action == "add":
            action = "get"
        if action in ("get", "clear"):
            return format_response(client.request("/config?action=login_ipwhite", {"type": action}))
        ip_list = [ip.strip() for ip in ips.replace(",", "\n").splitlines() if ip.strip()]
        results = []
        for ip in ip_list:
            results.append(client.request("/config?action=login_ipwhite", {"type": action, "ip": ip}))
        return format_response(results[0] if len(results) == 1 else results)

    @mcp.tool()
    def config_get_api_config(server: str = "") -> str:
        """Get API interface configuration.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/config?action=get_token")
        return format_response(data)

    @mcp.tool()
    def config_set_api_token(
        server: str = "",
        token: str = "",
        limit_ip: str = "",
    ) -> str:
        """Regenerate API token and configure IP limits.

        Args:
            server: Server name (optional)
            token: Action type ('1'=regenerate token, '2'=toggle API, '3'=set IP limits) or empty
            limit_ip: IP addresses allowed to use API (one per line)
        """
        client = client_manager.get_client(server or None)
        t_type = token if token in ("1", "2", "3") else ("3" if limit_ip else "1")
        params = {"t_type": t_type, "token": token, "limit_addr": limit_ip, "limit_ip": limit_ip}
        data = client.request("/config?action=set_token", params)
        return format_response(data)
