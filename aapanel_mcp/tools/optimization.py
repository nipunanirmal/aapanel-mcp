"""System optimization and cleanup tools for aaPanel MCP server.

Covers: system cleanup, RAM release, CPU optimization, storage management,
log deletion, process management, WAF management, and performance tuning.
"""

from mcp.server.fastmcp import FastMCP
from ..client import client_manager
from ..utils import format_response


def register_optimization_tools(mcp: FastMCP) -> None:
    """Register all system optimization and cleanup tools."""

    # ==================== System Cleanup ====================

    @mcp.tool()
    def system_clear_all_cache(server: str = "") -> str:
        """Clear all system garbage: mail logs, temp files, install cache, wwwlogs.
        Returns count of files cleaned and total space freed.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/system?action=ClearSystem")
        return format_response(data)

    @mcp.tool()
    def system_release_memory(server: str = "") -> str:
        """Release/flush system memory (RAM cleanup). Runs sync and memory release script.
        Returns updated memory info after release.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/system?action=ReMemory")
        return format_response(data)

    @mcp.tool()
    def system_clear_panel_logs(server: str = "") -> str:
        """Clear aaPanel error logs.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/config?action=clean_panel_error_logs")
        return format_response(data)

    @mcp.tool()
    def system_clear_site_logs(server: str = "", siteName: str = "") -> str:
        """Clear access/error logs for a specific site.

        Args:
            server: Server name (optional)
            siteName: Site domain name
        """
        client = client_manager.get_client(server or None)
        params = {"siteName": siteName}
        data = client.request("/files?action=CloseLogs", params)
        return format_response(data)

    @mcp.tool()
    def system_clear_all_logs(server: str = "") -> str:
        """Close/clear all website logs on the server.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/files?action=CloseLogs")
        return format_response(data)

    @mcp.tool()
    def system_clear_old_sessions(server: str = "") -> str:
        """Delete old panel sessions to free up resources.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/config?action=DelOldSession")
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
            start: Start timestamp
            end: End timestamp
        """
        client = client_manager.get_client(server or None)
        params = {"start": start, "end": end}
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
            start: Start timestamp
            end: End timestamp
        """
        client = client_manager.get_client(server or None)
        params = {"start": start, "end": end}
        data = client.request("/ajax?action=GetCpuIo", params)
        return format_response(data)

    @mcp.tool()
    def cpu_get_process_tops(server: str = "") -> str:
        """Get top processes by resource consumption (CPU/memory ranking).

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/ajax?action=get_process_tops")
        return format_response(data)

    @mcp.tool()
    def cpu_get_high_cpu_processes(server: str = "") -> str:
        """Get list of processes with high CPU usage.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/ajax?action=get_process_cpu_high")
        return format_response(data)

    @mcp.tool()
    def process_list(server: str = "") -> str:
        """List all running processes with CPU and memory usage.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/ajax?action=GetProcessList")
        return format_response(data)

    @mcp.tool()
    def process_kill(server: str = "", pid: str = "") -> str:
        """Kill a specific process by PID.

        Args:
            server: Server name (optional)
            pid: Process ID to kill
        """
        client = client_manager.get_client(server or None)
        params = {"pid": pid}
        data = client.request("/ajax?action=KillProcess", params)
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
            start: Start timestamp
            end: End timestamp
        """
        client = client_manager.get_client(server or None)
        params = {"start": start, "end": end}
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
            version: PHP version (e.g. 74, 80, 81, 82, 83)
        """
        client = client_manager.get_client(server or None)
        params = {"version": version}
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
        data = client.request("/ajax?action=GetMemcachedStatus")
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
        params = {"name": "btwaf", "fun": "index"}
        data = client.request("/plugin?action=a", params)
        return format_response(data)

    @mcp.tool()
    def waf_get_sites(server: str = "") -> str:
        """Get list of sites protected by WAF.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        params = {"name": "btwaf", "fun": "get_sites"}
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
        params = {"name": "btwaf", "fun": "set_site_status", "siteName": siteName, "status": status}
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
        params = {"name": "btwaf", "fun": "get_logs", "siteName": siteName, "p": page, "limit": limit}
        data = client.request("/plugin?action=a", params)
        return format_response(data)

    @mcp.tool()
    def waf_get_rules(server: str = "") -> str:
        """Get WAF rule list (URL, IP, UA, CC rules).

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        params = {"name": "btwaf", "fun": "get_rules"}
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
        params = {"name": "btwaf", "fun": "add_rule", "type": rule_type, "value": rule_value, "ps": ps}
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
        params = {"name": "btwaf", "fun": "del_rule", "id": rule_id}
        data = client.request("/plugin?action=a", params)
        return format_response(data)

    # ==================== Abnormal Detection ====================

    @mcp.tool()
    def abnormal_check_mysql_server(server: str = "") -> str:
        """Check MySQL server for abnormal configuration issues.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/abnormal?action=mysql_server")
        return format_response(data)

    @mcp.tool()
    def abnormal_check_mysql_cpu(server: str = "") -> str:
        """Check MySQL CPU usage for abnormalities.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/abnormal?action=mysql_cpu")
        return format_response(data)

    @mcp.tool()
    def abnormal_check_php_server(server: str = "") -> str:
        """Check PHP-FPM for abnormal configuration.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/abnormal?action=php_server")
        return format_response(data)

    @mcp.tool()
    def abnormal_check_php_cpu(server: str = "") -> str:
        """Check PHP-FPM CPU usage for abnormalities.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/abnormal?action=php_cpu")
        return format_response(data)

    @mcp.tool()
    def abnormal_check_cpu(server: str = "") -> str:
        """Check overall CPU for abnormal usage patterns.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/abnormal?action=CPU")
        return format_response(data)

    @mcp.tool()
    def abnormal_check_memory(server: str = "") -> str:
        """Check memory usage for abnormalities.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/abnormal?action=Memory")
        return format_response(data)

    @mcp.tool()
    def abnormal_check_disk(server: str = "") -> str:
        """Check disk usage for abnormalities.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/abnormal?action=disk")
        return format_response(data)

    @mcp.tool()
    def abnormal_check_all(server: str = "") -> str:
        """Run all abnormal detection checks at once (MySQL, PHP, CPU, memory, disk).

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/abnormal?action=start")
        return format_response(data)

    # ==================== Security Baseline ====================

    @mcp.tool()
    def security_baseline_scan(server: str = "") -> str:
        """Run security baseline scan (SSH, system config, permissions audit).

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/san?action=start")
        return format_response(data)

    @mcp.tool()
    def security_baseline_get_result(server: str = "") -> str:
        """Get security baseline scan results.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/san?action=get_resut")
        return format_response(data)

    @mcp.tool()
    def security_baseline_repair(server: str = "", item: str = "") -> str:
        """Repair a specific security baseline issue.

        Args:
            server: Server name (optional)
            item: Issue item to repair
        """
        client = client_manager.get_client(server or None)
        params = {"item": item}
        data = client.request("/san?action=repair", params)
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
            version: PHP version (e.g. 74, 80, 81, 82, 83)
        """
        client = client_manager.get_client(server or None)
        params = {"version": version}
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
        params = {"version": version, "config": config}
        data = client.request("/ajax?action=SetPHPConfig", params)
        return format_response(data)

    @mcp.tool()
    def php_get_fpm_config(server: str = "", version: str = "") -> str:
        """Get PHP-FPM pool configuration (process management, children limits).

        Args:
            server: Server name (optional)
            version: PHP version
        """
        client = client_manager.get_client(server or None)
        params = {"version": version}
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
            config: FPM config data (JSON string)
        """
        client = client_manager.get_client(server or None)
        params = {"version": version, "config": config}
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
            max_size: Max upload size (e.g. 50M, 100M)
        """
        client = client_manager.get_client(server or None)
        params = {"version": version, "max_size": max_size}
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
        params = {"version": version, "max_time": max_time}
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
        params = {"config": config}
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
        params = {"config": config}
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
        data = client.request("/system?action=UpdatePanel")
        return format_response(data)

    @mcp.tool()
    def panel_check_installed(server: str = "") -> str:
        """Check if essential components are installed.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/config?action=get_settings")
        return format_response(data)

    @mcp.tool()
    def panel_get_installed_software(server: str = "") -> str:
        """Get list of all installed software/components.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/config?action=get_settings")
        return format_response(data)

    @mcp.tool()
    def panel_get_soft_list(server: str = "") -> str:
        """Get full software store list (all available software).

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/system?action=GetSoftList")
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
        params = {"name": name, "version": version}
        data = client.request("/files?action=InstallSoft", params)
        return format_response(data)

    @mcp.tool()
    def soft_uninstall(server: str = "", name: str = "", version: str = "") -> str:
        """Uninstall a software component.

        Args:
            server: Server name (optional)
            name: Software name
            version: Version to uninstall
        """
        client = client_manager.get_client(server or None)
        params = {"name": name, "version": version}
        data = client.request("/files?action=UninstallSoft", params)
        return format_response(data)
