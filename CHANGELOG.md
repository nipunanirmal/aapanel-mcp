# Changelog

All notable changes to aaPanel MCP Server are documented here.
Tags follow semantic versioning (`vMAJOR.MINOR.PATCH`).

## Unreleased

_No unreleased changes yet._

---

## v1.3.0 — 2026-10-15

### Fixed (aaPanel v8.0.7 compatibility audit — all 282 tools checked against live panel)

- **Sites**: `site_get_domains` now uses correct `GetSiteDomains` action casing (was 404); `site_get_traffic_stats` sends `id` instead of `siteId`; `site_create` now serializes `webname` to the JSON format panel expects; `site_set_redirect` maps to `CreateRedirect` params (`tourl`, `redirectdomain`, `domainorpath`, `holdpath`); `site_set_proxy` sends `proxysite`/`todomain`/`subfilter`; `site_set_php_version` resolves `siteName` from ID; `site_delete_domain` resolves `webname`/`port`
- **Panel SSL**: `config_get_panel_ssl`/`config_save_panel_ssl` moved from `/ssl` to `/config` route and send `privateKey`/`certPem`
- **SSL certs**: `ssl_get_list`/`ssl_save_cert`/`ssl_delete_cert`/`ssl_apply_letsencrypt` migrated to `/v2/ssl_domain` actions; `ssl_get_cert` resolves by cert hash/subject via cert list; `ssl_renew` uses `renew_lets_ssl`
- **Docker**: all 10 tools migrated from dead `/panel/docker/*` paths to working `/v2/btdocker/*` routes (container list/info/status/stop/restart/logs, image list/remove, network, volume)
- **Projects**: remapped per-type endpoints to v2 routes (`/v2/project/nodejs/...`, `/v2/mod/java/...`, `/v2/mod/proxy/...`); `project_get_config`/`project_get_status` use `get_project_info` (was `get_project_config`/`get_project_status` → "not found method")
- **Firewall**: `network_scan_firewall_rules` uses `/v2/firewall/com/port_rules_list` + `ip_rules_list` (was 404 on `/firewall?action=GetList`); `network_scan_ports` uses `/v2/safe/firewall/get_listening_processes` (was "not found method scan_ports"); delete rules now include required `port`/`ip` params
- **Monitoring**: `monitor_get_history` replaced nonexistent `/monitor?action=GetHistory` with `/ajax` `GetCpuIo`/`GetDiskIo`/`GetNetWorkIo`; `monitor_get_process_list`/`process_list` use `/v2/monitor/process_management/specific_resource_load_type` (old `/ajax?action=GetProcessList` timed out); `cpu_get_process_tops`/`cpu_get_high_cpu_processes` now send required `start`/`end` params; `service_get_php_status`/`monitor_get_php_status` auto-detect installed PHP version
- **Security**: `antitheft_*` resolve site `id` from name and send full `SetSecurity` params; `tamper_*_file_deny` send required `website`/`deny_name`/`dir`/`suffix`; `harden_get_ssh_config`/`ssh_get_info` use `/v2/safe/ssh/GetSshInfo` + `/ssh_security?action=get_config` (was dead `/safe` route); `harden_set_ssh_key_auth` sends `ssh`/`type` key params; `cve_*` tools migrated from absent `/vul_scan` to `/warning` module; `security_baseline_*` use `/v2/safe/serversafe/*` + `/san`; `security_get_operation_logs` uses `/data?action=getData&table=logs` (was 500 on missing `path`); `alert_set_warning` sends required `id`; `virus_scan_web` uses `/v2/project/webbasicscanning/*`; `virus_scan_safe_detect` uses `/v2/safecloud`/`/v2/safe_detect`
- **Abnormal detection**: `abnormal_check_*` remapped from missing `/abnormal` module to composites of `/monitor?action=get_exception`, `/system?action=GetDiskInfo`, `/database?action=GetRunStatus`, and `/v2/monitor/process_management/specific_resource_load_type`
- **Backup/tasks**: `backup_create`/`backup_delete` use real routes (`/site?action=ToBackup`, `/database?action=ToBackup`, `/bak?action=backup_*`, `/site?action=DelBackup`) — `/backup` route doesn't exist; `backup_list`/`site_get_backup_list`/`database_get_backups` send correct `type` filter; `task_get_info` uses `/data?action=getFind` (was nonexistent `/task?action=get_task_find`)
- **Files**: `file_move`/`file_copy` send `dfile`; `file_compress` sends `path`/`sfile`/`dfile`/`z_type` per `Zip` signature; `file_unzip` sends `dfile`/`password`; `file_chmod` sends `filename`/`access`/`all`; `file_download` derives `filename`; `file_stat` sends `filename`
- **System/config**: `system_service_admin` sends `type` (was `act`); `config_set_username` sends `username1`/`username2`; `config_set_basic_auth` sends `open`; `config_set_ip_whitelist`/`harden_set_ip_whitelist` use `login_ipwhite` `type`+`ip` per-IP calls; `config_set_api_token` sends `t_type`; `config_get_login_log`/`logs_get_security_logs`/`ssh_get_logs` send `p` not `page`; `harden_set_improvement` uses `/v2/config`; `panel_update` uses `/ajax?action=UpdatePanel`; `panel_check_installed`/`panel_get_installed_software`/`panel_get_soft_list` use real endpoints (were stubs hitting `get_settings`/`GetSoftList`); `logs_get_panel_log_file` reads `logs/error.log` (was nonexistent `data/error.log`)
- **FTP**: `ftp_set_password` sends `ftp_username`/`new_password`
- **Deployment**: `deployment_get_list` uses `/v2/deployment?action=GetList` (was generic `/plugin?action=a` → HTTP 500); `deployment_install` sends `dname`/`site_name`
- **Plugins**: `plugin_get_installed_list` uses `get_soft_list` (was `getPluginList` 404); `plugin_get_config`/`plugin_set_config`/`plugin_set_status` send `name` and fallback to `get_soft_find`
- **Database**: `database_create` sends `db_user`/`dataAccess`/`codeing`/`dtype` fields panel requires
- **Crontab**: `crontab_get_backup_list` sends `cron_id`/`p`/`rows`
- **Safety/infra**: `safety.py` extracts actions from path-style `/v2/...` endpoints (e.g. `stop`, `remove`, `remove_cert`, `delete`); `format_response` handles v2 `{status: -1, message}` error envelopes; `pyproject.toml` had an invalid stray DMARC line removed from `[tool.setuptools]` section

