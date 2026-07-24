# aaPanel MCP Server

Full-featured MCP (Model Context Protocol) server for aaPanel management. Provides **278 tools** across 19 modules covering all major aaPanel functionality: system, sites, databases, FTP, files, firewall, crontab, SSL, config, plugins, Docker, projects, logs, SSH, backups, monitoring, deployment, **system optimization** (RAM cleanup, CPU tuning, storage management, WAF, PHP/Nginx/Apache optimization), and **security** (network scan, website statistics, tamper proof, system hardening, virus scan, CVE scanning, anti-theft).

## aaPanel Version Compatibility

**Tested against aaPanel v8.0.4** (Ubuntu 24.04, Nginx 1.30, MySQL 8.0, PHP 8.3)

> **Important:** aaPanel API endpoints may change between panel versions. If you encounter 404 errors or unexpected responses after updating aaPanel, the endpoint mappings in `aapanel_mcp/tools/*.py` may need to be updated. See [Contributing](#contributing) for details on how to fix endpoints.

| aaPanel Version | Status | Notes |
|----------------|--------|-------|
| 8.0.4 | ✅ Tested | All endpoints verified July 2026 |
| 8.x | ⚠️ Likely works | Report issues if endpoints change |
| 7.x | ❓ Untested | May require endpoint updates |

## Features

- **278 MCP tools** across 19 modules
- **Multi-server support** — manage multiple aaPanel instances from one MCP server
- **Full API coverage** — websites, databases, FTP, files, firewall, cron, SSL, Docker, projects, and more
- **System optimization** — RAM cleanup, CPU tuning, storage management, WAF, security baseline scanning, PHP/Nginx/Apache config optimization
- **Security** — network scanning, website statistics, tamper proof (file integrity), system hardening (SSH, 2FA, IP whitelist), virus/malware scan, CVE vulnerability scanning, anti-theft/hotlink protection, traffic limiting, alert configuration
- **Safety guard** — built-in protection against accidental deletion of critical resources
- **Token-based authentication** — uses aaPanel's native API token mechanism
- **Retry with backoff** — 2 retries with 1s/2s delays for transient errors
- **stdio transport** — integrates with Windsurf, Cursor, Claude Desktop, and other MCP clients

## Quick Start

### 1. Install dependencies

```bash
cd aapanel-mcp
pip install -r requirements.txt
```

### 2. Configure servers

Copy the example config and fill in your panel details:

```bash
cp config/servers.yaml.example config/servers.yaml
```

Edit `config/servers.yaml`:

```yaml
servers:
  - name: "prod-01"
    host: "http://192.168.1.100:8888"
    token: "YOUR_API_TOKEN"
    verify_ssl: false
    timeout: 30

global:
  default_server: "prod-01"
```

**To get your API token:**
1. Log in to aaPanel
2. Go to **Settings** → **API Interface**
3. Enable API interface
4. Copy the API token

### 3. Run the server

```bash
python main.py
```

### 4. Configure in Windsurf

Add to your Windsurf MCP settings:

```json
{
  "mcpServers": {
    "aapanel": {
      "command": "python",
      "args": ["/path/to/aapanel-mcp/main.py"],
      "env": {
        "AAPANEL_CONFIG_PATH": "/path/to/aapanel-mcp/config/servers.yaml"
      }
    }
  }
}
```

### 5. Configure in Cursor

Add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "aapanel": {
      "command": "python",
      "args": ["/path/to/aapanel-mcp/main.py"],
      "env": {
        "AAPANEL_CONFIG_PATH": "/path/to/aapanel-mcp/config/servers.yaml"
      }
    }
  }
}
```

### 6. Configure in Claude Desktop

Add to Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "aapanel": {
      "command": "python",
      "args": ["/path/to/aapanel-mcp/main.py"],
      "env": {
        "AAPANEL_CONFIG_PATH": "/path/to/aapanel-mcp/config/servers.yaml"
      }
    }
  }
}
```

## Tool Categories

