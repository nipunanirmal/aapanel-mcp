"""Security tools for aaPanel MCP server.

Covers: network scanning, website statistics, tamper proof (file integrity),
system hardening, virus/malware scanning, anti-theft, directory protection,
traffic limiting, and CVE vulnerability scanning.
"""

import json
import time
from mcp.server.fastmcp import FastMCP
from ..client import client_manager
from ..utils import format_response, request_compat, is_missing_endpoint


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
        """Scan listening ports and firewall port rules on the aaPanel server.

        Args:
            server: Server name (optional)
            target: Target IP or hostname (default 127.0.0.1 for self-scan)
            ports: Specific port(s) or range (e.g. 80,443 or 1-1024)
        """
        client = client_manager.get_client(server or None)
        results = {}
        if ports and "," in ports and "-" not in ports:
            port_details = {}
            for p in [x.strip() for x in ports.split(",") if x.strip().isdigit()]:
                port_details[p] = request_compat(
                    client,
                    ["/v2/safe/firewall/get_listening_processes", "/safe/firewall/scan_ports"],
                    {"port": p, "target": target, "ports": p},
                )
            results["listening_processes"] = port_details
        elif ports and ports.strip().isdigit():
            results["listening_processes"] = request_compat(
                client,
                ["/v2/safe/firewall/get_listening_processes", "/safe/firewall/scan_ports"],
                {"port": ports.strip(), "target": target, "ports": ports.strip()},
            )
        else:
            results["port_scan"] = client.request(
                "/safe/firewall/scan_ports", {"target": target, "ports": ports}
            )
        results["firewall_port_rules"] = request_compat(
            client,
            ["/v2/firewall/com/port_rules_list", "/data?action=getData"],
            {"p": 1, "limit": 100, "table": "firewall"},
        )
        results["active_connections"] = client.request("/ajax?action=GetNetWorkList")
        return format_response(results)

    @mcp.tool()
    def network_scan_firewall_rules(server: str = "", page: int = 1, limit: int = 100) -> str:
        """List all firewall rules (ports + IP rules) for network audit.

        Args:
            server: Server name (optional)
            page: Page number (default 1)
            limit: Items per page (default 100)
        """
        client = client_manager.get_client(server or None)
        data = {
            "port_rules": request_compat(
                client,
                ["/v2/firewall/com/port_rules_list", "/data?action=getData"],
                {"p": page, "limit": limit, "table": "firewall"},
            ),
            "ip_rules": request_compat(
                client,
                ["/v2/firewall/com/ip_rules_list", "/data?action=getData"],
                {"p": page, "limit": limit, "table": "firewall"},
            ),
        }
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
            start: Start timestamp (defaults to 1 hour ago)
            end: End timestamp (defaults to now)
        """
        client = client_manager.get_client(server or None)
        now = int(time.time())
        params = {"start": start or str(now - 3600), "end": end or str(now)}
        data = client.request("/ajax?action=GetNetWorkIo", params)
        return format_response(data)

    # ==================== Full Website Statistics ====================

    @mcp.tool()
    def site_stats_traffic(server: str = "", siteId: str = "") -> str:
        """Get full traffic statistics for a site (requests, bandwidth, visitors).

        Args:
            server: Server name (optional)
            siteId: Site ID or site domain name (optional, returns all-sites overview if empty)
        """
        client = client_manager.get_client(server or None)
        if not siteId:
            return format_response(request_compat(
                client,
                ["/v2/site_monitor?action=get_overview", "/site?action=GetTrafficStats"],
            ))
        site_name = siteId
        if siteId.isdigit():
            sites_data = client.request("/data?action=getData", {"table": "sites", "p": 1, "limit": 200})
            if isinstance(sites_data, dict):
                for s in sites_data.get("data", []):
                    if str(s.get("id")) == str(siteId):
                        site_name = s.get("name", siteId)
                        break
        data = request_compat(
            client,
            ["/v2/site_monitor?action=get_site_overview", "/site?action=GetTrafficStats"],
            {"site_name": site_name, "siteId": siteId},
        )
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
    def tamper_get_file_deny(server: str = "", website: str = "") -> str:
        """Get list of tamper-protected / execute-denied file rules for a website.

        Args:
            server: Server name (optional)
            website: Website domain name (optional; queries all sites if omitted)
        """
        client = client_manager.get_client(server or None)
        if website:
            return format_response(client.request("/config?action=get_file_deny", {"website": website}))
        sites_data = client.request("/data?action=getData", {"table": "sites", "p": 1, "limit": 100})
        results = {}
        if isinstance(sites_data, dict):
            for s in sites_data.get("data", []):
                sname = s.get("name", "")
                if sname:
                    results[sname] = client.request("/config?action=get_file_deny", {"website": sname})
        return format_response(results)

    @mcp.tool()
    def tamper_add_file_deny(
        server: str = "",
        path: str = "/",
        deny_type: str = "php",
        website: str = "",
        deny_name: str = "mcp_deny",
    ) -> str:
        """Add file execution deny protection (block script execution in a directory for a website).

        Args:
            server: Server name (optional)
            path: Directory path within the website (e.g. /uploads)
            deny_type: File extension(s) to block (e.g. php or php|jsp)
            website: Website domain name
            deny_name: Rule name (letters, numbers, underscores)
        """
        client = client_manager.get_client(server or None)
        suffix = "php" if deny_type == "all" else deny_type
        params = {
            "website": website,
            "deny_name": deny_name,
            "dir": path,
            "suffix": suffix,
            "act": "add",
        }
        data = client.request("/config?action=set_file_deny", params)
        return format_response(data)

    @mcp.tool()
    def tamper_remove_file_deny(
        server: str = "",
        path: str = "",
        website: str = "",
        deny_name: str = "",
        confirmed: bool = False,
    ) -> str:
        """Remove file execution deny protection rule from a website.

        Args:
            server: Server name (optional)
            path: Rule name or directory path to unprotect
            website: Website domain name
            deny_name: Rule name to remove (uses path if omitted)
            confirmed: Must be True to confirm this destructive action
        """
        client = client_manager.get_client(server or None)
        params = {
            "website": website,
            "deny_name": deny_name or path,
            "path": path,
        }
        data = client.request("/config?action=del_file_deny", params, confirmed=confirmed)
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
        data = {
            "ssh_info": request_compat(
                client,
                ["/v2/safe/ssh/GetSshInfo", "/firewall?action=GetSshInfo"],
            ),
            "sshd_config": client.request("/ssh_security?action=get_config"),
        }
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
        results = {}
        if port:
            results["port"] = client.request("/firewall?action=SetSshPort", {"port": port})
        if str(password_auth) in ("1", "true", "True", "yes"):
            results["password_auth"] = client.request("/ssh_security?action=set_password")
        elif str(password_auth) in ("0", "false", "False", "no"):
            results["password_auth"] = client.request("/ssh_security?action=stop_password", confirmed=True)
        if str(root_login) in ("1", "true", "True", "yes"):
            results["root_login"] = client.request("/ssh_security?action=set_root", {"p_type": "yes"})
        elif str(root_login) in ("0", "false", "False", "no"):
            results["root_login"] = client.request("/ssh_security?action=stop_root", confirmed=True)
        return format_response(results)

    @mcp.tool()
    def harden_set_ssh_key_auth(
        server: str = "",
        public_key: str = "ed25519",
    ) -> str:
        """Set up SSH key-based authentication for hardening.

        Args:
            server: Server name (optional)
            public_key: Key encryption type (ed25519, ecdsa, rsa, dsa; default ed25519)
        """
        client = client_manager.get_client(server or None)
        key_type = public_key if public_key in ("ed25519", "ecdsa", "rsa", "dsa") else "rsa"
        params = {"ssh": "yes", "type": key_type}
        data = client.request("/ssh_security?action=set_sshkey", params)
        return format_response(data)

    @mcp.tool()
    def harden_disable_ssh_password(server: str = "", confirmed: bool = False) -> str:
        """Disable SSH password authentication (enforce key-only auth for hardening).

        Args:
            server: Server name (optional)
            confirmed: Must be True to confirm this destructive action
        """
        client = client_manager.get_client(server or None)
        data = client.request("/ssh_security?action=stop_password", confirmed=confirmed)
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
        params = {"status": ssl_verify, "ssl_verify": ssl_verify}
        data = client.request("/config?action=set_ssl_verify", params)
        return format_response(data)

    @mcp.tool()
    def harden_set_ip_whitelist(server: str = "", ips: str = "", action: str = "add") -> str:
        """Set or query IP whitelist for panel login notifications.

        Args:
            server: Server name (optional)
            ips: IP addresses, one per line or comma-separated (empty to list current whitelist)
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
        params = {"act": enabled, "user_id": user_id, "enabled": enabled}
        data = client.request("/config?action=set_two_step_auth", params)
        return format_response(data)

    @mcp.tool()
    def harden_get_security_config(server: str = "") -> str:
        """Get current panel security configuration overview (SSL, 2FA, basic auth, IP whitelist, password policy).

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/config?action=get_config")
        return format_response(data)

    @mcp.tool()
    def harden_set_improvement(server: str = "", improvement: str = "1") -> str:
        """Enable/disable panel improvement program (data sharing toggle).

        Args:
            server: Server name (optional)
            improvement: 1=enable, 0=disable
        """
        client = client_manager.get_client(server or None)
        params = {"status": improvement, "improvement": improvement}
        data = request_compat(
            client,
            ["/v2/config?action=set_improvement", "/config?action=set_improvement"],
            params,
        )
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
        if str(lock) in ("1", "true", "True"):
            params.update({"files": "1", "tasks": "1", "config": "1"})
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
        """Run web vulnerability scanning on a site (uses webbasicscanning module).

        Args:
            server: Server name (optional)
            siteName: Site domain name
        """
        client = client_manager.get_client(server or None)
        params = {"name": siteName, "siteName": siteName, "def_name": "start"}
        data = request_compat(
            client,
            ["/v2/project/webbasicscanning/ScanSingleSite", "/panel/webscanning/start"],
            params,
        )
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
        params = {"name": siteName, "siteName": siteName, "def_name": "get_result"}
        data = request_compat(
            client,
            ["/v2/project/webbasicscanning/get_scan_result", "/panel/webscanning/get_result"],
            params,
        )
        return format_response(data)

    @mcp.tool()
    def virus_scan_safe_detect(
        server: str = "",
        action: str = "start",
    ) -> str:
        """Run system-level safe detection (file integrity, webshell detection, safecloud overview).

        Args:
            server: Server name (optional)
            action: Action to perform (start, get_result, get_log)
        """
        client = client_manager.get_client(server or None)
        if action in ("get_result", "get_safe_overview"):
            data = {
                "safe_overview": request_compat(
                    client,
                    ["/v2/safecloud?action=get_safe_overview", "/panel/safe_detect/get_result"],
                    {"def_name": "get_result"},
                ),
                "webshell_result": client.request("/v2/safecloud?action=get_webshell_result"),
                "safe_count": client.request("/v2/safe_detect?action=get_safe_count"),
            }
            return format_response(data)
        if action == "get_log":
            return format_response(request_compat(
                client,
                ["/v2/safecloud?action=get_security_dynamic", "/panel/safe_detect/get_log"],
                {"def_name": "get_log"},
            ))
        data = request_compat(
            client,
            ["/v2/safecloud?action=get_safecloud_list", "/panel/safe_detect/start"],
            {"def_name": "start"},
        )
        return format_response(data)

    # ==================== CVE Vulnerability Scan ====================

    @mcp.tool()
    def cve_scan_list(
        server: str = "",
        force: str = "",
    ) -> str:
        """Get CVE vulnerability and security warning scan results (risk items, security issues, ignored items).

        Args:
            server: Server name (optional)
            force: Pass '1' or 'force' to force a fresh scan
        """
        client = client_manager.get_client(server or None)
        params = {}
        if force:
            params["force"] = "1"
        data = request_compat(
            client,
            ["/warning?action=get_list", "/vul_scan?action=get_list"],
            params,
        )
        return format_response(data)

    @mcp.tool()
    def cve_check_find(
        server: str = "",
        id: str = "",
    ) -> str:
        """Check/verify a specific security warning / vulnerability finding.

        Args:
            server: Server name (optional)
            id: Vulnerability finding module name (m_name, e.g. sw_ssh_port)
        """
        client = client_manager.get_client(server or None)
        params = {"m_name": id, "id": id}
        data = request_compat(
            client,
            ["/warning?action=check_find", "/vul_scan?action=check_find"],
            params,
        )
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
        params = {"cve_id": cve_id}
        data = request_compat(
            client,
            ["/warning?action=check_cve", "/vul_scan?action=check_cve"],
            params,
        )
        return format_response(data)

    @mcp.tool()
    def cve_set_ignore(
        server: str = "",
        id: str = "",
    ) -> str:
        """Ignore/dismiss a security warning finding.

        Args:
            server: Server name (optional)
            id: Vulnerability finding module name (m_name, e.g. sw_ssh_port)
        """
        client = client_manager.get_client(server or None)
        params = {"m_name": id, "id": id}
        data = request_compat(
            client,
            ["/warning?action=set_ignore", "/vul_scan?action=set_ignore"],
            params,
        )
        return format_response(data)

    @mcp.tool()
    def cve_set_vuln_ignore(
        server: str = "",
        id: str = "",
    ) -> str:
        """Ignore a specific CVE vulnerability permanently.

        Args:
            server: Server name (optional)
            id: CVE vulnerability ID (e.g. CVE-2024-12345) or JSON array of CVE IDs
        """
        client = client_manager.get_client(server or None)
        cve_list = id if id.strip().startswith("[") else json.dumps([id.strip()])
        params = {"cve_list": cve_list, "id": id}
        data = request_compat(
            client,
            ["/warning?action=set_vuln_ignore", "/vul_scan?action=set_vuln_ignore"],
            params,
        )
        return format_response(data)

    @mcp.tool()
    def cve_get_scan_progress(server: str = "") -> str:
        """Get CVE scan progress bar/status.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = request_compat(
            client,
            ["/warning?action=get_scan_bar", "/vul_scan?action=get_scan_bar"],
        )
        return format_response(data)

    @mcp.tool()
    def cve_get_tmp_result(server: str = "") -> str:
        """Get temporary/intermediate CVE scan results.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = request_compat(
            client,
            ["/warning?action=get_tmp_result", "/vul_scan?action=get_tmp_result"],
        )
        return format_response(data)

    @mcp.tool()
    def cve_get_kill_list(server: str = "") -> str:
        """Stop/interrupt an ongoing CVE scan or get vulnerability info.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = request_compat(
            client,
            ["/warning?action=kill_get_list", "/vul_scan?action=kill_get_list"],
        )
        return format_response(data)

    # ==================== Security Baseline (Extended) ====================

    @mcp.tool()
    def security_baseline_get_api_log(server: str = "") -> str:
        """Get security baseline API audit logs and server security status.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/san?action=get_api_log")
        if isinstance(data, dict) and data.get("status") is False:
            return format_response(client.request("/v2/safe/serversafe/get_security_info"))
        return format_response(data)

    @mcp.tool()
    def security_baseline_get_ssh_errors(server: str = "") -> str:
        """Get SSH error login attempts (brute-force detection).

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = {
            "intrusion_stats": client.request("/v2/mod/ssh/com/get_ssh_intrusion"),
            "baseline_ssh_errors": client.request("/san?action=get_ssh_errorlogin"),
        }
        return format_response(data)

    # ==================== Anti-Theft (Hotlink Protection) ====================

    @mcp.tool()
    def antitheft_get_config(server: str = "", name: str = "", id: str = "") -> str:
        """Get anti-theft/hotlink protection configuration for a site.

        Args:
            server: Server name (optional)
            name: Site domain name
            id: Site ID (optional, resolved from name if omitted)
        """
        client = client_manager.get_client(server or None)
        site_id = id
        if not site_id and name:
            sites_data = client.request("/data?action=getData", {"table": "sites", "p": 1, "limit": 200, "search": name})
            if isinstance(sites_data, dict):
                for s in sites_data.get("data", []):
                    if s.get("name") == name:
                        site_id = str(s.get("id", ""))
                        break
        params = {"id": site_id or "0", "name": name}
        data = client.request("/site?action=GetSecurity", params)
        return format_response(data)

    @mcp.tool()
    def antitheft_set_config(
        server: str = "",
        name: str = "",
        fix: str = "jpg,jpeg,gif,png,js,css",
        domains: str = "",
        status: str = "1",
        id: str = "",
    ) -> str:
        """Set anti-theft/hotlink protection for a site.

        Args:
            server: Server name (optional)
            name: Site domain name
            fix: File extensions to protect (e.g. jpg,png,gif,css,js)
            domains: Allowed domains (comma-separated, referring sites)
            status: 1=enable, 0=disable
            id: Site ID (optional, resolved from name if omitted)
        """
        client = client_manager.get_client(server or None)
        site_id = id
        if not site_id and name:
            sites_data = client.request("/data?action=getData", {"table": "sites", "p": 1, "limit": 200, "search": name})
            if isinstance(sites_data, dict):
                for s in sites_data.get("data", []):
                    if s.get("name") == name:
                        site_id = str(s.get("id", ""))
                        break
        params = {
            "id": site_id or "0",
            "name": name,
            "fix": fix,
            "domains": domains or name,
            "status": status,
            "return_rule": "404",
            "none": "true",
        }
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
        perSec: str = "300",
        perMinute: str = "25",
        limit: str = "512",
    ) -> str:
        """Set traffic/rate limiting for a site (Nginx only). Protects against CC attacks.

        Args:
            server: Server name (optional)
            id: Site ID
            perSec: Concurrency limit (perserver, must be > 0, default 300)
            perMinute: Single IP concurrency limit (perip, must be > 0, default 25)
            limit: Traffic rate limit in KB/s (limit_rate, must be > 0, default 512)
        """
        client = client_manager.get_client(server or None)
        params = {
            "id": id,
            "perserver": perSec if int(perSec or 0) > 0 else "300",
            "perip": perMinute if int(perMinute or 0) > 0 else "25",
            "limit_rate": limit if int(limit or 0) > 0 else "512",
        }
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
        id: str = "1",
    ) -> str:
        """Dismiss/acknowledge a system warning by ID or configure alert thresholds.

        Args:
            server: Server name (optional)
            cpu: CPU usage alert threshold (e.g. 90 for 90%)
            mem: Memory usage alert threshold
            disk: Disk usage alert threshold
            id: Warning ID to acknowledge (default 1)
        """
        client = client_manager.get_client(server or None)
        params = {"id": id, "cpu": cpu, "mem": mem, "disk": disk}
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
        params = {"table": "logs", "p": page, "limit": limit}
        data = client.request("/data?action=getData", params)
        return format_response(data)