### Added

- **`request_compat()` endpoint fallback** (`utils/__init__.py`) — every tool migrated to a v8.0.7-only route now tries the new endpoint first and transparently falls back to the legacy v1 endpoint when the panel reports the route missing (HTTP 404, "not found method", "module not found"). The same MCP build works on both old and new aaPanel versions. Fallback chains cover: Docker (`/v2/btdocker/*` → `/panel/docker/*`), SSL (`/v2/ssl_domain` → `/ssl`), Projects (v2 → legacy per-type routes), SSH info/logs, process list, Memcached status, firewall info/rules, site stats, deployment list, panel SSL, plugin list, CVE scan (`/warning` → `/vul_scan`), safe detect, web scanning, security baseline, panel update/installed/soft-list

### Known limitations (environment-dependent, not MCP bugs)

- `waf_*` tools need the **btwaf** plugin installed
- `service_get_memcached_status` fails on panels without Memcached (panel-side traceback)
- `virus_scan_web`/`virus_scan_get_web_result` need the `webbasicscanning` module
- `deployment_*` needs the deployment plugin
- `terminal_execute_command` needs the Terminal Bridge plugin

### Changed

- Tool count corrected: 282 tools (was documented as 278)
- Tested and verified against **aaPanel v8.0.7** (Ubuntu 24.04, Nginx 1.30, MySQL 8.0, PHP 8.3); route files `v1.py`/`v2.py` verified byte-identical to panel

## v1.2.3 — 2026-07-24

### Fixed
- PyInstaller spec: use root `main.py` (absolute imports) instead of `aapanel_mcp/main.py` (relative imports) — fixes `ImportError` in standalone binaries

## v1.2.2 — 2026-07-24

### Fixed
- `pyproject.toml` build backend changed from `setuptools.backends._legacy:_Backend` to `setuptools.build_meta` (Copilot PR #1)
- Bumped version to `1.2.2` in `pyproject.toml` and `__init__.py`

## v1.2.0 — 2026-07-24

### Added
- **Dual distribution**: PyInstaller standalone binaries (Linux x64, macOS, Windows) + PyPI package (`pip install aapanel-mcp`)
- `aapanel_mcp.spec` — PyInstaller spec file with hidden imports for all 19 tool modules + MCP/httpx/yaml/pydantic dependencies
- GitHub Actions workflow expanded to 4 jobs: `plugin-zip`, `binaries` (3-OS matrix), `pypi` (trusted publishing), `publish-release`
- `pyproject.toml` updated with full PyPI metadata: authors, keywords, classifiers, project URLs, package-data
- README updated with three installation options (pip/uvx, standalone binary, from source) and MCP client config examples
- Entry point `aapanel-mcp` console script registered in `pyproject.toml`

### Changed
- Version bumped to `1.2.0`
- `.gitignore` updated with PyInstaller build output patterns

## v1.1.0 — 2026-07-24

### Added
- **Explicit Terminal Bridge installer** — `terminal_install_bridge` MCP tool with confirmation gate
- `terminal_bridge_status` tool to check bridge installation state
- `install_plugin_from_release()` method in `aaPanelClient` — downloads ZIP from GitHub release and imports via aaPanel plugin API
- GitHub Actions workflow (`release.yml`) to package `mcp_terminal.zip` and attach to releases
- Plugin icon (`icon.png`, 256x256) added to `plugin/mcp_terminal/`
- README section: "Optional aaPanel Terminal Bridge" documenting the opt-in workflow

### Changed
- Plugin `info.json` version bumped to `1.1`
- `pyproject.toml` version bumped to `1.1.0`
- Bridge is **never** installed silently — requires explicit `confirmed=true`

## v1.0.0 — 2026-07-23

### Added
- **278 MCP tools** across 19 modules
- Full aaPanel API coverage: system, sites, databases, FTP, files, firewall, crontab, SSL, panel config, plugins, Docker, projects, logs, SSH, backup/tasks, monitoring, deployment, optimization, security
- Multi-server support — manage multiple aaPanel instances from one MCP server
- Token-based authentication using aaPanel's native API token (MD5 signing)
- Safety guard module — blocks deletion of critical paths and system databases, requires confirmation for destructive operations
- Retry with backoff — 2 retries with 1s/2s delays for transient errors
- Config search order: `AAPANEL_CONFIG_PATH` env var → `./config/servers.yaml` → `~/.aapanel-mcp/servers.yaml`
- stdio transport for Windsurf, Cursor, Claude Desktop integration
- Tested against aaPanel v8.0.4 (Ubuntu 24.04, Nginx 1.30, MySQL 8.0, PHP 8.3)

### Known Issues (v1.0.0)
- `/abnormal?action=*` endpoints return 404 — panel version doesn't have this module
- Docker tools return "module not found" if Docker plugin not installed on panel