| Category | Tools | Description |
|----------|-------|-------------|
| System | 12 | CPU, memory, disk, network, service management |
| Sites | 20 | Create, delete, SSL, redirect, proxy, domains, backups |
| Databases | 12 | MySQL/PostgreSQL databases, backups, logs |
| FTP | 5 | FTP user management |
| Files | 15 | File operations (read, write, mkdir, compress, etc.) |
| Firewall | 8 | Port and IP rules, panel port |
| Crontab | 7 | Cron job management |
| SSL | 8 | Certificate management, Let's Encrypt |
| Panel Config | 15 | Panel settings, users, auth, API config |
| Plugins | 8 | Software/plugin install, configure |
| Docker | 10 | Container, image, network, volume management |
| Projects | 8 | Java/Node/Go/Python/.NET/Proxy/HTML projects |
| Logs | 8 | Panel, security, error, Nginx, Apache, Redis logs |
| SSH | 4 | SSH config, logs, security audit |
| Backup/Tasks | 6 | Backup management, background tasks |
| Monitoring | 5 | Real-time and historical monitoring |
| Deployment | 3 | One-click deployment packages |
| Optimization | 68 | RAM cleanup, CPU tuning, storage mgmt, WAF, security baseline, PHP/Nginx/Apache config, process mgmt, abnormal detection, software install |
| Security | 62 | Network scan, website stats, tamper proof, system hardening (SSH/2FA/IP whitelist), virus/malware scan, CVE scan, anti-theft, traffic limiting, alerts, operation logs |

## Safety Rules

The MCP server has a **built-in safety guard** that protects critical aaPanel resources from accidental or unauthorized deletion. This is enforced at the API client level — no tool can bypass it.

### Permanently Blocked (never allowed, even with confirmation)

- **Deleting files in critical paths**: `/www/server/panel`, `/www/server/data`, `/www/server/mysql`, `/www/server/nginx`, `/www/server/apache`, `/www/server/php`, `/www/server/docker`, `/www/wwwroot`, `/www/backup`, `/www/database`, `/root`, `/etc`, `/var/lib/mysql`, `/var/lib/docker`, `/var/lib/redis`, `/var/lib/postgresql`, `/boot`, `/proc`, `/sys`, `/dev`
- **Deleting system databases**: `mysql`, `information_schema`, `performance_schema`, `sys`, `postgres`, `template0`, `template1`

### Requires Explicit User Confirmation

The AI assistant **must ask for your permission** before executing any of these actions. Even if you request deletion in chat, the AI will prompt you to confirm before proceeding:

- **Databases**: `DeleteDatabase`, `DelBackup`
- **Docker**: `StopContainer`, `DeleteImage`, `DeleteVolume`, `DeleteNetwork`
- **Sites**: `DeleteSite`, `SiteStop`, `DelDomain`
- **Files**: `DeleteFile` (outside protected paths)
- **FTP**: `DeleteUser`
- **Firewall**: `DelAcceptPort`, `DelDropAddress`
- **Crontab**: `DelCrontab`
- **SSL**: `RemoveCert`
- **Plugins**: `uninstall_plugin`
- **Software**: `UninstallSoft`
- **System**: `KillProcess`, `ClearSystem`, `RestartServer`
- **Panel**: `ClosePanel`
- **Tasks**: `remove_task`
- **SSH**: `stop_password`, `stop_root`, `stop_key`, `stop_jian`
- **Tamper**: `del_file_deny`
- **Sessions**: `DelOldSession`
- **Cleanup**: `CloseLogs`, `clean_panel_error_logs`, `clear_temp_login`, `ReMemory`, `ReWeb`, `RepPanel`

### How It Works

1. Every API request passes through `check_request_safety()` before being sent to aaPanel
2. Blocked operations return `{"status": false, "blocked_by_safety": true}` with an explanation
3. Unconfirmed destructive operations return `{"status": false, "confirmation_required": true}` — the AI must ask you to confirm
4. Read-only operations (get, list, status) pass through without any restriction

## Multi-Server Usage

All tools accept an optional `server` parameter to target a specific panel:

```python
# Use default server
system_get_status()

# Target a specific server
system_get_status(server="staging-01")
```

