# Changelog

All notable changes to aaPanel MCP Server are documented here.
Tags follow semantic versioning (`vMAJOR.MINOR.PATCH`).

## Unreleased

_No unreleased changes yet._

---

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
