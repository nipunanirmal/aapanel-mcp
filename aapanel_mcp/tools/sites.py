"""Site management tools for aaPanel MCP server."""

from mcp.server.fastmcp import FastMCP
from ..client import client_manager
from ..utils import format_response


def register_site_tools(mcp: FastMCP) -> None:
    """Register all website management tools."""

    @mcp.tool()
    def site_list(
        server: str = "",
        page: int = 1,
        limit: int = 100,
        search: str = "",
    ) -> str:
        """List all websites on the panel.

        Args:
            server: Server name (optional)
            page: Page number (default 1)
            limit: Items per page (default 100)
            search: Search keyword (optional)
        """
        client = client_manager.get_client(server or None)
        params = {"table": "sites", "type": "-1", "search": search, "p": page, "limit": limit, "order": ""}
        data = client.request("/data?action=getData", params)
        return format_response(data)

    @mcp.tool()
    def site_create(
        server: str = "",
        webname: str = "",
        path: str = "",
        type_id: str = "0",
        version: str = "",
        port: str = "80",
        ps: str = "",
        ssl: str = "0",
    ) -> str:
        """Create a new website.

        Args:
            server: Server name (optional)
            webname: Domain name(s), comma-separated for multiple
            path: Site root directory path
            type_id: Site type (0=PHP, 1=Proxy, 2=Static)
            version: PHP version (e.g. 74, 80, 81, 82, 83)
            port: Site port (default 80)
            ps: Site remark/description
            ssl: Enable SSL (0=no, 1=yes)
        """
        client = client_manager.get_client(server or None)
        params = {
            "webname": webname,
            "path": path,
            "type_id": type_id,
            "version": version,
            "port": port,
            "ps": ps,
            "ssl": ssl,
        }
        data = client.request("/site?action=AddSite", params)
        return format_response(data)

    @mcp.tool()
    def site_delete(server: str = "", id: str = "", webname: str = "") -> str:
        """Delete a website.

        Args:
            server: Server name (optional)
            id: Site ID
            webname: Site domain name
        """
        client = client_manager.get_client(server or None)
        params = {"id": id, "webname": webname}
        data = client.request("/site?action=DeleteSite", params)
        return format_response(data)

    @mcp.tool()
    def site_stop(server: str = "", id: str = "", name: str = "") -> str:
        """Stop a website.

        Args:
            server: Server name (optional)
            id: Site ID
            name: Site domain name
        """
        client = client_manager.get_client(server or None)
        params = {"id": id, "name": name}
        data = client.request("/site?action=SiteStop", params)
        return format_response(data)

    @mcp.tool()
    def site_start(server: str = "", id: str = "", name: str = "") -> str:
        """Start a website.

        Args:
            server: Server name (optional)
            id: Site ID
            name: Site domain name
        """
        client = client_manager.get_client(server or None)
        params = {"id": id, "name": name}
        data = client.request("/site?action=SiteStart", params)
        return format_response(data)

    @mcp.tool()
    def site_get_domains(server: str = "", id: str = "") -> str:
        """List all domains bound to a site.

        Args:
            server: Server name (optional)
            id: Site ID
        """
        client = client_manager.get_client(server or None)
        params = {"id": id}
        data = client.request("/site?action=get_site_domains", params)
        return format_response(data)

    @mcp.tool()
    def site_add_domain(server: str = "", id: str = "", domain: str = "") -> str:
        """Add a domain to an existing site.

        Args:
            server: Server name (optional)
            id: Site ID
            domain: Domain name to add
        """
        client = client_manager.get_client(server or None)
        params = {"id": id, "webname": domain, "domain": domain}
        data = client.request("/site?action=AddDomain", params)
        return format_response(data)

    @mcp.tool()
    def site_delete_domain(server: str = "", id: str = "", domain: str = "") -> str:
        """Remove a domain from a site.

        Args:
            server: Server name (optional)
            id: Site ID
            domain: Domain name to remove
        """
        client = client_manager.get_client(server or None)
        params = {"id": id, "domain": domain}
        data = client.request("/site?action=DelDomain", params)
        return format_response(data)

    @mcp.tool()
    def site_set_ssl(
        server: str = "",
        siteName: str = "",
        key: str = "",
        csr: str = "",
    ) -> str:
        """Deploy SSL certificate to a site.

        Args:
            server: Server name (optional)
            siteName: Site domain name
            key: SSL private key content
            csr: SSL certificate content
        """
        client = client_manager.get_client(server or None)
        params = {"siteName": siteName, "key": key, "csr": csr}
        data = client.request("/site?action=SetSSL", params)
        return format_response(data)

    @mcp.tool()
    def site_get_ssl(server: str = "", siteName: str = "") -> str:
        """Get SSL certificate status for a site.

        Args:
            server: Server name (optional)
            siteName: Site domain name
        """
        client = client_manager.get_client(server or None)
        params = {"siteName": siteName}
        data = client.request("/site?action=GetSSL", params)
        return format_response(data)

    @mcp.tool()
    def site_set_redirect(
        server: str = "",
        sitename: str = "",
        redirectname: str = "",
        redirecttype: str = "301",
        redirectpath: str = "/",
        redirecturl: str = "",
    ) -> str:
        """Set URL redirect for a site.

        Args:
            server: Server name (optional)
            sitename: Site domain name
            redirectname: Redirect rule name
            redirecttype: Redirect type (301 or 302)
            redirectpath: Source path (default /)
            redirecturl: Target URL
        """
        client = client_manager.get_client(server or None)
        params = {
            "sitename": sitename,
            "redirectname": redirectname,
            "redirecttype": redirecttype,
            "redirectpath": redirectpath,
            "redirecturl": redirecturl,
        }
        data = client.request("/site?action=CreateRedirect", params)
        return format_response(data)

    @mcp.tool()
    def site_set_proxy(
        server: str = "",
        sitename: str = "",
        proxyname: str = "",
        proxyurl: str = "",
        proxydir: str = "/",
        type: str = "1",
    ) -> str:
        """Set reverse proxy for a site.

        Args:
            server: Server name (optional)
            sitename: Site domain name
            proxyname: Proxy rule name
            proxyurl: Target URL to proxy to
            proxydir: Directory to proxy (default /)
            type: Proxy type (1=proxy, 0=disable)
        """
        client = client_manager.get_client(server or None)
        params = {
            "sitename": sitename,
            "proxyname": proxyname,
            "proxyurl": proxyurl,
            "proxydir": proxydir,
            "type": type,
        }
        data = client.request("/site?action=CreateProxy", params)
        return format_response(data)

    @mcp.tool()
    def site_get_logs(server: str = "", siteName: str = "") -> str:
        """Get site access and error logs.

        Args:
            server: Server name (optional)
            siteName: Site domain name
        """
        client = client_manager.get_client(server or None)
        params = {"siteName": siteName}
        data = client.request("/site?action=GetSiteLogs", params)
        return format_response(data)

    @mcp.tool()
    def site_backup(server: str = "", id: str = "") -> str:
        """Create a backup of a website.

        Args:
            server: Server name (optional)
            id: Site ID
        """
        client = client_manager.get_client(server or None)
        params = {"id": id}
        data = client.request("/site?action=ToBackup", params)
        return format_response(data)

    @mcp.tool()
    def site_get_backup_list(server: str = "", id: str = "") -> str:
        """List website backups.

        Args:
            server: Server name (optional)
            id: Site ID
        """
        client = client_manager.get_client(server or None)
        params = {"table": "backup", "p": 1, "limit": 100, "search": id}
        data = client.request("/data?action=getData", params)
        return format_response(data)

    @mcp.tool()
    def site_set_php_version(server: str = "", id: str = "", version: str = "") -> str:
        """Change PHP version for a site.

        Args:
            server: Server name (optional)
            id: Site ID
            version: PHP version (e.g. 74, 80, 81, 82, 83)
        """
        client = client_manager.get_client(server or None)
        params = {"id": id, "version": version}
        data = client.request("/site?action=SetPHPVersion", params)
        return format_response(data)

    @mcp.tool()
    def site_set_password(
        server: str = "",
        sitename: str = "",
        username: str = "",
        password: str = "",
    ) -> str:
        """Set HTTP basic access password for a site.

        Args:
            server: Server name (optional)
            sitename: Site domain name
            username: Access username
            password: Access password
        """
        client = client_manager.get_client(server or None)
        params = {"sitename": sitename, "username": username, "password": password}
        data = client.request("/site?action=SetHasPwd", params)
        return format_response(data)

    @mcp.tool()
    def site_get_config(server: str = "", id: str = "") -> str:
        """Get site configuration.

        Args:
            server: Server name (optional)
            id: Site ID
        """
        client = client_manager.get_client(server or None)
        params = {"id": id}
        data = client.request("/site?action=GetIndex", params)
        return format_response(data)

    @mcp.tool()
    def site_get_traffic_stats(server: str = "", siteId: str = "") -> str:
        """Get traffic statistics for a site.

        Args:
            server: Server name (optional)
            siteId: Site ID
        """
        client = client_manager.get_client(server or None)
        params = {"siteId": siteId}
        data = client.request("/site?action=GetLimitNet", params)
        return format_response(data)
