"""Site management tools for aaPanel MCP server."""

import json
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
        raw_webname = webname.strip()
        if raw_webname and not raw_webname.startswith("{"):
            domains = [d.strip() for d in raw_webname.split(",") if d.strip()]
            primary = domains[0] if domains else ""
            domainlist = domains[1:] if len(domains) > 1 else []
            raw_webname = json.dumps({
                "domain": primary,
                "domainlist": domainlist,
                "count": len(domainlist),
            })
        params = {
            "webname": raw_webname,
            "path": path,
            "type_id": type_id,
            "type": "PHP",
            "version": version or "00",
            "port": port,
            "ps": ps or webname,
            "ftp": "false",
            "sql": "false",
            "codeing": "utf8",
            "ssl": ssl,
        }
        data = client.request("/site?action=AddSite", params)
        return format_response(data)

    @mcp.tool()
    def site_delete(server: str = "", id: str = "", webname: str = "", confirmed: bool = False) -> str:
        """Delete a website.

        Args:
            server: Server name (optional)
            id: Site ID
            webname: Site domain name
            confirmed: Must be True to confirm this destructive action
        """
        client = client_manager.get_client(server or None)
        params = {"id": id, "webname": webname, "path": "0"}
        data = client.request("/site?action=DeleteSite", params, confirmed=confirmed)
        return format_response(data)

    @mcp.tool()
    def site_stop(server: str = "", id: str = "", name: str = "", confirmed: bool = False) -> str:
        """Stop a website.

        Args:
            server: Server name (optional)
            id: Site ID
            name: Site domain name
            confirmed: Must be True to confirm this destructive action
        """
        client = client_manager.get_client(server or None)
        params = {"id": id, "name": name}
        data = client.request("/site?action=SiteStop", params, confirmed=confirmed)
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
        data = client.request("/site?action=GetSiteDomains", params)
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
    def site_delete_domain(
        server: str = "",
        id: str = "",
        domain: str = "",
        port: str = "80",
        webname: str = "",
        confirmed: bool = False,
    ) -> str:
        """Remove a domain from a site.

        Args:
            server: Server name (optional)
            id: Site ID
            domain: Domain name to remove
            port: Domain port (default 80)
            webname: Primary site name (optional, resolved from ID if omitted)
            confirmed: Must be True to confirm this destructive action
        """
        client = client_manager.get_client(server or None)
        site_name = webname or domain
        if id and not webname and confirmed:
            sites_data = client.request("/data?action=getData", {"table": "sites", "p": 1, "limit": 200})
            if isinstance(sites_data, dict):
                for s in sites_data.get("data", []):
                    if str(s.get("id")) == str(id):
                        site_name = s.get("name", site_name)
                        break
        params = {"id": id, "domain": domain, "port": port, "webname": site_name}
        data = client.request("/site?action=DelDomain", params, confirmed=confirmed)
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
        params = {"type": "1", "siteName": siteName, "key": key, "csr": csr}
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
            "redirectname": redirectname or f"redirect_{sitename}",
            "tourl": redirecturl,
            "redirectdomain": json.dumps([sitename] if sitename else []),
            "redirectpath": redirectpath,
            "redirecttype": redirecttype,
            "type": "1",
            "domainorpath": "path" if redirectpath and redirectpath != "/" else "domain",
            "holdpath": "1",
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
        todomain = "$host"
        if proxyurl and "://" in proxyurl:
            todomain = proxyurl.split("://", 1)[1].split("/", 1)[0]
        params = {
            "sitename": sitename,
            "proxyname": proxyname or f"proxy_{sitename}",
            "proxysite": proxyurl,
            "todomain": todomain,
            "proxydir": proxydir,
            "type": type,
            "cache": "0",
            "cachetime": "1",
            "advanced": "0",
            "subfilter": json.dumps([
                {"sub1": "", "sub2": ""},
                {"sub1": "", "sub2": ""},
                {"sub1": "", "sub2": ""},
            ]),
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
        params = {"table": "backup", "type": "0", "p": 1, "limit": 100, "search": id}
        data = client.request("/data?action=getData", params)
        return format_response(data)

    @mcp.tool()
    def site_set_php_version(
        server: str = "",
        id: str = "",
        version: str = "",
        siteName: str = "",
    ) -> str:
        """Change PHP version for a site.

        Args:
            server: Server name (optional)
            id: Site ID (or site domain name)
            version: PHP version (e.g. 74, 80, 81, 82, 83)
            siteName: Site domain name (optional if id is provided)
        """
        client = client_manager.get_client(server or None)
        resolved_name = siteName
        if not resolved_name and id:
            if "." in id:
                resolved_name = id
            else:
                sites_data = client.request("/data?action=getData", {"table": "sites", "p": 1, "limit": 200})
                if isinstance(sites_data, dict):
                    for s in sites_data.get("data", []):
                        if str(s.get("id")) == str(id):
                            resolved_name = s.get("name", "")
                            break
        params = {"id": id, "siteName": resolved_name, "version": version}
        data = client.request("/site?action=SetPHPVersion", params)
        return format_response(data)

    @mcp.tool()
    def site_set_password(
        server: str = "",
        sitename: str = "",
        username: str = "",
        password: str = "",
        id: str = "",
    ) -> str:
        """Set HTTP basic access password for a site.

        Args:
            server: Server name (optional)
            sitename: Site domain name
            username: Access username
            password: Access password
            id: Site ID (optional if sitename is provided)
        """
        client = client_manager.get_client(server or None)
        params = {"id": id, "siteName": sitename, "sitename": sitename, "username": username, "password": password}
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
        params = {"id": siteId, "siteId": siteId}
        data = client.request("/site?action=GetLimitNet", params)
        return format_response(data)