## Configuration Reference

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `name` | Yes | — | Server identifier |
| `host` | Yes | — | Panel URL (e.g. `http://ip:8888`) |
| `token` | Yes | — | API token from panel settings |
| `verify_ssl` | No | `false` | Verify SSL certificates |
| `timeout` | No | `30` | Request timeout in seconds |

## Authentication

The MCP server uses aaPanel's native API token mechanism:

```
request_token = md5(request_time + md5(api_token))
```

This is sent as query parameters with each API request. No session cookies or login flows are needed.

## Project Structure

```
aapanel-mcp/
├── main.py                     # Entry point
├── requirements.txt
├── pyproject.toml
├── LICENSE
├── .gitignore
├── config/
│   ├── servers.yaml.example    # Example configuration (safe to commit)
│   └── servers.yaml            # Your actual config (gitignored)
└── aapanel_mcp/
    ├── __init__.py
    ├── main.py                 # Main entry
    ├── server.py               # MCP server setup
    ├── client.py               # aaPanel API client (retry, timeout, auth)
    ├── config.py               # Configuration management
    ├── safety.py               # Safety guard for destructive operations
    ├── utils/
    │   └── __init__.py         # Utility functions (format_response)
    └── tools/
        ├── system.py           # System tools (12)
        ├── sites.py            # Site tools (20)
        ├── databases.py        # Database tools (12)
        ├── ftp.py              # FTP tools (5)
        ├── files.py            # File tools (15)
        ├── firewall.py         # Firewall tools (8)
        ├── crontab.py          # Crontab tools (7)
        ├── ssl.py              # SSL tools (8)
        ├── panel_config.py     # Config tools (15)
        ├── plugins.py          # Plugin tools (8)
        ├── docker.py           # Docker tools (10)
        ├── projects.py         # Project tools (8)
        ├── logs.py             # Log tools (8)
        ├── ssh.py              # SSH tools (4)
        ├── backup.py           # Backup/task tools (6)
        ├── monitoring.py       # Monitoring tools (5)
        ├── deployment.py       # Deployment tools (3)
        ├── optimization.py     # Optimization tools (68)
        └── security.py         # Security tools (62)
```

## Contributing

Contributions are welcome! aaPanel updates may change API endpoints, so community help keeping this project up-to-date is greatly appreciated.

### How to Fix Broken Endpoints

If a tool returns a 404 error or unexpected response after an aaPanel update:

1. **Find the broken tool** — check which tool returned the error and which file it's in (`aapanel_mcp/tools/*.py`)
2. **Find the correct endpoint** — open aaPanel's web UI, use browser DevTools (Network tab) to see which API endpoint the UI calls for the same action
3. **Update the endpoint** — edit the corresponding `client.request("/path?action=ActionName", params)` call in the tool file
4. **Test** — restart the MCP server and call the tool to verify
5. **Submit a PR** — with a description like "Fix endpoint for tool X (aaPanel v8.x)"

### Common Endpoint Patterns

aaPanel uses a few consistent patterns:

| Pattern | Example | Used for |
|---------|---------|----------|
| `/data?action=getData&table=X` | `/data?action=getData&table=sites` | Listing data (sites, databases, firewall, etc.) |
| `/module?action=ActionName` | `/database?action=AddDatabase` | Module-specific actions |
| `/config?action=get_config` | `/config?action=get_config` | Panel configuration |
| `/plugin?action=a` | `/plugin?action=a` | Plugin operations |
| `/ajax?action=GetX` | `/ajax?action=GetNginxStatus` | Real-time status/monitoring |
| `/system?action=GetX` | `/system?action=GetNetWork` | System information |

### Development Setup

```bash
git clone https://github.com/nipunanirmal/aapanel-mcp.git
cd aapanel-mcp
pip install -r requirements.txt
cp config/servers.yaml.example config/servers.yaml
# Edit servers.yaml with your panel details
python main.py
```

### Guidelines

- Keep changes minimal and focused
- Test against a real aaPanel instance before submitting
- Update the version compatibility table in this README if you test against a new aaPanel version
- Don't commit real credentials (servers.yaml is gitignored)

## License

MIT — see [LICENSE](LICENSE)
