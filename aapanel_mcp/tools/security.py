"""Security tools for aaPanel MCP server.

Covers: network scanning, website statistics, tamper proof (file integrity),
system hardening, virus/malware scanning, anti-theft, directory protection,
traffic limiting, and CVE vulnerability scanning.
"""

from mcp.server.fastmcp import FastMCP
from ..client import client_manager
from ..utils import format_response


def register_security_tools(mcp: FastMCP) -> None:
    """Register all security and scanning tools."""

    # ==================== Network Scan ====================

    @mcp.tool()
    def network_scan_connections(server: str = "") -> str:
        """Get all active network connections (TCP/UDP, states, ports, processes).

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/ajax?action=GetNetWorkList")
        return format_response(data)

    @mcp.tool()
    def network_scan_ports(server: str = "", target: str = "127.0.0.1", ports: str = "1-1024") -> str:
        """Scan ports on a target host from the aaPanel server.

        Args:
            server: Server name (optional)
            target: Target IP or hostname (default 127.0.0.1 for self-scan)
            ports: Port range (e.g. 1-1024 or 80,443,8080)
        """
        client = client_manager.get_client(server or None)
        params = {"target": target, "ports": ports}
        data = client.request("/safe/firewall/scan_ports", params)
        return format_response(data)

    @mcp.tool()
    def network_scan_firewall_rules(server: str = "", page: int = 1, limit: int = 100) -> str:
        """List all firewall rules (ports + IP rules) for network audit.

        Args:
            server: Server name (optional)
            page: Page number (default 1)
            limit: Items per page (default 100)
        """
        client = client_manager.get_client(server or None)
        params = {"p": page, "limit": limit}
        data = client.request("/firewall?action=GetList", params)
        return format_response(data)

    @mcp.tool()
    def network_get_interfaces(server: str = "") -> str:
        """Get network interface information (IPs, MAC, gateway, DNS).

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/system?action=GetNetWork")
        return format_response(data)

    @mcp.tool()
    def network_get_traffic_stats(
        server: str = "",
        start: str = "",
        end: str = "",
    ) -> str:
        """Get network traffic statistics over a time range.

        Args:
            server: Server name (optional)
            start: Start timestamp
            end: End timestamp
        """
        client = client_manager.get_client(server or None)
        params = {"start": start, "end": end}
        data = client.request("/ajax?action=GetNetWorkIo", params)
        return format_response(data)

    # ==================== Full Website Statistics ====================

    @mcp.tool()
    def site_stats_traffic(server: str = "", siteId: str = "") -> str:
        """Get full traffic statistics for a site (requests, bandwidth, visitors).

        Args:
            server: Server name (optional)
            siteId: Site ID
        """
        client = client_manager.get_client(server or None)
        params = {"siteId": siteId}
        data = client.request("/site?action=GetTrafficStats", params)
        return format_response(data)

    @mcp.tool()
    def site_stats_request_count_qps(server: str = "") -> str:
        """Get real-time request count and QPS (queries per second) across all sites.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/monitor?action=get_request_count_qps")
        return format_response(data)

    @mcp.tool()
    def site_stats_requests_by_hour(server: str = "") -> str:
        """Get hourly request count breakdown per site.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/monitor?action=get_request_count_by_hour")
        return format_response(data)

    @mcp.tool()
    def site_stats_spider_crawl(server: str = "") -> str:
        """Get search engine spider/bot crawl statistics per site.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/monitor?action=get_spider")
        return format_response(data)

    @mcp.tool()
    def site_stats_exceptions(server: str = "") -> str:
        """Get site exception statistics (MySQL slow queries, PHP slow logs, attacks, CC attacks, HTTP status code distribution).

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/monitor?action=get_exception")
        return format_response(data)

    @mcp.tool()
    def site_stats_load_and_flow(server: str = "") -> str:
        """Get system load average and upstream traffic flow.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/monitor?action=load_and_up_flow")
        return format_response(data)

    @mcp.tool()
    def site_stats_logs(server: str = "", siteName: str = "") -> str:
        """Get site access and error log summary.

        Args:
            server: Server name (optional)
            siteName: Site domain name
        """
        client = client_manager.get_client(server or None)
        params = {"siteName": siteName}
        data = client.request("/site?action=GetSiteLogs", params)
        return format_response(data)

    @mcp.tool()
    def site_stats_all(server: str = "") -> str:
        """Get comprehensive statistics overview: QPS, hourly requests, spider crawls, exceptions, load & flow — all in one call.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        results = {}
        try:
            results["qps"] = client.request("/monitor?action=get_request_count_qps")
        except Exception as e:
            results["qps"] = {"error": str(e)}
        try:
            results["requests_by_hour"] = client.request("/monitor?action=get_request_count_by_hour")
        except Exception as e:
            results["requests_by_hour"] = {"error": str(e)}
        try:
            results["spider"] = client.request("/monitor?action=get_spider")
        except Exception as e:
            results["spider"] = {"error": str(e)}
        try:
            results["exceptions"] = client.request("/monitor?action=get_exception")
        except Exception as e:
            results["exceptions"] = {"error": str(e)}
        try:
            results["load_and_flow"] = client.request("/monitor?action=load_and_up_flow")
        except Exception as e:
            results["load_and_flow"] = {"error": str(e)}
        return format_response(results)

    # ==================== Tamper Proof (File Integrity) ====================

    @mcp.tool()
    def tamper_get_file_deny(server: str = "") -> str:
        """Get list of tamper-protected files (file deny rules that prevent modification).

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/config?action=get_file_deny")
        return format_response(data)

    @mcp.tool()
    def tamper_add_file_deny(
        server: str = "",
        path: str = "",
        deny_type: str = "all",
    ) -> str:
        """Add file tamper protection (lock a file/directory from modification).

        Args:
            server: Server name (optional)
            path: File or directory path to protect
            deny_type: Deny type (all, write, delete)
        """
        client = client_manager.get_client(server or None)
        params = {"path": path, "type": deny_type}
        data = client.request("/config?action=set_file_deny", params)
        return format_response(data)

    @mcp.tool()
    def tamper_remove_file_deny(server: str = "", path: str = "") -> str:
        """Remove tamper protection from a file/directory.

        Args:
            server: Server name (optional)
            path: File or directory path to unprotect
        """
        client = client_manager.get_client(server or None)
        params = {"path": path}
        data = client.request("/config?action=del_file_deny", params)
        return format_response(data)

    @mcp.tool()
    def tamper_get_dir_protection(server: str = "", id: str = "", path: str = "") -> str:
        """Get directory protection status for a site (checks .user.ini and access controls).

        Args:
            server: Server name (optional)
            id: Site ID
            path: Directory path within the site
        """
        client = client_manager.get_client(server or None)
        params = {"id": id, "path": path}
        data = client.request("/site?action=GetDirUserINI", params)
        return format_response(data)

    @mcp.tool()
    def tamper_set_dir_protection(
        server: str = "",
        id: str = "",
        path: str = "",
        type: str = "1",
    ) -> str:
        """Enable or disable directory protection for a site (toggle .user.ini cross-site protection).

        Args:
            server: Server name (optional)
            id: Site ID
            path: Directory path within the site
            type: 1=enable protection, 0=disable protection
        """
        client = client_manager.get_client(server or None)
        params = {"id": id, "path": path, "type": type}
        data = client.request("/site?action=SetDirUserINI", params)
        return format_response(data)

    @mcp.tool()
    def tamper_fix_permissions(server: str = "", path: str = "") -> str:
        """Fix file/directory permissions to prevent unauthorized tampering.

        Args:
            server: Server name (optional)
            path: Path to fix permissions for
        """
        client = client_manager.get_client(server or None)
        params = {"path": path}
        data = client.request("/files?action=fix_permissions", params)
        return format_response(data)

    # ==================== System Hardening ====================

    @mcp.tool()
    def harden_get_ssh_config(server: str = "") -> str:
        """Get SSH security configuration for hardening audit (port, password auth, root login, key auth).

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/safe?action=GetSshInfo")
        return format_response(data)

    @mcp.tool()
    def harden_set_ssh_config(
        server: str = "",
        port: str = "22",
        password_auth: str = "1",
        root_login: str = "1",
    ) -> str:
        """Harden SSH configuration (change port, disable password auth, restrict root login).

        Args:
            server: Server name (optional)
            port: SSH port (use non-standard for hardening, e.g. 2222)
            password_auth: 1=allow password auth, 0=key-only auth (recommended)
            root_login: 1=allow root login, 0=disable root login (recommended)
        """
        client = client_manager.get_client(server or None)
        params = {
            "port": port,
            "password_auth": password_auth,
            "root_login": root_login,
        }
        data = client.request("/safe?action=SetSshInfo", params)
        return format_response(data)

    @mcp.tool()
    def harden_set_ssh_key_auth(
        server: str = "",
        public_key: str = "",
    ) -> str:
        """Set up SSH key-based authentication for hardening.

        Args:
            server: Server name (optional)
            public_key: SSH public key content to install
        """
        client = client_manager.get_client(server or None)
        params = {"key": public_key}
        data = client.request("/ssh_security?action=set_sshkey", params)
        return format_response(data)

    @mcp.tool()
    def harden_disable_ssh_password(server: str = "") -> str:
        """Disable SSH password authentication (enforce key-only auth for hardening).

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/ssh_security?action=stop_password")
        return format_response(data)

    @mcp.tool()
    def harden_set_panel_password_expire(
        server: str = "",
        expire_days: str = "90",
    ) -> str:
        """Set panel password expiration policy for hardening.

        Args:
            server: Server name (optional)
            expire_days: Password expiration in days (e.g. 90)
        """
        client = client_manager.get_client(server or None)
        params = {"expire": expire_days}
        data = client.request("/config?action=set_password_expire", params)
        return format_response(data)

    @mcp.tool()
    def harden_set_password_safe(
        server: str = "",
        level: str = "strong",
    ) -> str:
        """Set password complexity requirements for panel accounts.

        Args:
            server: Server name (optional)
            level: Password strength level (weak, medium, strong)
        """
        client = client_manager.get_client(server or None)
        params = {"level": level}
        data = client.request("/config?action=set_password_safe", params)
        return format_response(data)

    @mcp.tool()
    def harden_set_ssl_verify(server: str = "", ssl_verify: str = "1") -> str:
        """Enable/disable panel SSL certificate verification for hardening.

        Args:
            server: Server name (optional)
            ssl_verify: 1=enable SSL verification, 0=disable
        """
        client = client_manager.get_client(server or None)
        params = {"ssl_verify": ssl_verify}
        data = client.request("/config?action=set_ssl_verify", params)
        return format_response(data)

    @mcp.tool()
    def harden_set_ip_whitelist(server: str = "", ips: str = "") -> str:
        """Set IP whitelist for panel access (restrict admin access to specific IPs).

        Args:
            server: Server name (optional)
            ips: IP addresses, one per line or comma-separated
        """
        client = client_manager.get_client(server or None)
        params = {"ips": ips}
        data = client.request("/config?action=login_ipwhite", params)
        return format_response(data)

    @mcp.tool()
    def harden_set_admin_path(server: str = "", admin_path: str = "") -> str:
        """Change the panel admin access URL path (security URL suffix for hardening).

        Args:
            server: Server name (optional)
            admin_path: New admin path (must start with /, e.g. /mysecretadmin123)
        """
        client = client_manager.get_client(server or None)
        params = {"admin_path": admin_path}
        data = client.request("/config?action=set_admin_path", params)
        return format_response(data)

    @mcp.tool()
    def harden_set_basic_auth(
        server: str = "",
        open_basic_auth: str = "1",
        basic_user: str = "",
        basic_pwd: str = "",
    ) -> str:
        """Enable HTTP basic auth for the panel (double authentication layer).

        Args:
            server: Server name (optional)
            open_basic_auth: 1=enable, 0=disable
            basic_user: Basic auth username
            basic_pwd: Basic auth password
        """
        client = client_manager.get_client(server or None)
        params = {
            "open_basic_auth": open_basic_auth,
            "basic_user": basic_user,
            "basic_pwd": basic_pwd,
        }
        data = client.request("/config?action=set_basic_auth", params)
        return format_response(data)

    @mcp.tool()
    def harden_set_two_step_auth(
        server: str = "",
        user_id: str = "",
        enabled: str = "1",
    ) -> str:
        """Enable/disable two-factor authentication (2FA/TOTP) for a panel user.

        Args:
            server: Server name (optional)
            user_id: Panel user ID
            enabled: 1=enable 2FA, 0=disable
        """
        client = client_manager.get_client(server or None)
        params = {"user_id": user_id, "enabled": enabled}
        data = client.request("/config?action=set_two_step_auth", params)
        return format_response(data)

    @mcp.tool()
    def harden_get_security_config(server: str = "") -> str:
        """Get current panel security configuration overview (SSL, 2FA, basic auth, IP whitelist, password policy).

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/config?action=get_settings")
        return format_response(data)

    @mcp.tool()
    def harden_set_improvement(server: str = "", improvement: str = "1") -> str:
        """Enable/disable panel improvement program (data sharing toggle).

        Args:
            server: Server name (optional)
            improvement: 1=enable, 0=disable
        """
        client = client_manager.get_client(server or None)
        params = {"improvement": improvement}
        data = client.request("/config?action=set_improvement", params)
        return format_response(data)

    @mcp.tool()
    def harden_clear_temp_login(server: str = "") -> str:
        """Clear all temporary login sessions for security.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/config?action=clear_temp_login")
        return format_response(data)

    @mcp.tool()
    def harden_set_panel_lock(server: str = "", lock: str = "1") -> str:
        """Enable/disable panel lock (prevent modifications from other sessions).

        Args:
            server: Server name (optional)
            lock: 1=enable lock, 0=disable
        """
        client = client_manager.get_client(server or None)
        params = {"lock": lock}
        data = client.request("/config?action=SetPanelLock", params)
        return format_response(data)

    # ==================== Virus / Malware Scan ====================

    @mcp.tool()
    def virus_scan_site(
        server: str = "",
        id: str = "",
    ) -> str:
        """Start a virus/malware scan on a website (checks for web shells, malicious code, trojans).

        Args:
            server: Server name (optional)
            id: Site ID to scan
        """
        client = client_manager.get_client(server or None)
        params = {"id": id}
        data = client.request("/site?action=CheckSafe", params)
        return format_response(data)

    @mcp.tool()
    def virus_scan_get_result(
        server: str = "",
        id: str = "",
    ) -> str:
        """Get virus/malware scan results for a site.

        Args:
            server: Server name (optional)
            id: Site ID
        """
        client = client_manager.get_client(server or None)
        params = {"id": id}
        data = client.request("/site?action=GetCheckSafe", params)
        return format_response(data)

    @mcp.tool()
    def virus_scan_web(
        server: str = "",
        siteName: str = "",
    ) -> str:
        """Run web vulnerability scanning on a site (uses panel/scanning module).

        Args:
            server: Server name (optional)
            siteName: Site domain name
        """
        client = client_manager.get_client(server or None)
        params = {"siteName": siteName, "def_name": "start"}
        data = client.request("/panel/webscanning/start", params)
        return format_response(data)

    @mcp.tool()
    def virus_scan_get_web_result(
        server: str = "",
        siteName: str = "",
    ) -> str:
        """Get web vulnerability scan results.

        Args:
            server: Server name (optional)
            siteName: Site domain name
        """
        client = client_manager.get_client(server or None)
        params = {"siteName": siteName, "def_name": "get_result"}
        data = client.request("/panel/webscanning/get_result", params)
        return format_response(data)

    @mcp.tool()
    def virus_scan_safe_detect(
        server: str = "",
        action: str = "start",
    ) -> str:
        """Run system-level safe detection (file integrity, suspicious files, permission audit).

        Args:
            server: Server name (optional)
            action: Action to perform (start, get_result, get_log)
        """
        client = client_manager.get_client(server or None)
        params = {"def_name": action}
        data = client.request(f"/panel/safe_detect/{action}", params)
        return format_response(data)

    # ==================== CVE Vulnerability Scan ====================

    @mcp.tool()
    def cve_scan_list(
        server: str = "",
        force: str = "",
    ) -> str:
        """Get CVE vulnerability scan results (risk items, security issues, ignored items).

        Args:
            server: Server name (optional)
            force: Pass 'force' to force a fresh scan
        """
        client = client_manager.get_client(server or None)
        params = {"action": "get_list"}
        if force:
            params["force"] = force
        data = client.request("/vul_scan?action=get_list", params)
        return format_response(data)

    @mcp.tool()
    def cve_check_find(
        server: str = "",
        id: str = "",
    ) -> str:
        """Check/verify a specific CVE vulnerability finding.

        Args:
            server: Server name (optional)
            id: Vulnerability finding ID
        """
        client = client_manager.get_client(server or None)
        params = {"action": "check_find", "id": id}
        data = client.request("/vul_scan?action=check_find", params)
        return format_response(data)

    @mcp.tool()
    def cve_check_cve(
        server: str = "",
        cve_id: str = "",
    ) -> str:
        """Check a specific CVE by ID against installed software.

        Args:
            server: Server name (optional)
            cve_id: CVE identifier (e.g. CVE-2024-12345)
        """
        client = client_manager.get_client(server or None)
        params = {"action": "check_cve", "cve_id": cve_id}
        data = client.request("/vul_scan?action=check_cve", params)
        return format_response(data)

    @mcp.tool()
    def cve_set_ignore(
        server: str = "",
        id: str = "",
    ) -> str:
        """Ignore/dismiss a CVE vulnerability finding.

        Args:
            server: Server name (optional)
            id: Vulnerability finding ID
        """
        client = client_manager.get_client(server or None)
        params = {"action": "set_ignore", "id": id}
        data = client.request("/vul_scan?action=set_ignore", params)
        return format_response(data)

    @mcp.tool()
    def cve_set_vuln_ignore(
        server: str = "",
        id: str = "",
    ) -> str:
        """Ignore a specific vulnerability permanently.

        Args:
            server: Server name (optional)
            id: Vulnerability ID
        """
        client = client_manager.get_client(server or None)
        params = {"action": "set_vuln_ignore", "id": id}
        data = client.request("/vul_scan?action=set_vuln_ignore", params)
        return format_response(data)

    @mcp.tool()
    def cve_get_scan_progress(server: str = "") -> str:
        """Get CVE scan progress bar/status.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/vul_scan?action=get_scan_bar")
        return format_response(data)

    @mcp.tool()
    def cve_get_tmp_result(server: str = "") -> str:
        """Get temporary/intermediate CVE scan results.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/vul_scan?action=get_tmp_result")
        return format_response(data)

    @mcp.tool()
    def cve_get_kill_list(server: str = "") -> str:
        """Get list of killed/fixed vulnerabilities.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/vul_scan?action=kill_get_list")
        return format_response(data)

    # ==================== Security Baseline (Extended) ====================

    @mcp.tool()
    def security_baseline_get_api_log(server: str = "") -> str:
        """Get security baseline API audit logs.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/san?action=get_api_log")
        return format_response(data)

    @mcp.tool()
    def security_baseline_get_ssh_errors(server: str = "") -> str:
        """Get SSH error login attempts (brute-force detection).

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/san?action=get_ssh_errorlogin")
        return format_response(data)

    # ==================== Anti-Theft (Hotlink Protection) ====================

    @mcp.tool()
    def antitheft_get_config(server: str = "", name: str = "") -> str:
        """Get anti-theft/hotlink protection configuration for a site.

        Args:
            server: Server name (optional)
            name: Site domain name
        """
        client = client_manager.get_client(server or None)
        params = {"name": name}
        data = client.request("/site?action=GetSecurity", params)
        return format_response(data)

    @mcp.tool()
    def antitheft_set_config(
        server: str = "",
        name: str = "",
        fix: str = "",
        domains: str = "",
        status: str = "1",
    ) -> str:
        """Set anti-theft/hotlink protection for a site.

        Args:
            server: Server name (optional)
            name: Site domain name
            fix: File extensions to protect (e.g. jpg,png,gif,css,js)
            domains: Allowed domains (comma-separated, referring sites)
            status: 1=enable, 0=disable
        """
        client = client_manager.get_client(server or None)
        params = {"name": name, "fix": fix, "domains": domains, "status": status}
        data = client.request("/site?action=SetSecurity", params)
        return format_response(data)

    # ==================== Traffic Limiting (Rate Limiting) ====================

    @mcp.tool()
    def site_get_traffic_limit(server: str = "", id: str = "") -> str:
        """Get traffic/rate limiting configuration for a site.

        Args:
            server: Server name (optional)
            id: Site ID
        """
        client = client_manager.get_client(server or None)
        params = {"id": id}
        data = client.request("/site?action=GetLimitNet", params)
        return format_response(data)

    @mcp.tool()
    def site_set_traffic_limit(
        server: str = "",
        id: str = "",
        perSec: str = "0",
        perMinute: str = "0",
        limit: str = "0",
    ) -> str:
        """Set traffic/rate limiting for a site (Nginx only). Protects against CC attacks.

        Args:
            server: Server name (optional)
            id: Site ID
            perSec: Requests per second limit (0=no limit)
            perMinute: Requests per minute limit (0=no limit)
            limit: Total flow limit in MB (0=no limit)
        """
        client = client_manager.get_client(server or None)
        params = {"id": id, "perSec": perSec, "perMinute": perMinute, "limit": limit}
        data = client.request("/site?action=SetLimitNet", params)
        return format_response(data)

    @mcp.tool()
    def site_close_traffic_limit(server: str = "", id: str = "") -> str:
        """Disable traffic/rate limiting for a site.

        Args:
            server: Server name (optional)
            id: Site ID
        """
        client = client_manager.get_client(server or None)
        params = {"id": id}
        data = client.request("/site?action=CloseLimitNet", params)
        return format_response(data)

    # ==================== SSL Force Redirect ====================

    @mcp.tool()
    def site_force_https(server: str = "", siteName: str = "") -> str:
        """Force HTTP to HTTPS redirect for a site.

        Args:
            server: Server name (optional)
            siteName: Site domain name
        """
        client = client_manager.get_client(server or None)
        params = {"siteName": siteName}
        data = client.request("/site?action=HttpToHttps", params)
        return format_response(data)

    @mcp.tool()
    def site_close_force_https(server: str = "", siteName: str = "") -> str:
        """Disable HTTP to HTTPS redirect for a site.

        Args:
            server: Server name (optional)
            siteName: Site domain name
        """
        client = client_manager.get_client(server or None)
        params = {"siteName": siteName}
        data = client.request("/site?action=CloseToHttps", params)
        return format_response(data)

    # ==================== Warning/Alert Configuration ====================

    @mcp.tool()
    def alert_get_warning(server: str = "") -> str:
        """Get system warning/alert configuration (CPU, memory, disk thresholds).

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/ajax?action=GetWarning")
        return format_response(data)

    @mcp.tool()
    def alert_set_warning(
        server: str = "",
        cpu: str = "",
        mem: str = "",
        disk: str = "",
    ) -> str:
        """Set system warning/alert thresholds (CPU%, memory%, disk%).

        Args:
            server: Server name (optional)
            cpu: CPU usage alert threshold (e.g. 90 for 90%)
            mem: Memory usage alert threshold
            disk: Disk usage alert threshold
        """
        client = client_manager.get_client(server or None)
        params = {"cpu": cpu, "mem": mem, "disk": disk}
        data = client.request("/ajax?action=SetWarning", params)
        return format_response(data)

    # ==================== Panel Operation Logs ====================

    @mcp.tool()
    def security_get_operation_logs(
        server: str = "",
        page: int = 1,
        limit: int = 20,
    ) -> str:
        """Get panel operation logs (all actions performed through the panel).

        Args:
            server: Server name (optional)
            page: Page number (default 1)
            limit: Items per page (default 20)
        """
        client = client_manager.get_client(server or None)
        params = {"page": page, "limit": limit}
        data = client.request("/ajax?action=GetOpeLogs", params)
        return format_response(data)
