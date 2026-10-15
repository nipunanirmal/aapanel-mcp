"""SSL certificate management tools for aaPanel MCP server."""

import json
from mcp.server.fastmcp import FastMCP
from ..client import client_manager
from ..utils import format_response, request_compat

# v8.0.7 v2 routes first, legacy /ssl routes as fallback
_SSL_LIST_ENDPOINTS = [
    "/v2/ssl_domain?action=list_ssl_info",
    "/ssl?action=GetCertList",
]


def register_ssl_tools(mcp: FastMCP) -> None:
    """Register all SSL certificate management tools."""

    @mcp.tool()
    def ssl_get_list(server: str = "") -> str:
        """List all SSL certificates on the panel.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = request_compat(
            client,
            _SSL_LIST_ENDPOINTS,
            {"p": 1, "limit": "100", "is_order": 0, "search": ""},
        )
        return format_response(data)

    @mcp.tool()
    def ssl_get_cert(server: str = "", cert_id: str = "") -> str:
        """Get SSL certificate details by ID (certificate hash or subject domain).

        Args:
            server: Server name (optional)
            cert_id: Certificate hash or subject domain name
        """
        client = client_manager.get_client(server or None)
        ssl_list = request_compat(
            client,
            _SSL_LIST_ENDPOINTS,
            {"p": 1, "limit": "100", "is_order": 0, "search": ""},
        )
        items = []
        if isinstance(ssl_list, dict) and isinstance(ssl_list.get("message"), dict):
            items = ssl_list["message"].get("data", [])
        elif isinstance(ssl_list, list):
            items = ssl_list
        for item in items:
            if isinstance(item, dict) and (
                cert_id in (item.get("hash"), item.get("subject"))
                or cert_id in (item.get("verify_domains") or [])
            ):
                return format_response(item)
        params = {"certName": cert_id, "ssl_hash": cert_id, "id": cert_id}
        data = client.request("/ssl?action=GetCert", params)
        return format_response(data)

    @mcp.tool()
    def ssl_save_cert(
        server: str = "",
        key: str = "",
        csr: str = "",
        alias: str = "",
    ) -> str:
        """Save/upload an SSL certificate to the panel.

        Args:
            server: Server name (optional)
            key: Private key content
            csr: Certificate content
            alias: Certificate alias/name
        """
        client = client_manager.get_client(server or None)
        params = {"key": key, "cert": csr, "csr": csr, "alias": alias}
        data = request_compat(
            client,
            ["/v2/ssl_domain?action=upload_cert", "/ssl?action=SaveCert"],
            params,
        )
        return format_response(data)

    @mcp.tool()
    def ssl_delete_cert(server: str = "", cert_id: str = "", confirmed: bool = False) -> str:
        """Delete an SSL certificate from the panel.

        Args:
            server: Server name (optional)
            cert_id: Certificate hash or subject domain name
            confirmed: Must be True to confirm this destructive action
        """
        client = client_manager.get_client(server or None)
        params = {"hash": cert_id, "certName": cert_id, "id": cert_id}
        data = request_compat(
            client,
            ["/v2/ssl_domain?action=remove_cert", "/ssl?action=RemoveCert"],
            params,
            confirmed=confirmed,
        )
        return format_response(data)

    @mcp.tool()
    def ssl_apply_letsencrypt(
        server: str = "",
        domains: str = "",
        siteName: str = "",
        path: str = "",
        ssl_type: str = "http",
    ) -> str:
        """Apply for a Let's Encrypt SSL certificate.

        Args:
            server: Server name (optional)
            domains: Domain names (comma-separated or JSON array)
            siteName: Site name
            path: Site root path for HTTP verification
            ssl_type: Verification type (http or dns)
        """
        client = client_manager.get_client(server or None)
        raw_domains = domains.strip()
        if raw_domains.startswith("["):
            domain_list_json = raw_domains
        else:
            dlist = [d.strip() for d in raw_domains.split(",") if d.strip()]
            if not dlist and siteName:
                dlist = [siteName.strip()]
            domain_list_json = json.dumps(dlist)

        site_id = "-1"
        if siteName:
            sites_data = client.request("/data?action=getData", {"table": "sites", "p": 1, "limit": 200, "search": siteName})
            if isinstance(sites_data, dict):
                for s in sites_data.get("data", []):
                    if s.get("name") == siteName:
                        site_id = str(s.get("id", "-1"))
                        break

        params = {
            "domains": domain_list_json,
            "auth_type": ssl_type,
            "ssl_type": ssl_type,
            "auto_wildcard": "0",
            "deploy": "1" if site_id != "-1" else "-1",
            "site_id": site_id,
            "siteName": siteName,
            "path": path,
        }
        data = request_compat(
            client,
            ["/v2/ssl_domain?action=apply_new_ssl", "/ssl?action=GetDVSSL"],
            params,
        )
        return format_response(data)

    @mcp.tool()
    def ssl_renew(server: str = "", siteName: str = "") -> str:
        """Renew an SSL certificate for a site.

        Args:
            server: Server name (optional)
            siteName: Site domain name or certificate hash
        """
        client = client_manager.get_client(server or None)
        params = {"siteName": siteName}
        data = request_compat(
            client,
            ["/ssl?action=renew_lets_ssl", "/ssl?action=Renew_SSL"],
            params,
        )
        return format_response(data)

    @mcp.tool()
    def ssl_set_to_site(
        server: str = "",
        siteName: str = "",
        cert_id: str = "",
    ) -> str:
        """Deploy a stored SSL certificate to a site.

        Args:
            server: Server name (optional)
            siteName: Site domain name
            cert_id: Certificate hash or subject domain from the panel's cert list
        """
        client = client_manager.get_client(server or None)
        if len(cert_id) == 32 and "." not in cert_id:
            params = {"hash": cert_id, "domains": json.dumps([siteName]), "append": "1"}
            data = client.request("/v2/ssl_domain?action=cert_deploy_sites", params)
            return format_response(data)
        params = {"siteName": siteName, "certName": cert_id, "cert_id": cert_id}
        data = client.request("/ssl?action=SetCertToSite", params)
        return format_response(data)

    @mcp.tool()
    def ssl_get_site_ssl(server: str = "", siteName: str = "") -> str:
        """Get SSL certificate status for a specific site.

        Args:
            server: Server name (optional)
            siteName: Site domain name
        """
        client = client_manager.get_client(server or None)
        params = {"siteName": siteName}
        data = client.request("/site?action=GetSSL", params)
        return format_response(data)
