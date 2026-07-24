"""MCP server setup and tool registration."""

import logging

from mcp.server.fastmcp import FastMCP

from .client import client_manager
from .config import load_config
from .tools.system import register_system_tools
from .tools.sites import register_site_tools
from .tools.databases import register_database_tools
from .tools.ftp import register_ftp_tools
from .tools.files import register_file_tools
from .tools.firewall import register_firewall_tools
from .tools.crontab import register_crontab_tools
from .tools.ssl import register_ssl_tools
from .tools.panel_config import register_config_tools
from .tools.plugins import register_plugin_tools
from .tools.docker import register_docker_tools
from .tools.projects import register_project_tools
from .tools.logs import register_log_tools
from .tools.ssh import register_ssh_tools
from .tools.backup import register_backup_tools
from .tools.monitoring import register_monitoring_tools
from .tools.deployment import register_deployment_tools
from .tools.optimization import register_optimization_tools
from .tools.security import register_security_tools

logger = logging.getLogger(__name__)


def create_server() -> FastMCP:
    """Create and configure the MCP server with all tools."""
    # Load configuration
    config = load_config()

    # Initialize client manager
    client_manager.init_from_config(config)

    # Create MCP server
    mcp = FastMCP("aaPanel MCP")

    # Register all tool modules
    register_system_tools(mcp)
    register_site_tools(mcp)
    register_database_tools(mcp)
    register_ftp_tools(mcp)
    register_file_tools(mcp)
    register_firewall_tools(mcp)
    register_crontab_tools(mcp)
    register_ssl_tools(mcp)
    register_config_tools(mcp)
    register_plugin_tools(mcp)
    register_docker_tools(mcp)
    register_project_tools(mcp)
    register_log_tools(mcp)
    register_ssh_tools(mcp)
    register_backup_tools(mcp)
    register_monitoring_tools(mcp)
    register_deployment_tools(mcp)
    register_optimization_tools(mcp)
    register_security_tools(mcp)

    logger.info(
        "aaPanel MCP server initialized with %d servers",
        len(client_manager.get_server_names()),
    )
    return mcp
