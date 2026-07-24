import re
from typing import Any

from mcp.server.fastmcp import FastMCP

from ..client import client_manager
from ..utils import format_response

_SECRET_FIELDS = {"password", "pkey", "pkey_passwd"}
_BRIDGE_NAME = "mcp_terminal"
_BRIDGE_RELEASE_URL = "https://github.com/nipunanirmal/aapanel-mcp/releases/latest/download/mcp_terminal.zip"
_READ_ONLY_COMMANDS = re.compile(
    r"^\s*(?:cat|df|du|free|grep|head|hostname|id|ip|journalctl|ls|ps|pwd|ss|stat|tail|top|uname|uptime|whoami)\b",
    re.IGNORECASE,
)


def _redact_secrets(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: "[redacted]" if key.lower() in _SECRET_FIELDS else _redact_secrets(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_redact_secrets(item) for item in value]
    return value


def _bridge_status(server: str) -> dict[str, Any]:
    client = client_manager.get_client(server or None)
    data = client.request("/plugin?action=get_soft_list", {"type": "10", "query": _BRIDGE_NAME, "p": 1, "row": 30, "force": 0})
    entries = data.get("list", {}).get("data", []) if isinstance(data, dict) else []
    installed = any(entry.get("name") == _BRIDGE_NAME and entry.get("setup") for entry in entries)
    return {"status": True, "installed": installed, "release_url": _BRIDGE_RELEASE_URL}


def _execute_command(server: str, host: str, command: str, timeout: int, confirmed: bool) -> dict[str, Any]:
    client = client_manager.get_client(server or None)
    return client.request(
        "/mcp_terminal/execute.json",
        {
            "host": host,
            "command": command,
            "timeout": timeout,
            "confirmed": str(confirmed).lower(),
        },
    )


def register_terminal_tools(mcp: FastMCP) -> None:
    @mcp.tool()
    def terminal_bridge_status(server: str = "") -> str:
        """Check whether the aaPanel Terminal Bridge plugin is installed without changing the panel.

        The bridge is required because aaPanel Terminal uses an interactive browser WebSocket that cannot be securely
        reused by an API-token MCP client. The plugin runs inside aaPanel, validates the existing API-token signature,
        and uses only Terminal hosts already saved in the panel.
        """
        return format_response(_bridge_status(server))

    @mcp.tool()
    def terminal_install_bridge(server: str = "", confirmed: bool = False) -> str:
        """Install the aaPanel Terminal Bridge from this project's GitHub release.

        This is never automatic. The plugin enables MCP terminal commands through saved aaPanel Terminal hosts.
        It is downloaded only from the official release asset and imported through aaPanel's third-party plugin API.
        Call once with confirmed=false to review the reason and release URL, then again with confirmed=true to install.
        """
        status = _bridge_status(server)
        if status.get("installed"):
            return "The aaPanel Terminal Bridge is already installed. No action was taken."
        if not confirmed:
            return (
                "The aaPanel Terminal Bridge is not installed. It is required because aaPanel Terminal uses an "
                "interactive browser WebSocket, while MCP authenticates with the aaPanel API token. The bridge "
                "validates that token inside aaPanel and uses only saved Terminal hosts. No plugin was downloaded "
                f"or installed. Release URL: {_BRIDGE_RELEASE_URL}. Confirm explicitly, then call again with confirmed=true."
            )
        client = client_manager.get_client(server or None)
        return format_response(client.install_plugin_from_release(_BRIDGE_NAME, _BRIDGE_RELEASE_URL, confirmed=True))

    @mcp.tool()
    def terminal_list_servers(server: str = "") -> str:
        client = client_manager.get_client(server or None)
        data = client.request("/xterm?action=get_host_list")
        return format_response(_redact_secrets(data))

    @mcp.tool()
    def terminal_execute_command(
        host: str,
        command: str,
        server: str = "",
        timeout: int = 30,
        confirmed: bool = False,
    ) -> str:
        if not _READ_ONLY_COMMANDS.match(command) and not confirmed:
            return (
                "CONFIRMATION REQUIRED: This terminal command can modify the remote VPS. "
                "Confirm explicitly, then call again with confirmed=true."
            )
        if timeout < 1 or timeout > 300:
            return "Error: timeout must be between 1 and 300 seconds"
        return format_response(_execute_command(server, host, command, timeout, confirmed))
