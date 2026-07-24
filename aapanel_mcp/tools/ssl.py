"""SSL certificate management tools for aaPanel MCP server."""

from mcp.server.fastmcp import FastMCP
from ..client import client_manager
from ..utils import format_response


def register_ssl_tools(mcp: FastMCP) -> None:
    """Register all SSL certificate management tools."""

    @mcp.tool()
    def ssl_get_list(server: str = "") -> str:
        """List all SSL certificates on the panel.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/ssl?action=GetCertList")
        return format_response(data)

    @mcp.tool()
    def ssl_get_cert(server: str = "", cert_id: str = "") -> str:
        """Get SSL certificate details by ID.

        Args:
            server: Server name (optional)
            cert_id: Certificate ID
        """
        client = client_manager.get_client(server or None)
        params = {"id": cert_id}
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
        params = {"key": key, "csr": csr, "alias": alias}
        data = client.request("/ssl?action=SaveCert", params)
        return format_response(data)

    @mcp.tool()
    def ssl_delete_cert(server: str = "", cert_id: str = "") -> str:
        """Delete an SSL certificate from the panel.

        Args:
            server: Server name (optional)
            cert_id: Certificate ID
        """
        client = client_manager.get_client(server or None)
        params = {"id": cert_id}
        data = client.request("/ssl?action=RemoveCert", params)
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
            domains: Domain names (comma-separated)
            siteName: Site name
            path: Site root path for HTTP verification
            ssl_type: Verification type (http or dns)
        """
        client = client_manager.get_client(server or None)
        params = {
            "domains": domains,
            "siteName": siteName,
            "path": path,
            "ssl_type": ssl_type,
        }
        data = client.request("/ssl?action=GetDVSSL", params)
        return format_response(data)

    @mcp.tool()
    def ssl_renew(server: str = "", siteName: str = "") -> str:
        """Renew an SSL certificate for a site.

        Args:
            server: Server name (optional)
            siteName: Site domain name
        """
        client = client_manager.get_client(server or None)
        params = {"siteName": siteName}
        data = client.request("/ssl?action=Renew_SSL", params)
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
            cert_id: Certificate ID from the panel's cert list
        """
        client = client_manager.get_client(server or None)
        params = {"siteName": siteName, "cert_id": cert_id}
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
