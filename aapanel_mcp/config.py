"""Configuration management for aaPanel MCP server."""

import os
from dataclasses import dataclass, field
from typing import Optional

import yaml


@dataclass
class ServerConfig:
    """Configuration for a single aaPanel instance."""
    name: str
    host: str
    token: str
    verify_ssl: bool = False
    timeout: int = 30

    def __post_init__(self):
        self.host = self.host.rstrip("/")


@dataclass
class MCPConfig:
    """Global MCP configuration."""
    servers: dict[str, ServerConfig] = field(default_factory=dict)
    default_server: str = "default"

    def get_server(self, name: Optional[str] = None) -> ServerConfig:
        """Get server config by name, or the default server."""
        if name is None:
            name = self.default_server
        if name not in self.servers:
            raise KeyError(f"Server '{name}' not found. Available: {list(self.servers.keys())}")
        return self.servers[name]

    def get_server_names(self) -> list[str]:
        """Get list of configured server names."""
        return list(self.servers.keys())


def load_config(config_path: Optional[str] = None) -> MCPConfig:
    """Load configuration from YAML file.

    Search order:
    1. Explicit config_path argument
    2. AAPANEL_CONFIG_PATH environment variable
    3. ./config/servers.yaml
    4. ~/.aapanel-mcp/servers.yaml
    """
    if config_path is None:
        config_path = os.environ.get("AAPANEL_CONFIG_PATH")

    if config_path is None:
        candidates = [
            os.path.join(os.getcwd(), "config", "servers.yaml"),
            os.path.expanduser("~/.aapanel-mcp/servers.yaml"),
        ]
        for path in candidates:
            if os.path.exists(path):
                config_path = path
                break

    if config_path is None or not os.path.exists(config_path):
        raise FileNotFoundError(
            "No configuration file found. Set AAPANEL_CONFIG_PATH env var "
            "or create config/servers.yaml or ~/.aapanel-mcp/servers.yaml"
        )

    with open(config_path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    config = MCPConfig()
    for server_data in raw.get("servers", []):
        server = ServerConfig(
            name=server_data["name"],
            host=server_data["host"],
            token=server_data["token"],
            verify_ssl=server_data.get("verify_ssl", False),
            timeout=server_data.get("timeout", 30),
        )
        config.servers[server.name] = server

    global_cfg = raw.get("global", {})
    config.default_server = global_cfg.get("default_server", "default")

    if not config.servers:
        raise ValueError("No servers configured in configuration file")

    if config.default_server not in config.servers:
        first = next(iter(config.servers))
        config.default_server = first

    return config
