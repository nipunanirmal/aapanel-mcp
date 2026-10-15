"""System optimization and cleanup tools for aaPanel MCP server.

Covers: system cleanup, RAM release, CPU optimization, storage management,
log deletion, process management, WAF management, and performance tuning.
"""

import json
import time
from mcp.server.fastmcp import FastMCP
from ..client import client_manager
from ..utils import format_response, request_compat, is_missing_endpoint


def register_optimization_tools(mcp: FastMCP) -> None:
    """Register all system optimization and cleanup tools."""

    # ==================== System Cleanup ====================

    @mcp.tool()
    def system_clear_all_cache(server: str = "", confirmed: bool = False) -> str:
        """Clear all system garbage: mail logs, temp files, install cache, wwwlogs.
        Returns count of files cleaned and total space freed.

        Args:
            server: Server name (optional)
            confirmed: Must be True to confirm this destructive action
        """
        client = client_manager.get_client(server or None)
        data = client.request("/system?action=ClearSystem", confirmed=confirmed)
        return format_response(data)

    @mcp.tool()
    def system_release_memory(server: str = "", confirmed: bool = False) -> str:
        """Release/flush system memory (RAM cleanup). Runs sync and memory release script.
        Returns updated memory info after release.

        Args:
            server: Server name (optional)
            confirmed: Must be True to confirm this action
        """
        client = client_manager.get_client(server or None)
        data = client.request("/system?action=ReMemory", confirmed=confirmed)
        return format_response(data)

    @mcp.tool()
    def system_clear_panel_logs(server: str = "", confirmed: bool = False) -> str:
        """Clear aaPanel error logs.

        Args:
            server: Server name (optional)
            confirmed: Must be True to confirm this action
        """
        client = client_manager.get_client(server or None)
        data = client.request("/config?action=clean_panel_error_logs", confirmed=confirmed)
        return format_response(data)

    @mcp.tool()
    def system_clear_site_logs(server: str = "", siteName: str = "", confirmed: bool = False) -> str:
        """Clear access/error logs for a specific site.

        Args:
            server: Server name (optional)
            siteName: Site domain name
            confirmed: Must be True to confirm this action
        """
        client = client_manager.get_client(server or None)
        params = {"siteName": siteName}
        data = client.request("/files?action=CloseLogs", params, confirmed=confirmed)
        return format_response(data)

    @mcp.tool()
    def system_clear_all_logs(server: str = "", confirmed: bool = False) -> str:
        """Close/clear all website logs on the server.

        Args:
            server: Server name (optional)
            confirmed: Must be True to confirm this action
        """
        client = client_manager.get_client(server or None)
        data = client.request("/files?action=CloseLogs", confirmed=confirmed)
        return format_response(data)

    @mcp.tool()
    def system_clear_old_sessions(server: str = "", confirmed: bool = False) -> str:
        """Delete old panel sessions to free up resources.

        Args:
            server: Server name (optional)
            confirmed: Must be True to confirm this destructive action
        """
        client = client_manager.get_client(server or None)
        data = client.request("/config?action=DelOldSession", confirmed=confirmed)
        return format_response(data)

    # ==================== Storage Management ====================

    @mcp.tool()
    def storage_get_disk_info(server: str = "") -> str:
        """Get detailed disk/partition information including usage and mount points.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/system?action=GetDiskInfo")
        return format_response(data)

    @mcp.tool()
    def storage_get_disk_io(
        server: str = "",
        start: str = "",
        end: str = "",
    ) -> str:
        """Get disk I/O statistics for a time range.

        Args:
            server: Server name (optional)
            start: Start timestamp (defaults to 1 hour ago)
            end: End timestamp (defaults to now)
        """
        client = client_manager.get_client(server or None)
        now = int(time.time())
        params = {"start": start or str(now - 3600), "end": end or str(now)}
        data = client.request("/ajax?action=GetDiskIo", params)
        return format_response(data)

    @mcp.tool()
    def storage_get_dir_size(server: str = "", path: str = "") -> str:
        """Get total size of a directory on the server.

        Args:
            server: Server name (optional)
            path: Directory path
        """
        client = client_manager.get_client(server or None)
        params = {"path": path}
        data = client.request("/files?action=GetDirSize", params)
        return format_response(data)

    @mcp.tool()
    def storage_get_path_size(server: str = "", path: str = "") -> str:
        """Get detailed size breakdown of a path (recursive).

        Args:
            server: Server name (optional)
            path: Directory path
        """
        client = client_manager.get_client(server or None)
        params = {"path": path}
        data = client.request("/files?action=get_path_size", params)
        return format_response(data)

    @mcp.tool()
    def storage_fix_permissions(server: str = "", path: str = "") -> str:
        """Fix file/directory permissions for a path (restore to correct ownership/permissions).

        Args:
            server: Server name (optional)
            path: Path to fix permissions for
        """
        client = client_manager.get_client(server or None)
        params = {"path": path}
        data = client.request("/files?action=fix_permissions", params)
        return format_response(data)

    @mcp.tool()
    def storage_get_path_permissions(server: str = "", path: str = "") -> str:
        """Get current permissions for a path.

        Args:
            server: Server name (optional)
            path: Directory path
        """
        client = client_manager.get_client(server or None)
        params = {"path": path}
        data = client.request("/files?action=get_path_premissions", params)
        return format_response(data)

    @mcp.tool()
    def storage_restore_path_permissions(server: str = "", path: str = "") -> str:
        """Restore path permissions from backup.

        Args:
            server: Server name (optional)
            path: Directory path
        """
        client = client_manager.get_client(server or None)
        params = {"path": path}
        data = client.request("/files?action=restore_path_permissions", params)
        return format_response(data)

    # ==================== CPU & Process Optimization ====================

    @mcp.tool()
    def cpu_get_info(server: str = "") -> str:
        """Get detailed CPU information including model, cores, usage percentage.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/system?action=GetNetWork")
        return format_response(data)

    @mcp.tool()
    def cpu_get_io_stats(
        server: str = "",
        start: str = "",
        end: str = "",
    ) -> str:
        """Get CPU I/O statistics for a time range.

        Args:
            server: Server name (optional)
            start: Start timestamp (defaults to 1 hour ago)
            end: End timestamp (defaults to now)
        """
        client = client_manager.get_client(server or None)
        now = int(time.time())
        params = {"start": start or str(now - 3600), "end": end or str(now)}
        data = client.request("/ajax?action=GetCpuIo", params)
        return format_response(data)

    @mcp.tool()
    def cpu_get_process_tops(
        server: str = "",
        start: str = "",
        end: str = "",
    ) -> str:
        """Get top processes by resource consumption (CPU/memory ranking).

        Args:
            server: Server name (optional)
            start: Start timestamp (defaults to 1 hour ago)
            end: End timestamp (defaults to now)
        """
        client = client_manager.get_client(server or None)
        now = int(time.time())
        params = {"start": start or str(now - 3600), "end": end or str(now)}
        data = client.request("/ajax?action=get_process_tops", params)
        # Panel may return a raw string error ("error: no such table") when the
        # process-metrics DB table doesn't exist yet — fall back to v2 monitor.
        if (
            is_missing_endpoint(data)
            or (isinstance(data, str) and data.lower().startswith("error"))
            or (isinstance(data, list) and not data)
        ):
            data = request_compat(
                client,
                ["/v2/monitor/process_management/specific_resource_load_type", "/ajax?action=GetProcessList"],
            )
        return format_response(data)

    @mcp.tool()
    def cpu_get_high_cpu_processes(
        server: str = "",
        start: str = "",
        end: str = "",
    ) -> str:
        """Get list of processes with high CPU usage.

        Args:
            server: Server name (optional)
            start: Start timestamp (defaults to 1 hour ago)
            end: End timestamp (defaults to now)
        """
        client = client_manager.get_client(server or None)
        now = int(time.time())
        params = {"start": start or str(now - 3600), "end": end or str(now)}
        data = client.request("/ajax?action=get_process_cpu_high", params)
        # Panel may return a raw string error ("error: no such table") when the
        # process-metrics DB table doesn't exist yet — fall back to v2 monitor.
        if (
            is_missing_endpoint(data)
            or (isinstance(data, str) and data.lower().startswith("error"))
            or (isinstance(data, list) and not data)
        ):
            data = request_compat(
                client,
                ["/v2/monitor/process_management/specific_resource_load_type", "/ajax?action=GetProcessList"],
            )
        return format_response(data)

    @mcp.tool()
    def process_list(server: str = "") -> str:
        """List running processes with CPU and memory usage.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = request_compat(
            client,
            ["/v2/monitor/process_management/specific_resource_load_type", "/ajax?action=GetProcessList"],
        )
        return format_response(data)

    @mcp.tool()
    def process_kill(server: str = "", pid: str = "", confirmed: bool = False) -> str:
        """Kill a specific process by PID.

        Args:
            server: Server name (optional)
            pid: Process ID to kill
            confirmed: Must be True to confirm this destructive action
        """
        client = client_manager.get_client(server or None)
        params = {"pid": pid}
        data = client.request("/ajax?action=KillProcess", params, confirmed=confirmed)
        return format_response(data)

    @mcp.tool()
    def cpu_get_load_average(server: str = "") -> str:
        """Get system load average (1min, 5min, 15min).

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/system?action=GetLoadAverage")
        return format_response(data)

    # ==================== Memory Optimization ====================

    @mcp.tool()
    def memory_get_info(server: str = "") -> str:
        """Get detailed memory information (total, used, free, swap, cache).

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/system?action=GetMemInfo")
        return format_response(data)

    @mcp.tool()
    def memory_get_system_total(server: str = "") -> str:
        """Get complete system overview (memory, CPU, disk, network, version combined).

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/system?action=GetSystemTotal")
        return format_response(data)

    @mcp.tool()
    def memory_get_io_info(server: str = "") -> str:
        """Get disk I/O read/write speed information.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/system?action=get_io_info")
        return format_response(data)

    # ==================== Network I/O ====================

    @mcp.tool()
    def network_get_io_stats(
        server: str = "",
        start: str = "",
        end: str = "",
    ) -> str:
        """Get network I/O statistics for a time range.

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

    @mcp.tool()
    def network_get_list(server: str = "") -> str:
        """Get network connection list and statistics.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/ajax?action=GetNetWorkList")
        return format_response(data)

    # ==================== Service Status & Optimization ====================

    @mcp.tool()
    def service_get_nginx_status(server: str = "") -> str:
        """Get Nginx load status (connections, requests, workers).

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/ajax?action=GetNginxStatus")
        return format_response(data)

    @mcp.tool()
    def service_get_php_status(server: str = "", version: str = "") -> str:
        """Get PHP-FPM load status for a specific version.

        Args:
            server: Server name (optional)
            version: PHP version (e.g. 74, 80, 81, 82, 83; auto-detected if omitted)
        """
        client = client_manager.get_client(server or None)
        resolved_ver = version
        if not resolved_ver:
            cfg = client.request("/config?action=get_config")
            if isinstance(cfg, dict):
                for php in cfg.get("php", []):
                    if php.get("setup"):
                        resolved_ver = str(php.get("version", ""))
                        break
        params = {"version": resolved_ver or "83"}
        data = client.request("/ajax?action=GetPHPStatus", params)
        return format_response(data)

    @mcp.tool()
    def service_get_redis_status(server: str = "") -> str:
        """Get Redis server status and statistics.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/ajax?action=GetRedisStatus")
        return format_response(data)

    @mcp.tool()
    def service_get_memcached_status(server: str = "") -> str:
        """Get Memcached server status and statistics.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = request_compat(
            client,
            ["/v2/ajax?action=GetMemcachedStatus", "/ajax?action=GetMemcachedStatus"],
        )
        return format_response(data)

    @mcp.tool()
    def service_get_apache_status(server: str = "") -> str:
        """Get Apache server status and load information.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/ajax?action=GetApacheStatus")
        return format_response(data)

    # ==================== WAF (Web Application Firewall) ====================

    @mcp.tool()
    def waf_get_status(server: str = "") -> str:
        """Get WAF (btwaf) plugin status — installed, running, license state.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        params = {"name": "btwaf", "s": "get_config", "fun": "get_config"}
        data = client.request("/plugin?action=a", params)
        return format_response(data)

    @mcp.tool()
    def waf_get_sites(server: str = "") -> str:
        """Get list of sites protected by WAF.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        params = {"name": "btwaf", "s": "get_site_config", "fun": "get_site_config"}
        data = client.request("/plugin?action=a", params)
        return format_response(data)

    @mcp.tool()
    def waf_set_site_status(
        server: str = "",
        siteName: str = "",
        status: str = "1",
    ) -> str:
        """Enable or disable WAF protection for a specific site.

        Args:
            server: Server name (optional)
            siteName: Site domain name
            status: 1=enable, 0=disable
        """
        client = client_manager.get_client(server or None)
        params = {
            "name": "btwaf",
            "s": "set_site_obj_open",
            "fun": "set_site_obj_open",
            "siteName": siteName,
            "obj": "open",
            "status": status,
        }
        data = client.request("/plugin?action=a", params)
        return format_response(data)

    @mcp.tool()
    def waf_get_logs(
        server: str = "",
        siteName: str = "",
        page: int = 1,
        limit: int = 20,
    ) -> str:
        """Get WAF attack/interception logs.

        Args:
            server: Server name (optional)
            siteName: Site domain name (optional, empty for all sites)
            page: Page number (default 1)
            limit: Items per page (default 20)
        """
        client = client_manager.get_client(server or None)
        params = {
            "name": "btwaf",
            "s": "get_logs_list",
            "fun": "get_logs_list",
            "siteName": siteName,
            "p": page,
            "limit": limit,
        }
        data = client.request("/plugin?action=a", params)
        return format_response(data)

    @mcp.tool()
    def waf_get_rules(server: str = "") -> str:
        """Get WAF rule list (URL, IP, UA, CC rules).

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        params = {"name": "btwaf", "s": "get_rule", "fun": "get_rule"}
        data = client.request("/plugin?action=a", params)
        return format_response(data)

    @mcp.tool()
    def waf_add_rule(
        server: str = "",
        rule_type: str = "",
        rule_value: str = "",
        ps: str = "",
    ) -> str:
        """Add a WAF rule (block URL, IP, User-Agent, etc.).

        Args:
            server: Server name (optional)
            rule_type: Rule type (url, ip, ua, cc, etc.)
            rule_value: Rule content (URL pattern, IP address, UA string)
            ps: Remark/description
        """
        client = client_manager.get_client(server or None)
        params = {
            "name": "btwaf",
            "s": "add_rule",
            "fun": "add_rule",
            "ruleName": rule_type,
            "type": rule_type,
            "ruleValue": rule_value,
            "value": rule_value,
            "ps": ps,
        }
        data = client.request("/plugin?action=a", params)
        return format_response(data)

    @mcp.tool()
    def waf_delete_rule(server: str = "", rule_id: str = "") -> str:
        """Delete a WAF rule by ID.

        Args:
            server: Server name (optional)
            rule_id: Rule ID to delete
        """
        client = client_manager.get_client(server or None)
        params = {"name": "btwaf", "s": "remove_rule", "fun": "remove_rule", "id": rule_id}
        data = client.request("/plugin?action=a", params)
        return format_response(data)

    # ==================== Abnormal Detection ====================

    @mcp.tool()
    def abnormal_check_mysql_server(server: str = "") -> str:
        """Check MySQL server for abnormal configuration or status issues.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = {
            "run_status": client.request("/database?action=GetRunStatus"),
            "exceptions": client.request("/monitor?action=get_exception"),
        }
        return format_response(data)

    @mcp.tool()
    def abnormal_check_mysql_cpu(server: str = "") -> str:
        """Check MySQL CPU usage and slow queries for abnormalities.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = {
            "exceptions": client.request("/monitor?action=get_exception"),
            "process_load": request_compat(
                client,
                ["/v2/monitor/process_management/specific_resource_load_type", "/ajax?action=GetProcessList"],
            ),
        }
        return format_response(data)

    @mcp.tool()
    def abnormal_check_php_server(server: str = "") -> str:
        """Check PHP-FPM for abnormal configuration or status issues.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        cfg = client.request("/config?action=get_config")
        php_list = cfg.get("php", []) if isinstance(cfg, dict) else []
        results = {"installed_php": php_list}
        for php in php_list:
            if php.get("setup"):
                ver = str(php.get("version", ""))
                results[f"php_{ver}_status"] = client.request("/ajax?action=GetPHPStatus", {"version": ver})
        return format_response(results)

    @mcp.tool()
    def abnormal_check_php_cpu(server: str = "") -> str:
        """Check PHP-FPM CPU usage and slow logs for abnormalities.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = {
            "exceptions": client.request("/monitor?action=get_exception"),
            "process_load": request_compat(
                client,
                ["/v2/monitor/process_management/specific_resource_load_type", "/ajax?action=GetProcessList"],
            ),
        }
        return format_response(data)

    @mcp.tool()
    def abnormal_check_cpu(server: str = "") -> str:
        """Check overall CPU for abnormal usage patterns.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = request_compat(
            client,
            ["/v2/monitor/process_management/specific_resource_load_type", "/ajax?action=GetProcessList"],
        )
        return format_response(data)

    @mcp.tool()
    def abnormal_check_memory(server: str = "") -> str:
        """Check memory usage for abnormalities.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = {
            "memory": client.request("/system?action=GetMemInfo"),
            "process_load": request_compat(
                client,
                ["/v2/monitor/process_management/specific_resource_load_type", "/ajax?action=GetProcessList"],
            ),
        }
        return format_response(data)

    @mcp.tool()
    def abnormal_check_disk(server: str = "") -> str:
        """Check disk usage for abnormalities.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/system?action=GetDiskInfo")
        return format_response(data)

    @mcp.tool()
    def abnormal_check_all(server: str = "") -> str:
        """Run all abnormal detection checks at once (MySQL, PHP, CPU, memory, disk).

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = {
            "system_total": client.request("/system?action=GetSystemTotal"),
            "disk": client.request("/system?action=GetDiskInfo"),
            "exceptions": client.request("/monitor?action=get_exception"),
            "process_load": request_compat(
                client,
                ["/v2/monitor/process_management/specific_resource_load_type", "/ajax?action=GetProcessList"],
            ),
        }
        return format_response(data)

    # ==================== Security Baseline ====================

    @mcp.tool()
    def security_baseline_scan(server: str = "") -> str:
        """Run security baseline scan (SSH, system config, permissions audit).

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = request_compat(
            client,
            ["/v2/safe/serversafe/get_security_info", "/san?action=start"],
        )
        return format_response(data)

    @mcp.tool()
    def security_baseline_get_result(server: str = "") -> str:
        """Get security baseline scan results.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = {
            "server_safe": request_compat(
                client,
                ["/v2/safe/serversafe/get_security_info", "/san?action=get_resut"],
            ),
            "ssh_baseline": client.request("/ssh_security?action=san_ssh_security"),
        }
        return format_response(data)

    @mcp.tool()
    def security_baseline_repair(server: str = "", item: str = "") -> str:
        """Repair a specific security baseline issue.

        Args:
            server: Server name (optional)
            item: Issue ID or item name to repair
        """
        client = client_manager.get_client(server or None)
        if item.isdigit():
            data = client.request("/san?action=repair", {"id": item, "item": item})
        else:
            data = client.request("/v2/safe/serversafe/repair_security", {"name": item, "args": "{}"})
        return format_response(data)

    @mcp.tool()
    def security_baseline_repair_all(server: str = "") -> str:
        """Repair all security baseline issues at once.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/san?action=repair_all")
        return format_response(data)

    # ==================== PHP Configuration Optimization ====================

    @mcp.tool()
    def php_get_config(server: str = "", version: str = "") -> str:
        """Get PHP configuration for a specific version.

        Args:
            server: Server name (optional)
            version: PHP version (e.g. 74, 80, 81, 82, 83; auto-detected if omitted)
        """
        client = client_manager.get_client(server or None)
        resolved_ver = version
        if not resolved_ver:
            cfg = client.request("/config?action=get_config")
            if isinstance(cfg, dict):
                for php in cfg.get("php", []):
                    if php.get("setup"):
                        resolved_ver = str(php.get("version", ""))
                        break
        params = {"version": resolved_ver or "83"}
        data = client.request("/ajax?action=GetPHPConfig", params)
        return format_response(data)

    @mcp.tool()
    def php_set_config(
        server: str = "",
        version: str = "",
        config: str = "",
    ) -> str:
        """Set PHP configuration parameters for optimization.

        Args:
            server: Server name (optional)
            version: PHP version
            config: Configuration data (JSON string with key-value pairs)
        """
        client = client_manager.get_client(server or None)
        params = {"version": version}
        if config:
            try:
                parsed = json.loads(config)
                if isinstance(parsed, dict):
                    params.update(parsed)
            except Exception:
                params["config"] = config
        data = client.request("/config?action=SetPHPConf", params)
        return format_response(data)

    @mcp.tool()
    def php_get_fpm_config(server: str = "", version: str = "") -> str:
        """Get PHP-FPM pool configuration (process management, children limits).

        Args:
            server: Server name (optional)
            version: PHP version (auto-detected if omitted)
        """
        client = client_manager.get_client(server or None)
        resolved_ver = version
        if not resolved_ver:
            cfg = client.request("/config?action=get_config")
            if isinstance(cfg, dict):
                for php in cfg.get("php", []):
                    if php.get("setup"):
                        resolved_ver = str(php.get("version", ""))
                        break
        params = {"version": resolved_ver or "83"}
        data = client.request("/config?action=getFpmConfig", params)
        return format_response(data)

    @mcp.tool()
    def php_set_fpm_config(
        server: str = "",
        version: str = "",
        config: str = "",
    ) -> str:
        """Set PHP-FPM pool configuration for performance optimization.

        Args:
            server: Server name (optional)
            version: PHP version
            config: FPM config data (JSON string with max_children, start_servers, min_spare_servers, max_spare_servers, pm)
        """
        client = client_manager.get_client(server or None)
        current = client.request("/config?action=getFpmConfig", {"version": version})
        params = {"version": version, "listen": "unix"}
        if isinstance(current, dict):
            for k in ("max_children", "start_servers", "min_spare_servers", "max_spare_servers", "pm"):
                if k in current:
                    params[k] = str(current[k])
        if config:
            try:
                parsed = json.loads(config)
                if isinstance(parsed, dict):
                    for k, v in parsed.items():
                        params[k] = str(v)
            except Exception:
                params["config"] = config
        data = client.request("/config?action=setFpmConfig", params)
        return format_response(data)

    @mcp.tool()
    def php_set_max_size(
        server: str = "",
        version: str = "",
        max_size: str = "",
    ) -> str:
        """Set PHP max upload size for a version.

        Args:
            server: Server name (optional)
            version: PHP version
            max_size: Max upload size in MB (e.g. 50 or 50M)
        """
        client = client_manager.get_client(server or None)
        clean_max = max_size.rstrip("MmBbGgKk ")
        params = {"version": version, "max": clean_max, "max_size": clean_max}
        data = client.request("/config?action=setPHPMaxSize", params)
        return format_response(data)

    @mcp.tool()
    def php_set_max_time(
        server: str = "",
        version: str = "",
        max_time: str = "",
    ) -> str:
        """Set PHP max execution time for a version.

        Args:
            server: Server name (optional)
            version: PHP version
            max_time: Max execution time in seconds (e.g. 120, 300)
        """
        client = client_manager.get_client(server or None)
        params = {"version": version, "time": max_time, "max_time": max_time}
        data = client.request("/config?action=setPHPMaxTime", params)
        return format_response(data)

    # ==================== Nginx/Apache Configuration ====================

    @mcp.tool()
    def nginx_get_config(server: str = "") -> str:
        """Get Nginx main configuration parameters.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/config?action=GetNginxValue")
        return format_response(data)

    @mcp.tool()
    def nginx_set_config(server: str = "", config: str = "") -> str:
        """Set Nginx main configuration parameters for optimization.

        Args:
            server: Server name (optional)
            config: Nginx config data (JSON string with key-value pairs)
        """
        client = client_manager.get_client(server or None)
        params = {}
        if config:
            try:
                parsed = json.loads(config)
                if isinstance(parsed, dict):
                    params.update(parsed)
                elif isinstance(parsed, list):
                    for item in parsed:
                        if isinstance(item, dict) and "name" in item and "value" in item:
                            params[item["name"]] = item["value"]
            except Exception:
                params["config"] = config
        data = client.request("/config?action=SetNginxValue", params)
        return format_response(data)

    @mcp.tool()
    def apache_get_config(server: str = "") -> str:
        """Get Apache main configuration parameters.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/config?action=GetApacheValue")
        return format_response(data)

    @mcp.tool()
    def apache_set_config(server: str = "", config: str = "") -> str:
        """Set Apache main configuration parameters for optimization.

        Args:
            server: Server name (optional)
            config: Apache config data (JSON string)
        """
        client = client_manager.get_client(server or None)
        params = {}
        if config:
            try:
                parsed = json.loads(config)
                if isinstance(parsed, dict):
                    params.update(parsed)
                elif isinstance(parsed, list):
                    for item in parsed:
                        if isinstance(item, dict) and "name" in item and "value" in item:
                            params[item["name"]] = item["value"]
            except Exception:
                params["config"] = config
        data = client.request("/config?action=SetApacheValue", params)
        return format_response(data)

    # ==================== Panel Auto-Update & Sync ====================

    @mcp.tool()
    def panel_auto_update(server: str = "") -> str:
        """Enable or check panel auto-update setting.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/config?action=AutoUpdatePanel")
        return format_response(data)

    @mcp.tool()
    def panel_sync_time(server: str = "") -> str:
        """Sync server time with NTP.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/config?action=syncDate")
        return format_response(data)

    @mcp.tool()
    def panel_update(server: str = "") -> str:
        """Update aaPanel to the latest version.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = request_compat(
            client,
            ["/ajax?action=UpdatePanel", "/system?action=UpdatePanel"],
        )
        return format_response(data)

    @mcp.tool()
    def panel_check_installed(server: str = "") -> str:
        """Check if essential components are installed.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = request_compat(
            client,
            ["/ajax?action=CheckInstalled", "/config?action=get_settings"],
        )
        return format_response(data)

    @mcp.tool()
    def panel_get_installed_software(server: str = "") -> str:
        """Get list of all installed software/components.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = request_compat(
            client,
            ["/ajax?action=GetInstalled", "/config?action=get_settings"],
        )
        return format_response(data)

    @mcp.tool()
    def panel_get_soft_list(server: str = "") -> str:
        """Get full software store list (all available software).

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = request_compat(
            client,
            ["/plugin?action=get_soft_list", "/system?action=GetSoftList"],
            {"type": "0", "query": "", "p": 1, "row": 50, "force": 0},
        )
        return format_response(data)

    # ==================== Software Install/Uninstall via Files API ====================

    @mcp.tool()
    def soft_install(server: str = "", name: str = "", version: str = "") -> str:
        """Install a software component (nginx, apache, mysql, php, redis, etc.).

        Args:
            server: Server name (optional)
            name: Software name
            version: Version to install
        """
        client = client_manager.get_client(server or None)
        params = {"name": name, "version": version, "type": "0"}
        data = client.request("/files?action=InstallSoft", params)
        return format_response(data)

    @mcp.tool()
    def soft_uninstall(server: str = "", name: str = "", version: str = "", confirmed: bool = False) -> str:
        """Uninstall a software component.

        Args:
            server: Server name (optional)
            name: Software name
            version: Version to uninstall
            confirmed: Must be True to confirm this destructive action
        """
        client = client_manager.get_client(server or None)
        params = {"name": name, "version": version}
        data = client.request("/files?action=UninstallSoft", params, confirmed=confirmed)
        return format_response(data)
